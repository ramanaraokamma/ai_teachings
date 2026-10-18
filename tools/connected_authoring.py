"""Shared mechanics for individually authored weekly reading plans.
Content sequences, illustrations, runnable labs and teacher modelling are supplied
by each week's author. Common reference and record pages retain stable positions.
"""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
def g(title,indices,kind='text',collapsed=False,note=None):
 return {'title':title,'kind':kind,'indices':indices,**({'collapsed':True} if collapsed else {}),**({'note':note} if note else {})}
class Author:
 def __init__(self,week):
  self.path=ROOT/'content/programme.json';self.data=json.loads(self.path.read_text());self.w=next(w for w in self.data['weeks']+self.data['python_bridge'] if w['id']==week)
  if self.w['sections'][0].get('reading_flow'):raise ValueError(f'{week} already authored')
  self.original=copy.deepcopy(self.w);self.changes=[];self.tag='connected-reading-'+week.replace('/','-')
 def add(self,role,n,text=None,image=None,label=None):
  b=copy.deepcopy(image) if image else {'type':'paragraph','text':text,'presentation':{'kind':'body','paragraphs':[text],'emphasis':[]}}
  if b.get('type')=='table' and b.get('headers'):
   headers=b.pop('headers')
   if not b.get('rows') or b['rows'][0]!=headers:b['rows']=[headers]+b.get('rows',[])
  if label:b.setdefault('presentation',{})['label']=label
  b['reading_addition']=self.tag;self.w[role][n-1]['blocks'].append(b);return len(self.w[role][n-1]['blocks'])-1
 def pic(self,n):return next(b for b in self.w['sections'][-1]['blocks'] if b.get('src','').endswith(f"academy-story-{self.w['id'].replace('/','-')}-{n:02}"))
 def find(self,role,n,prefix):return next(i for i,b in enumerate(self.w[role][n-1]['blocks']) if b.get('text','').startswith(prefix))
 def design(self,role,n,title,purpose,groups,optional=False):
  s=self.w[role][n-1];used=[i for z in groups for i in z['indices']];assert len(used)==len(set(used)),(role,n,'duplicate index')
  rest=[i for i in range(len(s['blocks'])) if i not in used]
  if rest:groups.append(g('Earlier wording, alternatives and picture transcripts',rest,'reference',True))
  s['reading_flow']={'title':title,'purpose':purpose,'optional':optional,'groups':groups};s['reading_intro']=purpose
  assert sorted(i for z in groups for i in z['indices'])==list(range(len(s['blocks']))),(role,n)
 def fix(self,role,n,i,text):
  b=self.w[role][n-1]['blocks'][i];key='label' if b['type']=='response' else 'text';old=b[key];b[key]=text
  if b.get('presentation',{}).get('paragraphs'):b['presentation']['paragraphs']=[text]
  self.changes.append({'week':self.w['id'],'path':f'/{role}/{n-1}/blocks/{i}/{key}','old':old,'new':text})
 def replace_text(self,old,new):
  """Correct a reviewed factual phrase throughout this week's source records."""
  def visit(node,path=''):
   if isinstance(node,dict):
    changed_text=False
    for key,value in node.items():
     child=path+'/'+key
     if isinstance(value,str) and old in value:
      replacement=value.replace(old,new);node[key]=replacement
      if key=='text':changed_text=True
      if key not in ('paragraphs',):self.changes.append({'week':self.w['id'],'path':child,'old':value,'new':replacement})
     else:visit(value,child)
    if changed_text and node.get('presentation',{}).get('paragraphs'):node['presentation']['paragraphs']=[node['text']]
   elif isinstance(node,list):
    for i,value in enumerate(node):
     if isinstance(value,str) and old in value:
      replacement=value.replace(old,new);node[i]=replacement
      self.changes.append({'week':self.w['id'],'path':path+'/'+str(i),'old':value,'new':replacement})
     else:visit(value,path+'/'+str(i))
  visit(self.w)
 def comparisons(self,title,purpose):
  cells=[[copy.deepcopy(self.w['sections'][3]['blocks'][3+i]),copy.deepcopy(self.w['sections'][3]['blocks'][7+i])] for i in range(4)]
  index=self.add('sections',4,image={'type':'gallery','layout':'reading-cards','cells':cells})
  self.design('sections',4,title,purpose,[g('Pictures paired with their evidence',[index],'cards'),g('Discuss the confusing pair',[12],'prompts'),g('Keep the limit in view',[11],'example')])
 def common(self,case,check,workbook,teacher_lab,wb_extra=None):
  """Author the reviewed shared reference and evidence-record structure."""
  w=self.w;D=self.design;wb_extra=wb_extra or {}
  D('sections',5,'Your quick word guide','Use the words to explain a particular step, record or limit.',[g('Core vocabulary',[7]),g('Terms for the connected explanation',[13]),g('Repair a claim using a word',[9,10],'prompts')],True)
  D('sections',10,'Choose a stronger thinking challenge','Choose the next useful challenge rather than treating the whole ladder as compulsory.',[g('Pick your next step',list(range(4,11)),'prompts')],True)
  D('sections',12,'Reference: check your explanation',f'Use after practice. {case} is the selected independent case.',[g('Check the evidence and its limit',[5,6,7,8,9],'prompts'),g('Record support',[12])],True)
  tables=[i for i,b in enumerate(w['sections'][12]['blocks']) if b['type']=='table']
  D('sections',13,'Extra practice: '+w['sections'][12]['blocks'][12].get('text','a worked case'),'Try the question before opening its worked explanation.',[g('Read the supplied case and question',[3,5],'example'),g('Your explanation',[9,10],'prompts'),g('Check after trying',[7]+tables,'example',True)],True)
  D('sections',15,'Reference: original lesson checklist','Use an additional checklist when it helps inspect your explanation.',[g('Targets and evidence',[1]),g('Keep your route and first prediction',[2,3])],True)
  for role,n in [('sections',17),('workbook',20)]:
   bs=w[role][n-1]['blocks'];tail=[i for i in range(19,len(bs)) if bs[i]['type']!='subheading']
   D(role,n,'Extra practice: pictures, repair and feedback','Attempt each question before opening its explanation. Use one browser or paper copy.',[g('First supported question',list(range(1,10)),'prompts'),g('Check the first explanation',[10],'example',True),g('Changed-case question',list(range(11,18)),'prompts'),g('Check the changed case',[18],'example',True),g('Repair and save your work',tail)],True)
  D('sections',18,'Reference: the six-picture journey','Revisit the picture that serves the current question; key diagrams already sit beside the main explanation.',[g(w['sections'][17]['blocks'][4*i]['text'],list(range(4*i+1,4*i+4))) for i in range(6)],True)
  bs=w['teacher'][0]['blocks'];pre=self.find('teacher',1,'Preparation for the connected explanation');ready=self.find('teacher',1,'Readiness answer');end=self.find('teacher',1,'End goal for the pictorial case');prepare=self.find('teacher',1,'Prepare the class')
  recall=[i for i in range(5,prepare) if bs[i]['type']=='paragraph' and (bs[i]['text'].startswith(('Without opening','Look for:','Reference example')))]
  D('teacher',1,'Prepare this connected week','Use one main plan and keep practice separate from the independent first attempt.',[g('Learning goal and precision',[1,pre+1,end+1]),g('What to prepare',[prepare+1]+list(range(ready+2,end)),'prompts'),g('Main teaching plan',[2,3]),g('Opening retrieval and readiness',recall+[ready+1],'example')])
  D('teacher',3,'Guide the reasoning, then remove help','Collect a response from each learner before discussing the worked key.',[g('Prompt before revealing',[16],'example'),g('Expected reasoning and fading help',[17,18]),g('Check the misconception before discussion',[20,21,22],'example'),g('Use the pictorial check',[24,26,27,28]),g('Keep each learner explaining',[7,8,10],'prompts')])
  ti=self.add('teacher',4,teacher_lab)
  D('teacher',4,'Run the supplied investigation','Keep expected results, observed paper traces and remaining limits distinguishable.',[g('Supplied materials and answer guidance',[ti],'example'),g('Run and record',[3,4,5,6],'steps'),g('Keep an inspectable record',[10]),g('Diagnose the first misunderstanding',[15,16,17],'cards'),g('Choose support from the response',[19,20])])
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
  self.fix('teacher',4,9,f'Use the supplied investigation for shared practice. Keep predictions and observed paper-trace results separate. Reserve {case} for the individual first attempt before feedback; do not use the reserved case as a paired lab task.')
  self.fix('teacher',3,5,f'Use the earlier changed question as optional later practice. Reserve {case} for the first independent attempt before hints or feedback.')
  self.fix('teacher',5,3,'Additional transfer practice question');self.fix('teacher',5,5,'Reasoned practice answer')
  self.fix('workbook',7,1,'My practice answer and reason');self.fix('workbook',11,1,'My explanation after practice')
  self.fix('sections',12,1,'Checklist for explaining this week’s idea');self.fix('sections',12,2,f'Use after practice. {case} is the selected independent case.');self.fix('sections',12,4,'EXPLANATION CHECK  '+check)
 def finish(self,overviews):
  for role,(title,lead,outcome,order,route) in overviews.items():self.w[role][0]['reading_flow']['overview']={'title':title,'lead':lead,'outcome':outcome,'order':order,'route':[{'label':label,'section':n} for label,n in route]}
  for role in ('sections','teacher','workbook'):
   for si,(before,after) in enumerate(zip(self.original[role],self.w[role])):
    assert after.get('reading_flow'),(role,si)
    for bi,b in enumerate(before['blocks']):
     actual=after['blocks'][bi]
     if b!=actual:assert any(c['path'].startswith(f'/{role}/{si}/blocks/{bi}/') for c in self.changes),(role,si,bi)
  self.path.write_text(json.dumps(self.data,ensure_ascii=False,indent=2));p=ROOT/'reports/reviewed-source-corrections.json';ledger=json.loads(p.read_text());ledger['corrections'].extend(self.changes);p.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
  n=self.w['week'];report={'lesson':self.w['id'],'sections_reviewed':sum(len(self.w[r]) for r in overviews),'original_blocks_preserved':True,'wording_corrections':self.changes,'roles':{role:{'main_sections':sum(not s['reading_flow']['optional'] for s in self.w[role]),'reference_sections':sum(s['reading_flow']['optional'] for s in self.w[role]),'sections':[{'title':s['reading_flow']['title'],'groups':[g['title'] for g in s['reading_flow']['groups']]} for s in self.w[role]]} for role in overviews}}
  (ROOT/f"reports/{('week'+str(n)) if self.w['id'].split('/')[0]=='ai-1' else self.w['id'].split('/')[0]+'-week'+str(n)}-connected-reading.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Authored',self.w['id'],report['sections_reviewed'],'sections.')
def routes(student,teacher,workbook):
 """Attach individually written summaries to the approved cross-edition route."""
 orders={'sections':[1,2,3,4,6,7,8,9,14,11,16,5,10,12,13,15,17,18],'teacher':list(range(1,10)),'workbook':[1,12,13,14,16,4,9,17,10,2,3,5,6,7,8,11,15,18,19,20,21]}
 steps={'sections':[('Notice',2),('Trace',3),('Compare',6),('Practise',8),('Try alone',14),('Build & reflect',11)],'teacher':[('Prepare',1),('Explain',2),('Guide',3),('Investigate',4),('Assess',5),('Return',6)],'workbook':[('Recall',1),('Trace',12),('Compare',13),('Challenge',14),('Diagnose',16),('Try alone',4)]}
 return {role:(*text,orders[role],steps[role]) for role,text in [('sections',student),('teacher',teacher),('workbook',workbook)]}
