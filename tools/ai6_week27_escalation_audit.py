"""Local handoff packets and review-state decisions; no messaging or bookings."""
from copy import deepcopy
TRUSTED_REVIEWERS={'coordinator':{'room_conflict'},'adult_supervisor':{'equipment_concern'}}
def packet(case_id,kind,reported,source_ids,owner,deadline):
 if any(type(v) is not str or not v for v in [case_id,kind,reported]):raise ValueError('nonempty case fields required')
 if type(source_ids) is not list or not source_ids or any(type(v) is not str or not v for v in source_ids):
  raise ValueError('nonempty fictional evidence IDs required')
 if type(deadline) is not int or deadline<0:raise ValueError('nonnegative virtual minute deadline required')
 if owner is not None and type(owner) is not str:raise ValueError('owner must be a symbolic reviewer ID or None')
 assigned=owner in TRUSTED_REVIEWERS and kind in TRUSTED_REVIEWERS[owner]
 return {'case_id':case_id,'kind':kind,'reported':reported,'source_ids':list(source_ids),
         'owner':owner,'assigned':assigned,'deadline':deadline,'status':'needs_review',
         'fallback':'keep unresolved; perform no booking or certification'}
def progress(item,now,*,reachable):
 if type(now) is not int or now<0 or type(reachable) is not bool:raise ValueError('valid virtual time and reachability required')
 return {'status':'needs_review','overdue':now>=item['deadline'],
         'handoff_ready':item['assigned'] and reachable,'effects':[],'notifications_sent':[]}

effects=[];notifications=[]
unassigned=packet('ROOM-C1','room_conflict','Fictional cards disagree: B12 versus D4',['S1','S2'],None,30)
assigned=packet('ROOM-C1','room_conflict',unassigned['reported'],['S1','S2'],'coordinator',30)
before=deepcopy(assigned)
assert not unassigned['assigned'] and assigned['assigned']
ready=progress(assigned,10,reachable=True)
over=progress(assigned,30,reachable=True)
assert ready['handoff_ready'] and not ready['overdue']
assert over['overdue'] and over['status']=='needs_review' and over['effects']==[]
wrong_owner=packet('ROOM-C1','room_conflict',unassigned['reported'],['S1','S2'],'adult_supervisor',30)
assert not wrong_owner['assigned']
picture=packet('REPORT-P1','equipment_concern','Learner reports a damaged bottle; no physical condition verified',
               ['fictional-report-P1'],'adult_supervisor',30)
unreachable=progress(picture,31,reachable=False)
assert not unreachable['handoff_ready'] and unreachable['status']=='needs_review'
assert assigned==before and effects==notifications==[]
print('Main unassigned/assigned:',unassigned['assigned'],assigned['assigned'],'handoff state:',ready)
print('Deadline reached without a decision:',over)
print('Picture supplied report and route:',picture,'unreachable supervisor:',unreachable)
print('Handoff-ready means a packet and route are specified; it is not evidence of delivery, receipt, review or approval.')
print('No emails, messages, notifications, bookings, certifications or real-world safety decisions are made. Institutional procedures are outside this fictional model.')
