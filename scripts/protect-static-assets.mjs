import { readFile, writeFile } from "node:fs/promises";

const configUrl = new URL("../dist/server/wrangler.json", import.meta.url);
const config = JSON.parse(await readFile(configUrl, "utf8"));
config.assets = {
  ...config.assets,
  binding: "ASSETS",
  run_worker_first: ["/academy-art/*"],
};
await writeFile(configUrl, `${JSON.stringify(config)}\n`);
