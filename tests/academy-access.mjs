import assert from 'node:assert/strict';
import { readFile, readdir, writeFile, mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { createHmac, randomBytes } from 'node:crypto';

const root=resolve('.');
const manifest=JSON.parse(await readFile('lib/resource-manifest.json','utf8'));
const data=JSON.parse(await readFile('lib/academy-data.json','utf8'));
const plans=JSON.parse(await readFile('lib/topic-plans.json','utf8'));
const review=JSON.parse(await readFile('lib/grade6-review.json','utf8'));
const secret=randomBytes(32).toString('hex');
const results=[];
const testEnv={STUDENT_PASSCODE:'student1234',TEACHER_PASSCODE:'teacher1234',ACADEMY_SESSION_SECRET:secret,
  ASSETS:{fetch:async request=>{
    const path=new URL(request.url).pathname;
    if(!/^\/curriculum-blobs\/[a-f0-9]{64}\.bin$/.test(path))return new Response('Not found',{status:404});
    try{return new Response(await readFile(join(root,'public',path)));}catch{return new Response('Not found',{status:404});}
  }},
};
globalThis.__academyTestEnv=testEnv;
const {default:worker}=await import('../dist/server/index.js');
const context={waitUntil(){},passThroughOnException(){}};
const request=(path,cookie,options={})=>worker.fetch(new Request('https://academy.test'+path,{redirect:'manual',...options,headers:{accept:'text/html',...(cookie?{cookie}:{}),...options.headers}}),testEnv,context);
const check=(name,fn)=>fn().then(()=>results.push({name,passed:true}));
const session=(role,expires=Math.floor(Date.now()/1000)+3600)=>{
  const payload=`${role}.${expires}`;
  return 'academy_access='+payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');
};
try {
 await check('Signed-out lesson is protected',async()=>assert.equal((await request('/learn/student/ai-1/1')).status,307));
 await check('Student cannot open teacher portal',async()=>assert.equal((await request('/learn/teacher/ai-1/1',session('student'))).status,307));
 await check('Unified curriculum has 264 lessons',async()=>assert.equal(data.levels.reduce((n,l)=>n+l.weeks.length,0),264));
 for(const level of data.levels) for(const week of level.weeks) {
  await check(`${level.slug}/${week.number} complete student lesson`,async()=>{
   const r=await request(`/learn/student/${level.slug}/${week.number}`,session('student'));assert.equal(r.status,200);const html=await r.text();
   for(const page of week.student.pages)assert.ok(html.includes(`id="section-${page.number}"`));
   assert.ok(html.includes('Download PDF'));assert.ok(html.includes('instruction-visual'));
  });
 }
 for(const role of ['student','teacher']) await check(`${role} workbook and guide`,async()=>{
  const r=await request(`/learn/${role}/ai-7/36?resource=${role==='teacher'?'guide':'workbook'}`,session(role));assert.equal(r.status,200);
  assert.ok((await r.text()).includes(role==='teacher'?'Teacher guide':'textarea'));
 });
 for(const role of ['student','teacher']) {
  const id=Object.keys(manifest).find(id=>manifest[id].role===role&&manifest[id].filename?.endsWith('.pdf'));
  await check(`${role} protected PDF download`,async()=>{const r=await request('/api/resource/'+id,session(role));assert.equal(r.status,200);assert.equal(r.headers.get('content-type'),'application/pdf');assert.equal(Buffer.from(await r.arrayBuffer()).subarray(0,4).toString(),'%PDF');});
  if(role==='teacher')await check('Student cannot retrieve teacher download',async()=>assert.equal((await request('/api/resource/'+id,session('student'))).status,404));
 }
 await check('Old curriculum address redirects to unified portal',async()=>{const r=await request('/learn/student/curriculum',session('student'));assert.equal(r.status,307);assert.ok(r.headers.get('location').endsWith('/learn/student'));});
 console.log(`${results.length} access and lesson checks passed`);
} finally {await writeFile('access-test-results.json',JSON.stringify({results},null,2));}
