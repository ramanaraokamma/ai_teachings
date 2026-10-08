const {chromium}=await import(process.env.ACADEMY_PLAYWRIGHT_MODULE||'playwright-core');
import fs from 'node:fs/promises';import {resolve} from 'node:path';import {createHmac,randomBytes} from 'node:crypto';import assert from 'node:assert/strict';
const secret=randomBytes(32).toString('hex');const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{fetch:async r=>{try{return new Response(await fs.readFile('public'+new URL(r.url).pathname));}catch{return new Response('Not found',{status:404});}}}};globalThis.__academyTestEnv=env;
const {default:worker}=await import('../dist/server/index.js');const contextArgs={waitUntil(){},passThroughOnException(){}};
const browser=await chromium.launch({executablePath:process.env.ACADEMY_CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const results=[],failures=[],pageErrors=[];await fs.mkdir('work/learning-browser',{recursive:true});
const mime=path=>path.endsWith('.wasm')?'application/wasm':path.endsWith('.css')?'text/css':path.endsWith('.svg')?'image/svg+xml':path.endsWith('.json')?'application/json':path.endsWith('.zip')?'application/zip':'application/javascript';
try{
 for(const role of ['teacher']){
 const context=await browser.newContext();const payload=`${role}.${Math.floor(Date.now()/1000)+3600}`;const cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');await context.addCookies([{name:'academy_access',value:cookie,domain:'academy.test',path:'/',secure:true,httpOnly:true}]);
 await context.route('**/*',async route=>{const req=route.request(),url=new URL(req.url());if(url.hostname!=='academy.test')return route.abort();if(url.pathname.startsWith('/assets/')||url.pathname.startsWith('/python-runtime/')||url.pathname==='/python-lab-worker.mjs'||url.pathname==='/favicon.svg'){try{return route.fulfill({body:await fs.readFile('dist/client'+url.pathname),contentType:mime(url.pathname)});}catch{return route.abort();}}const response=await worker.fetch(new Request(req.url(),{method:req.method(),headers:{...req.headers(),cookie:`academy_access=${cookie}`}}),env,contextArgs);return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});});
 const page=await context.newPage();page.on('pageerror',e=>pageErrors.push({path:page.url(),error:String(e)}));
 await page.goto('https://academy.test/learn/teacher/pilot',{waitUntil:'networkidle'});
 const fields={group:'TEST_GROUP',learnerCode:'TEST01',date:'2026-10-07',minutes:'12',learnerEvidence:'Synthetic browser test only: learner traced the deciding step.'};
 for(const[name,value]of Object.entries(fields))await page.locator('[name="'+name+'"]').fill(value);
 for(const[name,value]of Object.entries({priorExposure:'no',supportUsed:'none',explanation:'independent',trace:'independent',limits:'with support'}))await page.locator('[name="'+name+'"]').selectOption(value);
 await page.getByRole('button',{name:'Save actual observation'}).click();await page.getByText('1 records · 1 learner codes',{exact:false}).waitFor();
 let pending=page.waitForEvent('download');await page.getByRole('button',{name:'Download observation JSON'}).click();const download=await pending;const body=await fs.readFile(await download.path(),'utf8');assert.equal(JSON.parse(body).rows[0].learnerCode,'TEST01');
 await page.getByText('Clear records from this browser',{exact:true}).click();await page.getByRole('button',{name:'Clear local pilot records'}).click();assert.ok(await page.getByText('0 records · 0 learner codes',{exact:false}).isVisible());
 await page.locator('input[type=file]').setInputFiles({name:'test.json',mimeType:'application/json',buffer:Buffer.from(body)});await page.getByText('1 records · 1 learner codes',{exact:false}).waitFor();
 await page.getByText('Clear records from this browser',{exact:true}).click();await page.getByRole('button',{name:'Clear local pilot records'}).click();
 assert.deepEqual(pageErrors,[]);await context.close();console.log('Pilot save, export, clear and restore passed with synthetic isolated browser records only.');
 }
}finally{await browser.close();}
