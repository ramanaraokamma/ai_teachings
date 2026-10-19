"""Shared record structure for individually reviewed fifteen-workbook bridge lessons."""
from connected_authoring import Author,g,routes
class BridgeAuthor(Author):
 def comparisons(self,title,purpose):
  self.design('sections',4,title,purpose,[g('Predict the supported change',[1,2],'prompts'),g('Predict the pictured variant',[4],'prompts'),g('Check after predicting',[5,6],'example',True)])
 def references(self,lab,reference):
  D=self.design;w=self.w
  D('sections',5,'Reference · The words used in this procedure','Explain each term using a particular code line.',[g('Vocabulary and response',[0,1])],True)
  D('sections',10,'Extra challenge · Explain, apply and challenge','Choose the next useful task after supported practice.',[g('Choose a challenge',[1,2,3,4],'prompts')],True)
  D('sections',12,'Reference · Inspect your evidence','Use the record after practice rather than revealing the independent answer.',[g('Self-check and explanation',list(range(len(w['sections'][11]['blocks']))),'prompts')],True)
  D('sections',13,'Extra practice · A complete trace','Predict before opening the supplied trace.',[g('Explain the input and procedure',[2,3],'prompts'),g('Check the complete trace',[1],'example',True)],True)
  D('sections',15,'Reference · Earlier route checklist','Keep one main lesson route and use this as a reminder.',[g('Checklist and first prediction',[1,2,3])],True)
  for role,n in [('sections',17),('workbook',14)]:
   bs=w[role][n-1]['blocks'];feedback=[i for i,b in enumerate(bs) if b.get('text','').startswith('After your attempt')];assert len(feedback)==2
   first,second=feedback
   D(role,n,'Extra practice · Predict, check and repair','Use only after an attempt; keep the reserved assessment separate.',[g('First question and hint',list(range(1,first)),'prompts'),g('Check the first explanation',[first],'example',True),g('Changed-case question and hint',list(range(first+1,second)),'prompts'),g('Check the changed explanation',[second],'example',True),g('Repair and keep the record',[i for i in range(second+1,len(bs)) if bs[i]['type']!='subheading'])],True)
  D('sections',18,'Reference · The six-picture journey','Choose the picture needed for the present question.',[g(w['sections'][17]['blocks'][4*i]['text'],list(range(4*i+1,4*i+4))) for i in range(6)],True)
  bs=w['teacher'][0]['blocks'];prep=self.find('teacher',1,'Preparation');prereq=self.find('teacher',1,'Prerequisite answer');end=self.find('teacher',1,'End goal for the pictorial case');out=self.find('teacher',1,'Outcomes')
  D('teacher',1,'Prepare the connected bridge lesson','Check prior exposure and keep execution practice distinct from paper reasoning.',[g('Goal and main plan',[1,2,3,4]),g('Retrieval and prerequisite guidance',list(range(6,out))),g('Materials and readiness',list(range(prep+1,prereq))+[prereq+1]),g('End goal',[end+1])])
  c=self.find('teacher',3,'Completion task:');q=self.find('teacher',3,'Use the worked case for');pq=self.find('teacher',3,'Pictorial practice question');pk=self.find('teacher',3,'Reasoned teacher answer')
  D('teacher',3,'Guide the trace, then fade the help','Collect predictions before execution or feedback.',[g('Main completion task and key',[c,c+1,c+2]),g('Individual misconception check',[q,q+1,q+2]),g('Pictorial question and changed-case key',[pq+1,pk+1,pk+2,pk+3]),g('Support and alternative plan',[1,2,3],'reference',True)])
  key=self.add('teacher',4,lab);bs=w['teacher'][3]['blocks'];support=self.find('teacher',4,'Match the support')
  D('teacher',4,'Run the complete supplied investigation','Preserve expected, observed and paper-trace records.',[g('Supplied case materials and checked guidance',[key]),g('Diagnose misconceptions',list(range(support)),'cards'),g('Choose accessible support',list(range(support+1,key)))])
  selected=self.find('teacher',5,'Selected case:');answer=self.find('teacher',5,'Selected case answer');bs=w['teacher'][4]['blocks'];table=next(i for i in range(answer,len(bs)) if bs[i]['type']=='table');feedback=self.find('teacher',5,'Feedback that the learner uses')
  groups=[g('Selected independent task and checked key',list(range(selected,answer))+[answer+1],'example'),g('Judge trace and support',[table,table+1]),g('Give one repair action',[feedback+1])]
  for number in [1,2,3,5]:
   h=next(i for i,b in enumerate(bs) if b['type']=='subheading' and b.get('text','').startswith('W'+str(number)+' '));stop=next(i for i in range(h+1,len(bs)) if bs[i]['type']=='subheading');groups.append(g(bs[h]['text'],list(range(h+1,stop))))
  D('teacher',5,'Assess the selected bridge transfer task','If a learner has seen this exact case, use a fresh parallel input and record exposure/support.',groups)
  ik=self.add('teacher',6,'Selected independent answer: '+w['method']['independent']['answer']+' Keep earlier W4 transfer as additional practice; do not substitute its numbers or key for this selected task. Record prior exposure and use a fresh parallel case after support.')
  D('teacher',6,'Keep the portfolio, support and delayed check','Track code execution separately from a correct paper trace.',[g('Project evidence',[0,10]),g('Support and selected assessment guidance',[1,ik]),g('Delayed return',[5,6,7,8]),g('Bridge to the next topic',[2,3])])
  D('teacher',7,'Reference · Alternative planning checklist','Use alongside the main route without repeating the teaching cycle.',[g('Planning and assessment reference',list(range(len(w['teacher'][6]['blocks']))))],True)
  D('teacher',8,'Reference · Feedback and evidence records','Keep individual first attempts separate from supported rehearsal.',[g('Feedback and repair',[0,1,2,3,4])],True)
  D('teacher',9,'Reference · Teach with the six pictures','Use the relevant picture for a specific reasoning move.',[g(w['teacher'][8]['blocks'][1+5*i]['text'],list(range(2+5*i,6+5*i))) for i in range(6)],True)
  titles={1:'Recall · Retrieve before notes',2:'Reference · Supported W2 record',3:'Extra practice · Individual reasoning check',4:'Try alone · Selected independent task',5:'W1 · Explain the procedure',6:'W2 · Predict, trace and observe',7:'W3 · Find the first error',8:'Additional practice · Earlier W4 transfer',9:'W5 · State an honest limit',10:'Project · Keep code and evidence',11:'Feedback · Repair and return',12:'Extra practice · Pictured case',13:'Reference · Project portfolio milestone'}
  for n,title in titles.items():
   ix=self.add('workbook',n,reference) if n in [5,6,7,9] else None;indices=([ix] if ix is not None else [])+list(range(len(self.original['workbook'][n-1]['blocks'])))
   D('workbook',n,title,'Keep the stated task, its own code/values and support record together.',[g('Task and evidence record',indices,'prompts')],n in [2,3,8,12,13])
  D('workbook',15,'Reference · Six-picture response sheets','Use the picture relevant to a current gap.',[g(w['workbook'][14]['blocks'][5*i]['text'],list(range(5*i+1,5*i+5))) for i in range(6)],True)
 def finish(self,overviews):
  v=list(overviews['workbook']);main=[1,5,6,7,9,4,10,11];v[3]=main+[i for i in range(1,16) if i not in main];v[4]=[('Recall',1),('Explain',5),('Trace',6),('Repair',7),('Limit',9),('Try alone',4)];overviews['workbook']=tuple(v);super().finish(overviews)
