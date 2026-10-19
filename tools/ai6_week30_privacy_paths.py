"""Fictional path review; no accounts, real notes, session secrets or networks."""
from copy import deepcopy
GUIDE='FICTIONAL-RESTRICTED-GUIDE-MARKER'
TRUSTED_ROLES={'learner-1':'student','teacher-1':'teacher'}
GUIDES={'G1':GUIDE}
UNSAFE_QUERY_ONLY_CACHE={'G1':GUIDE}  # deliberately broken path, constructed for inspection

def get_guide(actor,request,route,trace):
 if type(request) is not dict or set(request)!={'resource_id'}:return {'status':'invalid_input'}
 rid=request['resource_id']
 if type(rid) is not str or not rid:return {'status':'invalid_input'}
 if route not in ('direct','cache'):return {'status':'invalid_route'}
 if TRUSTED_ROLES.get(actor)!='teacher':return {'status':'denied'}
 if rid not in GUIDES:return {'status':'review'}
 trace.append({'route':route,'resource_id':rid})
 # Both routes share the same trusted access gate before any content enters context.
 value=GUIDES[rid] if route=='direct' else SAFE_CACHE.get((actor,rid))
 if value is None:return {'status':'review'}
 return {'status':'allowed_fixture','content':value}
SAFE_CACHE={('teacher-1','G1'):GUIDE}

student_trace=[];teacher_trace=[]
student_results=[get_guide('learner-1',{'resource_id':'G1'},route,student_trace) for route in ('direct','cache')]
teacher_results=[get_guide('teacher-1',{'resource_id':'G1'},route,teacher_trace) for route in ('direct','cache')]
assert all(item=={'status':'denied'} for item in student_results) and student_trace==[]
assert all(item['content']==GUIDE for item in teacher_results) and len(teacher_trace)==2
assert GUIDE not in repr(student_results)
assert get_guide('learner-1',{'resource_id':'G1','role':'teacher'},'cache',student_trace)['status']=='invalid_input'
assert get_guide('unknown',{'resource_id':'G1'},'direct',student_trace)['status']=='denied'
# Separate picture: access includes relationship, not merely the broad teacher role.
NOTES={'N1':{'owner':'learner-1','assigned_teacher':'teacher-1','text':'fictional practice note'}}
def note(actor,note_id):
 record=NOTES.get(note_id)
 if record is None:return {'status':'review'}
 if actor not in (record['owner'],record['assigned_teacher']):return {'status':'denied'}
 return {'status':'allowed_fixture','text':record['text']}
def analytics_packet(events):
 if type(events) is not list:raise ValueError('event list required')
 for event in events:
  if type(event) is not dict or set(event)!={'kind'} or event['kind']!='revision':
   raise ValueError('only minimized revision-kind events accepted')
 return {'revision_count':len(events)}
notes_before=deepcopy(NOTES)
picture_count=analytics_packet([{'kind':'revision'},{'kind':'revision'}])
assert picture_count=={'revision_count':2} and note('teacher-2','N1')=={'status':'denied'}
assert note('learner-1','N1')['text']==note('teacher-1','N1')['text']
try:analytics_packet([{'kind':'revision','text':NOTES['N1']['text']}])
except ValueError:pass
else:raise AssertionError('Full-note analytics event accepted')
assert NOTES==notes_before
print('Broken query-only cache contains the restricted marker:',GUIDE in UNSAFE_QUERY_ONLY_CACHE.values())
print('Repaired direct/cache student decisions:',student_results,'content-read trace:',student_trace)
print('Teacher fixture reads allowed on both routes:',[r['status'] for r in teacher_results])
print('Separate picture minimized analytics:',picture_count,'source notes unchanged:',NOTES==notes_before)
print('Counts can remain identifying in tiny groups. This fixture checks a declared field/access policy, not anonymity, retention enforcement, real authentication or complete security.')
