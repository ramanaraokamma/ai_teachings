"""Construct a native diagram of the supplied layout descriptions."""
from pathlib import Path
import subprocess,html
R=Path(__file__).resolve().parents[1]
def t(x,y,s,size=22,color='#16384d',weight=500):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(s)}</text>'
def bottle(x,y,label):return f'<path d="M{x-10} {y}v14l-15 12v55h50v-55l-15 -12V{y}Z" fill="#d7f0ee" stroke="#137c79" stroke-width="3"/>'+t(x-13,y+105,label,20)
def beaker(x,y):return f'<path d="M{x-42} {y}h8v76h68v-76h8" fill="#e2edf9" stroke="#326491" stroke-width="3"/>'+t(x-35,y+105,'Beaker',20)
s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800"><defs><marker id="tip" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="context-stroke"/></marker></defs><rect width="1000" height="800" rx="24" fill="#f3f8fb"/>'
s+=t(30,44,'CONSTRUCTED LAYOUTS FROM THE WRITTEN CASE',26,weight=700)+t(30,80,'Required: two bottles left of one beaker; flow from bottles to beaker.',21)
for top,title,original,reverse,status in [(100,'1 · Described original',True,False,'Counts pass · position fails · semantic flow fails'),(320,'2 · Move bottles only; keep beaker → bottles',False,True,'Counts pass · position passes · semantic flow fails'),(540,'3 · Complete proposed layout repair',False,False,'Counts pass · position passes · semantic flow passes')]:
 s+=f'<rect x="30" y="{top}" width="940" height="192" rx="16" fill="white" stroke="#bed3df"/>'+t(48,top+31,title,23,weight=700)
 y=top+48
 if original:s+=beaker(140,y)+bottle(740,y,'B1')+bottle(850,y,'B2')
 else:s+=bottle(140,y,'B1')+bottle(250,y,'B2')+beaker(820,y)
 left,right=(650,380) if reverse else (380,650);color='#a4472e' if original or reverse else '#08796d'
 s+=f'<path d="M{left} {top+95}H{right}" stroke="{color}" stroke-width="6" marker-end="url(#tip)"/>'
 s+=t(350,top+171,status,20,color,700)
s+=t(30,775,'These classroom diagrams illustrate descriptions; they are not generator outputs or verified chemistry.',18)+'</svg>'
(R/'assets/ai-3-11-spatial-layout-audit.svg').write_text(s)
js="""import{chromium}from'./work/render-tools/node_modules/playwright-core/index.mjs';import{pathToFileURL}from'node:url';import{resolve}from'node:path';const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});try{const p=await b.newPage({viewport:{width:1000,height:800},deviceScaleFactor:1.5});await p.goto(pathToFileURL(resolve('assets/ai-3-11-spatial-layout-audit.svg')).href);const bad=await p.locator('text').evaluateAll(ns=>ns.filter(n=>{const r=n.getBoundingClientRect();return r.x<0||r.y<0||r.right>1000||r.bottom>800;}).map(n=>n.textContent));if(bad.length)throw Error(JSON.stringify(bad));await p.screenshot({path:'assets/ai-3-11-spatial-layout-audit.png'});}finally{await b.close();}"""
subprocess.run(['node','--input-type=module','-'],input=js,text=True,cwd=R,check=True)
print('Rendered native spatial-layout audit with text bounds checked.')
