"""Apply the eight classroom improvements without removing original lesson content."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'content/programme.json').read_text())
route=['ai-1','ai-2','ai-3','python-bridge','ai-4','ai-5','ai-6','ai-7']
p['learning_sequence']=route
outcomes={
1:'Explain the difference between human decisions, written rules and learned models; build and test a classroom sorter.',
2:'Trace algorithms, inspect data and compare a transparent recommender with a simple starting method.',
3:'Build a study buddy that uses approved sources, checks generated claims and explains uncertainty.',
4:'Train and evaluate a plant classifier using separate data, a baseline and documented errors.',
5:'Trace a small neural network and investigate how representation and training affect its mistakes.',
6:'Build a grounded service with source checks, role permissions, tests and a safe fallback.',
7:'Design a reproducible investigation, compare alternatives and defend conclusions with evidence.'}
for l in p['levels']: l['exit_outcome']=outcomes[l['number']]

def section(title,blocks):return {'title':title,'blocks':blocks,'classroom_upgrade':'2026-10-07'}
def para(text):return {'type':'paragraph','text':text}
def response(label):return {'type':'response','label':label,'lines':5}
rows=[]
for w in p['weeks']+p['python_bridge']:
 for key in ['sections','teacher','workbook']:w[key]=[s for s in w[key] if not s.get('classroom_upgrade')]
 method=w['method'];case=w['pictorial_case']; bridge=w['id'].startswith('python'); goals=method['goals']
 def find(term):
  return next((i+1 for i,s in enumerate(w['sections']) if term.lower() in s['title'].lower()),1)
 flow=[('Wonder and remember',find('start'),w['recall']),('Watch and explain',find('Follow a worked'),case['scenario']),('Try with help',find('Practise together'),method['practice']['prompt']),('Investigate and repair',find('investigation'),'Record a prediction, a trace or actual result, and the first step you would repair.'),('Try independently',find('new case independently'),'Use the reserved new case. Explain the deciding step before receiving feedback.'),('Keep project evidence',find('Connect your project'),case['project_evidence'])]
 w['classroom']={'goals':goals,'flow':[{'title':a,'section':b,'task':c} for a,b,c in flow],'visual_question':case['student_task'],'project':w['project']}
 w['sections'].append(section('Your lesson route',[
  para('Start with this question: '+case['scenario']),
  {'type':'table','rows':[['By the end, I can','How I will show it']]+[[g,'Explain the deciding step, show a trace or test, and state one limit.'] for g in goals]},
  para('Remember → watch and explain → try with help → investigate → try independently → keep project evidence. Your teacher may spread this lesson across several classes.'),
  para('Keep your first prediction. Compare it with what the evidence shows and explain any change.')]))
 # A specific picture question points to the actual reviewed case, not a decorative icon.
 worked=next(s for s in w['sections'] if 'Follow a worked example' in s['title'])
 for s in w['sections']:s['blocks']=[b for b in s['blocks'] if not b.get('classroom_visual_prompt')]
 worked['blocks']=[b for b in worked['blocks'] if not b.get('classroom_visual_prompt')]
 worked['blocks'].extend([{**para('Read the labelled picture: '+case['student_task']),'classroom_visual_prompt':True},{**para('Change one thing: '+case['counterfactual']['change']+' Predict the result before checking the explanation. What remains the same?'),'classroom_visual_prompt':True}])
 # Six cumulative checkpoints use the named project and weekly evidence already present.
 phase=(w['week']-1)//6
 milestones=[('Frame the need','Name the user, the problem, allowed inputs and a safe simple starting method.'),('Make a transparent first version','Keep a trace of how one input becomes an output; explain the rule or learned component.'),('Test changed cases','Keep normal, boundary and failure cases; compare expected and observed results.'),('Evaluate and revise','Compare with your starting method, explain errors and record a justified revision.'),('Prepare the demonstration','Gather reproducible instructions, evidence, access checks and remaining limitations.'),('Present and defend','Demonstrate the system, explain one failure and justify the next improvement with evidence.')]
 if bridge: milestone=('Python readiness portfolio','Keep runnable code, predictions, actual outputs, one repaired error and an explanation of a function on changed inputs.')
 else:milestone=milestones[phase]
 w['classroom']['milestone']={'title':milestone[0],'task':milestone[1]}
 project_blocks=[para('Project: '+w['project']),para('Current milestone: '+milestone[0]+'. '+milestone[1]),para(case['project_evidence']),{'type':'table','rows':[['Evidence to keep','My record'],['This week’s input and deciding step',''],['Prediction and actual result (or labelled paper trace)',''],['One change since the previous checkpoint and why',''],['One error or limit and the next test','']]},response('Explain what this week adds to your project. Reuse last week’s record rather than starting again.')]
 w['workbook'].append(section('Project portfolio milestone',project_blocks))
 w['sections'].append(section('Finish and return',[
  para('Close your notes. Explain this goal in your own words: '+method['goal']),response('My deciding step, evidence and one remaining question'),
  para('If you are unsure, return to the worked picture and explain one arrow. If you are ready, change an input or assumption and justify your prediction.'),para('Save your workbook evidence. At the next review, try a different case before opening your old answer.')]))
 prep=[para('Teaching target: '+method['goal']),para('Prepare the labelled worked-case picture, the matching workbook, fictional input cards and a place for individual responses. '+('Check a local Python 3 environment before class; have a paper-trace version ready.' if bridge or w['level']>=4 else 'No paid AI account is required for the paper reasoning activities.')),
 {'type':'table','rows':[['Session','Plan','Resources']]+method['sessions']},
 para('Before class, solve the supported practice: '+method['practice']['prompt']),para('Reasoned practice answer: '+method['practice']['answer']),
 para('Check every learner before discussion: '+method['hinge']['prompt']),para('Misconception repair: '+method['hinge']['answer']),
 para('Support: read the exact case aloud, enlarge the labelled picture, supply input cards and model only the first deciding step. Accept a spoken explanation or drawing; retain the reasoning goal.'),
 para('Extension: '+case['counterfactual']['change']+' Require a prediction and a reason before comparing. Expected result: '+case['counterfactual']['prediction']+' Reason: '+case['counterfactual']['reason']),
 para('Independent assessment: withhold the reserved answer until the learner has attempted the new case. Record support separately from correctness.'),
 {'type':'table','rows':[['Criterion','Not yet','With support','Independent'],['Explanation','Names an answer without a deciding fact','Uses a hint to link fact and decision','Explains the deciding fact in own words'],['Trace or test','Cannot connect input and result','Completes steps with prompts','Traces or tests a changed case accurately'],['Limits and revision','Claims more than evidence supports','Names a limit after a prompt','States a defensible limit and useful next test']]},
 para('Project checkpoint: '+milestone[0]+'. '+milestone[1]),para('Use the weekly teacher answer for topic-specific reasoning. A saved progress tick is an activity record; judge mastery from the learner’s explanation and evidence.')]
 w['teacher'].append(section('Prepare, teach and assess',prep))
 # Resolve anchors after inserting the overview; retain every original section.
 # Original section numbers remain unchanged for teacher cross-references.
 rows.append({'week':w['id'],'goals':len(goals),'student_sections':len(w['sections']),'teacher_sections':len(w['teacher']),'project':w['project'],'milestone':milestone[0],'visual_question':case['student_task']})
p['classroom_improvements']={'version':'2026-10-07','sequence':route,'benchmark':'ai-1/1','lessons':len(rows)}
(R/'content/programme.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(R/'reports/classroom-improvements.json').write_text(json.dumps({'sequence':route,'benchmark':'ai-1/1','weeks':rows},indent=2)+'\n')
# Website metadata contains student-safe prompts only; teacher answers stay in protected pages.
meta={'sequence':route,'levels':{f"ai-{l['number']}":{'prerequisites':l['prerequisites'],'outcome':l['exit_outcome'],'project':l['project']} for l in p['levels']},'weeks':{w['id']:w['classroom'] for w in p['weeks']+p['python_bridge']}}
meta['levels']['python-bridge']={'prerequisites':'After Level 3; no previous Python required. Take the readiness check before deciding to skip.','outcome':'Independently trace, write, debug and test Python using conditions, loops, lists, dictionaries and functions.','project':'Python readiness portfolio'}
if (R/'lib').exists():(R/'lib/classroom-data.json').write_text(json.dumps(meta,ensure_ascii=False))
print('Updated all',len(rows),'lessons; preserved original sections and reserved assessments.')
