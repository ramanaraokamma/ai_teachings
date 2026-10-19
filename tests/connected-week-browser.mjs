const {chromium}=await import(process.env.ACADEMY_PLAYWRIGHT_MODULE||'playwright-core');
import fs from 'node:fs/promises';import {resolve} from 'node:path';import {createHmac,randomBytes} from 'node:crypto';import assert from 'node:assert/strict';
const secret=randomBytes(32).toString('hex');const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{fetch:async r=>{try{return new Response(await fs.readFile('public'+new URL(r.url).pathname));}catch{return new Response('Not found',{status:404});}}}};globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');const contextArgs={waitUntil(){},passThroughOnException(){}};
const browser=await chromium.launch({executablePath:process.env.ACADEMY_CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const level=process.env.CONNECTED_LEVEL||'ai-1';const week=Number(process.env.CONNECTED_WEEK||1);const reportPrefix=level==='ai-1'?`week${week}`:`${level}-week${week}`;const programme=JSON.parse(await fs.readFile('content/programme.json','utf8'));const source=[...programme.weeks,...programme.python_bridge].find(w=>w.id===`${level}/${week}`);assert.ok(source?.sections[0]?.reading_flow,'This week needs an authored connected reading flow');const revealTitle=source.sections[5].reading_flow.groups.find(g=>g.collapsed&&g.kind==='example')?.title;assert.ok(revealTitle);const firstResponse=source.workbook[0].blocks.findIndex(b=>b.type==='response');const out=`outputs/${level==='ai-1'?'':level+'-'}week-${String(week).padStart(2,'0')}-connected-review`;const results=[],pageErrors=[];await fs.mkdir(out,{recursive:true});
const oldWorksheetSuffix='section-1-block-'+(source.workbook.slice(0,11).reduce((n,s)=>n+1+s.blocks.filter(b=>!b.reading_addition).length,0)+1+source.workbook[11].blocks.findIndex(b=>b.type==='response'&&!b.reading_addition));
const labData=JSON.parse(await fs.readFile('content/learning-tools.json','utf8'))[source.id];
const mime=path=>path.endsWith('.wasm')?'application/wasm':path.endsWith('.css')?'text/css':path.endsWith('.svg')?'image/svg+xml':path.endsWith('.json')?'application/json':path.endsWith('.zip')?'application/zip':'application/javascript';
try{
 for(const role of ['student','teacher']){
 const context=await browser.newContext();const payload=`${role}.${Math.floor(Date.now()/1000)+3600}`;const cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');await context.addCookies([{name:'academy_access',value:cookie,domain:'academy.test',path:'/',secure:true,httpOnly:true}]);
 await context.route('**/*',async route=>{const req=route.request(),url=new URL(req.url());if(url.hostname!=='academy.test')return route.abort();if(url.pathname.startsWith('/assets/')||url.pathname.startsWith('/python-runtime/')||url.pathname==='/python-lab-worker.mjs'||url.pathname==='/favicon.svg'){try{return route.fulfill({body:await fs.readFile('dist/client'+url.pathname),contentType:mime(url.pathname)});}catch{return route.abort();}}const response=await worker.fetch(new Request(req.url(),{method:req.method(),headers:{...req.headers(),cookie:`academy_access=${cookie}`}}),env,contextArgs);return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});});

 const page=await context.newPage();page.on('pageerror',e=>pageErrors.push(String(e)));
 const resources=role==='student'?['lesson','workbook']:['guide'];
 for(const resource of resources)for(const width of[1280,390]){
  const url='https://academy.test/learn/'+role+'/'+level+'/'+week+'?resource='+resource;
  const draftKey=`academy-answer-v1:/learn/student/${level}/${week}:workbook:${level}/${week}/workbook-section-1-block-${firstResponse+1}`;
  if(resource==='workbook'&&((level==='ai-2'&&[5,15,24].includes(week))||(level==='ai-3'&&[6,11,13,16,25].includes(week))))await page.addInitScript(key=>localStorage.setItem(key,'Earlier worksheet answer'),`academy-answer-v1:/learn/student/${level}/${week}:workbook:${level}/${week}/workbook-${oldWorksheetSuffix}`);
  if(resource==='workbook')await page.addInitScript(key=>{if(!localStorage.getItem(key))localStorage.setItem(key,'A draft from the earlier workbook.');},draftKey);
  if(resource==='lesson'&&level==='ai-2'&&week===5)await page.addInitScript(()=>localStorage.setItem('academy-code-v1:student:ai-2/5:0','# Earlier for-loop draft\nprint(6)'));
  await page.setViewportSize({width,height:950});await page.goto(url,{waitUntil:'networkidle'});
  const expected=source[resource==='guide'?'teacher':resource==='workbook'?'workbook':'sections'].length;
  assert.equal(await page.locator('.lesson-reader-shell .lesson-section').count(),expected);
  assert.equal(await page.locator('.flow-overview .flow-route a').count(),6);
  assert.ok(await page.locator('.flow-reference-bank > details:not([open])').count()>0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),resource+' overflow '+width);
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
  if(resource==='lesson'&&labData.labs.length){
   const preferred=Math.max(0,labData.labs.findIndex(l=>l.primary));const select=page.locator('.python-lab select');assert.equal(await select.inputValue(),String(preferred));
   await page.waitForFunction(code=>document.querySelector('.python-editor')?.value===code,labData.labs[preferred].code);
   if(level==='ai-2'&&week===5){await select.selectOption('0');await page.waitForFunction(()=>document.querySelector('.python-editor')?.value==='# Earlier for-loop draft\nprint(6)');await select.selectOption(String(preferred));await page.waitForFunction(code=>document.querySelector('.python-editor')?.value===code,labData.labs[preferred].code);}
  }
  if(resource==='workbook'){
   const saved=page.locator('textarea[data-evidence-key="'+draftKey+'"]');await saved.waitFor();assert.ok((await saved.inputValue()).includes('earlier workbook'));
   if(((level==='ai-2'&&[5,15,24].includes(week))||(level==='ai-3'&&[6,11,13,16,25].includes(week)))){const old=page.locator(`textarea[data-evidence-key$="workbook-${oldWorksheetSuffix}"]`);assert.equal(await old.inputValue(),'Earlier worksheet answer');assert.ok((await old.locator('xpath=ancestor::details[1]').textContent()).includes(level==='ai-3'?(week===6?'List required output fields':'Explain the weekly mechanism'):week===5?'range(2, 5)':week===15?'Identify the root':'Why does A win'));const last=source.workbook[11].blocks.findLastIndex(b=>b.type==='response');const fresh=page.locator(`textarea[data-evidence-key$="workbook-section-12-added-block-${last+1}"]`);assert.equal(await fresh.inputValue(),'');assert.ok(await fresh.isVisible());}
  }
  if(resource==='lesson'){
   const check=page.locator('#section-6 details').filter({has:page.locator('summary',{hasText:revealTitle})});
   assert.equal(await check.getAttribute('open'),null);await check.locator('summary').focus();await page.keyboard.press('Enter');assert.equal(await check.getAttribute('open'),'');
   await page.goto(url+'#section-18',{waitUntil:'networkidle'});await page.waitForFunction(()=>document.querySelector('#section-18').closest('details')?.open);assert.ok(await page.locator('#section-18').isVisible());
   await page.goto(url,{waitUntil:'networkidle'});
  }
  const closed=await page.locator('[data-connected-reading] details:not([open])').count();await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));assert.equal(await page.locator('[data-connected-reading] details:not([open])').count(),0);await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));assert.equal(await page.locator('[data-connected-reading] details:not([open])').count(),closed);
  await page.addScriptTag({path:resolve(process.env.ACADEMY_AXE_PATH||'work/learning-audit/node_modules/axe-core/axe.min.js')});const audit=await page.evaluate(async()=>await window.axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}}));const violations=audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}));assert.deepEqual(violations,[],resource+' '+width);
  await page.locator('.flow-overview').scrollIntoViewIfNeeded();await page.screenshot({path:out+'/'+resource+'-website-'+width+'.png'});
  await page.evaluate(async()=>{await Promise.all([...document.images].filter(i=>i.complete&&i.naturalWidth).map(i=>i.decode().catch(()=>{})));});
  if(width===1280)await page.locator('#section-'+(resource==='workbook'?(level==='python-bridge'||['ai-5','ai-6','ai-7'].includes(level)?6:13):resource==='guide'?2:week>=2?6:3)).screenshot({path:out+'/'+resource+'-website-explanation.png',style:'.portal-header{display:none !important}'});
  results.push({role,resource,width,sections:expected,overflow:false,accessibility_violations:violations,draft_keys_preserved:resource==='workbook',print_includes_reference:true});console.log(role,resource,width,'passed');
 }
 await context.close();
 }
 assert.deepEqual(pageErrors,[]);await fs.writeFile(`reports/${reportPrefix}-connected-browser.json`,JSON.stringify({checks:results,accessibility_audits:6,errors:pageErrors},null,2));console.log('Connected Week '+week+': all '+(source.sections.length+source.teacher.length+source.workbook.length)+' sections, draft compatibility, reveal-before-feedback, reference anchors, print completeness and six accessibility audits passed.');
}finally{await browser.close();}
