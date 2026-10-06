// Lossless protected storage shared by release verification and offline exports.
import {readFile,open} from 'node:fs/promises';
import {createDecipheriv} from 'node:crypto';
import {gunzipSync} from 'node:zlib';
export function decryptPacked(packed,id,key){
 const d=createDecipheriv('aes-256-gcm',key,packed.subarray(0,12));
 d.setAAD(Buffer.from(id));d.setAuthTag(packed.subarray(-16));
 return Buffer.concat([d.update(packed.subarray(12,-16)),d.final()]);
}
async function packedBytes(id,metadata,read,path){
 if(!metadata.pack)return read(path);
 const f=await open(new URL(`../public/curriculum-packs/${metadata.pack}.bin`,import.meta.url),'r');
 try{const bytes=Buffer.alloc(metadata.packedLength);const result=await f.read(bytes,0,bytes.length,metadata.offset);if(result.bytesRead!==bytes.length)throw new Error('Truncated protected pack');return bytes;}finally{await f.close();}
}
export async function readResource(id,metadata,key,read=path=>readFile(path)){
 const plain=decryptPacked(await packedBytes(id,metadata,read,`public/curriculum-blobs/${id}.bin`),id,key);
 if(!['parts-v1','parts-v2'].includes(metadata.storage))return plain;
 const index=JSON.parse(metadata.storage==='parts-v2'?gunzipSync(plain):plain);if(index.version!==1)throw new Error('Unknown storage version');
 const parts=[];
 for(const part of index.parts){
  if(!/^[a-f0-9]{64}$/.test(part.id))throw new Error('Invalid protected part');
  const packed=decryptPacked(await packedBytes(part.id,part,read,`public/curriculum-blobs/parts/${part.id}.bin`),part.id,key);
  const bytes=part.gzip?gunzipSync(packed):packed;
  if(bytes.length!==part.length)throw new Error('Protected part length mismatch');
  parts.push(bytes);
 }
 const result=Buffer.concat(parts);if(result.length!==index.size)throw new Error('Resource length mismatch');
 return result;
}
