"""Build student-safe formative practice and repair links from reviewed public examples."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];p=json.loads((R/'content/programme.json').read_text());weeks=p['weeks']+p['python_bridge'];lookup={w['id']:w for w in weeks};result={}
for w in weeks:
 c=w['pictorial_case'];steps=c['steps'];labels=list(dict.fromkeys(s['label'] for s in steps));target=next(s for s in reversed(steps) if labels.count(s['label'])==1)
 def shuffle(options,salt):return sorted(options,key=lambda o:hashlib.sha256((w['id']+salt+o['text']).encode()).hexdigest())
 choices=[{'text':label,'correct':label==target['label'],'feedback':(target['detail']+' '+c['explanation']) if label==target['label'] else 'This stage does not match the supplied detail. Follow the labelled trace and identify which step uses that information.'} for label in labels]
 trace={'id':'trace','prompt':'Which labelled step matches this detail? '+target['detail'],'choices':shuffle(choices,'trace'),'hint':'Read the steps in the pictorial case. Match the supplied detail to the stage that performs or records it.'}
 change={'id':'change','prompt':'Changed-case practice: '+c['counterfactual']['change']+' Which conclusion is supported by the supplied facts?', 'choices':shuffle([
 {'text':c['counterfactual']['prediction'],'correct':True,'feedback':c['counterfactual']['reason']},
 {'text':'This one example guarantees correct results for every future input.','correct':False,'feedback':'One worked example cannot establish that guarantee. Use the actual changed input and deciding rule; keep the stated limitations.'},
 {'text':'We can decide the result without examining the changed input or the procedure.','correct':False,'feedback':'A justified conclusion needs the given facts and procedure. Trace the changed condition and connect it to the result.'}], 'change'),'hint':'Use the changed condition and the deciding step in the pictorial trace. The answer must say what follows from those facts.'}
 repairs=[]
 for item in w['method']['retrieval'][:3]:
  old=lookup[item['week']];section=next((i+1 for i,s in enumerate(old['sections']) if s['title']=='Follow a worked example'),1)
  repairs.append({'week':old['id'],'title':old['title'],'goal':item['goal'],'task':old['pictorial_case']['student_task'],'section':section})
 if not repairs:
  prev={'ai-2':'ai-1/36','ai-3':'ai-2/36','ai-4':'python-bridge/12','ai-5':'ai-4/36','ai-6':'ai-4/36','ai-7':'ai-6/36','python-bridge':'ai-2/6'}.get(w['id'].split('/')[0])
  if prev:
   old=lookup[prev];repairs.append({'week':prev,'title':old['title'],'goal':old['method']['goal'],'task':old['pictorial_case']['student_task'],'section':next((i+1 for i,s in enumerate(old['sections']) if s['title']=='Follow a worked example'),1)})
 codes=[]
 for s in w['sections']:
  if s['title']=='Try a new case independently':continue
  for b in s['blocks']:
   if b['type']=='code' and b.get('teaching_method',{}).get('kind')!='independent-transfer' and b['text'].strip() and b['text'] not in codes:codes.append(b['text'])
 result[w['id']]={'scenario':c['scenario'],'questions':[trace,change],'repairs':repairs,'labs':[{'title':f'Supported code example {i+1}','code':code} for i,code in enumerate(codes)],'limits':c['limits']}
# No reserved assessment task or teacher answer is used in the client tools.
for w in weeks:
 assert w['method']['independent']['task'] not in [q['prompt'] for q in result[w['id']]['questions']]
 assert all(sum(choice['correct'] for choice in q['choices'])==1 and len(set(choice['text'] for choice in q['choices']))==len(q['choices']) for q in result[w['id']]['questions'])
(R/'content/learning-tools.json').write_text(json.dumps(result,ensure_ascii=False))
if (R/'lib').is_dir():(R/'lib/learning-tools.json').write_text(json.dumps(result,ensure_ascii=False))
report={'lessons':len(result),'formative_questions':sum(len(v['questions']) for v in result.values()),'lessons_with_code':sum(bool(v['labs']) for v in result.values()),'supported_code_examples':sum(len(v['labs']) for v in result.values()),'repair_links':sum(len(v['repairs']) for v in result.values()),'reserved_assessments_replaced':0}
(R/'reports/learning-tools-coverage.json').write_text(json.dumps(report,indent=2));print(report)
