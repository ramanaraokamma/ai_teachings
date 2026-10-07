"""Audit coverage, role alignment, diagram geometry and declared numerical visuals."""
from pathlib import Path
import json,math,re,sys,os
from PIL import Image
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/programme.json').read_text());weeks=D['weeks']+D['python_bridge'];folder=R/'tools/lesson-upgrades';errors=[];rows=[];owners={};practice_questions={}
for assignment in (R/'tools/lesson-review-packs').glob('assignment-*.json'):
 for row in json.loads(assignment.read_text()):owners[row['week']]='weekly_lessons_'+assignment.stem.split('-')[-1]
icons={'book','sensor','rule','data','model','person','check','chart','code','shield','question','output','experiment','network','clock'}
def fail(week,message):errors.append({'week':week,'error':message})
for w in weeks:
 path=folder/(w['id'].replace('/','-')+'.json')
 if not path.exists():fail(w['id'],'Missing week review');continue
 try:a=json.loads(path.read_text())
 except (ValueError,OSError) as e:fail(w['id'],str(e));continue
 for key in ['week','title','outcome','scenario','explanation','student_task','teacher_answer','project_evidence','limits','review_note']:
  if not isinstance(a.get(key),str) or not a[key].strip():fail(w['id'],'Missing/non-text '+key)
 if a.get('week')!=w['id']:fail(w['id'],'Week identity mismatch')
 if not isinstance(a.get('given'),list) or len(a['given'])<1:fail(w['id'],'Supplied facts are required')
 steps=a.get('steps',[])
 if not 3<=len(steps)<=5:fail(w['id'],'Three to five visual stages needed')
 for i,s in enumerate(steps):
  if s.get('icon') not in icons:fail(w['id'],'Unknown icon at step '+str(i+1))
  if not s.get('label') or len(s['label'])>28:fail(w['id'],'Step label must fit 28 chars at step '+str(i+1))
  if not s.get('detail') or len(s['detail'])>145:fail(w['id'],'Step detail must fit 145 chars at step '+str(i+1))
 for key in ['change','prediction','reason']:
  if not a.get('counterfactual',{}).get(key):fail(w['id'],'Missing changed-case '+key)
 if a.get('student_task') in practice_questions:fail(w['id'],'Identical practice question reused from '+practice_questions[a['student_task']])
 practice_questions[a.get('student_task')]=w['id']
 if a.get('student_task')==w['method']['independent']['task']:fail(w['id'],'Worked practice reuses selected independent task')
 v=a.get('mini_visual')
 if v:
  kind=v.get('kind')
  if not v.get('title'):fail(w['id'],'Plot title missing')
  if kind=='bars':
   if len(v.get('labels',[]))!=len(v.get('values',[])) or not v.get('values'):fail(w['id'],'Bar labels/value counts mismatch')
   if any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in v.get('values',[])):fail(w['id'],'Non-finite bar value')
   if not v.get('unit'):fail(w['id'],'Bar unit/denominator description missing')
  elif kind=='grid':
   cells=v.get('cells',[])
   if not cells or not cells[0] or any(len(row)!=len(cells[0]) for row in cells):fail(w['id'],'Grid is not rectangular')
   elif len(v.get('row_labels',[]))!=len(cells) or len(v.get('column_labels',[]))!=len(cells[0]):fail(w['id'],'Grid axis labels mismatch')
  elif kind=='scatter':
   for point in v.get('points',[])+([v['query']] if v.get('query') else []):
    if not point.get('label') or any(not isinstance(point.get(k),(int,float)) or not math.isfinite(point[k]) for k in ['x','y']):fail(w['id'],'Scatter point lacks coordinates/label')
   if not v.get('points'):fail(w['id'],'Scatter has no points')
  elif kind=='weights':
   if len(v.get('inputs',[]))!=len(v.get('weights',[])) or not v.get('inputs'):fail(w['id'],'Weight/input counts mismatch')
   else:
    raw=sum(x*y for x,y in zip(v['inputs'],v['weights']))+v['bias'];out=max(0,raw) if v['activation']=='relu' else raw
    if v['activation'] not in ['relu','identity'] or not math.isclose(out,v['output'],rel_tol=1e-8,abs_tol=1e-8):fail(w['id'],'Weighted-output arithmetic mismatch')
  else:fail(w['id'],'Unsupported numerical illustration '+str(kind))
 if not os.environ.get('DRAFT_CHECK'):
  for stem in ['academy-visual-']+(['academy-detail-'] if v else []):
   image=R/'assets'/(stem+w['id'].replace('/','-')+'.png');vector=image.with_suffix('.svg')
   if not image.exists() or not vector.exists():fail(w['id'],'Missing pictorial assets')
   else:
    with Image.open(image) as im:
     if im.width<1000 or im.height<300:fail(w['id'],'Image resolution insufficient')
  if w.get('pictorial_case')!=a:fail(w['id'],'Canonical worked case differs from agent review')
  for role,key in [('student','sections'),('teacher','teacher'),('workbook','workbook')]:
   blocks=[b for sec in w[key] for b in sec['blocks']]
   if not any(b.get('text')==a['student_task'] for b in blocks):fail(w['id'],'Practice question missing in '+role)
   if role=='teacher' and not any(b.get('text')==a['teacher_answer'] for b in blocks):fail(w['id'],'Reasoned teacher key missing')
   if role!='teacher' and any(b.get('lesson_upgrade',{}).get('role')=='teacher' for b in blocks):fail(w['id'],'Teacher-only block in learner resource')
 rows.append({'week':w['id'],'owner':owners.get(w['id']),'picture_stages':len(steps),'topic_visual':v['kind'] if v else None,'outcome':a.get('outcome'),'case':a.get('scenario')})
report={'lessons_expected':len(weeks),'lessons_reviewed':len(rows),'agents':sorted(set(owners.values())),'topic_specific_plots':sum(bool(x['topic_visual']) for x in rows),'draft_check':bool(os.environ.get('DRAFT_CHECK')),'errors':errors,'scope':'Coverage, constrained diagram data, role/question/key alignment and declared numeric-visual consistency. Topic explanations and new case traces also require editorial review; this is not a classroom impact test.','weeks':rows}
(R/'reports/weekly-agent-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='weeks'},indent=2));sys.exit(bool(errors))
