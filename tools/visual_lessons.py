"""Integrate individually reviewed worked cases without replacing source lessons."""
from pathlib import Path
import copy,json
R=Path(__file__).resolve().parents[1]
def p(text):return {'type':'paragraph','text':text}
def h(text):return {'type':'subheading','text':text}
def r(text,lines=4):return {'type':'response','label':text,'lines':lines}
def stamp(blocks,role):return [dict(copy.deepcopy(b),lesson_upgrade={'role':role,'kind':'agent-reviewed-pictorial-case'}) for b in blocks]
def apply_visual_lessons(programme):
 folder=R/'tools/lesson-upgrades'
 if not (folder/'READY.json').exists():return programme
 weeks=programme['weeks']+programme['python_bridge'];reviews=[];owners={}
 for assignment in (R/'tools/lesson-review-packs').glob('assignment-*.json'):
  for row in json.loads(assignment.read_text()):owners[row['week']]='weekly_lessons_'+assignment.stem.split('-')[-1]
 for w in weeks:
  stem=w['id'].replace('/','-');a=json.loads((folder/(stem+'.json')).read_text());assert a['week']==w['id']
  visual={'type':'image','src':'/api/resource/academy-visual-'+stem,'alt':a['title']+'. '+'. '.join(s['label']+': '+s['detail'] for s in a['steps']),'width':560,'academy_visual':True}
  readable={'type':'diagram','kind':'pathway','title':'Read the picture one step at a time','columns':['Step','What happens and why'],'rows':[[str(i+1)+'. '+s['label'],s['detail']] for i,s in enumerate(a['steps'])],'caption':'Match each pictured step to the supplied facts. This is a worked teaching case, not an independent assessment.'}
  extra=[]
  if a.get('mini_visual'):extra=[{'type':'image','src':'/api/resource/academy-detail-'+stem,'alt':a['mini_visual']['title'],'width':560,'academy_visual':True}]
  worked=[dict(h('A pictorial worked case: '+a['title']),anchor='pictorial-case'),p(a['scenario']),h('The facts we will use')]+[p(x) for x in a['given']]+extra+[visual,readable,h('Why this result follows'),p(a['explanation']),h('What this example does not establish'),p(a['limits'])]
  w['sections'][0]['blocks']+=stamp([h('This week’s end goal'),p(a['outcome'])],'student')
  w['sections'][5]['blocks']+=stamp(worked,'student')
  change=a['counterfactual']
  comparison=[h('Change one thing in the pictured case'),p('Change: '+change['change']),p('Prediction: '+change['prediction']),p('Reason: '+change['reason'])]
  w['sections'][3]['blocks']+=stamp(comparison,'student')
  w['sections'][7]['blocks']+=stamp([h('Explain the picture'),p(a['student_task']),r('My explanation using a pictured step and the given facts'),p('This is supported practice. Keep the separately named independent case for an attempt before feedback.')],'student')
  w['sections'][10]['blocks']+=stamp([h('Evidence for your project'),p(a['project_evidence'])],'student')
  w['teacher'][0]['blocks']+=stamp([h('End goal for the pictorial case'),p(a['outcome']),p('This added worked case illustrates the week’s main idea. Retain all original and connected topics; schedule its practice within the teaching cycle.')],'teacher')
  w['teacher'][1]['blocks']+=stamp(worked+comparison+[h('Ask while showing the picture'),p('Cover the result. Ask learners to name the inputs and predict the next step. Uncover one step, connect the icon to the actual procedure, and explain its evidence. Then change the supplied condition and compare. The picture is a representation; it does not document execution of a real AI model.')],'teacher')
  w['teacher'][2]['blocks']+=stamp([h('Pictorial practice question'),p(a['student_task']),h('Reasoned teacher answer'),p(a['teacher_answer']),p('Changed-case reasoning: '+change['prediction']+' '+change['reason']),p('Collect each learner’s explanation before discussion. Use the first missing connection between input, deciding step and result to choose support. This question is worked-case practice, not fresh mastery evidence.')],'teacher')
  w['teacher'][5]['blocks']+=stamp([h('Project evidence from this case'),p(a['project_evidence'])],'teacher')
  w['workbook'].append({'title':'Pictorial case practice: '+a['title'],'blocks':stamp([p(a['scenario'])]+[p(x) for x in a['given']]+extra+[visual,p(a['student_task']),r('My picture-based explanation and changed-case prediction',6),p('Support used: alone / hint / worked example. This record is practice evidence.'),p('Project connection: '+a['project_evidence'])],'workbook')})
  w['pictorial_case']=a
  reviews.append({'week':w['id'],'title':a['title'],'outcome':a['outcome'],'visual':'assets/academy-visual-'+stem+'.png','review_note':a['review_note'],'owner':owners[w['id']],'steps':len(a['steps'])})
 programme['pictorial_case_design']={'lessons':len(reviews),'method':'One assigned lesson agent reviews each week; topic-specific worked cases, vector pictorial traces, changed conditions, answer keys and project evidence.','scope':'Editorial design and consistency checks; no claim of classroom learning impact.'}
 (R/'reports/pictorial-case-review.json').write_text(json.dumps(reviews,indent=2))
 return programme
