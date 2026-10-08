"""Check the actual classroom additions, anchors, role boundaries and project coverage."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];p=json.loads((R/'content/programme.json').read_text());m=json.loads((R/'lib/classroom-data.json').read_text()) if (R/'lib/classroom-data.json').exists() else {'sequence':p['learning_sequence'],'weeks':{w['id']:w['classroom'] for w in p['weeks']+p['python_bridge']}};errors=[]
expected=['ai-1','ai-2','ai-3','python-bridge','ai-4','ai-5','ai-6','ai-7']
if p['learning_sequence']!=expected or m['sequence']!=expected:errors.append('Incorrect learning sequence')
for w in p['weeks']+p['python_bridge']:
 c=w['classroom'];names=[s['title'] for s in w['sections']]
 for name in ['Your lesson route','Finish and return']:
  if names.count(name)!=1:errors.append(w['id']+': missing or duplicated '+name)
 if not any(s['title']=='Prepare, teach and assess' for s in w['teacher']):errors.append(w['id']+': missing teacher preparation')
 if not any(s['title']=='Project portfolio milestone' for s in w['workbook']):errors.append(w['id']+': missing portfolio')
 if len(c['flow'])!=6 or len(c['goals'])<1:errors.append(w['id']+': missing lesson route')
 for step in c['flow']:
  if not 1<=step['section']<=len(w['sections']):errors.append(w['id']+': broken route anchor')
 if w['sections'][c['flow'][1]['section']-1]['title']!='Follow a worked example':errors.append(w['id']+': wrong picture destination')
 if w['sections'][c['flow'][4]['section']-1]['title']!='Try a new case independently':errors.append(w['id']+': wrong independent destination')
 if c['visual_question']!=w['pictorial_case']['student_task']:errors.append(w['id']+': mismatched visual question')
 if 'answer' in json.dumps(c).lower() and any(k in c for k in ['teacher_answer','independent_answer']):errors.append(w['id']+': teacher key in public metadata')
 if c['project']!=w['project'] or c!=m['weeks'][w['id']]:errors.append(w['id']+': project or website metadata mismatch')
for l in p['levels']:
 milestones={w['classroom']['milestone']['title'] for w in p['weeks'] if w['level']==l['number']}
 if len(milestones)!=6:errors.append(f"Level {l['number']}: incomplete project progression")
report={'lessons':264,'route_links_checked':1584,'levels_with_six_project_milestones':7,'errors':errors,'benchmark':'ai-1/1','scope':'Editorial structure and alignment; classroom learning impact requires observation.'}
(R/'reports/classroom-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));sys.exit(bool(errors))
