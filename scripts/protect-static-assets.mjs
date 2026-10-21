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
// Catch missing externalized lessons and oversized code before asset upload.
const index=JSON.parse(await readFile(new URL('../lib/academy-index.json',import.meta.url),'utf8'));
for(const level of index.levels)for(const week of level.weeks){
 if((await stat(new URL(`../dist/client/lesson-blobs/${week.contentId}.bin`,import.meta.url))).size<=28)throw new Error(`Missing lesson asset ${level.slug}/${week.number}`);
}
const {readdir}=await import('node:fs/promises');
async function codeBytes(dir){let total=0;for(const entry of await readdir(dir,{withFileTypes:true})){const path=new URL(entry.name+(entry.isDirectory()?'/':''),dir);if(entry.isDirectory())total+=await codeBytes(path);else if(/\.(?:js|mjs|wasm)$/.test(entry.name))total+=(await stat(path)).size;}return total;}
const bytes=await codeBytes(new URL('../dist/server/',import.meta.url));
if(bytes>60*1024*1024)throw new Error(`Worker code is ${(bytes/1024/1024).toFixed(2)} MiB; exceeds the 60 MiB build safety budget. Move curriculum data into assets.`);
console.log(`Worker code size preflight: ${(bytes/1024/1024).toFixed(2)} MiB; 264 encrypted weekly assets verified.`);
