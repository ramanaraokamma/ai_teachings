"""Apply a reviewable reading hierarchy to Level 1 Week 1 only.
Original text remains canonical; presentation metadata supplies labels, paragraph breaks and emphasis.
"""
from pathlib import Path
import json,re,hashlib,copy
R=Path(__file__).resolve().parents[1];p=R/'content/programme.json';d=json.loads(p.read_text());w=next(w for w in d['weeks'] if w['id']=='ai-1/1')
others=lambda x:hashlib.sha256(json.dumps([v for v in x['weeks']+x['python_bridge'] if v['id']!='ai-1/1'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
before=others(d);snapshot=copy.deepcopy(w)
# An earlier run's definition row is unwrapped before rebuilding.
for key in ['sections','teacher','workbook']:
 for sec in w[key]:
  sec['blocks']=[child for b in sec['blocks'] for child in ([c for cell in b['cells'] for c in cell] if b.get('week1_definition_row') else [b])]
  for b in sec['blocks']:b.pop('presentation',None)
terms=['input','process','output','mechanism','written rule','learned model','human decision','human control','evidence','observation','prediction','fixed automation','hybrid system','not enough information','more information','70%','80%','60%','12 minutes','training','fitting']
def paras(text):
 if len(text)<220:return [text]
 sentences=re.split(r'(?<=[.!?]) (?=[A-Z“"\[])',text);groups=[];current=''
 for sentence in sentences:
  if current and len(current)+len(sentence)>225:groups.append(current);current=sentence
  else:current=(current+' '+sentence).strip()
 if current:groups.append(current)
 assert ' '.join(groups)==text
 return groups
prefixes={'CORE IDEA':('concept','The principle to teach'),'UNDER THE HOOD':('note','Mechanism, not appearance'),'MODEL REASONING':('example','Model answer'),'DO NOT OVERCLAIM':('caution','A claim to avoid'),'CASE':('example','The case to investigate'),'MYSTERY':('example','Start with this puzzle'),'GOOD THINKING':('concept','Thinking habit'),'BOUNDARY':('caution','Keep this boundary clear'),'RESPONSIBLE DESIGN':('caution','Responsible design'),'PARTNER CHECK':('question','Check with a partner'),'REQUIRED PROOF':('concept','What success looks like'),'RETRY RULE':('note','When to retry'),'STRONG ANSWER FRAME':('example','A frame for explaining'),'CLAIM A':('question','Challenge claim A'),'CLAIM B':('question','Challenge claim B'),'CLAIM TO REPAIR':('question','Find the unsupported claim'),'SELF-CHECK':('question','Check your explanation'),'NEXT BRIDGE':('note','Connect to the next lesson'),'LEARNING TARGET':('concept','Your target'),'Teaching target:':('concept','Teaching target'),'Reasoned practice answer:':('example','Supported practice answer'),'Misconception repair:':('caution','Repair the misconception'),'Support:':('note','Support without giving away the answer'),'Extension:':('question','Extend the reasoning'),'Independent assessment:':('caution','Protect the independent attempt'),'Project checkpoint:':('concept','Project checkpoint'),'Teacher prompt:':('note','Discuss while showing the picture'),'Supported practice key:':('example','Reasoning to listen for')}
custom={
 'teacher':{'Explain the mechanism':{
  'Follow the information instead':'The organising idea',
  'INPUT a command':'1. Input — information entering',
  'PROCESS a human':'2. Process — the deciding step',
  'OUTPUT movement':'3. Output — the result',
  'Every step connects':'Connect a claim to its evidence',
  'The lamp uses':'Reasoning for the six devices',
  'The school bus display':'Worked example · two explanations of the same display',
  'An output is':'Separate the result from the mechanism',
  'For this lesson we have':'The supplied engineering evidence',
  'In the first row':'Explain the three decisions separately',
  'AI is a broader field':'Precision · rules can also be part of AI',
  'Question: Does the red':'Think aloud · observation → evidence → conclusion',
  'A strong answer states':'Model the limit of the conclusion',
  'Use the diagram and verbal':'Teach with the picture and the explanation together',
  'Cover the result.':'Reveal the picture one step at a time'}},
 'sections':{'Notice the evidence':{'The school bus display':'One display, two first impressions','An output is':'Result versus mechanism','For this lesson we have':'Read the engineering note'},'See how it works':{'In the first row':'Read the three decisions separately','AI is a broader field':'An important boundary'}},
 'workbook':{}}
counts={}
for key in ['sections','teacher','workbook']:
 count=0
 for sec in w[key]:
  last_heading=sec['title']
  for b in sec['blocks']:
   if b['type']=='table' and b.get('headers') and b['rows'][0]!=b['headers']:b['rows'].insert(0,b['headers'])
   if b['type'] in ['subheading','heading','title']:
    if b.get('text','').casefold()==sec['title'].casefold():b['presentation']={'kind':'section-label'}
    last_heading=b.get('text',last_heading);continue
   if b['type'] not in ['paragraph','step','list','callout']:continue
   text=b.get('text','');fmt={'kind':'body','paragraphs':paras(text),'emphasis':[v for v in terms if v.casefold() in text.casefold()]}
   if text.isupper() and len(text)<45:fmt['kind']='eyebrow'
   if b['type']=='callout':fmt['kind']={'caution':'caution','answer':'example','think':'question','teacher':'note'}.get(b.get('tone'),'concept')
   for prefix,(kind,label) in prefixes.items():
    if text.startswith(prefix):fmt.update(kind=kind,label=label);break
   if re.match(r'STEP\s*\d',text):fmt.update(kind='step',label=re.match(r'STEP\s*\d',text).group().title())
   elif re.match(r'^(RECALL|EXPLAIN|TRACE|DIAGNOSE|TRANSFER|CREATE|DEFEND)\s',text):fmt['kind']='step'
   elif text.startswith('□'):fmt['kind']='check'
   elif text.endswith('?') and len(text)<260 and b['type']=='paragraph':fmt.update(kind='question')
   for prefix,label in custom.get(key,{}).get(sec['title'],{}).items():
    if text.startswith(prefix):fmt['label']=label;fmt['kind']='definition' if text.startswith(('INPUT ','PROCESS ','OUTPUT ')) else ('note' if 'Precision' in label else 'example' if text.startswith(('The school bus','Question:','The lamp uses')) else 'body');break
   # Long explanations get a descriptive heading only when their section lacks an immediate one.
   if len(text)>300 and 'label' not in fmt and not sec.get('graphic_journey'):
    labels={'Practise together':'Trace the photo-library decisions','Follow a worked example':'Explain the deciding evidence','Find and repair a mistake':'Investigate before guessing','Explain the mechanism':'Explain what the facts support'}
    if sec['title'] in labels:fmt['label']=labels[sec['title']]
   b['presentation']=fmt;count+=1
  sec['reading_design']='week1-review'
 counts[key]=count
# A true group of three parallel definitions, rather than a loose run of paragraphs.
s=next(s for s in w['teacher'] if s['title']=='Explain the mechanism');start=next(i for i,b in enumerate(s['blocks']) if b.get('text','').startswith('INPUT a command'));cards=s['blocks'][start:start+3];assert all(b['presentation']['kind']=='definition' for b in cards)
s['blocks'][start:start+3]=[{'type':'gallery','cells':[[b] for b in cards],'layout':'reading-cards','week1_definition_row':True}]

overviews={
 'sections':[
 'Know the learning target, try the clock question, and keep observations separate from explanations.',
 'Inspect the bus display, compare first impressions, and use the engineering note to identify what is actually supported.',
 'Trace the bus estimate, colour rule and driver override as three separate decisions.',
 'Compare human control, a written instruction, a trained model and a device whose mechanism is unknown.',
 'Use the vocabulary to explain a decision, then challenge an unsupported claim about robots.',
 'Follow the bus and umbrella worked cases. Predict a step before revealing the explanation.',
 'Repair claims based on a robot body, a screen or a correct answer; identify the missing mechanism evidence.',
 'Practise the photo-library explanation with support, then explain the deciding evidence in your own words.',
 'Investigate the supplied devices. Keep predictions, evidence, conclusions and unresolved questions distinct.',
 'Move from recalling a word to tracing, diagnosing, transferring and defending an explanation.',
 'Apply the evidence habit to the Helpful Classroom Sorter and retain a labelled project decision.',
 'Use a genuinely new case for independent evidence. If the six devices were discussed earlier, treat them as practice; the reserved greenhouse task is in Section 14.',
 'Revisit the six-device worked example for extra explanation. This is supported practice, not a fresh assessment.',
 'Attempt the reserved greenhouse case before feedback. The other examples below are additional practice, not repeated fresh assessments.',
 'Use this map to navigate the week and connect the goals to the evidence you will produce.',
 'Explain the idea without notes, name a remaining question, and plan a later return check.',
 'Use supported questions, hints and feedback to improve an explanation, then keep your completed work.',
 'Read each graphic, explain one labelled step, and connect its evidence to your project.'
 ],
 'teacher':[
 'Prepare the resources, check readiness and choose a realistic teaching schedule before starting the explanation.',
 'Teach the information path, distinguish the three mechanisms, and model how evidence supports a limited conclusion.',
 'Use the board sequence and dialogue to model reasoning, reduce help, and check every learner before discussion.',
 'Run the evidence investigation, capture actual observations and choose support from the first reasoning error.',
 'Use the keys after the relevant attempts. Previously discussed cases are practice; the reserved independent transfer question is the greenhouse case.',
 'Connect the explanation to the project, plan extensions and revisit prerequisites where needed.',
 'Use this preparation summary alongside the detailed sections; it is a checklist, not a replacement lesson.',
 'Use feedback, review links and portfolios purposefully. Coding guidance applies when a later lesson contains a lab.',
 'Show one graphic at a time, ask for a prediction, then use the labelled trace and teacher reasoning to discuss it.'
 ],
 'workbook':[
 'Record your first explanation before opening notes, then show any correction separately.',
 'Use the photo-library completion task. Keep a trace of the step you completed and any help you used.',
 'Challenge the proposed claim using the supplied facts before discussing it with a partner.',
 'Write one first attempt at the reserved greenhouse case before feedback; Section W4 refers to this same case.',
 'Use the bus target to explain which component makes each decision and which evidence supports the classification.',
 'Classify the six supplied devices and support each conclusion with mechanism evidence.',
 'Apply the distinction to the toy, photo app and talking clock, and explain each classification.',
 'Design a changed or missing-information case and keep the expected result separate from what you observe.',
 'Justify a project decision and retain the evidence that would let another person check it.',
 'Assess explanation, evidence, transfer and limits separately; attach the work behind your judgement.',
 'Use the original bus question as transfer practice. A previously discussed case is not fresh assessment evidence.',
 'Separate what is visible at the door from the question you still need answered about its mechanism.',
 'Classify the photo-library decisions and name the records needed to diagnose a misplaced picture.',
 'Offer plausible alternatives for the vacuum turn, then identify evidence that could distinguish them.',
 'This is the same greenhouse task as the independent transfer section. Reuse that recorded first attempt.',
 'Design one product with two mechanisms, then state one supported and one unsupported claim.',
 'Record the feedback, the first step you repaired and a different case to revisit after a delay.',
 'Explain the umbrella picture and predict a changed boundary using the supplied facts.',
 'Keep the sorter milestone, input, deciding step, result and limitation together in the project record.',
 'Use the supported questions once, compare with feedback after attempting them, and record what you repaired.',
 'Explain each picture using its labels and evidence, then record a relevant limit.'
 ]}
for role,key in [('student','sections'),('teacher','teacher'),('workbook','workbook')]:
 assert len(overviews[key])==len(w[key])
 for sec,intro in zip(w[key],overviews[key]):sec['reading_intro']=intro
# Clarify the purpose of alternative schedules without deleting any original plan.
for b in w['teacher'][0]['blocks']:
 text=b.get('text','')
 if text.startswith('Allow 80 minutes:'):b['presentation'].update(kind='note',label='Compact overview · 80-minute option',context='This is an alternative compact allocation. The main starting plan above uses three 45-minute sessions; allow more time for the full investigation, independent work and project.')
for sec in w['teacher']:
 heading='';pair=0
 for b in sec['blocks']:
  if b['type'] in ['heading','subheading']:heading=b.get('text','');pair=0
  f=b.get('presentation');text=b.get('text','')
  if not f or 'text' not in b:continue
  if sec['title']=='Assess and explain the answers' and b['type']=='paragraph':
   if heading.startswith(('W1 ','W2 ','W3 ','W4 ','W5 ')):
    pair+=1;f.update(kind='question' if pair==1 else 'example',label=('Workbook question · ' if pair==1 else 'Teacher reasoning · ')+heading.split(' ')[0])
   elif 'answer' in heading.lower():f.update(kind='example',label='Teacher key · '+heading)
   elif heading=='Independent question':f.update(kind='question',label='Independent question · withhold the key')
  teaching_labels={'Write the given facts:':('step','1. Put the facts on the board'),'Write the question to explain:':('step','2. State the decision to explain'),'Reveal after predictions:':('example','3. Reveal the worked reasoning'),'Keep for an independent attempt:':('caution','4. Hold back the independent task'),'Ask:':('question','Ask the class'),'Say:':('note','Language to model'),'Teacher check:':('example','Reasoning to listen for'),'Expected correction:':('example','Expected repair'),'Completion task:':('question','Completion practice'),'State your prediction':('step','1. Predict'),'Complete the task:':('step','2. Investigate'),'Keep a normal case':('step','3. Compare cases'),'Record what happened':('step','4. Record honestly'),'Explain the result,':('step','5. Explain and plan the next test')}
  for prefix,(kind,label) in teaching_labels.items():
   if text.startswith(prefix):f.update(kind=kind,label=label);break
  if text.startswith('Ask students to predict before running code.'):f.update(kind='note',label='For lessons with executable code',context='Week 1 has no Python lab. Retain this routine for later coding weeks.')
 # The detailed two-session table is a focused option within the adaptable weekly schedule.
 if sec['title']=='Demonstrate and guide practice':
  for b in sec['blocks']:
   if b.get('text','').startswith('Start by identifying'):b['presentation']['context']='The case-specific table above is a focused two-session sequence (90 minutes). Allow additional sessions for the rest of the weekly work; the allocations are planning examples, not validated durations.'
# Make hint/feedback labels and numbered choices visibly distinct in both learner resources.
for key in ['sections','workbook']:
 for sec in w[key]:
  for b in sec['blocks']:
   f=b.get('presentation');text=b.get('text','')
   if not f:continue
   if text.startswith('Hint if needed:'):f.update(kind='note',label='Hint · use only after trying')
   elif text.startswith('After your attempt, compare'):f.update(kind='example',label='Feedback · compare after your attempt')
   elif text.startswith('Changed-case practice:'):f.update(kind='question',label='Changed case · predict first')
   elif re.match(r'^\d+\. ',text):f['kind']='step'
   elif text.startswith('Support used:'):f.update(kind='note',label='Record the help you used')
   elif text.startswith(('Project:','Current milestone:','Project connection:')):f.update(kind='concept')

# Present the genuine parallel self-check statements as a checklist.
for b in w['workbook'][9]['blocks']:
 text=b.get('text','')
 if text.startswith('I can explain the mechanism.'):
  parts=re.split(r'(?<=\.) (?=I can|Mark each)',text)
  b['presentation'].update(kind='checklist',items=parts[:-1],tail=parts[-1])
for b in w['teacher'][0]['blocks']:
 text=b.get('text','')
 if text.startswith('The bus diagram and photo-library'):b['presentation'].update(kind='check',label='Resources to prepare')
 elif text.startswith(('Blank paper and three colours','A copy of workbook tasks')):b['presentation']['kind']='check'

# Audit each section, rather than treating the week as a single formatted document.
section_audit=[]
for key in ['sections','teacher','workbook']:
 for number,sec in enumerate(w[key],1):
  section_audit.append({'audience':key,'number':number,'title':sec['title'],'reviewed':True,'purpose':sec['reading_intro'],'checks':['heading hierarchy','reading chunks','instruction versus explanation','questions versus answers','table labels','image/context alignment','assessment boundary']})

w['reading_design']={'edition':'Week 1 formatting review','scope':'student, teacher and workbook','approach':'semantic hierarchy, short paragraphs, emphasis, definition cards, labelled examples, questions and cautions'}
assert others(d)==before
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
(R/'reports/week1-formatting.json').write_text(json.dumps({'week':'ai-1/1','formatted_blocks':counts,'other_lessons_unchanged':True,'other_lessons_sha256':before,'sections_reviewed':len(section_audit),'section_audit':section_audit},indent=2))
print('Formatted Level 1 Week 1 only:',counts)
