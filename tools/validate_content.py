"""Check preservation, role alignment, assets and executable source examples."""
from pathlib import Path
import json,runpy,collections,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
ns=runpy.run_path(str(ROOT/'tools/build_programme.py'))
D=json.loads((ROOT/'content/programme.json').read_text());S=ns['S'];errors=[];rows=[]
def strings(obj):
 if isinstance(obj,str):yield obj
 elif isinstance(obj,list):
  for child in obj:yield from strings(child)
 elif isinstance(obj,dict):
  for key,child in obj.items():
   if key in ['text','label','alt','rows','cells','caption','title','columns','values']:yield from strings(child)
def blocks(obj):
 if isinstance(obj,list):
  for child in obj:yield from blocks(child)
 elif isinstance(obj,dict):
  if 'type' in obj:yield obj
  for key,child in obj.items():
   if isinstance(child,(list,dict)):yield from blocks(child)
lookup={w['id']:w for w in D['weeks']}
for level in S['original']['levels']:
 for old in level['weeks']:
  id=f"{level['slug']}/{old['number']}";w=lookup[id];fix=ns['fix'];clean=ns['clean'];missing=[]
  for source,key in [('student','sections'),('teacher','teacher')]:
   for i,page in enumerate(old[source]['pages']):
    expected=list(strings(clean(fix(page['blocks']))));actual=list(strings(w[key][i]['blocks']))
    missing.extend(x for x in expected if x not in actual)
  actual=list(strings([s['blocks'] for s in w['workbook']]))
  missing.extend(x for x in strings(clean(fix(old['workbook']['blocks']))) if x not in actual and x not in [s['title'] for s in w['workbook']])
  if missing:errors.append({'week':id,'missing_original_blocks':missing})
  rows.append({'week':id,'original_preserved':not missing,'student_sections':len(w['sections']),'teacher_sections':len(w['teacher']),'workbook_sections':len(w['workbook'])})
assets=set()
for w in D['weeks']+D['python_bridge']:
 if len(w['sections'])<14 or len(w['teacher'])<6:errors.append({'week':w['id'],'structure':'incomplete'})
 answer=w['independent_answer'];teacher=list(strings([s['blocks'] for s in w['teacher']]))
 if answer not in teacher:errors.append({'week':w['id'],'independent_answer':'missing'})
 for b in blocks(w):
  if b['type']=='image':
   name=b['src'].split('/')[-1]+'.png';assets.add(name)
   if not (ROOT/'assets'/name).exists():errors.append({'week':w['id'],'image':name})
 for role in ['student','teacher','workbook']:
  stem=('bridge-' if w['id'].startswith('python') else f"ai-{w['level']}-")+f"week-{w['week']:02}"
  if not (ROOT/role/(stem+'.html')).exists():errors.append({'week':w['id'],'html':role})
# Each of the 252 later lessons is present in the main programme or readiness bridge.
covered={}
for w in D['weeks']+D['python_bridge']:
 for source in [w['sources']['rebuilt']]+w['sources'].get('additional',[]):covered.setdefault(source,[]).append(w)
for source,c in S['rebuilt'].items():
 if source not in covered:errors.append({'later_lesson_missing':source});continue
 for w in covered[source]:
  actual=list(strings([sec['blocks'] for sec in w['sections']]))
  expected=list(strings([ns['newblock'](b) for sec in c['lesson'] for b in sec['blocks'] if b['type']!='response']))
  missing=[x for x in expected if x not in actual]
  if missing:errors.append({'week':w['id'],'missing_later_explanation':source,'blocks':missing})
  teacher=list(strings([sec['blocks'] for sec in w['teacher']]))
  for q in c['workbook']:
   if q['answer'] not in teacher:errors.append({'week':w['id'],'missing_answer':source+' '+q['id']})
# Every stale, specifically corrected sentence must be absent from the new canonical data.
text=json.dumps(D)
for old,new in ns['FIXES'].items():
 if old in text:errors.append({'correction_not_applied':old})
# Run unique rebuilt Python examples with a timeout and per-example temporary folder.
code_results=[]
for id,w in S['rebuilt'].items():
 for index,b in enumerate(blocks(w['lesson'])):
  if b['type']!='code':continue
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'lesson.py';path.write_text(b['text'])
   # A file exercise explicitly reads the local fictional durations fixture.
   (Path(temp)/'durations.txt').write_text('12\n8\n')
   (Path(temp)/'minutes.txt').write_text('12\n8\n')
   result=subprocess.run([sys.executable,str(path)],cwd=temp,capture_output=True,text=True,timeout=10)
   expected_error=id=='ai-2/7' and 'IndexError' in result.stderr
   okay=result.returncode==0 or expected_error
   code_results.append({'week':id,'block':index,'passed':okay,'expected_failure':expected_error,'stdout':result.stdout,'stderr':result.stderr})
   if not okay:errors.append({'week':id,'python':result.stderr})
# Verify the original executable labs against their published outputs.
for id,want in [('ai-4/13','2.5 [0, 1] 2 2'),('ai-4/22','2.0 1.0 [9.0] 1.0')]:
 for b in lookup[id]['sections'][14]['blocks']:
  if b['type']=='code':
   result=subprocess.run([sys.executable,'-c',b['text']],capture_output=True,text=True,timeout=10)
   okay=result.returncode==0 and result.stdout.strip()==want
   code_results.append({'week':id,'passed':okay,'stdout':result.stdout,'expected':want})
   if not okay:errors.append({'original_lab':id,'stdout':result.stdout,'stderr':result.stderr})
report={'main_weeks':len(D['weeks']),'bridge_lessons':len(D['python_bridge']),'original_weeks_checked':len(rows),'unique_original_images':sum(not name.startswith(('academy-visual-','academy-detail-')) for name in assets),'new_pictorial_diagrams':sum(name.startswith(('academy-visual-','academy-detail-')) for name in assets),'corrected_illustration_cards':len(ns['CORRECTED_ASSETS']),'source_python_examples':len(code_results),'later_lessons_covered':len(covered),'errors':errors,'weeks':rows,'python':code_results}
(ROOT/'reports/content-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['weeks','python']},indent=2))
if errors:sys.exit(1)
