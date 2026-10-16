"""Apply the approved reading design to the remaining lessons without rewriting their text.
The approved Week 1 remains byte-for-byte equivalent as a canonical object.
"""
from pathlib import Path
import ast,json,re,hashlib,copy
R=Path(__file__).resolve().parents[1]
# Reuse the approved paragraph/emphasis rules without executing the Week 1 migration.
tree=ast.parse((R/'tools/format_week1.py').read_text());env={'re':re}
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['terms','prefixes'] for t in node.targets) or isinstance(node,ast.FunctionDef) and node.name=='paras':exec(compile(ast.Module(body=[node],type_ignores=[]),'approved-reading-rules','exec'),env)
PREFIXES={**env['prefixes'],'UNDER THE HOOD':('note','How the mechanism works'),'CORE IDEA':('concept','Key idea'),'NORMAL CASE':('example','The normal case'),'MISSING INFORMATION':('caution','Check missing information'),'INDEPENDENT MASTERY':('caution','Independent evidence'),'QUESTION':('question','Question to explain'),'CHALLENGE':('question','Try a more demanding case'),'ERROR':('caution','Find the first error'),'EXPECTED':('example','Expected result'),'SOLUTION':('example','Worked explanation'),'SYSTEM MAP':('concept','Trace the system'),'INDEPENDENCE':('caution','Use a fresh case after support'),'Completion task:':('question','Completion practice'),'Teacher check:':('example','Reasoning to listen for'),'Expected correction:':('example','Expected repair'),'Hint if needed:':('note','Hint · try first'),'After your attempt, compare':('example','Feedback · compare after trying'),'Change:':('question','Change one thing'),'Prediction:':('example','Predicted result'),'Reason:':('example','Why the result follows'),'Teacher explanation:':('example','Teacher reasoning'),'Write the given facts:':('step','1. Put the facts on the board'),'Write the question to explain:':('step','2. State the decision to explain'),'Reveal after predictions:':('example','3. Reveal the worked reasoning'),'Keep for an independent attempt:':('caution','Hold back the independent task'),'Ask:':('question','Ask the class'),'Say:':('note','Language to model'),'State your prediction':('step','1. Predict'),'Complete the task:':('step','2. Investigate'),'Keep a normal case':('step','3. Compare cases'),'Record what happened':('step','4. Record honestly'),'Explain the result,':('step','5. Explain and plan the next test'),'Support used:':('note','Record the help used'),'Changed-case practice:':('question','Changed case · predict first')}
P=R/'content/programme.json';D=json.loads(P.read_text());weeks=D['weeks']+D['python_bridge'];approved=copy.deepcopy(weeks[0])

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def walk(bs):
 for b in bs:
  yield b
  if b['type']=='gallery':
   for cell in b['cells']:yield from walk(cell)
def original_content(w):
 return [[{'title':s['title'],'blocks':[{k:v for k,v in b.items() if k not in ['presentation','layout','programme_definition_row']} for b in walk(s['blocks']) if b['type']!='gallery']} for s in w[key]] for key in ['sections','teacher','workbook']]
def paragraph_chunks(text):
 # Split on sentence boundaries, preserving every original character when joined.
 if len(text)<220:return [text]
 sentences=re.split(r'(?<=[.!?]) (?=[A-Z“"\[])',text);rows=[];row=''
 for sentence in sentences:
  if row and len(row)+len(sentence)>225:rows.append(row);row=sentence
  else:row=(row+' '+sentence).strip()
 if row:rows.append(row)
 return rows if ' '.join(rows)==text else [text]

def purpose(w,key,s,number):
 title=s['title'];topic=w['title'];case=w['pictorial_case'];project=w['project'];goal=w['method']['goals'][0].rstrip('.')
 student={
 'Your mission':f'Start with the target: {goal}. Try the recall before opening notes.',
 'Notice the evidence':f'Investigate the supplied {topic} case. Separate observations, given facts and assumptions before choosing an explanation.',
 'See how it works':f'Follow the mechanism for {topic}. Connect each labelled input, deciding step and result.',
 'Compare the cases':f'Compare the supplied cases for {topic}. Identify the detail that changes the conclusion.',
 'Words that unlock the idea':f'Use the vocabulary of {topic} to explain a concrete decision, rather than only memorising definitions.',
 'Follow a worked example':f'Follow the worked trace for {topic}, predict a step, then compare with its explanation.',
 'Find and repair a mistake':f'Find the unsupported step in the {topic} claim and explain a repair using the supplied evidence.',
 'Practise together':f'Practise {topic} with support, then explain the deciding step in your own words.',
 'Run the investigation':f'Investigate {topic}. Record the prediction, actual observation or labelled paper trace, explanation and next test separately.',
 'Build your understanding':f'Move from recall to tracing, diagnosis and transfer in {topic}. Explain why each step is justified.',
 'Connect your project':f'Apply this week’s idea to {project}. Keep an annotated decision and the evidence supporting it.',
 'Show what you know':'Use a genuinely new case for independent evidence. Previously discussed examples remain practice; use the separately named independent case before feedback.',
 'Study a complete case':f'Revisit the complete {topic} case for supported practice. Repeated examples do not become fresh assessments.',
 'Try a new case independently':'Attempt the reserved new case before feedback. Record support; the earlier examples below remain additional practice.',
 'Your lesson route':f'Use this map to navigate {topic}, connect the goals to tasks and keep one evidence record for each attempt.',
 'Finish and return':f'Explain {topic} without notes, identify a remaining question and plan a later check with a changed case.',
 'Supported practice, repair and portfolio':'Attempt supported questions before using hints or feedback. Review a missing building block, then keep the completed work.',
 'Visual concept journey':f'Explain each {topic} graphic using its labels, deciding evidence and relevant limitation.'}
 if key=='sections':return student.get(title,f'Follow the supplied {topic} lab. Predict first, keep actual results and explain the changed test.')
 if key=='teacher':
  if number==1:return f'Prepare {topic}: check the target, prerequisites, resources and adaptable teaching schedule.'
  if title in ['Explain the mechanism','Explain and model the mechanism']:return f'Model {topic} using the supplied case, labelled mechanism and reasoning. Make the scope of each conclusion explicit.'
  if title=='Demonstrate and guide practice':return f'Demonstrate {topic}, reduce support deliberately and check individual reasoning before discussing answers.'
  if title in ['Run the weekly evidence lab','Run the investigation and diagnose misconceptions']:return f'Run the {topic} investigation and use the first unsupported step to choose a teaching response.'
  if title=='Assess and explain the answers':return f'Use the {topic} questions, teacher keys and criteria after the relevant attempts. Previously discussed cases are practice; protect the separately selected independent task.'
  if title in ['Connect and extend learning','Connect the project, support and next lesson']:return f'Connect {topic} to {project}, adapt support and plan a later changed-case check.'
  if title=='Prepare, teach and assess':return f'Use this preparation summary alongside the detailed {topic} lesson; it is a checklist rather than a replacement for the full sequence.'
  if title=='Use feedback, labs and repair paths':return 'Use feedback, earlier review and portfolios purposefully. Apply the coding routine only when this lesson has an executable lab.'
  if title=='Visual concept journey':return f'Show one {topic} graphic at a time, request a prediction and discuss its trace before the independent assessment.'
 if title=='Recall and choose your starting point':return f'Record your starting explanation for {topic} before opening notes. Show any later correction separately.'
 if title=='Practise with fading help':return f'Complete the supported {topic} trace and record the first step you can explain without help.'
 if title=='Individual reasoning check':return f'Check the proposed {topic} explanation against the supplied facts before discussing it.'
 if title=='Independent transfer case':return 'Write one first attempt at the reserved independent case before feedback. Repeated copies of that case refer to the same recorded attempt.'
 if re.match(r'^W\d+ ',title):return ('Attempt before feedback. If this repeats the selected independent case, reuse that first attempt; otherwise keep a separate record. ' if title.startswith('W4 ') else '')+title.split(' ',1)[1].rstrip('.')+f'. Apply the supplied {topic} facts and keep your reasoning.'
 if title.startswith('Pictorial case practice:'):return case['scenario']+' Explain the labelled step before checking the changed condition.'
 m={'Your learning target':f'Connect the {topic} target to a trace and a justified conclusion.','Solve the given case':f'Solve the supplied {topic} case and show the deciding evidence.','Check a changed case':'Apply the procedure to the changed case and record why the conclusion follows.','Design a revealing test':'Specify a changed input, expected result and observation separately.','Project checkpoint':f'Justify what {topic} adds to {project} and keep the evidence.','Project checkpoint and reflection':f'Connect {topic} to {project}, identify a limit and choose the next useful test.','Self check':'Judge explanation, evidence, transfer and limits separately; attach the work behind your judgement.','Transfer practice from the original programme':'Use this earlier case as transfer practice. A case already discussed with feedback is not fresh assessment evidence.','Feedback, return check and learning record':'Record the first repaired step and a different case to revisit after a delay.','Project portfolio milestone':f'Keep this week’s input, deciding step, result and limit together in the {project} record.','Supported practice and learning evidence':'Try the supported questions before comparing with hints and feedback. Record what you repaired and the evidence you retained.','Visual concept journey':f'Explain each {topic} picture from its labels, then record a relevant limit.'}
 return m.get(title,f'Use the supplied {topic} task to record your reasoning, evidence and next step.')

rows=[];counts={'sections':0,'teacher':0,'workbook':0};fixed_tables=0;definition_rows=0;preservation_errors=[]
for w in weeks:
 if w['id']=='ai-1/1':
  rows.extend({'week':w['id'],'audience':key,'section':i,'title':s['title'],'purpose':s['reading_intro'],'status':'approved reference retained'} for key in counts for i,s in enumerate(w[key],1));continue
 original=original_content(w)
 # Topic-specific emphasis comes from the existing learner glossary, not teacher-only keys.
 terms=list(env['terms'])
 for sec in w['sections']:
  for b in sec['blocks']:
   if b['type']=='table' and b.get('rows') and b['rows'][0][0].casefold() in ['term','word']:
    terms.extend(str(row[0]) for row in b['rows'][1:] if row and 4<=len(str(row[0]))<=38 and len(str(row[0]).split())<=5)
 terms=list(dict.fromkeys(terms))
 for key in counts:
  for number,sec in enumerate(w[key],1):
   # Unwrap only groups created by this formatter on a previous run.
   sec['blocks']=[child for b in sec['blocks'] for child in ([child for cell in b['cells'] for child in cell] if b.get('programme_definition_row') else [b])]
   heading='';pair=0;explanation_number=0
   for b in walk(sec['blocks']):
    if b['type']=='table' and b.get('headers') and b.get('rows') and b['rows'][0]!=b['headers']:b['rows'].insert(0,b['headers']);fixed_tables+=1
    if b['type'] in ['subheading','heading','title']:
     heading=b.get('text','');pair=0
     if heading.casefold()==sec['title'].casefold():b['presentation']={'kind':'section-label'}
     continue
    if b['type'] not in ['paragraph','step','list','callout']:continue
    text=b.get('text','');f={'kind':'body','paragraphs':paragraph_chunks(text),'emphasis':[term for term in terms if term.casefold() in text.casefold()]}
    if text.isupper() and len(text)<45:f['kind']='eyebrow'
    if b['type']=='callout':f['kind']={'caution':'caution','answer':'example','think':'question','teacher':'note'}.get(b.get('tone'),'concept')
    for prefix,(kind,label) in PREFIXES.items():
     if text.startswith(prefix):f.update(kind=kind,label=label);break
    if re.match(r'^STEP\s*\d',text):f.update(kind='step',label=re.match(r'^STEP\s*\d',text).group().title())
    elif re.match(r'^(RECALL|EXPLAIN|TRACE|DIAGNOSE|TRANSFER|CREATE|DEFEND)\s',text):f['kind']='step'
    elif text.startswith('□'):f['kind']='check'
    elif re.match(r'^\d+\. ',text):f['kind']='step'
    elif text.endswith('?') and len(text)<260 and b['type']=='paragraph':f['kind']='question'
    if key=='teacher' and text.startswith(('INPUT ','PROCESS ','OUTPUT ')):
     label={'INPUT':'1. Input — information entering','PROCESS':'2. Process — the deciding step','OUTPUT':'3. Output — the result'}[text.split()[0]];f.update(kind='definition',label=label)
    if key=='teacher' and sec['title']=='Assess and explain the answers':
     if re.match(r'^W\d+ ',heading):
      pair+=1;f.update(kind='question' if pair==1 else 'example',label=('Workbook question · ' if pair==1 else 'Teacher reasoning · ')+heading.split()[0])
     elif any(word in heading.casefold() for word in ['answer','solution','key','fresh retry']):f.update(kind='example',label='Teacher key · '+heading)
     elif heading in ['Independent question','Assess independent transfer']:f.update(kind='question',label='Independent question · withhold the key')
    if heading in ['The facts we will use','Given facts','Concrete teaching case'] and f['kind']=='body':f.update(kind='example',label='Supplied facts' if heading!='Concrete teaching case' else 'The teaching case')
    if heading=='What this example does not establish':f.update(kind='caution',label='Keep the stated limit')
    if heading in ['Why this result follows','Exact explanation to model']:f.update(kind='example',label='Why the result follows')
    if len(text)>280 and 'label' not in f and not sec.get('graphic_journey'):
     if sec['title'] in ['Explain the mechanism','Explain and model the mechanism']:
      explanation_number+=1;label='Explain '+w['title'] if not heading else heading
      f['label']=f'{label} · {explanation_number}'
     elif sec['title'] in ['Follow a worked example','Study a complete case']:f.update(kind='example',label='Worked explanation · '+w['title'])
     elif sec['title']=='Find and repair a mistake':f.update(kind='caution',label='Check the claim against the facts')
    if text.startswith('I can explain the mechanism.'):
     parts=re.split(r'(?<=\.) (?=I can|Mark each)',text)
     if len(parts)>2:f.update(kind='checklist',items=parts[:-1],tail=parts[-1])
    if text.startswith('Allow 80 minutes:'):f.update(kind='note',label='Alternative compact allocation',context='This compact option is not the full-week schedule. Use the main teaching cycle and allow extra sessions for the investigation, independent work and project.')
    if text.startswith('Ask students to predict before running code.'):
     has_code=any(x['type']=='code' for s in w['sections'] for x in walk(s['blocks']))
     if not has_code:f.update(kind='note',label='For later coding lessons',context='This week has no code block. Use this routine when a later lesson includes an executable lab.')
    assert ' '.join(f['paragraphs'])==text
    b['presentation']=f;counts[key]+=1
   # Preserve response positions: group definition rows only in sections with no response fields.
   if key=='teacher' and not any(b['type']=='response' for b in walk(sec['blocks'])):
    bs=sec['blocks']
    for i in range(len(bs)-2):
     group=bs[i:i+3]
     if [b.get('text','').split(' ',1)[0] for b in group]==['INPUT','PROCESS','OUTPUT']:
      bs[i:i+3]=[{'type':'gallery','cells':[[b] for b in group],'layout':'reading-cards','programme_definition_row':True}];definition_rows+=1;break
   sec['reading_intro']=purpose(w,key,sec,number);sec['reading_design']='approved-programme-format'
   rows.append({'week':w['id'],'audience':key,'section':number,'title':sec['title'],'purpose':sec['reading_intro'],'formatted_blocks':sum(bool(b.get('presentation')) for b in walk(sec['blocks'])),'status':'format checked'})
 w['reading_design']={'edition':'Approved programme reading format','scope':'student, teacher and workbook','approach':'section purposes, heading hierarchy, reading chunks, emphasis, definitions, questions, keys and cautions'}
 # Only explicit table headers may add text; no original cell or explanation is removed.
 after=original_content(w)
 for oldsecs,newsecs in zip(original,after):
  for old,new in zip(oldsecs,newsecs):
   assert old['title']==new['title'] and len(old['blocks'])==len(new['blocks'])
   for oldb,newb in zip(old['blocks'],new['blocks']):
    if oldb['type']=='table' and oldb.get('headers'):
     oldb=copy.deepcopy(oldb)
     if oldb['rows'][0]!=oldb['headers']:oldb['rows'].insert(0,oldb['headers'])
    if oldb!=newb:preservation_errors.append({'week':w['id'],'section':old['title'],'type':oldb['type']})
assert weeks[0]==approved and not preservation_errors,preservation_errors[:5]
D['reading_design']={'status':'approved format applied throughout','lessons':len(weeks),'sections':len(rows),'reference':'ai-1/1','original_text_preserved':True}
P.write_text(json.dumps(D,ensure_ascii=False,indent=2))
previous=json.loads((R/'reports/programme-formatting.json').read_text()) if (R/'reports/programme-formatting.json').exists() else {}
report={'lessons':len(weeks),'newly_formatted_lessons':len(weeks)-1,'sections':len(rows),'formatted_blocks':counts,'restored_table_headers':previous.get('restored_table_headers',0)+fixed_tables,'definition_rows':definition_rows,'approved_week1_sha256':digest(approved),'preservation_errors':preservation_errors,'sections_audited':rows,'scope':'Every section receives source-preserving reading structure. This audit covers format and content retention, not new classroom learning outcomes.'}
(R/'reports/programme-formatting.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print({k:v for k,v in report.items() if k!='sections_audited'})
