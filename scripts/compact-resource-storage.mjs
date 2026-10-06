// Share identical ZIP members and gzip PDFs, preserving every original byte.
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {createHash,createCipheriv,randomBytes} from 'node:crypto';
import {gzipSync} from 'node:zlib';
import assert from 'node:assert/strict';
import {readResource} from './resource-storage.mjs';
const manifest=JSON.parse(await readFile('lib/resource-manifest.json'));
const key=Buffer.from((await readFile('lib/resource-key.ts','utf8')).match(/resourceKey = "([^"]+)"/)[1],'base64');
const hash=b=>createHash('sha256').update(b).digest('hex');
const encrypt=(bytes,id)=>{const nonce=randomBytes(12),c=createCipheriv('aes-256-gcm',key,nonce);c.setAAD(Buffer.from(id));return Buffer.concat([nonce,c.update(bytes),c.final(),c.getAuthTag()]);};
await mkdir('public/curriculum-blobs/parts',{recursive:true});
const seen=new Map();let before=0,after=0,count=0;
async function part(bytes){
 const id=hash(bytes);if(seen.has(id))return seen.get(id);
 const gzip=gzipSync(bytes),compressed=gzip.length<bytes.length;
 const entry={id,length:bytes.length,gzip:compressed};
 const path=`public/curriculum-blobs/parts/${id}.bin`;
 try{await stat(path);}catch(e){if(e.code!=='ENOENT')throw e;await writeFile(path,encrypt(compressed?gzip:bytes,id));}
 after+=(await stat(path)).size;seen.set(id,entry);return entry;
}
for(const [id,metadata] of Object.entries(manifest)){
 if(!metadata.filename)continue;
 const plain=await readResource(id,metadata,key);before+=plain.length+28;
 const parts=[];
 if(metadata.filename.endsWith('.docx')){
  let pos=0;
  while(pos+30<=plain.length&&plain.readUInt32LE(pos)===0x04034b50){
   assert.equal(plain.readUInt16LE(pos+6)&8,0,'ZIP data descriptors require explicit parsing');
   const size=plain.readUInt32LE(pos+18),start=pos+30+plain.readUInt16LE(pos+26)+plain.readUInt16LE(pos+28);
   assert.ok(start+size<=plain.length);
   parts.push(await part(plain.subarray(pos,start)),await part(plain.subarray(start,start+size)));pos=start+size;
  }
  parts.push(await part(plain.subarray(pos)));
 }else parts.push(await part(plain));
 const index=Buffer.from(JSON.stringify({version:1,size:plain.length,parts}));
 const packed=encrypt(index,id);await writeFile(`public/curriculum-blobs/${id}.bin`,packed);
 delete metadata.pack;delete metadata.offset;delete metadata.packedLength;
 metadata.storage='parts-v1';after+=packed.length;
 assert.equal(hash(await readResource(id,metadata,key)),hash(plain),`Changed bytes: ${id}`);count++;
}
await writeFile('lib/resource-manifest.json',JSON.stringify(manifest));
console.log(JSON.stringify({documents:count,uniqueParts:seen.size,before,after,saved:before-after}));
