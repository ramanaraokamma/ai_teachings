"""Refresh corrected pictorial sources and drawings without rebuilding approved lesson sections.

Use a pre-review canonical snapshot to identify changed source facts. Existing reading
presentation and response positions are preserved. The browser raster pass follows.
"""
from pathlib import Path
import ast, json, sys
from draw_lesson_visuals import draw as draw_pathway
from draw_topic_visuals import draw as draw_numeric

ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:raise SystemExit('Usage: refresh_review_assets.py PRE_REVIEW_PROGRAMME_JSON')
before=json.loads(Path(sys.argv[1]).read_text())
data=json.loads((ROOT/'content/programme.json').read_text())
old={w['id']:w for w in before['weeks']+before['python_bridge']}
# Load drawing functions, stopping before the bulk integration entry point.
source=ROOT/'tools/build_graphic_journeys.py';tree=ast.parse(source.read_text());nodes=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rows' for t in node.targets):break
 nodes.append(node)
ns={'__file__':str(source),'__name__':'review_asset_drawing'}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
changed=[];assets=[]
pathway_manifest=json.loads((ROOT/'reports/pictorial-assets.json').read_text())
numeric_manifest=json.loads((ROOT/'reports/topic-visual-assets.json').read_text())
manifest=json.loads((ROOT/'reports/graphic-journeys.json').read_text())
by_id={r['week']:r for r in manifest['weeks']}

def update_blocks(value,graphics,replacements):
 if isinstance(value,list):
  for child in value:update_blocks(child,graphics,replacements)
 elif isinstance(value,dict):
  if value.get('type')=='image':
   g=graphics.get(value['src'].split('/')[-1])
   if g:
    for key in ['alt','width','height']:value[key]=g[key]
  if 'text' in value:
   for a,b in replacements.items():value['text']=value['text'].replace(a,b)
   p=value.get('presentation')
   if p:
    if p.get('paragraphs'):
     p['paragraphs']=[replacements.get(t,t) for t in p['paragraphs']]
     if ' '.join(p['paragraphs'])!=value['text']:p['paragraphs']=[value['text']]
  for key,child in value.items():
   if key!='presentation' and isinstance(child,(list,dict)):update_blocks(child,graphics,replacements)

for w in data['weeks']+data['python_bridge']:
 prior=old[w['id']]
 # Keep editable source packs aligned with the reviewed canonical worked case.
 path=ROOT/'tools/lesson-upgrades'/(w['id'].replace('/','-')+'.json')
 if json.loads(path.read_text())!=w['pictorial_case']:path.write_text(json.dumps(w['pictorial_case'],ensure_ascii=False,indent=2))
 a=w['pictorial_case'];p=prior['pictorial_case']
 if a!=p:
  row=draw_pathway(a)
  pathway_manifest=[row if item['week']==w['id'] else item for item in pathway_manifest]
  if a.get('mini_visual')!=p.get('mini_visual'):
   row=draw_numeric(a)
   if row:numeric_manifest=[row if item['week']==w['id'] else item for item in numeric_manifest]
 # Story 03 may use a corrected lesson diagram even when pictorial_case is unchanged.
 def diagrams(v):return [b for s in v['sections'] for b in s['blocks'] if b.get('type')=='diagram' and not b.get('lesson_upgrade')]
 redraw=a!=p or diagrams(w)!=diagrams(prior)
 if not redraw or w['id']=='ai-1/1':continue
 graphics=ns['make'](w);reps={g['alt']:n['alt'] for g,n in zip(w['graphic_story'],graphics) if g['alt']!=n['alt']}
 lookup={g['asset']:g for g in graphics}
 for role in ['sections','teacher','workbook']:update_blocks(w[role],lookup,reps)
 w['graphic_story']=graphics;by_id[w['id']]['graphics']=graphics
 changed.append(w['id']);assets.extend(g['asset'] for g in graphics)
(ROOT/'content/programme.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(ROOT/'reports/graphic-journeys.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(ROOT/'reports/pictorial-assets.json').write_text(json.dumps(pathway_manifest,indent=2))
(ROOT/'reports/topic-visual-assets.json').write_text(json.dumps(numeric_manifest,indent=2))
(ROOT/'work/week-review/graphics-to-render.json').write_text(json.dumps({'weeks':changed,'assets':assets},indent=2))
print('Refreshed corrected worked-case sources;',len(changed),'story journeys require browser raster rendering.')
