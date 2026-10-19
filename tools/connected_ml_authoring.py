"""Shared reference layout for individually reviewed ML weeks with 21 workbook sections."""
from connected_level_authoring import LevelAuthor,g,routes
import copy
class MLAuthor(LevelAuthor):
 def comparisons(self,title,purpose):
  bs=self.w['sections'][3]['blocks'];cells=[[copy.deepcopy(bs[i]),copy.deepcopy(bs[i+4])] for i in range(3,7)]
  ix=self.add('sections',4,image={'type':'gallery','layout':'reading-cards','cells':cells})
  change=self.find('sections',4,'Change:');D=self.design
  D('sections',4,title,purpose,[g('Four evaluation conditions',[ix],'cards'),g('Keep the claim bounded',[11],'example'),g('Choose a revealing case',[12],'prompts'),g('Predict the supplied changed case',[change],'prompts'),g('Check after predicting',[change+1,change+2],'example',True)])
 def references(self,case,lab,reference,extras=None):
  D=self.design;w=self.w;extras=extras or {};assert len(w['workbook']) in (21,26,31)
  shift=len(w['workbook'])-21
  student_shift=len(w['sections'])-18;teacher_shift=len(w['teacher'])-9
  assert student_shift in (0,1) and teacher_shift in (0,1)
  D('sections',5,'Reference · Words for the current experiment','Tie each word to a particular input, fitted choice or evidence record.',[g('Core vocabulary',[7]),g('Closer-explanation terms',[11])]+[g('Extension vocabulary',[i],'reference',True) for i,b in enumerate(w['sections'][4]['blocks']) if b['type']=='table' and i not in [7,11]],True)
  D('sections',10,'Extra challenge · Build a stronger explanation','Choose the next useful challenge after the main route.',[g('Thinking ladder',[i for i,b in enumerate(w['sections'][9]['blocks']) if i>=4 and b['type'] not in ['subheading','heading']],'prompts')],True)
  D('sections',12,'Reference · Inspect your evidence','Use after practice; keep '+case+' for the individual attempt.',[g('Experiment evidence checklist',list(range(5,12)),'prompts')],True)
  tables=[i for i,b in enumerate(w['sections'][12]['blocks']) if b['type']=='table']
  D('sections',13,'Extra practice · Earlier complete case','Attempt the question before opening its worked explanation.',[g('Situation and question',[3,5]),g('Your explanation',[9,10],'prompts'),g('Check after trying',[7]+tables,'example',True)],True)
  D('sections',15+student_shift,'Reference · Earlier route checklist','Use one main route; revisit the checklist only when useful.',[g('Checklist and first prediction',[1,2,3])],True)
  for role,n in [('sections',17+student_shift),('workbook',20+shift)]:
   bs=w[role][n-1]['blocks'];feedback=[i for i,b in enumerate(bs) if b.get('text','').startswith('After your attempt')]
   if not feedback and len(bs)==4:
    D(role,n,'Extra practice · Explain, repair and return','Use this compact reflection after the main lesson; keep one evidence record.',[g('Reflection and next attempt',list(range(len(bs))),'prompts')],True)
    continue
   assert len(feedback)==2
   first,second=feedback;D(role,n,'Extra practice · Predict, check and repair','Keep supported feedback separate from the reserved independent case.',[g('First supported question and hint',list(range(1,first)),'prompts'),g('Check the first explanation',[first],'example',True),g('Changed-case question and hint',list(range(first+1,second)),'prompts'),g('Check the changed explanation',[second],'example',True),g('Repair and keep the record',[i for i in range(second+1,len(bs)) if bs[i]['type']!='subheading'])],True)
  D('sections',18+student_shift,'Reference · The six-picture journey','Choose the picture needed for the current question.',[g(w['sections'][17+student_shift]['blocks'][4*i]['text'],list(range(4*i+1,4*i+4))) for i in range(6)],True)
  bs=w['teacher'][0]['blocks'];pre=self.find('teacher',1,'Preparation for the connected explanation');ready=self.find('teacher',1,'Readiness answer');prep=self.find('teacher',1,'Prepare the class');end=self.find('teacher',1,'End goal for the pictorial case')
  recall=[i for i in range(5,prep) if bs[i]['type']=='paragraph' and bs[i]['text'].startswith(('Without opening','Look for:','Reference example'))]
  D('teacher',1,'Prepare the connected experiment','Keep prior exposure, shared practice and independent evidence distinct.',[g('Goal and main teaching plan',[1,2,3]),g('Materials and prerequisite',[pre+1,prep+1,ready+1]+list(range(ready+2,end))),g('Opening retrieval',recall),g('End goal',[end+1])])
  c=self.find('teacher',3,'Completion task:');q=self.find('teacher',3,'Use the worked case for');pq=self.find('teacher',3,'Pictorial practice question');pk=self.find('teacher',3,'Reasoned teacher answer');dialog=self.find('teacher',3,'Classroom dialogue')
  D('teacher',3,'Guide the calculation, then remove help','Collect each learner’s prediction before showing its key.',[g('Current completion task and checked key',[c,c+1,c+2]),g('Individual misconception check',[q,q+1,q+2]),g('Pictorial question and changed-case reasoning',[pq+1,pk+1,pk+2,pk+3]),g('Keep each learner explaining',[dialog+1,dialog+2,dialog+4])])
  ti=self.add('teacher',4,lab);mis=self.find('teacher',4,'Address these additional misconceptions');support=self.find('teacher',4,'Match the support to the first error');exmis=next((i for i,b in enumerate(w['teacher'][3]['blocks']) if b.get('text','').startswith('Check these misconceptions')),support)
  D('teacher',4,'Run the complete supplied investigation','Keep predictions, observed or supplied outcomes and unmeasured cases separate.',[g('Supplied inputs and checked guidance',[ti]),g('Predict, investigate and record',[2,3,4,5,6],'steps'),g('Keep the experiment ledger',[9]),g('Diagnose the current misconceptions',list(range(mis+1,exmis)),'cards'),g('Choose accessible support',list(range(support+1,ti)))]+([g('Extension misconceptions',list(range(exmis+1,support)),'reference',True)] if exmis<support else []))
  bs=w['teacher'][4]['blocks'];selected=self.find('teacher',5,'Selected case:');answer=self.find('teacher',5,'Selected case answer');table=next(i for i in range(answer,len(bs)) if bs[i]['type']=='table');feedback=self.find('teacher',5,'Feedback that the learner uses')
  groups=[g('Selected independent task and checked key',list(range(selected,answer))+[answer+1],'example'),g('Judge trace, scope and support',[table,table+1]),g('Give one repair action',[feedback+1])]
  for number in [1,2,3,5]:
   h=next(i for i,b in enumerate(bs) if b['type']=='subheading' and b.get('text','').startswith('W'+str(number)+' '));stop=next(i for i in range(h+1,len(bs)) if bs[i]['type']=='subheading');groups.append(g(bs[h]['text'],list(range(h+1,stop))))
  D('teacher',5,'Assess the selected experiment transfer','Keep this key until after a first attempt; record any help and prior exposure.',groups)
  delay=self.find('teacher',6,'Plan the delayed return');project=self.find('teacher',6,'Project evidence from this case')
  D('teacher',6,'Connect, support and revisit the experiment','Retain failures and assess a fresh parallel case after help.',[g('Project evidence',[2,3,project+1]),g('Support and selected reassessment',[5,11,12]),g('Delayed return',list(range(delay+1,project))),g('Bridge and reflection',[7,9,13])])
  D('teacher',7+teacher_shift,'Reference · Alternative planning checklist','Use alongside the main route without repeating the whole cycle.',[g('Planning and assessment reference',list(range(len(w['teacher'][6+teacher_shift]['blocks']))))],True)
  D('teacher',8+teacher_shift,'Reference · Feedback and evidence records','Keep supported rehearsal separate from independent performance.',[g('Record and repair',[0,1,3,4])],True)
  D('teacher',9+teacher_shift,'Reference · Teach with the six pictures','Choose one picture for a specific reasoning move.',[g(w['teacher'][8+teacher_shift]['blocks'][1+5*i]['text'],list(range(2+5*i,6+5*i))) for i in range(6)],True)
  titles={1:'Recall · Retrieve before notes',2:'Reference · Supported W2 record',3:'Extra practice · Individual reasoning check',4:'Try alone · Selected experiment task',5:'Reference · Earlier learning target',6:'Extra practice · Earlier complete case',7:'Extra practice · Changed case',8:'Extra practice · Design a revealing test',9:'Project · Keep the experiment evidence',10:'Finish · Judge your evidence',11:'Extra practice · Earlier transfer',12:'W1 · Explain the mechanism',13:'W2 · Trace the current experiment',14:'W3 · Repair the reasoning',15:'Reference · Earlier W4 record',16:'W5 · Plan the next check',17+shift:'Feedback · Repair and return',18+shift:'Extra practice · Pictured case',19+shift:'Reference · Project portfolio milestone'}
  for n,title in titles.items():
   ref=[self.add('workbook',n,reference)] if n in [12,13,14,16] else [];indices=extras.get(n,[])+ref+list(range(len(self.original['workbook'][n-1]['blocks'])))
   D('workbook',n,title,'Keep this task’s complete inputs, stated rule and support record together.',[g('Task and evidence record',indices,'prompts')],n in [2,3,5,6,7,8,11,15,18+shift,19+shift])
  D('workbook',21+shift,'Reference · Six-picture response sheets','Choose the relevant picture instead of repeating every task.',[g(w['workbook'][20+shift]['blocks'][5*i]['text'],list(range(5*i+1,5*i+5))) for i in range(6)],True)
  if shift:
   for n in range(17,17+shift):
    D('workbook',n,'Extension · '+w['workbook'][n-1]['title'],'Retained extension task with its own values and teacher key.',[g('Extension question and evidence',list(range(len(self.original['workbook'][n-1]['blocks']))),'prompts')],True)
   # Name retained extension teacher material instead of burying it in a generic bank.
   for role,n,title,prefix in [('teacher',3,'Extension teaching cycles','Connected teaching cycle:'),('teacher',6,'Extension support and reassessment','Readiness and reassessment for')]:
    section=w[role][n-1];start=next((i for i,b in enumerate(section['blocks']) if b.get('text','').startswith(prefix)),None)
    if start is not None:
     bank=section['reading_flow']['groups'][-1];assert bank['title']=='Earlier wording, alternatives and picture transcripts'
     stop=self.find('teacher',3,'Pictorial practice question') if n==3 else self.find('teacher',6,'Plan the delayed return')
     selected=[i for i in bank['indices'] if start<=i<stop]
     if selected:
      bank['indices']=[i for i in bank['indices'] if i not in selected];section['reading_flow']['groups'].append(g(title,selected,'reference',True))
   bs=w['teacher'][4]['blocks'];topics=[t['title'] for t in w['method'].get('connected_topics',[])]
   start=next((i for i,b in enumerate(bs) if b['type']=='subheading' and any(b.get('text','').startswith(t+' —') for t in topics)),None)
   if start is not None:
    section=w['teacher'][4];bank=section['reading_flow']['groups'][-1];selected=[i for i in bank['indices'] if start<=i<self.find('teacher',5,'Selected case:')-1]
    if selected:
     bank['indices']=[i for i in bank['indices'] if i not in selected];section['reading_flow']['groups'].append(g('Extension questions and checked keys',selected,'reference',True))
  self.fix('teacher',4,8,'Use the supplied complete investigation for shared practice. Reserve '+case+' for the individual first attempt before hints or feedback; earlier transfer questions remain additional practice.')
  self.fix('teacher',3,self.find('teacher',3,'Keep for an independent attempt:'),'Use the earlier transfer question as additional practice. Reserve '+case+' for the first individual attempt and record support used.')
  self.fix('teacher',5,3,'Additional transfer practice question');self.fix('teacher',5,5,'Reasoned practice answer')

 def finish(self,overviews):
  count=len(self.w['workbook'])
  if count>21:
   v=list(overviews['workbook']);main=[1,12,13,14,16,4,9,17+count-21,10];v[3]=main+[i for i in range(1,count+1) if i not in main];overviews['workbook']=tuple(v)
  super().finish(overviews)
