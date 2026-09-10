import assert from 'node:assert/strict';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { createHmac, randomBytes } from 'node:crypto';

const root=resolve('.');
const manifest=JSON.parse(await readFile('lib/resource-manifest.json','utf8'));
const data=JSON.parse(await readFile('lib/academy-data.json','utf8'));
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
 await check('Only landing content is public',async()=>{
  const r=await request('/');assert.equal(r.status,200);const html=await r.text();
  assert.match(html,/Curious minds/);assert.doesNotMatch(html,/student1234|teacher1234|AI or Not|Expected independent answer/);
 });
 for(const role of ['student','teacher']) {
  await check(`${role} requires authentication`,async()=>{const r=await request(`/learn/${role}/ai-1/1`);assert.equal(r.status,307);assert.match(r.headers.get('location'),/access=required/);});
  await check(`${role} passcode creates a protected session`,async()=>{
   const r=await request('/api/access',null,{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded',origin:'https://academy.test'},body:new URLSearchParams({role,passcode:role+'1234'}).toString()});
   assert.equal(r.status,303);assert.match(r.headers.get('set-cookie'),/HttpOnly/i);assert.match(r.headers.get('set-cookie'),/Secure/i);assert.match(r.headers.get('location'),new RegExp('/learn/'+role));
  });
 }
 await check('Wrong passcode is rejected',async()=>{const r=await request('/api/access',null,{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:'role=teacher&passcode=student1234'});assert.equal(r.status,303);assert.match(r.headers.get('location'),/incorrect/);assert.equal(r.headers.get('set-cookie'),null);});
 await check('Student cannot open teacher pages',async()=>{assert.equal((await request('/learn/teacher/ai-4/17',session('student'))).status,307);});
 await check('Expired and tampered sessions are rejected',async()=>{for(const c of [session('student',1),session('teacher')+'bad'])assert.equal((await request('/learn/student',c)).status,307);});
 for(const level of data.levels) {
  await check(`${level.code} has 36 accessible weeks`,async()=>{
   const r=await request(`/learn/student/${level.slug}`,session('student'));assert.equal(r.status,200);const html=(await r.text()).replace(/<!--.*?-->/gs,'');assert.ok(html.includes('Week 36'));assert.ok(html.includes(level.phases[0].name));
  });
 }
 await check('Student lesson contains full visuals and no teacher answers',async()=>{
  const r=await request('/learn/student/ai-4/17?resource=guide',session('student'));assert.equal(r.status,200);const html=await r.text();assert.match(html,/instruction-visual/);assert.match(html,/Download editable/);assert.doesNotMatch(html,/Expected independent answer|Teacher-ready background/);assert.match(r.headers.get('cache-control'),/no-store/);
 });
 await check('Teacher guide includes aligned reasoning',async()=>{const r=await request('/learn/teacher/ai-4/17',session('teacher'));assert.equal(r.status,200);assert.match(await r.text(),/Precision is 6/);});
 await check('Workbook offers response fields',async()=>{const r=await request('/learn/student/ai-3/8?resource=workbook',session('student'));assert.equal(r.status,200);assert.match(await r.text(),/<textarea/);});
 const studentImage=Object.entries(manifest).find(([,m])=>m.mime==='image/png'&&m.role==='student')[0];
 const teacherDoc=Object.entries(manifest).find(([,m])=>m.role==='teacher'&&m.filename)[0];
 const studentDoc=Object.entries(manifest).find(([,m])=>m.role==='student'&&m.filename)[0];
 await check('Images require a session and decrypt to PNG',async()=>{
  assert.equal((await request('/api/resource/'+studentImage)).status,401);
  const r=await request('/api/resource/'+studentImage,session('student'));assert.equal(r.status,200);assert.equal(r.headers.get('content-type'),'image/png');assert.equal(Buffer.from(await r.arrayBuffer()).subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.match(r.headers.get('cache-control'),/no-store/);
 });
 await check('Teacher documents are forbidden to students',async()=>{assert.equal((await request('/api/resource/'+teacherDoc,session('student'))).status,404);});
 for(const [role,id] of [['student',studentDoc],['teacher',teacherDoc]])await check(`${role} Word download is intact`,async()=>{const r=await request('/api/resource/'+id,session(role));assert.equal(r.status,200);assert.match(r.headers.get('content-disposition'),/attachment/);assert.equal(Buffer.from(await r.arrayBuffer()).subarray(0,2).toString(),'PK');});
 await check('Image optimizer cannot bypass access',async()=>{assert.equal((await request('/_vinext/image?url=/api/resource/'+studentImage+'&w=640&q=75')).status,404);});
 await check('Cross-origin sign-in is rejected',async()=>{const r=await request('/api/access',null,{method:'POST',headers:{origin:'https://other.test'}});assert.equal(r.status,403);});
 await check('Logout clears session cookie',async()=>{const r=await request('/api/logout',session('student'),{method:'POST'});assert.equal(r.status,303);assert.match(r.headers.get('set-cookie'),/Max-Age=0/i);});
 await writeFile('access-test-results.json',JSON.stringify({passed:results.length,checks:results},null,2));
 console.log(JSON.stringify({passed:results.length,checks:results.map(r=>r.name)}));
} finally { delete globalThis.__academyTestEnv; }
