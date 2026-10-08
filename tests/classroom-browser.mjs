// Optional browser check: provide ACADEMY_PLAYWRIGHT_MODULE if playwright-core is not installed.
const {chromium}=await import(process.env.ACADEMY_PLAYWRIGHT_MODULE || 'playwright-core');
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {createHmac,randomBytes} from 'node:crypto';
import assert from 'node:assert/strict';
const secret=randomBytes(32).toString('hex');
const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{fetch:async r=>{try{return new Response(await readFile('public'+new URL(r.url).pathname));}catch{return new Response('Not found',{status:404});}}}};
globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');
const browser=await chromium.launch({executablePath:process.env.ACADEMY_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const out='work/classroom-browser';await mkdir(out,{recursive:true});const results=[],errors=[];
try{
 for(const role of ['student','teacher']){
  const context=await browser.newContext();const payload=`${role}.${Math.floor(Date.now()/1000)+3600}`;const cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');
  await context.addCookies([{name:'academy_access',value:cookie,domain:'academy.test',path:'/',secure:true,httpOnly:true}]);
  await context.route('**/*',async route=>{const req=route.request(),url=new URL(req.url());if(url.hostname!=='academy.test')return route.abort();if(url.pathname.startsWith('/assets/')||url.pathname==='/favicon.svg'){try{return route.fulfill({body:await readFile('dist/client'+url.pathname),contentType:url.pathname.endsWith('.css')?'text/css':url.pathname.endsWith('.svg')?'image/svg+xml':'application/javascript'});}catch{return route.abort();}}
   const r=await worker.fetch(new Request(req.url(),{method:req.method(),headers:{...req.headers(),cookie:`academy_access=${cookie}`}}),env,{waitUntil(){},passThroughOnException(){}});await route.fulfill({status:r.status,headers:Object.fromEntries(r.headers),body:Buffer.from(await r.arrayBuffer())});});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
  for(const width of [1280,390]){
   await page.setViewportSize({width,height:900});
   const paths=[`/learn/${role}`,...['ai-1','ai-2','ai-3','python-bridge','ai-4','ai-5','ai-6','ai-7'].map(l=>`/learn/${role}/${l}`),...['ai-1/1','ai-2/15','ai-3/17','python-bridge/12','ai-4/22','ai-5/15','ai-6/15','ai-7/36'].map(id=>`/learn/${role}/${id}`)];
   for(const path of paths){const r=await page.goto('https://academy.test'+path,{waitUntil:'networkidle'});assert.equal(r.status(),200,path);await page.locator('img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{timeout:15000});const metrics=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0)}));assert.equal(metrics.overflow,false,path+' '+width);assert.ok(metrics.images,path);results.push({path,width,...metrics});}
   await page.goto(`https://academy.test/learn/${role}`,{waitUntil:'networkidle'});assert.deepEqual(await page.locator('.level-number').allTextContents(),['01','02','03','Bridge','04','05','06','07']);await page.screenshot({path:`${out}/map-${role}-${width}.png`,fullPage:true});
   await page.goto(`https://academy.test/learn/${role}/ai-1/1?resource=workbook`,{waitUntil:'networkidle'});const answer=page.locator('textarea').first();await answer.fill('My evidence connects the input, deciding step and output.');await page.reload({waitUntil:'networkidle'});assert.equal(await page.locator('textarea').first().inputValue(),'My evidence connects the input, deciding step and output.');
   const tick=page.locator('.learning-progress input');await tick.check();await page.reload({waitUntil:'networkidle'});assert.ok(await tick.isChecked());await page.screenshot({path:`${out}/workbook-${role}-${width}.png`,fullPage:true});await page.locator('.week-pagination > a').last().click();await page.waitForURL('**/ai-1/2?resource=workbook');await page.waitForFunction(()=>document.querySelector('textarea')?.value==='');await page.locator('.week-pagination > a').first().click();await page.waitForURL('**/ai-1/1?resource=workbook');await page.waitForFunction(()=>document.querySelector('textarea')?.value==='My evidence connects the input, deciding step and output.');
   await page.locator('.interactive-response button').first().click();await page.reload({waitUntil:'networkidle'});assert.equal(await page.locator('textarea').first().inputValue(),'');
   await page.goto(`https://academy.test/learn/${role}/ai-1/1?resource=lesson`,{waitUntil:'networkidle'});await page.locator('.explanation-toggle').first().click();assert.ok(await page.locator('.worked-reveal').first().isVisible());await page.locator('.visual-expand').first().click();assert.ok(await page.getByRole('dialog').isVisible());await page.keyboard.press('Escape');await page.screenshot({path:`${out}/lesson-${role}-${width}.png`,fullPage:true});
   if(width===1280)await page.pdf({path:`${out}/lesson-${role}.pdf`,printBackground:true,preferCSSPageSize:true});
   await page.goto(`https://academy.test/learn/${role}/python-bridge`,{waitUntil:'networkidle'});await page.getByRole('button',{name:'Compare after your independent attempt'}).click();assert.ok(await page.getByText('The outputs are 7, then 2.',{exact:false}).isVisible());
   console.log(role,width,'navigation, pictures, draft reload/clear, progress, readiness and print passed');
  }await context.close();
 }
 assert.deepEqual(errors,[]);await writeFile('reports/classroom-browser-validation.json',JSON.stringify({navigation_checks:results.length,interactive_checks:24,errors,results},null,2));console.log(results.length,'browser navigation checks passed');
}finally{await browser.close();delete globalThis.__academyTestEnv;}
