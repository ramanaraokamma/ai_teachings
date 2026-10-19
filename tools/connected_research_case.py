"""Shared reading layout for individually authored research cases; no content generator."""
from connected_research_authoring import ResearchAuthor,g,routes
from connected_paragraphs import format_additions
from connected_typography import space_additions

def present_case(a, *, headline, purpose, intro, contract, ledger, picture, picture_table, probes, investigation, teacher_key, reference, independent, image=None, code=None):
 D=a.design;ready=a.find('sections',1,'Retrieve what you already know');end=a.find('sections',1,'This week’s end goal')
 D('sections',1,headline,purpose,[g('Learning goals',[1,2,3]),g('Retrieve before reading',[i for i in range(5,ready) if a.w['sections'][0]['blocks'][i].get('text','').startswith(('Close your','Without opening','After trying'))]),g('Starting explanation',[ready+1,ready+2],'prompts'),g('End goal',[end+1])])
 opening=a.add('sections',2,intro);rules=a.add('sections',2,image={'type':'table','rows':contract})
 D('sections',2,'Understand the question and evidence contract',purpose,[g('Start with the research problem',[opening]),g('Original concept explanation',[0]),g('Complete case inputs, rules and limits',[rules],'example'),g('Name given and missing evidence',[2],'prompts')])
 trace=a.add('sections',3,image={'type':'table','rows':ledger})
 D('sections',3,'Trace the complete main case before interpreting it','Follow each evidence-to-conclusion step and retain unknown quantities.',[g('Original declared procedure',[0]),g('Complete main-case evidence ledger',[trace],'example'),g('State the scope and explain the visual',[2,4])])
 D('sections',4,'Predict the changed case before reading the explanation','Keep the rule and evidence boundary visible.',[g('Main task and response',[1,2],'prompts'),g('Predict the pictured change',[4],'prompts'),g('Check after predicting',[5,6],'example',True)])
 # Find the old picture trace rather than assuming optional-code/image offsets.
 bs=a.w['sections'][5]['blocks'];di=next(i for i,b in enumerate(bs) if b.get('type')=='diagram' and b.get('title')=='Read the picture one step at a time')
 facts=next(i for i,b in enumerate(bs) if b.get('text')=='The facts we will use')+1
 pi=next(i for i,b in enumerate(bs) if b.get('anchor')=='pictorial-case')+1
 pic=a.add('sections',6,image=a.pic(2));changed=a.add('sections',6,image=a.pic(4));scope=a.add('sections',6,picture);pt=a.add('sections',6,image={'type':'table','rows':picture_table})
 native=[a.add('sections',6,image=image)] if image else []
 D('sections',6,'Connect the main result with the separate pictured case','Keep the two scenarios and their supplied evidence distinct.',[g('Main case and original checked reasoning',[0,1,2]),g('Separate pictured inputs and complete explanation',[pi,facts,scope]),g('Read the labelled representation',native+[pic,di,di+2]),g('Complete picture evidence and limits',[pt],'example'),g('Predict the changed condition',[di+6],'prompts'),g('Check after predicting',[changed],'example',True),g('Explain what remains unknown',[di+4,di+5],'prompts')])
 audit=a.add('sections',7,image={'type':'table','rows':probes})
 D('sections',7,'Find the first unsupported inference and repair it','Use the supplied conditions rather than inventing missing evidence.',[g('Original qualification and repair setup',[0,1]),g('Complete boundary and misconception probes',[audit],'example'),g('Write and justify the repair',[2,4,5],'prompts')])
 D('sections',8,'Practise the mechanism with progressively less help','Keep the selected independent case for a first attempt.',[g('Shared explanation',[0,1,2],'prompts'),g('Supported workbook trace',[4,5,6]),g('Individual scope check',[8,9],'prompts'),g('Picture response',[11,12],'prompts'),g('Reserve the independent task',[13])])
 instructions=a.add('sections',9,investigation);newcode=[a.add('sections',9,image=code)] if code else []
 old=a.original['sections'][8]['blocks'];records=[i for i,b in enumerate(old) if b['type']=='table'];notes=[i for i,b in enumerate(old) if b['type']=='paragraph' and i!=1]
 D('sections',9,'Investigate, record the evidence and check the limits','Distinguish a prediction, a paper trace and an actual local execution.',[g('Current investigation',[1]),g('Complete investigation instructions',newcode+[instructions],'steps'),g('Evidence record and reflection',records+notes)])
 D('sections',11,'Save the research artifact and unresolved conditions','Keep supplied evidence, proposed revisions and actual work distinct.',[g('Project task and artifact',[0,1]),g('Evidence and limitations',[3])])
 D('sections',14,'Try the selected new case independently',independent,[g('Complete independent task',[1],'example'),g('First attempt and support record',[2,3]),g('Feedback after trying',[9])])
 D('sections',16,'Retrieve the mechanism and state the evidence boundary','Explain what follows and what would require new evidence.',[g('Retrieve and explain',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
 tb=a.w['teacher'][1]['blocks'];td=next(i for i,b in enumerate(tb) if b.get('type')=='diagram' and b.get('title')=='Read the picture one step at a time');tf=next(i for i,b in enumerate(tb) if b.get('text')=='The facts we will use')+1;ti=next(i for i,b in enumerate(tb) if b.get('anchor')=='pictorial-case')+1
 cr=a.add('teacher',2,image=a.w['sections'][1]['blocks'][rules]);tr=a.add('teacher',2,image=a.w['sections'][2]['blocks'][trace]);ar=a.add('teacher',2,image=a.w['sections'][6]['blocks'][audit]);ex=a.add('teacher',2,picture);ptr=a.add('teacher',2,image=a.w['sections'][5]['blocks'][pt]);key=a.add('teacher',2,teacher_key);tpi=a.add('teacher',2,image=a.pic(2));tn=[a.add('teacher',2,image=image)] if image else []
 D('teacher',2,'Model the whole case and check each inference','Keep the independent answer private until after the first attempt.',[g('Definitions and complete contract',[0,2,cr]),g('Main evidence ledger and checked key',[tr,key,5,6,9,10,11]),g('Boundary and misconception probes',[ar],'example'),g('Separate pictured facts and full reasoning',[ti,tf,ex,ptr]+tn),g('Picture trace and changed-condition key',[tpi,td,td+2,td+4,td+6,td+7,td+8])])
 a.references('the selected independent research case',teacher_key,reference)
 wt=a.add('workbook',6,image=a.w['sections'][2]['blocks'][trace]);a.w['workbook'][5]['reading_flow']['groups'][0]['indices'].insert(0,wt)
 if image:
  wi=a.add('workbook',12,image=image);a.w['workbook'][11]['reading_flow']['groups'][0]['indices'].insert(0,wi)
 space_additions(a);format_additions(a)
 a.finish(routes((headline,purpose,'Question and contract → complete main ledger → separate picture → boundary probes → investigation → independent attempt.'),('Teach the evidence-to-conclusion chain for '+a.w['title'],purpose,'Model the main case → reveal the picture gradually → probe limits → assess independent reasoning → plan a changed-case return.'),('One complete research-case evidence record.',purpose,'Recall → W1–W3/W5 → independent case → project evidence → feedback and delayed return.')))
