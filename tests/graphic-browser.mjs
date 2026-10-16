const {chromium}=await import(process.env.ACADEMY_PLAYWRIGHT_MODULE||'playwright-core');
import fs from 'node:fs/promises';import {resolve} from 'node:path';import {createHmac,randomBytes} from 'node:crypto';import assert from 'node:assert/strict';
const secret=randomBytes(32).toString('hex');const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{fetch:async r=>{try{return new Response(await fs.readFile('public'+new URL(r.url).pathname));}catch{return new Response('Not found',{status:404});}}}};globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');const contextArgs={waitUntil(){},passThroughOnException(){}};
const browser=await chromium.launch({executablePath:process.env.ACADEMY_CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const results=[],failures=[],pageErrors=[];await fs.mkdir('work/learning-browser',{recursive:true});
const mime=path=>path.endsWith('.wasm')?'application/wasm':path.endsWith('.css')?'text/css':path.endsWith('.svg')?'image/svg+xml':path.endsWith('.json')?'application/json':path.endsWith('.zip')?'application/zip':'application/javascript';
try{
 for(const role of ['student','teacher']){
 const context=await browser.newContext();const payload=`${role}.${Math.floor(Date.now()/1000)+3600}`;const cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');await context.addCookies([{name:'academy_access',value:cookie,domain:'academy.test',path:'/',secure:true,httpOnly:true}]);
 await context.route('**/*',async route=>{const req=route.request(),url=new URL(req.url());if(url.hostname!=='academy.test')return route.abort();if(url.pathname.startsWith('/assets/')||url.pathname.startsWith('/python-runtime/')||url.pathname==='/python-lab-worker.mjs'||url.pathname==='/favicon.svg'){try{return route.fulfill({body:await fs.readFile('dist/client'+url.pathname),contentType:mime(url.pathname)});}catch{return route.abort();}}const response=await worker.fetch(new Request(req.url(),{method:req.method(),headers:{...req.headers(),cookie:`academy_access=${cookie}`}}),env,contextArgs);return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});});
 const page=await context.newPage();page.on('pageerror',e=>pageErrors.push({path:page.url(),error:String(e)}));
 const samples=['ai-1/2','ai-2/8','ai-3/20','python-bridge/5','ai-4/18','ai-5/20','ai-6/20','ai-7/20'];
 for(const width of [1280,390]){await page.setViewportSize({width,height:900});
  for(const id of samples){const path='/learn/'+role+'/'+id+'?resource='+(role==='teacher'?'guide':'lesson');await page.goto('https://academy.test'+path,{waitUntil:'networkidle'});await page.getByRole('link',{name:'Open this week’s visual concept journey'}).click();const journey=page.locator('.lesson-section').filter({has:page.getByText('Visual concept journey',{exact:true})});assert.equal(await journey.locator('img').count(),6);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));results.push({role,path,width,journeyImages:6,imagesLoaded:true,pageOverflow:false});
   if(id==='python-bridge/5'){await journey.locator('.visual-expand').nth(2).click();const dialog=page.getByRole('dialog');assert.ok(await dialog.isVisible());await dialog.getByRole('button',{name:'Read labels',exact:true}).click();const dimensions=await dialog.locator('.visual-detail-scroll').evaluate(el=>({scroll:el.scrollWidth,client:el.clientWidth,image:el.querySelector('img').getBoundingClientRect().width}));assert.ok(dimensions.image>=1100);if(width===390)assert.ok(dimensions.scroll>dimensions.client);await dialog.getByRole('button',{name:'Fit whole picture'}).click();assert.ok(await dialog.locator('.visual-detail-scroll.fit-picture').count());await page.keyboard.press('Escape');}
  }
 }
 await context.close();console.log(role,'eight levels, six-picture journeys, image loading, mobile zoom and fit passed.');
 }
 assert.deepEqual(pageErrors,[]);await fs.writeFile('reports/graphic-browser-validation.json',JSON.stringify({navigation_checks:results.length,errors:pageErrors,results},null,2));
}finally{await browser.close();}
