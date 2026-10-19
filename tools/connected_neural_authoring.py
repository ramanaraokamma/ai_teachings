"""Reference and record layout for individually reviewed compact neural lessons."""
from connected_level_authoring import LevelAuthor,g,routes
class NeuralAuthor(LevelAuthor):
 def references(self,case,lab,reference):
  D=self.design;w=self.w
  assert len(w['sections'])==18 and len(w['teacher'])==9 and len(w['workbook'])==15
  D('sections',5,'Reference · Use the mathematical words precisely','Connect each term to a value or step in the current example.',[g('Vocabulary and your explanation',list(range(len(w['sections'][4]['blocks']))))],True)
  D('sections',10,'Extra challenge · Explain a stronger case','Choose the next challenge after the main route.',[g('Explain,repair and extend',list(range(len(w['sections'][9]['blocks']))),'prompts')],True)
  D('sections',12,'Reference · Check the representation and its limits','Use after practice;reserve '+case+' for the first individual attempt.',[g('Current explanation and response',list(range(len(w['sections'][11]['blocks']))),'prompts')],True)
  D('sections',13,'Extra practice · Revisit the complete trace','Predict before reading the supplied steps.',[g('Complete trace and evidence',list(range(len(w['sections'][12]['blocks']))),'example')],True)
  D('sections',15,'Reference · The earlier route checklist','Use one main route rather than repeating the lesson.',[g('Targets,route and first prediction',list(range(len(w['sections'][14]['blocks']))))],True)
  for role,n in [('sections',17),('workbook',14)]:
   bs=w[role][n-1]['blocks'];feedback=[i for i,b in enumerate(bs) if b.get('text','').startswith('After your attempt')];assert len(feedback)==2
   first,second=feedback
   D(role,n,'Extra practice · Predict,check and repair','Keep supported feedback separate from the independent case.',[g('First supported question and optional hint',list(range(1,first)),'prompts'),g('Check after the first attempt',[first],'example',True),g('Changed-case question and optional hint',list(range(first+1,second)),'prompts'),g('Check after the changed attempt',[second],'example',True),g('Repair and retain the record',[i for i in range(second+1,len(bs)) if bs[i]['type']!='subheading'])],True)
  D('sections',18,'Reference · Six-picture concept journey','Choose the picture that supports the current explanation.',[g(w['sections'][17]['blocks'][4*i]['text'],list(range(4*i+1,4*i+4))) for i in range(6)],True)
  bs=w['teacher'][0]['blocks'];ready=self.find('teacher',1,'Prerequisite answer');end=self.find('teacher',1,'End goal for the pictorial case');prep=self.find('teacher',1,'Preparation');recall=[i for i,b in enumerate(bs) if b.get('text','').startswith(('Without opening','Look for:','Reference example'))]
  D('teacher',1,'Prepare the connected mathematical investigation','Keep explanation,shared practice and independent evidence distinct.',[g('Target and main teaching plan',[1,2,3]),g('Preparation and prerequisite',list(range(prep+1,ready))+[ready+1]),g('Opening retrieval',recall),g('Pictured end goal',[end+1])])
  c=self.find('teacher',3,'Completion task:');q=self.find('teacher',3,'Use the worked case for');pq=self.find('teacher',3,'Pictorial practice question');pk=self.find('teacher',3,'Reasoned teacher answer')
  D('teacher',3,'Model a step,then remove help','Collect each learner’s reasoning before showing a key.',[g('Current completion task and checked reasoning',[c,c+1,c+2]),g('Individual misconception check',[q,q+1,q+2]),g('Pictured reasoning and changed case',[pq+1,pk+1,pk+2,pk+3]),g('Accessible support and extension',[1,2])])
  ti=self.add('teacher',4,lab);support=self.find('teacher',4,'Match the support to the first error')
  D('teacher',4,'Run the complete supplied investigation','Separate predictions,actual runs and paper traces.',[g('Complete inputs,expected results and limits',[ti]),g('Diagnose the current misconceptions',list(range(support))),g('Choose accessible support',list(range(support+1,ti)))])
  bs=w['teacher'][4]['blocks'];sel=self.find('teacher',5,'Selected case:');answer=self.find('teacher',5,'Selected case answer');rubric=next(i for i in range(answer,len(bs)) if bs[i]['type']=='table');feedback=self.find('teacher',5,'Feedback that the learner uses')
  groups=[g('Selected independent task and checked answer',[sel,answer+1],'example'),g('Judge explanation,trace and limits',[rubric,rubric+1]),g('Give one usable repair',[feedback+1])]
  for number in [1,2,3,5]:
   h=next(i for i,b in enumerate(bs) if b['type']=='subheading' and b.get('text','').startswith('W'+str(number)+' '));stop=next(i for i in range(h+1,len(bs)) if bs[i]['type']=='subheading');groups.append(g(bs[h]['text'],list(range(h+1,stop))))
  D('teacher',5,'Assess the new schema or calculation transfer','Keep the selected answer private until after a first attempt.',groups)
  delay=self.find('teacher',6,'Plan the delayed return');project=self.find('teacher',6,'Project evidence from this case')
  D('teacher',6,'Connect,support and revisit the mathematics','Use the saved evidence to choose the next step.',[g('Project and next-week bridge',[0,1,2,3,project+1]),g('Delayed return and support record',list(range(delay+1,project)))])
  D('teacher',7,'Reference · Alternative planning checklist','Use alongside the main route when helpful.',[g('Planning,assessment and project reminders',list(range(len(w['teacher'][6]['blocks']))))],True)
  D('teacher',8,'Reference · Feedback,labs and repair paths','Retain the first attempt and the evidence used for a repair.',[g('Feedback and record guidance',list(range(len(w['teacher'][7]['blocks']))))],True)
  D('teacher',9,'Reference · Teach with the six pictures','Choose one picture for a particular reasoning move.',[g(w['teacher'][8]['blocks'][1+5*i]['text'],list(range(2+5*i,6+5*i))) for i in range(6)],True)
  titles={1:'Recall · Retrieve before notes',2:'Reference · Supported W2 record',3:'Extra practice · Individual reasoning check',4:'Try alone · Selected transfer',5:'W1 · Explain the current example',6:'W2 · Trace the calculation',7:'W3 · Repair a misconception',8:'Reference · Earlier W4 response copy',9:'W5 · Explain the limitation',10:'Project · Keep the mathematical evidence',11:'Feedback · Repair and return',12:'Extra practice · Pictured case',13:'Reference · Project milestone'}
  for n,title in titles.items():
   extra=[self.add('workbook',n,reference)] if n in [5,6,7,9] else []
   D('workbook',n,title,'Keep this task’s inputs,rule and response together.',[g('Complete task and evidence',extra+list(range(len(self.original['workbook'][n-1]['blocks']))),'prompts')],n in [2,3,8,12,13])
  D('workbook',15,'Reference · Six-picture response sheets','Choose the picture that helps explain the current step.',[g(w['workbook'][14]['blocks'][5*i]['text'],list(range(5*i+1,5*i+5))) for i in range(6)],True)
 def finish(self,overviews):
  v=list(overviews['workbook']);v[3]=[1,5,6,7,9,4,10,11,2,3,8,12,13,14,15];v[4]=[('Recall',1),('Explain',5),('Trace',6),('Repair',7),('Try alone',4),('Project',10)];overviews['workbook']=tuple(v)
  super().finish(overviews)
