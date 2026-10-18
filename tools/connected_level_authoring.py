"""Level 2 onward: retain the different source layout and code evidence."""
from connected_authoring import Author,g,routes,ROOT
import copy
class LevelAuthor(Author):
 def __init__(self,week):
  super().__init__(week)
  from connected_retrieval import refresh_reviewed_priors
  refresh_reviewed_priors(self)
 def comparisons(self,title,purpose):
  bs=self.w['sections'][3]['blocks']
  labels=['Normal case: predict the result and deciding evidence.','Boundary case: identify the exact limit.','Missing information: name what must be clarified.','Transfer case: explain which procedure still applies.']
  cells=[[copy.deepcopy(bs[i]),{'type':'paragraph','text':label}] for i,label in zip([3,4,6,7],labels)]
  ix=self.add('sections',4,image={'type':'gallery','layout':'reading-cards','cells':cells})
  self.design('sections',4,title,purpose,[g('Four pictures with a purpose',[ix],'cards'),g('Choose a revealing case',[9,10],'prompts'),g('Predict the supplied changed case',[12],'prompts'),g('Check after predicting',[13,14],'example',True)])
 def preserve_replaced_tasks(self,numbers):
  """Keep earlier tasks with their saved responses; new tasks get new keys."""
  fresh={}
  for n in numbers:
   section=self.w['workbook'][n-1];original=self.original['workbook'][n-1]['blocks'];prompt=copy.deepcopy(section['blocks'][0]);flow=copy.deepcopy(section['reading_flow'])
   self.fix('workbook',n,0,original[0]['text'])
   question=self.add('workbook',n,image=prompt)
   response=copy.deepcopy(next(b for b in original if b['type']=='response'));response.pop('id',None);response['label']='My while-loop reasoning and evidence'
   answer=self.add('workbook',n,image=response);prior=list(range(len(original)));extra=[i for group in flow['groups'] for i in group['indices'] if i not in prior]
   self.design('workbook',n,flow['title'],flow['purpose'],[g('Current while-loop task and answer',extra+[question,answer],'prompts'),g('Earlier for-loop task and saved response',prior,'reference',True)])
   fresh[n]=question
  return fresh
 def common(self,case,check,workbook,teacher_lab,wb_extra=None):
  """Author the reviewed shared reference and evidence-record structure."""
  w=self.w;D=self.design;wb_extra=wb_extra or {}
  D('sections',5,'Your quick word guide','Use the words to explain a particular step, record or limit.',[g('Core vocabulary',[7]),g('Terms for the connected explanation',[9])],True)
  D('sections',10,'Choose a stronger thinking challenge','Choose the next useful challenge rather than treating the whole ladder as compulsory.',[g('Pick your next step',list(range(4,11)),'prompts')],True)
  D('sections',12,'Reference: check your explanation',f'Use after practice. {case} is the selected independent case.',[g('Check the evidence and its limit',[5,6,7,8,9],'prompts'),g('Self-check and record',[11])],True)
  tables=[i for i,b in enumerate(w['sections'][12]['blocks']) if b['type']=='table']
  D('sections',13,'Extra practice: '+w['sections'][12]['blocks'][12].get('text','a worked case'),'Try the question before opening its worked explanation.',[g('Read the supplied case and question',[3,5],'example'),g('Your explanation',[9,10],'prompts'),g('Check after trying',[7]+tables,'example',True)],True)
  D('sections',15,'Reference: original lesson checklist','Use an additional checklist when it helps inspect your explanation.',[g('Targets and evidence',[1]),g('Keep your route and first prediction',[2,3])],True)
  for role,n in [('sections',17),('workbook',20)]:
   bs=w[role][n-1]['blocks'];tail=[i for i in range(19,len(bs)) if bs[i]['type']!='subheading']
   D(role,n,'Extra practice: pictures, repair and feedback','Attempt each question before opening its explanation. Use one browser or paper copy.',[g('First supported question',list(range(1,10)),'prompts'),g('Check the first explanation',[10],'example',True),g('Changed-case question',list(range(11,18)),'prompts'),g('Check the changed case',[18],'example',True),g('Repair and save your work',tail)],True)
  D('sections',18,'Reference: the six-picture journey','Revisit the picture that serves the current question; key diagrams already sit beside the main explanation.',[g(w['sections'][17]['blocks'][4*i]['text'],list(range(4*i+1,4*i+4))) for i in range(6)],True)
  bs=w['teacher'][0]['blocks'];pre=self.find('teacher',1,'Preparation for the connected explanation');ready=self.find('teacher',1,'Readiness answer');end=self.find('teacher',1,'End goal for the pictorial case');prepare=self.find('teacher',1,'Prepare the class')
  recall=[i for i in range(5,prepare) if bs[i]['type']=='paragraph' and (bs[i]['text'].startswith(('Without opening','Look for:','Reference example')))]
  D('teacher',1,'Prepare this connected week','Use one main plan and keep practice separate from the independent first attempt.',[g('Learning goal and precision',[1,pre+1,end+1]),g('What to prepare',[prepare+1]+([4] if bs[4].get('text','').startswith('Case exposure check:') else [])+list(range(ready+2,end)),'prompts'),g('Main teaching plan',[2,3]),g('Opening retrieval and readiness',recall+[ready+1],'example')])
  D('teacher',3,'Guide the reasoning, then remove help','Collect a response from each learner before discussing the worked key.',[g('Prompt before revealing',[16],'example'),g('Expected reasoning and fading help',[17,18]),g('Check the misconception before discussion',[20,21,22],'example'),g('Use the pictorial check',[24,26,27,28]),g('Keep each learner explaining',[self.find('teacher',3,'Classroom dialogue')+i for i in [1,2,4]],'prompts')])
  ti=self.add('teacher',4,teacher_lab);mis=self.find('teacher',4,'Address these additional misconceptions');support=self.find('teacher',4,'Match the support to the first error')
  D('teacher',4,'Run the supplied investigation','Keep expected results, observed paper traces and remaining limits distinguishable.',[g('Supplied materials and answer guidance',[ti],'example'),g('Run and record',[3,4,5,6],'steps'),g('Keep an inspectable record',[9]),g('Diagnose the first misunderstanding',list(range(mis+1,support)),'cards'),g('Choose support from the response',list(range(support+1,ti)))])
  D('teacher',5,'Assess the selected new case','Keep this key until after the first attempt; accept valid alternatives with defensible reasoning.',[g('Selected independent question and key',[31,33],'example'),g('Judge explanation, trace and limits',[34,35]),g('Give one usable repair action',[37])]+[g(w['teacher'][4]['blocks'][i-1]['text'],[i,i+1],'example') for i in [16,19,22,28]])
  D('teacher',6,'Connect, adapt and return','Retain the project evidence and revisit the reasoning on a changed case.',[g('Project evidence to keep',[2,3,20]),g('Support while preserving the reasoning goal',[5,11,12]),g('Plan the delayed check',[15,16,17,18]),g('Bridge to next week',[7,9,13])])
  D('teacher',7,'Reference: alternative planning checklist','Use as a reminder alongside the main route rather than teaching the cycle twice.',[g('Preparation and schedule',[0,1,2]),g('Practice and assessment reminders',list(range(3,13)))],True)
  D('teacher',8,'Reference: feedback and records','Use digital tools where they help retain an explanation and its evidence.',[g('Keep practice and independent evidence separate',[0,1]),g('Repair and portfolio records',[3,4])],True)
  D('teacher',9,'Reference: teach with the six pictures','Choose the picture for the teaching move and connect it to the explanation.',[g(w['teacher'][8]['blocks'][1+5*i]['text'],list(range(2+5*i,6+5*i))) for i in range(6)],True)
  # The author supplies a title/purpose for every main task, plus any standalone givens.
  for n,title,purpose in [(1,'Recall: reconnect earlier ideas','Retrieve before opening notes.'),*workbook,(4,'W4 · '+case,'Keep one first attempt before hints or feedback.'),(9,'Project · Keep the decision and its evidence','Add this week’s change to your existing project record.'),(17,'Feedback · Repair and return','Keep the first attempt, the repair and a changed-case return.'),(10,'Finish · Judge the evidence in your work','Point to work that supports your confidence level.')]:
   if n==1:groups=[g('Retrieve and explain',[i for i,b in enumerate(w['workbook'][0]['blocks']) if b['type']!='subheading'],'prompts')]
   elif n==4:groups=[g('Read and explain independently',wb_extra.get(n,[])+[1,2],'example'),g('Keep a fair record',[3])]
   else:groups=[g('Your evidence record',wb_extra.get(n,[])+list(range(len(self.original['workbook'][n-1]['blocks']))),'prompts' if n in [12,13,14,16] else 'text')]
   D('workbook',n,title,purpose,groups)
  refs={2:('Reference · Supported W2 record','This is the same W2 attempt. Keep one response record.'),3:('Extra practice · Repair the explanation','Explain the deciding fact before discussing the answer.'),5:('Reference · Original learning target','Use this target to inspect an explanation.'),6:('Extra practice · A complete case','Try the question before checking the worked explanation.'),7:('Extra practice · A changed case','Keep this practice separate from the reserved independent attempt.'),8:('Extra practice · Design a revealing test','Predict before tracing or testing.'),11:('Reference · Original target response space','This teaching case is practice rather than a fresh assessment.'),15:('Reference · Independent-case response copy','This duplicates W4. Reuse the same first-attempt record.'),18:('Extra practice · Use the worked picture','Keep the explanation and the support you used.'),19:('Reference · Project portfolio record','Extend your main project response when helpful.'),21:('Reference · Six-picture response sheets','Choose the image that helps rather than repeating all six.')}
  for n,(title,purpose) in refs.items():
   bs=w['workbook'][n-1]['blocks'];groups=([g(bs[5*i]['text'],list(range(5*i+1,5*i+5))) for i in range(6)] if n==21 else [g('Use this when helpful',list(range(len(bs))))]);D('workbook',n,title,purpose,groups,True)
  self.fix('teacher',4,8,f'Use the supplied investigation for shared practice. Keep predictions and observed paper-trace results separate. Reserve {case} for the individual first attempt before feedback; do not use the reserved case as a paired lab task.')
  self.fix('teacher',3,self.find('teacher',3,'Keep for an independent attempt:'),f'Use the earlier changed question as optional later practice. Reserve {case} for the first independent attempt before hints or feedback.')
  self.fix('teacher',5,3,'Additional transfer practice question');self.fix('teacher',5,5,'Reasoned practice answer')
  self.fix('workbook',7,1,'My practice answer and reason');self.fix('workbook',11,1,'My explanation after practice')
  self.fix('sections',12,1,'Checklist for explaining this week’s idea');self.fix('sections',12,2,f'Use after practice. {case} is the selected independent case.');self.fix('sections',12,4,'EXPLANATION CHECK  '+check)
