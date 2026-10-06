import {readResource} from './resource-storage.mjs';
// Create audience-separated offline bundles from the exact registered artifacts.
import {readFile,writeFile,mkdir,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const releases=JSON.parse(await readFile('curriculum-v3/releases.json','utf8'));
const resources=JSON.parse(await readFile('lib/resource-manifest.json','utf8'));
const roadmap=JSON.parse(await readFile('curriculum-v3/progression.json','utf8'));
const keyText=await readFile('lib/resource-key.ts','utf8');
const key=Buffer.from(keyText.match(/resourceKey = "([^"]+)"/)[1],'base64');
const hash=b=>createHash('sha256').update(b).digest('hex');
const out='outputs/curriculum-complete';
await mkdir(out,{recursive:true});
const manifests={};
for(const audience of ['student','teacher']){
 const folder=`work/v3-complete/${audience}`;await mkdir(folder,{recursive:true});
 const manifest={audience,packages:0,documents:0,figures:0,files:{}};
 manifests[audience]=manifest;
 async function save(relative,bytes){
  const path=`${folder}/${relative}`;
  await mkdir(path.slice(0,path.lastIndexOf('/')),{recursive:true});
  await writeFile(path,bytes);manifest.files[relative]=hash(bytes);
 }
 async function artifact(a,role,relative){
  assert.equal(resources[a.id]?.role,role,`Role mismatch: ${a.id}`);
  const plain=await readResource(a.id,resources[a.id],key);
  assert.equal(hash(plain),a.sha256,`Artifact mismatch: ${relative}`);
  await save(relative,plain);
 }
 const index=[];
 for(const level of roadmap.levels){
  index.push(`${level.slug.toUpperCase()} — ${level.name} — Grade ${level.grade}`);
  for(const [i,title] of level.weeks.entries()){
   const week=i+1,id=`${level.slug}/${week}`,release=releases[id];assert.ok(release,`Missing package: ${id}`);
   const source=await readFile(`curriculum-v3/${level.slug}-week-${String(week).padStart(2,'0')}.json`);
   assert.equal(hash(source),release.sourceHash,`Source changed: ${id}`);
   index.push(`  ${String(week).padStart(2,'0')} ${title}`);manifest.packages++;
   for(const [name,a] of Object.entries(release.documents)){
    const role=name.startsWith('guide.')?'teacher':'student';if(role!==audience)continue;
    await artifact(a,role,`${level.slug}/${resources[a.id].filename}`);manifest.documents++;
   }
   if(audience==='student')for(const [j,a] of release.diagrams.entries()){
    await artifact(a,'student',`${level.slug}/${level.slug}-week-${String(week).padStart(2,'0')}-diagram-${j+1}.png`);manifest.figures++;
   }
  }
  index.push('');
 }
 assert.equal(manifest.packages,252);
 assert.equal(manifest.documents,audience==='student'?1008:504);
 if(audience==='student')assert.equal(manifest.figures,252);
 await save('CHAPTER_INDEX.txt',index.join('\n'));
 await save('READ_ME.txt',`CURRICULUM 3 — COMPLETE ${audience.toUpperCase()} COLLECTION\n\nSeven levels, Grades 6–12, 36 weeks each: 252 weekly packages.\n${audience==='student'?'Student lessons and workbooks in Word/PDF, plus teaching diagrams. Teacher answer guides are in a separate collection.':'Teacher guides in Word/PDF. This archive contains solutions; keep it within teacher access.'}\n\nArtifacts match the reviewed local release manifest.\nThe local Python labs require Python 3 and no external AI account.\nClassroom pacing and learning effectiveness require teacher feedback and student trials.\nThe collection does not indicate a live website deployment.\n`);
 for(const name of await readdir('examples/curriculum-v3'))if(/\.(py|md)$/.test(name))await save(`local-labs/${name}`,await readFile(`examples/curriculum-v3/${name}`));
 await writeFile(`${folder}/ARTIFACT_MANIFEST.json`,JSON.stringify(manifest,null,2)+'\n');
 // Use the allowlist, not a directory walk, so stale work files cannot enter a bundle.
 const script=`import hashlib,json,pathlib,sys,zipfile\nroot=pathlib.Path(sys.argv[1])\nm=json.loads((root/'ARTIFACT_MANIFEST.json').read_text())\nwith zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED) as z:\n for name,digest in m['files'].items():\n  data=(root/name).read_bytes()\n  assert hashlib.sha256(data).hexdigest()==digest,name\n  z.writestr(name,data)\n z.write(root/'ARTIFACT_MANIFEST.json','ARTIFACT_MANIFEST.json')\nwith zipfile.ZipFile(sys.argv[2]) as z:\n assert z.testzip() is None\n assert len(z.namelist())==len(m['files'])+1\n for name,digest in m['files'].items():\n  assert hashlib.sha256(z.read(name)).hexdigest()==digest,name\n`;
 const target=`${out}/${audience}-complete.zip`;
 const result=spawnSync('python3',['-c',script,folder,target],{encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);
 console.log(`${audience}: ${manifest.packages} weeks, ${manifest.documents} Word/PDF files, ${manifest.figures} figures -> ${target}`);
}
await writeFile(`${out}/collection-manifest.json`,JSON.stringify(manifests,null,2)+'\n');
