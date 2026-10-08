"""Keep the printed/offline curriculum aligned with the new classroom tools."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=json.loads((R/'content/programme.json').read_text());data=json.loads((R/'content/learning-tools.json').read_text())
def paragraph(text):return {'type':'paragraph','text':text}
def response(label):return {'type':'response','label':label,'lines':5}
for w in p['weeks']+p['python_bridge']:
 tools=data[w['id']]
 for role in ['sections','teacher','workbook']:w[role]=[s for s in w[role] if not s.get('learning_tools_upgrade')]
 blocks=[paragraph('Use this supported practice once, in the browser or on paper. Keep the reserved independent assessment for a separate first attempt before teacher feedback.'),paragraph(tools['scenario'])]
 for i,q in enumerate(tools['questions'],1):
  blocks += [{'type':'subheading','text':f'Practice {i}: explain the deciding evidence'},paragraph(q['prompt'])]+[paragraph(f"{j+1}. {choice['text']}") for j,choice in enumerate(q['choices'])]+[response('My selected conclusion, deciding fact and explanation'),paragraph('Hint if needed: '+q['hint']),paragraph('After your attempt, compare with the supported explanation: '+next(c['text']+' '+c['feedback'] for c in q['choices'] if c['correct']))]
 blocks += [{'type':'subheading','text':'Repair a missing building block'}]
 if tools['repairs']:
  for repair in tools['repairs']:blocks += [paragraph(f"Review {repair['title']} ({repair['week']}). Goal: {repair['goal']}. Short practice: {repair['task']}. Return to this week and explain what you changed.")]
 else:blocks += [paragraph('This is the starting lesson. Ask your teacher to model one observation, one written rule and one deciding step, then try your own example.')]
 if tools['labs']:blocks += [{'type':'subheading','text':'Predict, run and debug'},paragraph('The browser lab lets you edit the supported Python examples already included in this lesson. Predict first, run, inspect the actual output or error, change one input, then run again. Keep code, predictions, actual results and a reasoned revision together. On paper, label your result as a trace rather than an execution.')]
 blocks += [{'type':'subheading','text':'Keep your completed work'},paragraph('Use Download completed work in the hosted lesson to export your answers, reflections, practice feedback and code-run evidence. Open the HTML copy to read or print it. Drafts stay in this browser when storage is available; clear drafts on a shared device.')]
 w['sections'].append({'title':'Supported practice, repair and portfolio','blocks':blocks,'learning_tools_upgrade':True})
 w['workbook'].append({'title':'Supported practice and learning evidence','blocks':blocks[:]+[response('What I repaired, the evidence I kept and the next test')],'learning_tools_upgrade':True})
 w['teacher'].append({'title':'Use feedback, labs and repair paths','blocks':[paragraph('Use the two formative questions as supported practice, not as independent mastery scores. Discuss the deciding evidence rather than accepting a guessed selection.'),paragraph('The feedback comes from the reviewed public worked case. Do not reveal the separately reserved independent teacher answer until the learner has attempted that case.'),paragraph('Ask students to predict before running code. Preserve errors and actual outputs; collect a changed test and an explanation. The branch-boundary and indexing lessons deliberately include failure cases.'),paragraph('Use the earlier worked-explanation links to address a specific missing building block, then return to the current question. Adapt this suggestion after observing the learner; it is not an automatic diagnosis.'),paragraph('Collect the completed-work portfolio as evidence. Record support separately from correctness, and assess explanation, trace/test and limitations. Progress ticks and quiz selections alone do not establish mastery.')],'learning_tools_upgrade':True})
(R/'content/programme.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print('Aligned print and offline content for all 264 lessons.')
