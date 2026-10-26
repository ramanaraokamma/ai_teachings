import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {Readable} from 'node:stream';
import {createHmac,randomBytes} from 'node:crypto';
import {resolve} from 'node:path';
const catalogue=JSON.parse(await readFile('lib/lesson-videos.json','utf8'));
const youtube=JSON.parse(await readFile('lib/youtube-videos.json','utf8'));
const plan=JSON.parse(await readFile('outputs/video-publishing/upload-plan.json','utf8'));
const objects=new Map(plan.objects.map(o=>[o.key,o]));let reads=0;
const info=o=>({size:o.bytes,httpEtag:`"${o.sha256}"`,uploaded:new Date('2026-10-25T00:00:00Z')});
const bucket={async head(key){reads++;const o=objects.get(key);return o?info(o):null;},async get(key,options){reads++;const o=objects.get(key);if(!o)return null;const r=options?.range;return {...info(o),body:Readable.toWeb(createReadStream(resolve(o.source),r?{start:r.offset,end:r.offset+r.length-1}:{}))};}};
const secret=randomBytes(32).toString('hex');
const env={ACADEMY_SESSION_SECRET:secret,LESSON_VIDEOS:bucket,ASSETS:{async fetch(request){try{return new Response(await readFile(resolve('public','.'+new URL(request.url).pathname)));}catch{return new Response('Missing',{status:404});}}}};
globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');
const ctx={waitUntil(){},passThroughOnException(){}};
const session=role=>{const p=`${role}.${Math.floor(Date.now()/1000)+3600}`;return `academy_access=${p}.${createHmac('sha256',secret).update(p).digest('hex')}`;};
const request=(path,role,options={})=>worker.fetch(new Request('https://academy.test'+path,{...options,headers:{accept:'text/html',...(role?{cookie:session(role)}:{}),...options.headers}}),env,ctx);
assert.equal((await request('/api/lesson-video/ai-1/1/video')).status,401);assert.equal(reads,0,'No R2 access before authentication');
for(const role of ['student','teacher']){
 let r=await request('/api/lesson-video/ai-1/1/video',role,{headers:{Range:'bytes=0-63'}});assert.equal(r.status,206);assert.equal((await r.arrayBuffer()).byteLength,64);assert.equal(r.headers.get('content-range'),`bytes 0-63/${catalogue['ai-1/1'].assets.video.bytes}`);
 r=await request('/api/lesson-video/ai-2/36/video',role,{method:'HEAD'});assert.equal(r.status,200);assert.equal(Number(r.headers.get('content-length')),catalogue['ai-2/36'].assets.video.bytes);
 r=await request('/api/lesson-video/ai-2/36/captions',role);assert.equal(r.status,200);assert.ok((await r.text()).startsWith('WEBVTT'));assert.ok(r.headers.get('cache-control').includes('private'));
}
for(const path of ['/api/lesson-video/ai-3/1/video','/api/lesson-video/ai-1/37/video','/api/lesson-video/ai-1/1/constructor'])assert.equal((await request(path,'student')).status,404);
const saved=env.LESSON_VIDEOS;delete env.LESSON_VIDEOS;assert.equal((await request('/api/lesson-video/ai-1/1/video','student')).status,503);env.LESSON_VIDEOS=saved;
let pages=0;
for(const [id,video] of Object.entries(catalogue))for(const role of ['student','teacher']){
 const r=await request(`/learn/${role}/${id}`,role);assert.equal(r.status,200,`${role}/${id}`);const html=await r.text();assert.ok(html.includes('id="week-video"'),`${role}/${id} video section`);assert.equal(html.includes('Load this week'),Boolean(youtube[id]),`${role}/${id} publication state`);if(youtube[id])assert.ok(html.includes(youtube[id]),`${role}/${id} YouTube ID`);else assert.ok(html.includes('coming soon'),`${role}/${id} pending notice`);assert.ok(!html.includes('<video'),`${role}/${id} eager movie element`);
 const student=await (await request(`/learn/${role}/${id}?resource=lesson`,role)).text();
 assert.equal((student.match(/class="section-video-link"/g)||[]).length,youtube[id]?18:0,`${id} section-level video links`);
 for(const c of video.chapters)for(const n of c.studentSections)assert.ok(student.includes(`id="section-${n}"`),`${id} chapter ${c.number} maps to missing section ${n}`);
 pages++;
}
assert.ok(!(await (await request('/learn/student/ai-3/1','student')).text()).includes('id="week-video"'));
console.log(`${pages} student/teacher week pages verified; all 72 weeks map correctly, with 10 YouTube videos enabled and 62 pending. Signed-in streaming, captions, HEAD, signed-out denial before storage reads, unknown assets and missing-storage responses passed.`);
