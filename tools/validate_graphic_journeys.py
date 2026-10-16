"""Audit lesson coverage, source boundaries, image packaging and approved-reference preservation."""
from pathlib import Path
import json,sys,hashlib,xml.etree.ElementTree as ET
from PIL import Image
R=Path(__file__).resolve().parents[1];d=json.loads((R/'content/programme.json').read_text());errors=[];rows=[]
def check(ok,week,message):
 if not ok:errors.append({'week':week,'error':message})
for w in d['weeks']+d['python_bridge']:
 gs=w.get('graphic_story',[]);check(len(gs)==6,w['id'],'Expected six graphics');check(len({g['asset'] for g in gs})==6,w['id'],'Duplicate assets')
 for key in ['sections','teacher','workbook']:
  sections=[s for s in w[key] if s.get('graphic_journey')];check(len(sections)==1,w['id'],'Missing or duplicate journey in '+key)
  if not sections:continue
  blocks=sections[0]['blocks'];images=[b for b in blocks if b['type']=='image'];check([b['src'].split('/')[-1] for b in images]==[g['asset'] for g in gs],w['id'],'Role/image mismatch in '+key)
  check(all(b['alt'].strip() for b in images),w['id'],'Missing text alternative')
  text=' '.join(b.get('text',b.get('label','')) for b in blocks)
  check(w['method']['independent']['task'] not in text,w['id'],'Reserved independent case leaked into supported graphics')
  if key!='teacher':check('Supported practice key:' not in text,w['id'],'Teacher guidance in learner resource')
  else:check(w['pictorial_case']['teacher_answer'] in text,w['id'],'Supported teacher reasoning missing')
 for g in gs:
  p=R/'assets'/g['asset'];svg=p.with_suffix('.svg');png=p.with_suffix('.png');check(svg.exists() and png.exists(),w['id'],'Missing SVG/PNG '+g['asset'])
  if not svg.exists() or not png.exists():continue
  root=ET.fromstring(svg.read_text());check(root.find('{http://www.w3.org/2000/svg}title') is not None and root.find('{http://www.w3.org/2000/svg}desc') is not None,w['id'],'Missing accessible SVG title/description')
  check(all(not source.startswith(('method.independent','sections:Try a new case independently')) for source in g['source']),w['id'],'Independent assessment used as source')
  with Image.open(png) as im:check(im.width>=1200 and im.height>=600,w['id'],'Insufficient image resolution')
 rows.append({'week':w['id'],'graphics':len(gs),'roles':['student','teacher','workbook'],'chart':w['pictorial_case'].get('mini_visual',{}).get('kind')})
ref=R/'tools/graphic-references/week1';m=json.loads((ref/'review-manifest.json').read_text())
for i,g in enumerate(m['graphics'],1):check((ref/(g['id']+'.svg')).read_bytes()==(R/'assets'/f'academy-story-ai-1-1-{i:02}.svg').read_bytes(),'ai-1/1','Approved Week 1 illustration changed')
report={'lessons':len(rows),'new_graphics':sum(r['graphics'] for r in rows),'role_image_placements':sum(r['graphics']*3 for r in rows),'numerical_closeups':sum(bool(r['chart']) for r in rows),'errors':errors,'weeks':rows,'scope':'Content source, assessment boundary, resolution, role coverage and approved-reference preservation; not evidence of classroom learning impact.'}
(R/'reports/graphic-content-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='weeks'},indent=2));sys.exit(bool(errors))
