// Run only after rendering and visually reviewing every page; the review receipt
// binds that review to the exact source, renderer and artifact bytes.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash,createCipheriv,randomBytes} from 'node:crypto';
import assert from 'node:assert/strict';
const hash=b=>createHash('sha256').update(b).digest('hex');
const read=p=>readFile(p);
const review=JSON.parse(await read(process.argv[2]??'curriculum-v3/print-review.json'));
const keyText=await readFile('lib/resource-key.ts','utf8');
const key=Buffer.from(keyText.match(/resourceKey = "([^"]+)"/)[1],'base64');
const manifest=JSON.parse(await read('lib/resource-manifest.json'));
const releases=JSON.parse(await read('curriculum-v3/releases.json'));
for(const [file,digest] of Object.entries(review.renderers))assert.equal(hash(await read(file)),digest,`Renderer changed: ${file}`);
async function protect(path,role,filename,mime,expected){
 const plain=await read(path);assert.equal(hash(plain),expected,`Unreviewed bytes: ${path}`);
 const id=hash(Buffer.concat([Buffer.from(`curriculum3\0${role}\0${filename??''}\0`),plain]));
 const nonce=randomBytes(12),cipher=createCipheriv('aes-256-gcm',key,nonce);cipher.setAAD(Buffer.from(id));
 const packed=Buffer.concat([nonce,cipher.update(plain),cipher.final(),cipher.getAuthTag()]);
 // Preserve existing identical resources so rerunning a release is idempotent.
 if(!manifest[id])await writeFile(`public/curriculum-blobs/${id}.bin`,packed);
 manifest[id]={mime,role,filename};return {id,sha256:expected};
}
for(const [id,r] of Object.entries(review.chapters)){
 const [level,num]=id.split('/'),stem=`${level}-week-${num.padStart(2,'0')}`;
 assert.equal(hash(await read(`curriculum-v3/${stem}.json`)),r.sourceHash,`Source changed: ${id}`);
 assert.equal(r.visualReview,'Every rendered page inspected');
 const release={sourceHash:r.sourceHash,documents:{},diagrams:[],review:{pages:0,checked:review.checked}};
 for(const role of ['lesson','workbook','guide']){
  const doc=r.documents[role];assert.ok(doc.pages.length>0);
  for(let i=0;i<doc.pages.length;i++)assert.equal(hash(await read(`work/v3-render/${stem}-${role}/page-${i+1}.png`)),doc.pages[i],`Review page changed: ${id}/${role}/${i+1}`);
  release.review.pages+=doc.pages.length;
  for(const ext of ['docx','pdf']){
   const filename=`${stem}-${role}.${ext}`;
   const path=ext==='docx'?`work/v3-docs/${filename}`:`work/v3-render/${stem}-${role}/${filename}`;
   release.documents[`${role}.${ext}`]=await protect(path,role==='guide'?'teacher':'student',filename,ext==='pdf'?'application/pdf':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',doc[ext]);
  }
 }
 for(let i=0;i<r.diagrams.length;i++)release.diagrams.push(await protect(`work/v3-diagrams/${stem}-diagram-${i+1}.png`,'student',null,'image/png',r.diagrams[i]));
 releases[id]=release;
}
await writeFile('lib/resource-manifest.json',JSON.stringify(manifest));
await writeFile('curriculum-v3/releases.json',JSON.stringify(releases,null,2)+'\n');
console.log(`${Object.keys(releases).length} complete packages registered in protected storage.`);
