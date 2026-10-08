"""Rebuild the programme from preserved sources. Run with Python 3 from any folder."""
from pathlib import Path
import json,copy,re,html,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'tools/source-inputs.json').read_text())
LABELS=['Your mission','Notice the evidence','See how it works','Compare the cases','Words that unlock the idea','Follow a worked example','Find and repair a mistake','Practise together','Run the investigation','Build your understanding','Connect your project','Show what you know','Study a complete case','Try a new case independently']
NAMES=['Foundations','Algorithms and Data','Generative AI Systems','Machine Learning','Neural Networks','AI Engineering','Research and Advanced Projects']
PROJECTS=['Helpful Classroom Sorter','Transparent Book Recommender','Verified Study Buddy','Responsible Plant Classifier','Image-pattern Network Investigation','Grounded Learning Service','Reproducible AI Research Study']
PREREQS=['Separate an observation from a guess; use whole numbers and explain a simple rule.','Complete Foundations exit evidence; trace ordered instructions and compare counts.','Explain inputs, rules, evidence and privacy; use approved sources and simple fractions.','Complete the Python bridge or demonstrate equivalent skills; use fractions, coordinates and independently trace a function.','Complete Machine Learning exit evidence and Python readiness; use signed numbers, linear equations and coordinates.','Complete Generative AI and Machine Learning; demonstrate Python/JSON readiness and understand role permissions.','Complete Machine Learning and AI Engineering; compare baselines, control variables and keep a reproducible record.']
# Local corrections are confined to this dedicated programme.
FIXES={
 'Both outputs are food release. The clock version follows a directly written condition. The prediction version uses a pattern fitted from examples. The outward action does not reveal which mechanism created it.':'The motion light follows a directly written sensor condition. The animal recogniser uses a model fitted on labelled examples. Observing that both react to input does not tell us how their decisions were produced.',
 'Agreement of 7/8 reveals one case that needs a clearer rule.':'Agreement of 7/8 identifies one disagreement to review. Check the source, each annotator’s application and the label rule before choosing a repair.',
 'Begin with random visual noise.':'In this simplified diffusion-style image generator, begin with random visual noise. Other image-generation methods use different procedures.',
 'A visible-spot rule gets 15 ÷ 20 = 75% accuracy and 60% spotted recall.':'On the same 20 leaves, the visible-spot rule correctly labels 5 spotted leaves, misses 3 spotted leaves, correctly labels 10 healthy leaves and falsely marks 2 healthy leaves as spotted. Accuracy=(5+10)/20=75%; spotted recall=5/8=62.5%.',
 'Training leaves at (2, 2), (4, 3), and (1, 5) have distances 1, 2, and 3.':'Using Manhattan distance, add the absolute coordinate differences. Training leaves at (2, 2), (4, 3), and (1, 5) have distances 1, 2, and 3 from (2, 3).',
 'Ten predictions have scores near 0.8. Only six are correct, so observed correctness is 6 ÷ 10 = 60%.':'For this example, each score estimates the probability that the selected label is correct. Ten predictions have scores near 0.8; six are correct, so observed correctness is 6/10=60%. If instead scores mean probability of the spotted class, compare them with the fraction of reference-spotted leaves.',
 'Majority baseline: 60% accuracy, 0% spotted recall; rule baseline: 75% and 60%.':'Validation has 12 healthy and 8 spotted leaves. The always-healthy baseline scores 12/20=60% accuracy and 0/8=0% spotted recall. The rule has TP=5, FN=3, TN=10, FP=2: accuracy 75% and spotted recall 62.5%.',
 'Ten predictions have scores near 0.8.':'Each score estimates the probability that the selected label is correct. Ten predictions have such scores near 0.8.',
 'Error audit finds six low-light failures and one label disagreement.':'The six failed cases are low-light cases. One of those same six also has a disputed reference label; that is an overlapping review flag, not a seventh failed case.'}
CORRECTED_ASSETS={}
def fix(value):
 if isinstance(value,str):
  for a,b in FIXES.items():value=value.replace(a,b)
  return value
 if isinstance(value,list):return [fix(v) for v in value]
 if isinstance(value,dict):
  if value.get('type')=='image' and value.get('src','').split('/')[-1] in CORRECTED_ASSETS:return copy.deepcopy(CORRECTED_ASSETS[value['src'].split('/')[-1]])
  return {k:fix(v) for k,v in value.items()}
 return value
# Correct inconsistent source illustration cards without editing the original bitmaps.
# The active lesson uses a native diagram; the inherited card remains in private provenance.
for level in S['original']['levels']:
 for week in level['weeks']:
  id=f"{level['slug']}/{week['number']}"
  if id not in ['ai-2/8','ai-3/10','ai-4/10','ai-4/12','ai-4/14','ai-4/34','ai-4/35']:continue
  page=week['student']['pages'][5]
  steps=[fix(b['text']) for b in page['blocks'] if b['type']=='paragraph' and re.match(r'^(STEP \d|\d[.])',b.get('text',''))]
  for b in page['blocks']:
   if b['type']=='image' and 'worked evidence' in b.get('alt','').lower():
    asset=b['src'].split('/')[-1]
    CORRECTED_ASSETS[asset]={'type':'diagram','kind':'lanes','title':b['alt'],'columns':['Step','Evidence and reasoning'],'rows':[[str(i+1),re.sub(r'^(STEP \d\s*|\d[.]\s*)','',step)] for i,step in enumerate(steps)],'caption':'Trace these corrected steps. Keep the stated metric, assumptions and interpretation when you change the case.'}
    old=ROOT/'assets'/(asset+'.png');archive=ROOT/'tools/source-assets'/(asset+'.png');archive.parent.mkdir(exist_ok=True)
    if old.exists():old.replace(archive)
(ROOT/'reports/corrected-illustrations.json').write_text(json.dumps(CORRECTED_ASSETS,indent=2))
# Repair mechanically shortened figure labels using their complete source explanation.
# Short noun-phrase labels remain concise; incomplete sentence excerpts become complete.
diagram_repairs=[]
for source,c in S['rebuilt'].items():
 candidates=[b.get('text','') for sec in c['lesson'] for b in sec['blocks'] if b['type']=='paragraph']+[c['teacher']['guidedAnswer']]+[q['answer'] for q in c['workbook']]
 for sec in c['lesson']:
  for b in sec['blocks']:
   if b['type']=='diagram':
    for row in b.get('rows',[]):
     for i,cell in enumerate(row):
      if len(cell)>=70 and cell[-1] not in '.?!':
       matches=[t for t in candidates if len(t)>len(cell) and t.startswith(cell)]
       if matches:
        complete=min(matches,key=len);row[i]=complete
        diagram_repairs.append({'source':source,'before':cell,'after':complete})
(ROOT/'reports/diagram-clarifications.json').write_text(json.dumps(diagram_repairs,indent=2))
def P(t):return {'type':'paragraph','text':t}
def H(t):return {'type':'subheading','text':t}
def R(t,lines=5):return {'type':'response','label':t,'lines':lines}
def T(headers,rows):return {'type':'table','rows':[headers]+rows}
def paragraphs(section):return [copy.deepcopy(b) for b in section['blocks'] if b['type']=='paragraph']
def clean(blocks):
 out=[]
 for b in copy.deepcopy(blocks):
  t=b.get('text','')
  if t in ['MASTER CURRICULUM 2.0','Student workbook','Teacher guide'] or 'ILLUSTRATED STUDENT EDITION' in t or 'Grade 6 entry edition' in t or t.startswith('Name ______'):continue
  if b['type']=='title':continue
  if b['type']=='response':b=R('Write or draw your reasoning and evidence.')
  if b['type']=='gallery':b['cells']=[clean(c) for c in b['cells']]
  out.append(b)
 return out
def newblock(b):
 b=copy.deepcopy(b)
 if b['type']=='table' and 'headers' in b:b['rows']=[b['headers']]+b['rows'];b.pop('headers')
 return b
def topic_case(id):
 p=fix(S['plans'][id]);return [H(p['title']),T(['Evidence or stage','Value or result'],[[i['label'],i['value']] for i in p['items']]),P(p['scenario']),P(p['question']),P(p['explanation'])]
def transfer(id):
 t=fix(S['transfer'][id])
 if id=='ai-1/12':t['task']='The requirement is to move exactly three squares forward from any valid starting square, then stop. Starting at square 0, repeat twice {MOVE 1}; STOP ends at 2. A teammate reduces the required distance to two squares. Repair the program without changing the requirement; test starts 0 and 2.'
 return t

def diagram_blocks(c):
 return [newblock(b) for s in c['lesson'] for b in s['blocks'] if b['type']=='diagram']
def core_enrichment(c):
 s=c['lesson'];result={1:[],2:[],5:[],6:[],7:[]}
 for j,key in [(0,1),(1,2),(2,5),(3,7),(4,6)]:result[key]=[newblock(b) for b in s[j]['blocks']]
 return result

def original_week(level,w):
 id=f"{level['slug']}/{w['number']}";match=next(x for x in S['coverage'] if x['legacy']==id);c=S['rebuilt'][match['destination']];w=fix(copy.deepcopy(w));tr=transfer(id)
 sections=[{'title':LABELS[i],'blocks':clean(w['student']['pages'][i]['blocks'])} for i in range(14)]
 # Original page numbers 13 and 14 already hold the worked case and independent application.
 sections[12]['blocks'] += [H('Trace the supplied case visually')]+topic_case(id)
 enrichment=core_enrichment(c)
 for index,blocks in enrichment.items():sections[index]['blocks'] += [H('A closer explanation')]+blocks
 if match['destination'] in S['reading']:sections[2]['blocks'] += [H(S['reading'][match['destination']]['title']),P(S['reading'][match['destination']]['studentExplanation'])]
 vocab=next((b['rows'][1:] for s in sections for b in s['blocks'] if b['type']=='table' and b['rows'] and b['rows'][0][0]=='Word'),[])
 known={row[0].lower() for row in vocab}
 extra=[v for v in c['vocabulary'] if v[0].lower() not in known]
 if extra:sections[4]['blocks'] += [H('Words used in the closer explanation'),T(['Word','Meaning'],extra)]
 sections[13]['blocks'] += [H('Transfer practice from the original programme'),P(tr['task']),R('Explain the mechanism, evidence and one limit.',7)]
 # Preserve complete executable labs in the two original weeks with a fifteenth section.
 for p in w['student']['pages'][14:]:sections.append({'title':p['label'],'blocks':clean(p['blocks'])})
 if id=='ai-1/3':sections[2]['blocks'].append({'type':'sensor','title':'The sensor measures. The rule decides.'})
 tasks=[];current={'title':'Before you begin','blocks':[]}
 for b in clean(w['workbook']['blocks']):
  if b['type']=='subheading':
   if current['blocks']:tasks.append(current)
   current={'title':b['text'],'blocks':[]}
  else:current['blocks'].append(b)
 if current['blocks']:tasks.append(current)
 tasks.append({'title':'Transfer practice from the original programme','blocks':[P(tr['task']),R('My independently reasoned answer',7),P('Record support used: none, hint or teacher explanation.')]})
 teacher=[{'title':p['label'],'blocks':clean(p['blocks'])} for p in w['teacher']['pages']]
 sections[0]['blocks'] += [H('Readiness for the connected explanation'),P(c['prerequisite']['prompt'])]
 teacher[0]['blocks'] += [H('Preparation for the connected explanation'),P(c['teacher']['background']),H('Readiness answer'),P(c['prerequisite']['answer'])]+[P(m) for m in c['teacher']['materials']]
 teacher[1]['blocks'] += [H('Explain the added worked example')]+paragraphs(c['lesson'][0])+paragraphs(c['lesson'][1])+[H('Key terms') ,T(['Term','Meaning'],c['vocabulary'])]
 teacher[2]['blocks'] += [H('Model these guided questions'),P(c['teacher']['guidedAnswer']),H('Case-specific teaching sequence'),T(['Stage','Teacher action'],c['teacher']['sessions'])]
 teacher[3]['blocks'] += [H('Address these additional misconceptions')]+[P(a+': '+b) for a,b in c['teacher']['misconceptions']]
 # Add answers explicitly; student question pages never receive these blocks.
 teacher[4]['blocks'] += [H('Original transfer answer'),P(tr['solution']),H('Explanations for the additional workbook examples')]
 for q in c['workbook']:
  teacher[4]['blocks'] += [H(q['id']+' '+q['title']),P(q['prompt']),P(q['answer'])]
  extra=S['answers'].get(match['destination'],{}).get(q['id'])
  if extra:teacher[4]['blocks'].append(P(extra))
 teacher[5]['blocks'] += [H('Support and fresh reassessment'),P(c['teacher']['support']),P(c['teacher']['assessment']),P(c['teacher']['next'])]
 # Added questions from the rebuilt example are part of the integrated workbook, not separate practice links.
 for q in c['workbook']:tasks.append({'title':q['id']+' '+q['title'],'blocks':[P(q['prompt']),R('My reasoning and evidence',q['lines'])]})
 return {'id':id,'level':int(level['slug'][-1]),'week':w['number'],'title':w['student']['title'].split(': ',1)[-1],'grade':int(level['slug'][-1])+5,'project':level['capstone'],'recall':tr['recall'],'sections':sections,'teacher':teacher,'workbook':tasks,'sources':{'original':id,'rebuilt':match['destination']},'independent_answer':tr['solution']}

PROJECT_STAGE={
1:'Write the user need, permitted inputs and one action that the project must never take.',2:'Draw the information path and name the evidence needed to trust each stage.',3:'State a complete input/output contract, including missing values and a safe fallback.',4:'Create a small fictional example set and preserve it with a version label.',5:'Trace the worked procedure and identify the first place a wrong result could arise.',6:'Record the vocabulary and prerequisite evidence needed to explain this component.'}
def project_checkpoint(c,project,n):
 goals=c['goals'];task=c['workbook'][3]
 if n>=33:return f"For {project}, use this week’s independent task as a rehearsal for the final evidence pack: {task['prompt']} Keep actual observations separate from expected results, preserve failures, compare a baseline and explain the limits."
 return f"Add a labelled {c['title'].lower()} evidence sheet to {project}. Show how you can {goals[0].rstrip('.').lower()}. Use the supplied fictional case and keep its inputs, intermediate steps, calculation or prediction, and limitation. Connect this record to last week’s record; a matching answer without a trace is insufficient."
def extended(c,newlevel,n,bridge=False):
 c=copy.deepcopy(c);project=PROJECTS[newlevel-1] if not bridge else 'Python readiness portfolio';sections=[{'title':t,'blocks':[]} for t in LABELS]
 def add(i,*b):sections[i]['blocks'] += list(b)
 add(0,P('This week you will practise:'),* [P(g) for g in c['goals']],H('Retrieve what you already know'),P(c['prerequisite']['prompt']),R('My starting explanation',3))
 add(1,*[newblock(b) for b in c['lesson'][0]['blocks']],R('List the given facts and one fact that is not supplied.',3))
 add(2,*[newblock(b) for b in c['lesson'][1]['blocks']])
 add(3,H('Compare a familiar case with a changed case'),P(c['workbook'][1]['prompt']),R('Keep the procedure fixed. Explain what changed in the inputs and result.',5))
 add(4,T(['Word','Meaning'],c['vocabulary']),R('Use two terms to explain a step in this week’s example.',3))
 add(5,*[newblock(b) for b in c['lesson'][2]['blocks']])
 add(6,*[newblock(b) for b in c['lesson'][3]['blocks']],H('Locate the earliest unsupported step'),P(c['workbook'][2]['prompt']),R('State one repair and the checks you would rerun.',6))
 response=[newblock(b) for s in c['lesson'] for b in s['blocks'] if b['type']=='response']
 add(7,P(c['workbook'][0]['prompt']),*response[:1],R('Explain your prediction to a partner before comparing results.',4))
 codes=[newblock(b) for s in c['lesson'] for b in s['blocks'] if b['type']=='code']
 add(8,H('Predict, investigate and preserve the evidence'),P(c['workbook'][1]['prompt']),*codes,T(['Record','Your evidence'],[['Given input and fixed rule',''],['Prediction before checking',''],['Actual result, or “not run”',''],['First mismatch and one explanation',''],['Boundary or missing input and expected response','']]),P('On paper, trace the supplied procedure. If code is provided, predict before running it in a local practice file. Never write an expected answer as though it were an observed run.'))
 add(9,H('Explain → apply → challenge'),P(c['workbook'][0]['prompt']),P(c['workbook'][2]['prompt']),P(c['workbook'][4]['prompt']),R('Explain which evidence supports your conclusion and which claim remains unproved.',5))
 checkpoint=project_checkpoint(c,project,n)
 add(10,P(checkpoint),T(['Project evidence','Record'],[['Component and version',''],['Inputs permitted at prediction time',''],['Trace and comparison with earlier work',''],['Failure, limit and human review','']]))
 add(11,*[newblock(b) for b in c['lesson'][4]['blocks']],P(c['workbook'][4]['prompt']),R('My limited claim and a useful next check',4))
 add(12,H('Complete evidence record'),*diagram_blocks(c),P('Follow the input through the stated procedure to its result. Cover the result first, predict it, then explain every intermediate step. The text/table accompanies the figure so the example can be read without colour.'),R('My complete trace of the worked case',6))
 add(13,H('Attempt this without hints'),P(c['workbook'][3]['prompt']),R('My independent procedure, result and limitation',8),P('Record support used: none, hint or teacher explanation. After feedback, a different case is needed to demonstrate independence.'))
 t=c['teacher'];teacher=[
 {'title':'Prepare the purpose, prerequisites and materials','blocks':[P(t['background']),H('Outcomes')]+[P(g) for g in c['goals']]+[H('Preparation')]+[P(m) for m in t['materials']]+[H('Prerequisite answer'),P(c['prerequisite']['answer'])]},
 {'title':'Explain and model the mechanism','blocks':paragraphs(c['lesson'][0])+paragraphs(c['lesson'][1])+[T(['Term','Meaning'],c['vocabulary'])]+diagram_blocks(c)+[P(t['guidedAnswer'])]},
 {'title':'Demonstrate and guide practice','blocks':[T(['Time or stage','Teacher action'],t['sessions']),P('Use the worked example in Sections 3 and 6. Collect a prediction before revealing its result; ask the learner to point to each intermediate fact.'),P(t['support'])]},
 {'title':'Run the investigation and diagnose misconceptions','blocks':[P(a+': '+b) for a,b in t['misconceptions']]+[P('Use Section 9 for the evidence ledger. Add a boundary or missing-input case and record the expected response before checking. More successful repeats of one case do not establish wider coverage.')]},
 {'title':'Assess and explain the answers','blocks':[H('Guided and exit questions'),P(t['guidedAnswer'])]+sum(([H(q['id']+' '+q['title']),P(q['prompt']),P(q['answer'])] for q in c['workbook']),[])+[H('Independent assessment and fresh retry'),P(t['assessment'])]},
 {'title':'Connect the project, support and next lesson','blocks':[P(checkpoint),P(t['support']),P(t['next']),P('Retain the project ledger and assess a changed case after support. Check the relevant prerequisite before carrying this component forward.')]}
 ]
 tasks=[{'title':q['id']+' '+q['title'],'blocks':[P(q['prompt']),R('My reasoning and evidence',q['lines'])]} for q in c['workbook']]+[{'title':'Project checkpoint and reflection','blocks':[P(checkpoint),R('My project change, supporting evidence and remaining limit',6)]}]
 return {'id':f'ai-{newlevel}/{n}' if not bridge else f'python-bridge/{n}','level':newlevel,'week':n,'title':c['title'],'grade':newlevel+5 if not bridge else 8,'project':project,'recall':c['prerequisite']['prompt'],'sections':sections,'teacher':teacher,'workbook':tasks,'sources':{'rebuilt':f"{c['level']}/{c['week']}"},'independent_answer':c['workbook'][3]['answer']}

weeks=[]
for level in S['original']['levels']:
 for w in level['weeks']:weeks.append(original_week(level,w))
for newlevel,sourcelevel in [(5,4),(6,6),(7,7)]:
 for n in range(1,37):weeks.append(extended(S['rebuilt'][f'ai-{sourcelevel}/{n}'],newlevel,n))
bridges=[extended(S['rebuilt'][f'ai-2/{n}'],2,n,True) for n in range(1,13)]
# Retain every later source lesson, including topics without a one-to-one original match.
INTEGRATE={
'ai-2/15':'ai-4/5','ai-2/16':'ai-2/12','ai-2/18':'ai-2/19','ai-2/21':'ai-4/29',
'ai-2/25':'ai-4/4','ai-2/27':'ai-4/4','ai-2/28':'ai-4/26','ai-2/29':'ai-2/31',
'ai-2/30':'ai-2/32','ai-2/32':'ai-2/33','ai-2/33':'ai-2/35',
'ai-3/8':'ai-4/13','ai-3/11':'ai-4/8','ai-3/29':'ai-4/30','ai-3/34':'ai-4/34',
'ai-5/5':'ai-3/2','ai-5/6':'ai-3/3','ai-5/7':'ai-3/4','ai-5/8':'ai-3/5',
'ai-5/9':'ai-3/6','ai-5/18':'ai-3/18','ai-5/19':'ai-3/18','ai-5/20':'ai-3/26',
'ai-5/23':'ai-3/31','ai-5/25':'ai-3/27','ai-5/31':'ai-3/35'}
lookup={w['id']:w for w in weeks}
for source,destination in INTEGRATE.items():
 w=lookup[destination];c=S['rebuilt'][source];label='Apply the connected idea: '+c['title']
 for index,bb in core_enrichment(c).items():w['sections'][index]['blocks'] += [H(label)]+bb
 w['sections'][0]['blocks'] += [H('Readiness for '+c['title']),P(c['prerequisite']['prompt']),R('My readiness explanation',3)]
 w['sections'][4]['blocks'] += [H('Terms for '+c['title']),T(['Term','Meaning'],c['vocabulary'])]
 if source in S['reading']:w['sections'][2]['blocks'] += [H(S['reading'][source]['title']),P(S['reading'][source]['studentExplanation'])]
 w['teacher'][0]['blocks'] += [H(label),P(c['teacher']['background']),H('Readiness answer'),P(c['prerequisite']['answer'])]+[P(m) for m in c['teacher']['materials']]
 w['teacher'][1]['blocks'] += [H(label)]+paragraphs(c['lesson'][0])+paragraphs(c['lesson'][1])+[P(c['teacher']['guidedAnswer'])]
 w['teacher'][2]['blocks'] += [H('Teach the connected idea'),T(['Stage','Teacher action'],c['teacher']['sessions'])]
 w['teacher'][3]['blocks'] += [H('Check these misconceptions')]+[P(a+': '+b) for a,b in c['teacher']['misconceptions']]
 for q in c['workbook']:
  w['workbook'].append({'title':c['title']+' — '+q['id']+' '+q['title'],'blocks':[P(q['prompt']),R('My reasoning and evidence',q['lines'])]})
  w['teacher'][4]['blocks'] += [H(c['title']+' — '+q['id']+' '+q['title']),P(q['prompt']),P(q['answer'])]
  extra=S['answers'].get(source,{}).get(q['id'])
  if extra:w['teacher'][4]['blocks'].append(P(extra))
 w['teacher'][5]['blocks'] += [H('Readiness and reassessment for '+c['title']),P(c['teacher']['support']),P(c['teacher']['assessment'])]
 w['sources'].setdefault('additional',[]).append(source)
programme={'title':'AI Academy — Complete Learning Programme','purpose':'Learn to understand, design, build, test and explain AI systems responsibly.','levels':[{'number':i+1,'name':NAMES[i],'grade':i+6,'project':PROJECTS[i],'prerequisites':PREREQS[i],'weeks':36} for i in range(7)],'weeks':weeks,'python_bridge':bridges,'pacing':'Plan two or three 45-minute sessions per week. Reserve further sessions for the named connected topics and investigations; adjust after checking readiness.','source_note':'Preserves the original four-level sequence; integrates topic-matched explanatory material; adds three complete levels. Teacher answers are exported separately.'}
assert len(weeks)==252 and len({w['id'] for w in weeks})==252
from teaching_method import apply_method
programme=apply_method(programme,S)
from visual_lessons import apply_visual_lessons
programme=apply_visual_lessons(programme)
if __name__=='__main__':
 (ROOT/'content/programme.json').write_text(json.dumps(programme,indent=2))
 print('Canonical programme written:',len(weeks),'weeks and',len(bridges),'Python bridge lessons')
