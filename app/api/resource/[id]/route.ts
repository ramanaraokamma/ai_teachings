import { env } from "cloudflare:workers";
import { readSession } from "@/lib/access";
import manifestData from "@/lib/resource-manifest.json";
import { resourceKey } from "@/lib/resource-key";

export const dynamic = "force-dynamic";
const manifest = manifestData as Record<string, { mime: string; role: string; filename: string | null; storage?: string; pack?: string; offset?: number; packedLength?: number }>;

export async function GET(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const role = await readSession();
  const headers = { "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff", "Vary": "Cookie" };
  if (!role) return new Response("Sign in to view this resource.", { status: 401, headers });
  const { id } = await params;
  const resource = /^[a-f0-9]{64}$/.test(id) ? manifest[id] : undefined;
  if (!resource || (resource.role === "teacher" && role !== "teacher")) return new Response("Resource unavailable.", { status: 404, headers });
  const assets = (env as unknown as { ASSETS: { fetch(request: Request): Promise<Response> } }).ASSETS;
  async function fetchPacked(path: string, metadata: { pack?: string; offset?: number; packedLength?: number }) {
    if (!metadata.pack) return assets.fetch(new Request(new URL(path, request.url)));
    if (!/^[a-f0-9]$/.test(metadata.pack) || !Number.isSafeInteger(metadata.offset) || !Number.isSafeInteger(metadata.packedLength)) return new Response("Invalid resource", { status: 503 });
    const start = metadata.offset!, length = metadata.packedLength!;
    const response = await assets.fetch(new Request(new URL(`/curriculum-packs/${metadata.pack}.bin`, request.url), { headers: { Range: `bytes=${start}-${start + length - 1}` } }));
    if (!response.ok) return response;
    const bytes = new Uint8Array(await response.arrayBuffer());
    const packed = response.status === 206 ? bytes : bytes.slice(start, start + length);
    return packed.length === length ? new Response(packed) : new Response("Invalid resource", { status: 503 });
  }
  const packed = await fetchPacked(`/curriculum-blobs/${id}.bin`, resource);
  if (!packed.ok) return new Response("Resource unavailable.", { status: 503, headers });
  const bytes = new Uint8Array(await packed.arrayBuffer());
  const keyBytes = Uint8Array.from(atob(resourceKey), c => c.charCodeAt(0));
  const key = await crypto.subtle.importKey("raw", keyBytes, "AES-GCM", false, ["decrypt"]);
  let content = await crypto.subtle.decrypt({ name: "AES-GCM", iv: bytes.slice(0, 12), additionalData: new TextEncoder().encode(id) }, key, bytes.slice(12));
  if (resource.storage === "parts-v1" || resource.storage === "parts-v2") {
    if (resource.storage === "parts-v2") content = await new Response(new Blob([content]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer();
    const index = JSON.parse(new TextDecoder().decode(content)) as { version: number; size: number; parts: { id: string; length: number; gzip: boolean; pack?: string; offset?: number; packedLength?: number }[] };
    if (index.version !== 1) return new Response("Resource unavailable.", { status: 503, headers });
    const output = new Uint8Array(index.size);
    let offset = 0;
    for (const part of index.parts) {
      if (!/^[a-f0-9]{64}$/.test(part.id)) return new Response("Resource unavailable.", { status: 503, headers });
      const response = await fetchPacked(`/curriculum-blobs/parts/${part.id}.bin`, part);
      if (!response.ok) return new Response("Resource unavailable.", { status: 503, headers });
      const packedPart = new Uint8Array(await response.arrayBuffer());
      const decoded = await crypto.subtle.decrypt({ name: "AES-GCM", iv: packedPart.slice(0, 12), additionalData: new TextEncoder().encode(part.id) }, key, packedPart.slice(12));
      const plain = part.gzip ? new Uint8Array(await new Response(new Blob([decoded]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer()) : new Uint8Array(decoded);
      if (plain.length !== part.length || offset + plain.length > output.length) return new Response("Resource unavailable.", { status: 503, headers });
      output.set(plain, offset); offset += plain.length;
    }
    if (offset !== output.length) return new Response("Resource unavailable.", { status: 503, headers });
    content = output.buffer;
  }
  const responseHeaders = new Headers(headers);
  responseHeaders.set("Content-Type", resource.mime);
  if (resource.filename) responseHeaders.set("Content-Disposition", `attachment; filename="${resource.filename.replace(/[^a-zA-Z0-9_.-]/g, "_")}"`);
  return new Response(content, { headers: responseHeaders });
}
