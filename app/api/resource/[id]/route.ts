import { env } from "cloudflare:workers";
import { readSession } from "@/lib/access";
import manifestData from "@/lib/resource-manifest.json";
import { resourceKey } from "@/lib/resource-key";

export const dynamic = "force-dynamic";
const manifest = manifestData as Record<string, { mime: string; role: string; filename: string | null }>;

export async function GET(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const role = await readSession();
  const headers = { "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff", "Vary": "Cookie" };
  if (!role) return new Response("Sign in to view this resource.", { status: 401, headers });
  const { id } = await params;
  const resource = /^[a-f0-9]{64}$/.test(id) ? manifest[id] : undefined;
  if (!resource || (resource.role === "teacher" && role !== "teacher")) return new Response("Resource unavailable.", { status: 404, headers });
  const assets = (env as unknown as { ASSETS: { fetch(request: Request): Promise<Response> } }).ASSETS;
  const packed = await assets.fetch(new Request(new URL(`/curriculum-blobs/${id}.bin`, request.url)));
  if (!packed.ok) return new Response("Resource unavailable.", { status: 503, headers });
  const bytes = new Uint8Array(await packed.arrayBuffer());
  const keyBytes = Uint8Array.from(atob(resourceKey), c => c.charCodeAt(0));
  const key = await crypto.subtle.importKey("raw", keyBytes, "AES-GCM", false, ["decrypt"]);
  const content = await crypto.subtle.decrypt({ name: "AES-GCM", iv: bytes.slice(0, 12), additionalData: new TextEncoder().encode(id) }, key, bytes.slice(12));
  const responseHeaders = new Headers(headers);
  responseHeaders.set("Content-Type", resource.mime);
  if (resource.filename) responseHeaders.set("Content-Disposition", `attachment; filename="${resource.filename.replace(/[^a-zA-Z0-9_.-]/g, "_")}"`);
  return new Response(content, { headers: responseHeaders });
}
