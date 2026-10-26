import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createHmac,randomBytes} from 'node:crypto';
const {chromium}=await import(process.env.ACADEMY_PLAYWRIGHT_MODULE||'playwright-core');
const secret=randomBytes(32).toString('hex');
const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{fetch:async r=>{try{return new Response(await fs.readFile('public'+new URL(r.url).pathname));}catch{return new Response('Missing',{status:404});}}}};
globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const errors=[];
try{
 for(const role of ['student','teacher']){
  const context=await browser.newContext({acceptDownloads:true});
  const payload=`${role}.${Math.floor(Date.now()/1000)+3600}`;
  const cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');
  await context.route('**/*',async route=>{
   const req=route.request(),url=new URL(req.url());if(url.hostname!=='academy.test')return route.abort();
   if(url.pathname.startsWith('/assets/'))return route.fulfill({body:await fs.readFile('dist/client'+url.pathname),contentType:url.pathname.endsWith('.css')?'text/css':'application/javascript'});
   const response=await worker.fetch(new Request(req.url(),{headers:{...req.headers(),cookie:`academy_access=${cookie}`}}),env,{waitUntil(){},passThroughOnException(){}});
   return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});
  });
  const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
  for(const width of [1280,390]){
   await page.setViewportSize({width,height:900});
   await page.goto(`https://academy.test/learn/${role}/ai-1/1?resource=${role==='teacher'?'guide':'lesson'}`,{waitUntil:'networkidle'});
   const panel=page.locator('.learning-checkpoint');assert.equal(await panel.count(),1);
   assert.equal(await panel.locator('.checkpoint-route > li').count(),3);
   await panel.locator('summary').click();
   const answer=`${role}: I can trace the example and name what to check next.`;
   await panel.locator('textarea').first().fill(answer);
   await page.reload({waitUntil:'networkidle'});await panel.locator('summary').click();
   assert.equal(await panel.locator('textarea').first().inputValue(),answer);
   const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download evidence (.json)',exact:true}).click();
   const download=await downloadPromise;const exported=JSON.parse(await fs.readFile(await download.path(),'utf8'));
   assert.ok(exported.evidence.some(e=>e.answer===answer));assert.ok(exported.evidence.every(e=>e.role===role));
   await panel.locator('summary').click();await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));
   assert.equal(await panel.locator('details').getAttribute('open'),'');await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
   assert.equal(await panel.locator('details').getAttribute('open'),null);
   assert.ok(await panel.evaluate(el=>el.scrollWidth<=el.clientWidth+1));
   await page.addScriptTag({path:'work/learning-audit/node_modules/axe-core/axe.min.js'});
   const violations=await page.evaluate(async()=> (await window.axe.run('.learning-checkpoint')).violations.map(v=>v.id));assert.deepEqual(violations,[]);
   console.log(`${role} ${width}px: checkpoint, saved draft, portfolio, print and accessibility passed`);
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser.close();}
