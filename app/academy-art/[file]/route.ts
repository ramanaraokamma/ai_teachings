import { env } from "cloudflare:workers";

import { readSession } from "@/lib/access";

const SAFE_ART_FILE = /^[a-f0-9]{18}\.(?:png|jpg|webp)$/;

export async function GET(request: Request, { params }: { params: Promise<{ file: string }> }) {
  if (!(await readSession())) return new Response("Not found", { status: 404 });
  const { file } = await params;
  if (!SAFE_ART_FILE.test(file)) return new Response("Not found", { status: 404 });

  const response = await (env as unknown as { ASSETS: Fetcher }).ASSETS.fetch(request);
  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "private, max-age=3600");
  headers.set("X-Content-Type-Options", "nosniff");
  return new Response(response.body, { status: response.status, headers });
}
