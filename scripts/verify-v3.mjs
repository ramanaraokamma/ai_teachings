import {readResource} from './resource-storage.mjs';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const json=async p=>JSON.parse(await readFile(p,'utf8'));
const hash=b=>createHash('sha256').update(b).digest('hex');
const roadmap=await json('curriculum-v3/progression.json');
const release=await json('curriculum-v3/releases.json');
const review=await json('curriculum-v3/print-review.json');
const manifest=await json('lib/resource-manifest.json');
const key=Buffer.from((await readFile('lib/resource-key.ts','utf8')).match(/resourceKey = "([^"]+)"/)[1],'base64');
assert.equal(roadmap.levels.length,7);
for(const [i,l] of roadmap.levels.entries()){assert.equal(l.grade,6+i);assert.equal(l.weeks.length,36);assert.ok(l.prerequisites&&l.exitEvidence);assert.equal(new Set(l.weeks).size,36);}
for(const [file,digest] of Object.entries(review.renderers))assert.equal(hash(await readFile(file)),digest,`Renderer changed; regenerate and review downloads: ${file}`);
async function artifact(a,role,mime){
 assert.equal(manifest[a.id]?.role,role);assert.equal(manifest[a.id]?.mime,mime);
 const plain=await readResource(a.id,manifest[a.id],key);assert.equal(hash(plain),a.sha256,`Artifact changed: ${a.id}`);
 if(mime==='application/pdf')assert.equal(plain.subarray(0,5).toString(),'%PDF-');
 return plain;
}
for(const [id,r] of Object.entries(release)){
 const [level,num]=id.split('/'),stem=`${level}-week-${num.padStart(2,'0')}`;
 const bytes=await readFile(`curriculum-v3/${stem}.json`),w=JSON.parse(bytes);
 assert.equal(hash(bytes),r.sourceHash,`Web/print mismatch: ${id}; rebuild and review this package`);
 const l=roadmap.levels.find(l=>l.slug===level);assert.equal(l.weeks[Number(num)-1],w.title);assert.equal(w.week,Number(num));assert.equal(w.level,level);
 assert.equal(review.chapters[id].sourceHash,r.sourceHash);
 assert.equal(w.minutes,90);assert.equal(w.goals.length,3);assert.equal(w.lesson.length,5);assert.equal(w.workbook.length,5);
 const diagramCount=w.lesson.flatMap(s=>s.blocks).filter(b=>b.type==='diagram').length;
 assert.ok(diagramCount>0);assert.equal(r.diagrams.length,diagramCount);
 for(const role of ['lesson','workbook','guide'])for(const ext of ['docx','pdf']){
  const a=r.documents[`${role}.${ext}`];assert.equal(a.sha256,review.chapters[id].documents[role][ext]);
  await artifact(a,role==='guide'?'teacher':'student',ext==='pdf'?'application/pdf':'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
 }
 for(const a of r.diagrams)await artifact(a,'student','image/png');
 assert.equal(Object.keys(r.documents).length,6);
 for(const task of w.workbook)assert.ok(task.prompt&&task.answer&&task.lines>=4);
}
console.log(`Curriculum 3 verified: ${Object.keys(release).length} released packages; seven levels and ${252-Object.keys(release).length} remaining planned positions. Source, reviewed downloads and protected roles match.`);
