from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/programme.json').read_text());weeks=D['weeks']+D['python_bridge'];errors=[];seen=set();tasks=set();executions=[]
for w in weeks:
 m=w['method'];case=m['independent'];source=w['sources']['rebuilt']
 if case['task'] in tasks:errors.append({'week':w['id'],'error':'Duplicate selected assessment prompt'})
 tasks.add(case['task'])
 if source in seen and not w['id'].startswith('python') and case['source']!='new parallel transfer case':errors.append({'week':w['id'],'error':'Reused source without changed case'})
 seen.update([source]+w['sources'].get('additional',[]))
 if w['independent_answer']!=case['answer']:errors.append({'week':w['id'],'error':'Active answer mismatch'})
 if not any(b.get('text')==case['answer'] for s in w['teacher'] for b in s['blocks']):errors.append({'week':w['id'],'error':'Teacher key missing'})
 for role,key in [('student','sections'),('workbook','workbook')]:
  blocks=[b for s in w[key] for b in s['blocks']]
  if not any(b.get('text')==case['task'] for b in blocks):errors.append({'week':w['id'],'role':role,'error':'Selected question missing'})
  if any(b.get('teaching_method',{}).get('role')=='teacher' for b in blocks):errors.append({'week':w['id'],'role':role,'error':'Teacher-only method block leaked'})
 for future in m['review_at']:
  other=next(x for x in weeks if x['id']==future)
  if other['level']!=w['level'] or other['week']-w['week'] not in [1,3,6]:errors.append({'week':w['id'],'error':'Review schedule mismatch'})
 if len(m['connected_topics'])!=len(w['sources'].get('additional',[])):errors.append({'week':w['id'],'error':'Connected topic cycle missing'})
 if case.get('code'):
  run=subprocess.run([sys.executable,'-c',case['code']],capture_output=True,text=True,timeout=5)
  passed=run.returncode==0 and run.stdout==case['expected_stdout'];executions.append({'week':w['id'],'passed':passed,'stdout':run.stdout})
  if not passed:errors.append({'week':w['id'],'error':'Fresh code result mismatch'})
report={'lessons':len(weeks),'unique_selected_cases':len(tasks),'parallel_transfer_cases':sum(w['method']['independent']['source']=='new parallel transfer case' for w in weeks),'fresh_readiness_cases':len(executions),'connected_cycles':sum(len(w['method']['connected_topics']) for w in weeks),'errors':errors,'executions':executions,'scope':'Structure, exposure within this curriculum, question/key alignment and code execution. Does not establish prior exposure outside the programme or classroom learning impact.'}
(R/'reports/teaching-method-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));sys.exit(bool(errors))
