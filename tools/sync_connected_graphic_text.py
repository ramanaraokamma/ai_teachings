"""Regenerate only story assets whose SVG transcript trails the corrected source."""
from pathlib import Path
import ast,copy,hashlib,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];source=R/'content/programme.json';d=json.loads(source.read_text());weeks=d['weeks']+d['python_bridge'];targets={}
for w in weeks:
 for g in w['graphic_story']:
  root=ET.fromstring((R/'assets'/(g['asset']+'.svg')).read_text());desc=root.find('{http://www.w3.org/2000/svg}desc')
  text=''.join(desc.itertext()) if desc is not None else ''
  if text!=g['alt']:targets.setdefault(w['id'],set()).add(g['asset'])
assert not any(id=='ai-1/1' for id in targets),'Approved first-week artwork requires its separate workflow'
tree=ast.parse((R/'tools/build_graphic_journeys.py').read_text());nodes=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rows' for t in node.targets):break
 nodes.append(node)
ns={'__file__':str(R/'tools/build_graphic_journeys.py'),'__name__':'connected_graphic_sync'}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(R/'tools/build_graphic_journeys.py'),'exec'),ns)
manifest_path=R/'reports/graphic-journeys.json';manifest=json.loads(manifest_path.read_text());manifest_weeks={x['week']:x for x in manifest['weeks']};results=[];metadata=[]
backup=R/'work/connected-recovery/graphic-text-backup';backup.mkdir(parents=True,exist_ok=True)
for w in weeks:
 if w['id'] not in targets:continue
 wanted=targets[w['id']];saved={g['asset']:(R/'assets'/(g['asset']+'.svg')).read_bytes() for g in w['graphic_story']};before={g['asset']:copy.deepcopy(g) for g in w['graphic_story']}
 for name,data in saved.items():(backup/(name+'.svg')).write_bytes(data)
 try:
  generated={g['asset']:g for g in ns['make'](w)}
  for name in wanted:assert generated[name]['alt']==before[name]['alt'],(name,'Generator would change the corrected source transcript')
 except BaseException:
  for name,data in saved.items():(R/'assets'/(name+'.svg')).write_bytes(data)
  raise
 for name,data in saved.items():
  if name not in wanted:(R/'assets'/(name+'.svg')).write_bytes(data)
 for i,g in enumerate(w['graphic_story']):
  name=g['asset']
  if name not in wanted:continue
  new=generated[name];w['graphic_story'][i]=new
  results.append({'week':w['id'],'asset':name,'old_svg_sha256':hashlib.sha256(saved[name]).hexdigest(),'new_svg_sha256':hashlib.sha256((R/'assets'/(name+'.svg')).read_bytes()).hexdigest(),'old_dimensions':[g['width'],g['height']],'new_dimensions':[new['width'],new['height']]})
 for role in ['sections','teacher','workbook']:
  for si,section in enumerate(w[role]):
   for bi,block in enumerate(section['blocks']):
    if block.get('type')!='image':continue
    name=block.get('src','').split('/')[-1]
    if name not in wanted:continue
    new=generated[name]
    for key in ['alt','width','height']:
     if block.get(key)!=new[key]:metadata.append({'week':w['id'],'path':f'/{role}/{si}/blocks/{bi}/{key}','old':block.get(key),'new':new[key]});block[key]=new[key]
 manifest_weeks[w['id']]['graphics']=w['graphic_story']
source.write_text(json.dumps(d,ensure_ascii=False,indent=2));manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
correction_path=R/'reports/reviewed-source-corrections.json';corrections=json.loads(correction_path.read_text())
for item in metadata:
 if item['path'].endswith('/alt') and isinstance(item['old'],str):corrections['corrections'].append(item)
correction_path.write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+'\n')
report={'assets':results,'image_metadata_updates':metadata,'affected_weeks':[w['id'] for w in weeks if w['id'] in targets],'scope':'SVGs regenerated from already-corrected source text; non-target SVG bytes restored exactly. PNG raster generation, matching downloads and fresh browser checks must follow.'}
(R/'reports/connected-graphic-text-sync.json').write_text(json.dumps(report,indent=2)+'\n')
(R/'work/connected-recovery/final-graphic-assets.txt').write_text(','.join(r['asset'] for r in results))
(R/'work/connected-recovery/final-graphic-weeks.txt').write_text(','.join(report['affected_weeks']))
print('Regenerated',len(results),'SVGs in',len(targets),'weeks;',len(metadata),'image metadata values aligned.')
