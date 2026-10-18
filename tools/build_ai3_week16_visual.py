"""Represent supplied aggregate counts without inventing per-trial records."""
from pathlib import Path
import subprocess,html
R=Path(__file__).resolve().parents[1]
def t(x,y,s,size=22,color='#17384c',weight=500):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(s)}</text>'
s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500"><rect width="1000" height="500" rx="24" fill="#f3f8fb"/>'
s+=t(32,44,'SAME DENOMINATOR · CHANGED NUMERATOR',27,weight=700)+t(32,82,'Cells illustrate aggregate counts; their positions are not actual trial identities.',20)
for x,count,title in [(60,15,'Original supplied count'),(620,14,'Revised supplied count')]:
 s+=t(x,120,title,22,weight=700)
 for i in range(20):
  xx=x+(i%5)*58;yy=142+(i//5)*54;passed=i<count
  s+=f'<rect x="{xx}" y="{yy}" width="48" height="44" rx="7" fill="{"#d4eee8" if passed else "#e3e9ef"}" stroke="#68899b"/>'
  s+=t(xx+16,yy+30,'P' if passed else '–',25,'#086e61' if passed else '#4a6173',700)
 s+=t(x,409,f'{count} ÷ 20 × 100 = {count*5}%',28,weight=700)
s+='<path d="M400 240H550M530 220L550 240L530 260" fill="none" stroke="#147b79" stroke-width="6"/>'+t(405,285,'One fewer pass',18)
s+=t(32,455,'P = counted as passing; – = not counted as passing. Total stays 20.',20)
s+=t(32,484,'A changed count supplies no new evidence for the intended meeting date.',20)+'</svg>'
(R/'assets/ai-3-16-percentage-counts.svg').write_text(s)
js="""import{chromium}from'./work/render-tools/node_modules/playwright-core/index.mjs';import{resolve}from'node:path';import{pathToFileURL}from'node:url';const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});try{const p=await b.newPage({viewport:{width:1000,height:500},deviceScaleFactor:1.5});await p.goto(pathToFileURL(resolve('assets/ai-3-16-percentage-counts.svg')).href);const bad=await p.locator('text').evaluateAll(ns=>ns.filter(n=>{const r=n.getBoundingClientRect();return r.x<0||r.y<0||r.right>1000||r.bottom>500;}).map(n=>n.textContent));if(bad.length)throw Error(JSON.stringify(bad));await p.screenshot({path:'assets/ai-3-16-percentage-counts.png'});}finally{await b.close();}"""
subprocess.run(['node','--input-type=module','-'],input=js,text=True,cwd=R,check=True)
print('Rendered native aggregate-percentage grid with text bounds checked.')
