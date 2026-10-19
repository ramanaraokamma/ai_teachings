"""A native comparison table showing why an exact boundary test matters."""
from pathlib import Path
import html,subprocess
R=Path(__file__).resolve().parents[1]
def t(x,y,s,size=22,color='#17384c',weight=500):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(s)}</text>'
s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500"><rect width="1000" height="500" rx="24" fill="#f3f8fb"/>'
s+=t(32,45,'THE EXACT BOUNDARY REVEALS THE BUG',28,weight=700)+t(32,83,'Compare each expression separately for the same supplied integer.',21)
for x,label in [(390,'x = 2'),(590,'x = 3'),(790,'x = 4')]:s+=t(x+30,135,label,25,weight=700)
s+=t(608,166,'boundary',18,'#8a3b12',700)
for y,label,values in [(185,'Intended: x < 3',[True,False,False]),(280,'Bug: x <= 3',[True,True,False])]:
 s+=t(35,y+48,label,25,weight=700)
 for j,value in enumerate(values):
  x=390+j*200;special=j==1
  s+=f'<rect x="{x}" y="{y}" width="175" height="75" rx="12" fill="{"#fff0ce" if special else "#dfedea"}" stroke="{"#a35118" if special else "#6b8a97"}" stroke-width="{3 if special else 1}"/>'
  s+=t(x+45,y+47,str(value),28,weight=700)
s+=t(32,405,'Only x = 3 distinguishes these versions. Tests at 2 and 4 both miss the bug.',21)
s+=t(32,447,'A failing assertion stops its run; later assertions are not evaluated.',21)
s+=t(32,480,'The table compares expressions, rather than claiming all checks ran after failure.',19)+'</svg>'
(R/'assets/python-bridge-12-boundary-comparison.svg').write_text(s)
js="""import{chromium}from'./work/render-tools/node_modules/playwright-core/index.mjs';import{resolve}from'node:path';import{pathToFileURL}from'node:url';const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});try{const p=await b.newPage({viewport:{width:1000,height:500},deviceScaleFactor:1.5});await p.goto(pathToFileURL(resolve('assets/python-bridge-12-boundary-comparison.svg')).href);const bad=await p.locator('text').evaluateAll(ns=>ns.filter(n=>{const r=n.getBoundingClientRect();return r.x<0||r.y<0||r.right>1000||r.bottom>500;}).map(n=>n.textContent));if(bad.length)throw Error(JSON.stringify(bad));await p.screenshot({path:'assets/python-bridge-12-boundary-comparison.png'});}finally{await b.close();}"""
subprocess.run(['node','--input-type=module','-'],input=js,text=True,cwd=R,check=True)
print('Rendered boundary comparison with text bounds checked.')
