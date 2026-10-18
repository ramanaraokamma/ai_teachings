"""Native timeline: upload dates are distinct from effective authority changes."""
from pathlib import Path
import subprocess,html
R=Path(__file__).resolve().parents[1]
def t(x,y,s,size=22,color='#17384c',weight=500):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(s)}</text>'
def x(day):return 80+(day-1)*65
s='<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="600" viewBox="0 0 1100 600"><rect width="1100" height="600" rx="24" fill="#f3f8fb"/>'
s+=t(34,44,'FICTIONAL AUTHORITY TIMELINE',27,weight=700)+t(34,83,'A: Hall 1 from day 1. B: signed change to Hall 3 from day 8, inclusive.',22)
for y,title,segments in [(180,'Original A → B chain',[(1,8,'Hall 1 · A','#d7e9ff'),(8,15,'Hall 3 · B','#e5ddfa')]),(410,'Changed case: C revokes B from day 12',[(1,8,'Hall 1 · A','#d7e9ff'),(8,12,'Hall 3 · B','#e5ddfa'),(12,15,'Hall 1 · C','#d7e9ff')])]:
 s+=t(34,y-40,title,23,weight=700)
 for start,end,label,color in segments:
  s+=f'<rect x="{x(start)}" y="{y}" width="{x(end)-x(start)}" height="64" fill="{color}" stroke="#7c93a5"/>'
  s+=t(x(start)+24,y+40,label,23,weight=700)
 for day in [1,6,8,9,10,12,13,14]:
  s+=f'<path d="M{x(day)} {y+64}v9" stroke="#536d80"/>'+t(x(day)-8,y+96,str(day),18)
 s+=t(1005,y+96,'day',18)
 for day in ([6,9] if y==180 else [9,13]):
  s+=f'<path d="M{x(day)} {y-16}v16" stroke="#087b72" stroke-width="3" stroke-dasharray="6 4"/>'
 if y==180:s+=t(332,y+130,'Query day 6: Hall 1',20,'#086f6a',700)+t(646,y+130,'Query day 9: Hall 3',20,'#086f6a',700)
 else:s+=t(524,y+130,'Day 9 stays Hall 3',20,'#086f6a',700)+t(824,y+130,'Day 13: Hall 1',20,'#086f6a',700)
s+=t(34,341,'Old A uploaded on day 10 is a copy, not a new authorised rule.',22,'#8d4228',700)
s+=t(34,580,'Signed/effective status is given here; this diagram does not verify real signatures or rules.',20)+'</svg>'
(R/'assets/ai-3-15-authority-timeline.svg').write_text(s)
js="""import{chromium}from'./work/render-tools/node_modules/playwright-core/index.mjs';import{resolve}from'node:path';import{pathToFileURL}from'node:url';const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});try{const p=await b.newPage({viewport:{width:1100,height:600},deviceScaleFactor:1.5});await p.goto(pathToFileURL(resolve('assets/ai-3-15-authority-timeline.svg')).href);const bad=await p.locator('text').evaluateAll(ns=>ns.filter(n=>{const r=n.getBoundingClientRect();return r.x<0||r.y<0||r.right>1100||r.bottom>600;}).map(n=>n.textContent));if(bad.length)throw Error(JSON.stringify(bad));await p.screenshot({path:'assets/ai-3-15-authority-timeline.png'});}finally{await b.close();}"""
subprocess.run(['node','--input-type=module','-'],input=js,text=True,cwd=R,check=True)
print('Rendered native effective-date timeline with text bounds checked.')
