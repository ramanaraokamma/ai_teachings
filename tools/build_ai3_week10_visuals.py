"""Render code-native classroom evidence cards; no image model is called."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1];A=R/'assets'
def text(x,y,s,size=22,fill='#16384d',weight=500):
 import html
 return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{fill}" font-weight="{weight}">{html.escape(s)}</text>'
start='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="440" viewBox="0 0 1000 440"><rect width="1000" height="440" rx="24" fill="#f3f8fb"/>'
body=start+text(32,45,'TWO SUPPLIED TOY GRIDS · ONE ILLUSTRATIVE UPDATE',24,weight=700)
for x,title,grid in [(50,'Before',[[.2,.8],[.6,.3]]),(590,'After (supplied)',[[.1,.9],[.4,.2]])]:
 body+=text(x,90,title,24,weight=700)
 for row in range(2):
  for col in range(2):
   value=grid[row][col];shade=round(value*255);xx=x+col*145;yy=110+row*110
   body+=f'<rect x="{xx}" y="{yy}" width="130" height="95" rx="12" fill="rgb({shade},{shade},{shade})" stroke="#6c8595"/>'
   body+=text(xx+40,yy+57,str(value),30,'#fff' if value<.5 else '#102a3b',700)
body+='<path d="M380 215H500M480 195L500 215L480 235" fill="none" stroke="#147b79" stroke-width="7"/>'
body+=text(32,375,'These arrays are invented teaching values, not trained-model outputs.',23)
body+=text(32,412,'No target image or learned update rule is supplied; do not infer measured denoising quality.',19)+'</svg>'
(A/'ai-3-10-toy-grid-update.svg').write_text(body)
body=start+text(32,45,'CONSTRUCTED POSTER CARD · INSPECT THE REQUIREMENTS',24,weight=700)
body+=text(32,84,'Required: exactly three circles labelled A, B, C from left to right.',22)
for i,label in enumerate(['A','B',None,'D']):
 x=135+i*240;body+=f'<circle cx="{x}" cy="205" r="75" fill="#d9f1ef" stroke="#137d79" stroke-width="4"/>'
 if label:body+=text(x-13,220,label,40,weight=700)
 else:body+=f'<path d="M{x-35} 201l12 -9 9 19 9 -18 10 18 12 -15 11 6" fill="none" stroke="#16384d" stroke-width="5"/>'
body+=text(32,325,'Draft caption to audit: “Photograph of a real lesson.”',23,'#8c3b23',700)
body+=text(32,373,'This is a fictional output card drawn for the lesson, not an actual generator run.',20)
body+=text(32,410,'Count, legible labels and the authenticity claim must be checked separately.',20)+'</svg>'
(A/'ai-3-10-poster-audit.svg').write_text(body)
js="""import {chromium} from './work/render-tools/node_modules/playwright-core/index.mjs';
import {pathToFileURL} from 'node:url';import {resolve} from 'node:path';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{for(const stem of ['ai-3-10-toy-grid-update','ai-3-10-poster-audit']){const page=await browser.newPage({viewport:{width:1000,height:440},deviceScaleFactor:1.5});await page.goto(pathToFileURL(resolve('assets',stem+'.svg')).href);const overflow=await page.locator('text').evaluateAll(nodes=>nodes.filter(n=>{const b=n.getBoundingClientRect();return b.left<0||b.top<0||b.right>1000||b.bottom>440;}).map(n=>n.textContent));if(overflow.length)throw Error(JSON.stringify(overflow));await page.screenshot({path:resolve('assets',stem+'.png')});await page.close();}}finally{await browser.close();}
"""
subprocess.run(['node','--input-type=module','-'],input=js,text=True,cwd=R,check=True)
print('Rendered two native evidence cards with text bounds checked.')
