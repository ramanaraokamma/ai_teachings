import { readFile, writeFile, stat } from "node:fs/promises";
import { createHash } from "node:crypto";

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
const runtime=JSON.parse(await readFile(new URL('../reports/python-runtime-manifest.json',import.meta.url),'utf8'));
for(const file of runtime.files){
 const bytes=await readFile(new URL(`../dist/client/python-runtime/${file.file}`,import.meta.url));
 if(createHash('sha256').update(bytes).digest('hex')!==file.sha256)throw new Error(`Build omitted or changed Python runtime ${file.file}`);
}
if((await stat(new URL('../dist/client/python-lab-worker.mjs',import.meta.url))).size<100)throw new Error('Build omitted Python lab worker');
console.log(`Deployment ready: ai-teachings; ${Object.keys(manifest).length} protected resources included; complete-programme-2026-10-07.`);
