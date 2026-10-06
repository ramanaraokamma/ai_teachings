// Pack encrypted assets into sixteen containers to avoid per-file archive overhead.
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createCipheriv,randomBytes} from 'node:crypto';
import {gzipSync,gunzipSync} from 'node:zlib';
import {decryptPacked} from './resource-storage.mjs';
const manifest=JSON.parse(await readFile('lib/resource-manifest.json'));
const key=Buffer.from((await readFile('lib/resource-key.ts','utf8')).match(/resourceKey = "([^"]+)"/)[1],'base64');
const buckets=Array.from({length:16},()=>[]),sizes=Array(16).fill(0),parts=new Map();
function append(id,bytes){const pack=id[0],i=parseInt(pack,16),entry={pack,offset:sizes[i],packedLength:bytes.length};buckets[i].push(bytes);sizes[i]+=bytes.length;return entry;}
const encrypt=(bytes,id)=>{const nonce=randomBytes(12),c=createCipheriv('aes-256-gcm',key,nonce);c.setAAD(Buffer.from(id));return Buffer.concat([nonce,c.update(bytes),c.final(),c.getAuthTag()]);};
// Stage shared parts first, so protected indexes can carry their container ranges.
for(const [id,m] of Object.entries(manifest))if(['parts-v1','parts-v2'].includes(m.storage)){
 const raw=await readFile(`public/curriculum-blobs/${id}.bin`),index=JSON.parse(m.storage==='parts-v2'?gunzipSync(decryptPacked(raw,id,key)):decryptPacked(raw,id,key));
 for(const part of index.parts)if(!parts.has(part.id))parts.set(part.id,append(part.id,await readFile(`public/curriculum-blobs/parts/${part.id}.bin`)));
}
for(const [id,m] of Object.entries(manifest)){
 let raw=await readFile(`public/curriculum-blobs/${id}.bin`);
 if(['parts-v1','parts-v2'].includes(m.storage)){
  const index=JSON.parse(m.storage==='parts-v2'?gunzipSync(decryptPacked(raw,id,key)):decryptPacked(raw,id,key));
  for(const part of index.parts)Object.assign(part,parts.get(part.id));
  raw=encrypt(gzipSync(Buffer.from(JSON.stringify(index))),id);m.storage='parts-v2';
  // Keep the individual encrypted index available to local tooling as well.
  await writeFile(`public/curriculum-blobs/${id}.bin`,raw);
 }
 Object.assign(m,append(id,raw));
}
await mkdir('public/curriculum-packs',{recursive:true});
for(let i=0;i<16;i++)await writeFile(`public/curriculum-packs/${i.toString(16)}.bin`,Buffer.concat(buckets[i]));
await writeFile('lib/resource-manifest.json',JSON.stringify(manifest));
console.log(JSON.stringify({packs:16,totalBytes:sizes.reduce((a,b)=>a+b,0),largestPack:Math.max(...sizes)}));
