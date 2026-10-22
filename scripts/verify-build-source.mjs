import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const revision=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
console.log(`AI Academy build: externalized-lessons-v1; commit=${revision}`);
if(process.env.WORKERS_CI_COMMIT_SHA){
 console.log(`Cloudflare build commit=${process.env.WORKERS_CI_COMMIT_SHA}`);
 if(process.env.WORKERS_CI_COMMIT_SHA!==revision)throw new Error('Cloudflare commit does not match the checked-out Git revision. Check repository, branch and root settings.');
}
const runtime=await readFile(new URL('../lib/academy.ts',import.meta.url),'utf8');
if(!runtime.includes('"./academy-index.json"')||runtime.includes('"./academy-data.json"'))throw new Error('Runtime must load the small academy-index.json, not the full academy-data.json.');
console.log('Build source verified: full curriculum excluded from Worker code.');
