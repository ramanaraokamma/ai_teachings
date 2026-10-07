/** Export and validate offline HTML. PLAYWRIGHT_MODULE may specify playwright-core. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const module=process.env.PLAYWRIGHT_MODULE||path.resolve(root,'../..','work/render-tools/node_modules/playwright-core/index.mjs');
const {chromium}=await import(pathToFileURL(module));
const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
let manifest=JSON.parse(await fs.readFile(path.join(root,'reports/html-manifest.json'),'utf8'));
let retained=[];
if(process.env.INCREMENTAL==='1'){
 const previous=JSON.parse(await fs.readFile(path.join(root,'reports/browser-validation.json'),'utf8'));
 const hashes=new Map(previous.results.map(r=>[r.file,r.sha256]));
 const changed=new Set(manifest.filter(r=>hashes.get(r.file)!==r.sha256).map(r=>r.file));
 retained=previous.results.filter(r=>!changed.has(r.file));manifest=manifest.filter(r=>changed.has(r.file));
 console.log('Refreshing changed resources:',manifest.length);
}
let next=0,done=0;const results=[...retained],errors=[];
async function worker(){
 const page=await browser.newPage();
 page.on('pageerror',e=>errors.push({type:'javascript',error:e.message}));
 while(next<manifest.length){
  const item=manifest[next++];
  try{
   await page.setViewportSize({width:1280,height:900});
   await page.goto(pathToFileURL(path.join(root,item.file)).href,{waitUntil:'load'});
   await page.evaluate(()=>document.fonts.ready);
   const check=await page.evaluate(()=>({sections:document.querySelectorAll('[data-section]').length,images:[...document.images].length,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),overflow:document.documentElement.scrollWidth>innerWidth+1,words:document.body.innerText.trim().split(/\s+/).length}));
   await page.setViewportSize({width:390,height:844});
   const mobile=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   if(check.sections!==item.sections||check.broken.length||check.overflow||mobile)errors.push({file:item.file,...check,mobileOverflow:mobile});
   const input=page.locator('textarea').first();
   if(await input.count()){
    await input.fill('My evidence survives printing.');
    const value=await input.evaluate(t=>t.nextElementSibling.textContent);
    if(value!=='My evidence survives printing.')errors.push({file:item.file,type:'response-print-sync'});
    await input.fill('');
   }
   if(item.week==='ai-1/3'&&item.role==='student'){
    for(const [v,want] of [[29,'Lamp ON'],[30,'Lamp OFF']]){
     const got=await page.locator('[data-sensor]').evaluate((s,v)=>{const i=s.querySelector('input');i.value=v;i.dispatchEvent(new Event('input'));return s.querySelector('[data-action]').textContent},v);
     if(got!==want)errors.push({type:'sensor-boundary',v,got});
    }
    await page.locator('[data-sensor] input').evaluate(i=>{i.value=18;i.dispatchEvent(new Event('input'))});
   }
   await page.setViewportSize({width:1280,height:900});
   const output=path.join(root,'downloads',item.role,path.basename(item.file,'.html')+'.pdf');
   await fs.mkdir(path.dirname(output),{recursive:true});
   await page.pdf({path:output,format:'Letter',printBackground:true,preferCSSPageSize:true});
   results.push({...item,desktop:check,mobileOverflow:mobile,pdf:path.relative(root,output)});
  }catch(e){errors.push({file:item.file,error:String(e)});}
  done++;if(done%36===0)console.log(`Validated and exported ${done}/${manifest.length}`);
 }
 await page.close();
}
await Promise.all([worker(),worker(),worker()]);
await browser.close();
await fs.writeFile(path.join(root,'reports/browser-validation.json'),JSON.stringify({resources:results.length,viewportChecks:results.length*2,errors,results},null,2));
console.log(JSON.stringify({resources:results.length,errors:errors.length}));
if(errors.length)process.exitCode=1;
