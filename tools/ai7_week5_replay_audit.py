"""Fictional replay/new-data accounting; no partner or new experiment is claimed."""
from fractions import Fraction
from copy import deepcopy

def score(records):
 if type(records) is not list or not records:raise ValueError('nonempty case records required')
 ids=[];correct=0
 for record in records:
  if type(record) is not dict or set(record)!={'case_id','correct'}:raise ValueError('exact case ID and correctness fields required')
  if type(record['case_id']) is not str or not record['case_id'] or record['case_id'] in ids:
   raise ValueError('unique nonempty within-run IDs required')
  if type(record['correct']) is not int or record['correct'] not in (0,1):raise ValueError('exact binary outcome required')
  ids.append(record['case_id']);correct+=record['correct']
 return {'count':len(records),'correct':correct,'rate':Fraction(correct,len(records))}
def case_accounting(old_ids,replay_ids,new_ids):
 for ids in [old_ids,replay_ids,new_ids]:
  if type(ids) is not list or any(type(v) is not str or not v for v in ids) or len(set(ids))!=len(ids):
   raise ValueError('unique symbolic IDs within each declared set required')
 if set(replay_ids)!=set(old_ids):raise ValueError('replay must use the same case IDs')
 if set(new_ids)&set(old_ids):raise ValueError('new-case set must not silently reuse old IDs')
 return {'evaluation_events':len(old_ids)+len(replay_ids)+len(new_ids),
         'distinct_case_ids':len(set(old_ids+replay_ids+new_ids)),'new_case_ids':len(new_ids),
         'statistical_independence':'not established by distinct IDs alone'}
main_ids=['Q'+str(i) for i in range(1,9)]
main=case_accounting(main_ids,list(main_ids),[])
assert main['evaluation_events']==16 and main['distinct_case_ids']==8 and main['new_case_ids']==0
# Separate picture: supplied binary entries are correctness outcomes, not class labels.
original=[{'case_id':'OLD'+str(i+1),'correct':v} for i,v in enumerate([1,0,1,1])]
new=[{'case_id':'NEW'+str(i+1),'correct':v} for i,v in enumerate([1,1,0,0])]
before=deepcopy(original)
first=score(original);replayed=score(deepcopy(original));new_result=score(new)
assert first==replayed and first['rate']==Fraction(3,4) and new_result['rate']==Fraction(1,2)
assert original==before
picture_counts=case_accounting([r['case_id'] for r in original],[r['case_id'] for r in original],[r['case_id'] for r in new])
# A deliberately changed analysis is one possible mismatch mechanism, not a diagnosis.
buggy_rate=Fraction(sum(r['correct'] for r in original[:-1]),len(original))
assert buggy_rate==Fraction(1,2) and buggy_rate!=first['rate']
manifest={'analysis':'sum exact binary correctness / recorded count','data':'picture-outcomes-v1',
          'procedure':'toy-score-v1','environment':'standard-library local calculation',
          'actual_partner_rerun':'not performed','new_data_collection':'not performed; supplied fixture only'}
print('Main old-case replay accounting:',main)
print('Picture original/replay/new-data scores:',first,replayed,new_result,'case accounting:',picture_counts)
print('Deliberately changed-analysis mismatch:',buggy_rate,'investigate artifacts/code/settings before interpreting a mismatched replay')
print('Manifest and evidence status:',manifest)
print('A new-sample difference can arise without a code defect. These tiny supplied samples prove no broad reliability, population independence or actual replication study.')
