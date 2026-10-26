import {readdir,stat} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
export async function verifyVideoAssets(directory){
 directory=directory instanceof URL?fileURLToPath(directory):directory;
 let count=0;
 async function walk(dir){for(const entry of await readdir(dir,{withFileTypes:true})){const path=join(dir,entry.name);if(entry.isDirectory())await walk(path);else{if(/\.(mp4|mov|mkv|webm)$/i.test(entry.name))throw Error(`Video bundled as a static asset: ${path}. Upload it to R2 instead.`);if((await stat(path)).size>25*1024*1024)throw Error(`Static asset exceeds 25 MiB: ${path}`);count++;}}}
 await walk(directory);return count;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){const n=await verifyVideoAssets(resolve(process.argv[2]||'dist/client'));console.log(`Static-media guard passed: ${n} assets; no bundled video and no file over 25 MiB.`);}
