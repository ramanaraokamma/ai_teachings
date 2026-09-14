import { readFile, writeFile, stat } from "node:fs/promises";

const configUrl = new URL("../dist/server/wrangler.json", import.meta.url);
const config = JSON.parse(await readFile(configUrl, "utf8"));
config.name = "ai-teachings";
config.assets = {
  ...config.assets,
  binding: "ASSETS",
  run_worker_first: ["/api/*", "/learn/*", "/academy-art/*", "/_vinext/image"],
};
await writeFile(configUrl, `${JSON.stringify(config)}\n`);
const manifest = JSON.parse(await readFile(new URL("../lib/resource-manifest.json", import.meta.url), "utf8"));
for (const id of Object.keys(manifest)) {
  const emitted = new URL(`../dist/client/curriculum-blobs/${id}.bin`, import.meta.url);
  if ((await stat(emitted)).size <= 28) throw new Error(`Build omitted curriculum asset ${id}`);
}
console.log(`Deployment ready: ai-teachings; ${Object.keys(manifest).length} protected resources included; grade6-entry-2026-09-14.`);
