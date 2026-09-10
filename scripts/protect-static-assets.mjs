import { readFile, writeFile } from "node:fs/promises";

const configUrl = new URL("../dist/server/wrangler.json", import.meta.url);
const config = JSON.parse(await readFile(configUrl, "utf8"));
config.name = "ai-academy";
config.assets = {
  ...config.assets,
  binding: "ASSETS",
  run_worker_first: ["/api/*", "/learn/*", "/academy-art/*", "/_vinext/image"],
};
await writeFile(configUrl, `${JSON.stringify(config)}\n`);
