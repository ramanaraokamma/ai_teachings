import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createHmac,randomBytes} from 'node:crypto';
const {chromium}=await import('../work/render-tools/node_modules/playwright-core/index.mjs');
const catalogue=JSON.parse(await fs.readFile('lib/lesson-videos.json','utf8')),links=JSON.parse(await fs.readFile('lib/youtube-videos.json','utf8'));
const secret=randomBytes(32).toString('hex');const env={ACADEMY_SESSION_SECRET:secret,ASSETS:{async fetch(r){try{return new Response(await fs.readFile('public'+new URL(r.url).pathname));}catch{return new Response('Missing',{status:404});}}}};
globalThis.__academyTestEnv=env;const {default:worker}=await import('../dist/server/index.js');
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});const errors=[],results=[];
const fixture=`window.__ytCalls=[];window.YT={Player:class{constructor(frame,options){this.frame=frame;setTimeout(()=>{window.__ytCalls.push({type:'ready'});options.events.onReady({target:this});},0);}seekTo(time,ahead){window.__ytCalls.push({type:'seek',time,ahead});}playVideo(){window.__ytCalls.push({type:'play'});}destroy(){this.frame.remove();}}};window.onYouTubeIframeAPIReady?.();`;
async function setup(role,width,failAPI=false){
 const context=await browser.newContext();const payload=role+'.'+(Math.floor(Date.now()/1000)+3600),cookie=payload+'.'+createHmac('sha256',secret).update(payload).digest('hex');let ytRequests=0,mediaRequests=0;
 await context.route('**/*',async route=>{
  const request=route.request(),url=new URL(request.url());
  if(url.hostname==='www.youtube.com'&&url.pathname==='/iframe_api'){ytRequests++;return failAPI?route.abort():route.fulfill({contentType:'application/javascript',body:fixture});}
  if(url.hostname==='www.youtube-nocookie.com'){ytRequests++;return route.fulfill({contentType:'text/html',body:'<!doctype html><html lang="en"><title>Controlled YouTube player fixture</title><body>Player fixture</body></html>'});}
  if(url.hostname!=='academy.test')return route.abort();
  if(url.pathname==='/favicon.ico')return route.fulfill({status:204});
  if(url.pathname.startsWith('/assets/'))return route.fulfill({body:await fs.readFile('dist/client'+url.pathname),contentType:url.pathname.endsWith('.css')?'text/css':'application/javascript'});
  if(url.pathname.startsWith('/api/lesson-video/'))mediaRequests++;
  const r=await worker.fetch(new Request(request.url(),{headers:{...request.headers(),cookie:'academy_access='+cookie}}),env,{waitUntil(){},passThroughOnException(){}});
  return route.fulfill({status:r.status,headers:Object.fromEntries(r.headers),body:Buffer.from(await r.arrayBuffer())});
 });
 const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));await page.setViewportSize({width,height:900});return {context,page,counts:()=>({ytRequests,mediaRequests})};
}
try{
 for(const [role,id,width] of [['student','ai-1/1'],['teacher','ai-1/10']].flatMap(([r,id])=>[1280,390].map(w=>[r,id,w]))){
  const {context,page,counts}=await setup(role,width);await page.goto(`https://academy.test/learn/${role}/${id}?resource=${role==='teacher'?'guide':'lesson'}`,{waitUntil:'networkidle'});
  const panel=page.locator('#week-video');assert.equal(await panel.locator('iframe').count(),0);assert.deepEqual(counts(),{ytRequests:0,mediaRequests:0});
  await panel.getByRole('button',{name:'Load this week’s video'}).click();await page.waitForFunction(()=>window.__ytCalls?.some(c=>c.type==='ready'));
  const frame=panel.locator('iframe'),url=new URL(await frame.getAttribute('src'));assert.equal(url.hostname,'www.youtube-nocookie.com');assert.equal(url.pathname,'/embed/'+links[id]);assert.equal(url.searchParams.get('origin'),'https://academy.test');assert.equal(await frame.getAttribute('referrerpolicy'),'strict-origin-when-cross-origin');assert.ok(await frame.getAttribute('title'));
  const chapter=catalogue[id].chapters[5];await panel.locator('summary').click();await panel.locator('ol button').nth(5).click();await page.waitForFunction(time=>window.__ytCalls.some(c=>c.type==='seek'&&c.time===time),chapter.start);
  assert.ok(await panel.evaluate(el=>el.scrollWidth<=el.clientWidth+1));assert.ok(await frame.evaluate(el=>el.clientHeight>=200));
  await page.addScriptTag({path:'work/learning-audit/node_modules/axe-core/axe.min.js'});assert.deepEqual(await page.evaluate(async()=>(await axe.run('#week-video')).violations.map(v=>v.id)),[]);
  await panel.locator('ol li').nth(5).getByRole('link',{name:'Read the matching section'}).click();await page.waitForLoadState('networkidle');
  const section=page.locator('#section-'+chapter.studentSections[0]);await section.waitFor({state:'visible'});await section.getByRole('link',{name:'Watch this section in the video'}).click();
  const mapped=catalogue[id].chapters.find(c=>c.studentSections.includes(chapter.studentSections[0]));await page.waitForFunction(time=>window.__ytCalls?.some(c=>c.type==='seek'&&c.time===time),mapped.start);assert.equal(counts().mediaRequests,0);
  results.push({role,id,width,lazyLoading:true,matchingYouTubeID:true,chapterSeeking:true,sectionSeeking:true,accessibilityViolations:0});console.log(role,id,width,'lazy YouTube iframe, API chapter/section seeking and accessibility passed');await context.close();
 }
 for(const id of Object.keys(links).filter(id=>!links[id])){const {context,page,counts}=await setup('student',390);await page.goto('https://academy.test/learn/student/'+id,{waitUntil:'networkidle'});const p=page.locator('#week-video');assert.ok((await p.textContent()).includes('coming soon'));assert.equal(await p.locator('iframe,video,button').count(),0);assert.equal(await page.locator('.section-video-link').count(),0);assert.deepEqual(counts(),{ytRequests:0,mediaRequests:0});await context.close();console.log(id,'pending, with no broken embeds or remote media requests');}
 const {context,page}=await setup('student',390,true);await page.goto('https://academy.test/learn/student/ai-1/1',{waitUntil:'networkidle'});await page.getByRole('button',{name:'Load this week’s video'}).click();await page.locator('#week-video [role=status]').waitFor();assert.equal(await page.getByRole('link',{name:'Open it on YouTube'}).getAttribute('href'),'https://www.youtube.com/watch?v='+links['ai-1/1']);await context.close();
 assert.deepEqual(errors,[]);await fs.writeFile('outputs/video-publishing/youtube-browser-validation.json',JSON.stringify({results,pendingWeeksChecked:Object.keys(links).filter(id=>!links[id]),blockedAPIFallback:true,pageErrors:errors,network:'Controlled API/player fixture; real oEmbed link checks saved separately.'},null,2)+'\n');
}finally{await browser.close();}
