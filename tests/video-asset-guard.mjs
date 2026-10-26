import assert from 'node:assert/strict';
import {mkdtemp,writeFile,open,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {verifyVideoAssets} from '../scripts/verify-video-assets.mjs';
const dir=await mkdtemp(join(tmpdir(),'academy-video-guard-'));
try{
 await writeFile(join(dir,'app.js'),'export {};');assert.equal(await verifyVideoAssets(dir),1);
 await writeFile(join(dir,'lesson.mp4'),'fixture');await assert.rejects(verifyVideoAssets(dir),/Video bundled/);await rm(join(dir,'lesson.mp4'));
 const file=await open(join(dir,'oversized.bin'),'w');await file.truncate(25*1024*1024+1);await file.close();await assert.rejects(verifyVideoAssets(dir),/exceeds 25 MiB/);
 console.log('Deployment guard accepts small assets and blocks bundled videos and oversized static files.');
}finally{await rm(dir,{recursive:true,force:true});}
