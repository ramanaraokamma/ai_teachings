"""Versioned fictional gate records; no approvals, deletion or deployment."""
from copy import deepcopy
from fractions import Fraction

def ordinary_gate(passed,total):
 if type(passed) is not int or type(total) is not int or total<=0 or not 0<=passed<=total:
  raise ValueError('valid exact counts required')
 return Fraction(passed,total)>=Fraction(9,10)

def gate(state,candidate,evidence_id=None):
 return {'state':state,'candidate':candidate,'evidence_id':evidence_id}

def review(candidate,required,evidence):
 if type(candidate) is not str or not candidate:raise ValueError('candidate version required')
 if type(required) is not set or not required or any(type(k) is not str or not k for k in required):
  raise ValueError('nonempty declared gate-name set required')
 if type(evidence) is not dict or set(evidence)-required:raise ValueError('only declared gate records accepted')
 blockers=[]
 for name in sorted(required):
  record=evidence.get(name)
  if record is None:blockers.append((name,'missing'));continue
  if type(record) is not dict or set(record)!={'state','candidate','evidence_id'}:raise ValueError('exact evidence record fields required')
  if record['state'] not in ('pass','fail','not_run'):raise ValueError('explicit gate state required')
  if record['state']!='not_run' and (type(record['evidence_id']) is not str or not record['evidence_id']):
   raise ValueError('pass/fail needs a supplied evidence reference')
  if record['candidate']!=candidate:blockers.append((name,'wrong candidate version'))
  elif record['state']!='pass':blockers.append((name,record['state']))
 return {'candidate':candidate,'eligible_under_declared_fixture_gates':not blockers,'blockers':blockers}

main_required={'ordinary','access','no_unauthorized_effects','compatible_rollback'}
main_records={'ordinary':gate('pass' if ordinary_gate(18,20) else 'fail','r2','ORD-18-20'),
              'access':gate('pass','r2','ACCESS-MAIN'),
              'no_unauthorized_effects':gate('pass','r2','TRACE-MAIN'),
              'compatible_rollback':gate('not_run','r2')}
main=review('r2',main_required,main_records)
assert ordinary_gate(18,20) and main['blockers']==[('compatible_rollback','not_run')]
# Separate picture declares three gates, not the main example's four-gate set.
picture_required={'factual','access','deletion'}
failed_records={'factual':gate('pass','p2','FACT-P2'),'access':gate('pass','p2','ACCESS-P2'),
                'deletion':gate('fail','p2','BACKUP-RESIDUAL-P2')}
failed_before=deepcopy(failed_records);initial=review('p2',picture_required,failed_records)
assert initial['blockers']==[('deletion','fail')]
# Constructed repaired candidate evidence; no real copy is deleted or check performed.
stale_repair={**failed_records,'deletion':gate('pass','p3','ALL-LISTED-LOCATIONS-P3')}
stale=review('p3',picture_required,stale_repair)
assert not stale['eligible_under_declared_fixture_gates']
fresh_records={name:gate('pass','p3','FIXTURE-'+name.upper()+'-P3') for name in picture_required}
fresh=review('p3',picture_required,fresh_records)
history=[deepcopy(initial),deepcopy(stale),deepcopy(fresh)]
assert fresh['eligible_under_declared_fixture_gates'] and failed_records==failed_before
assert history[0]['blockers']==[('deletion','fail')]
print('Main 18/20 = 90 percent; ordinary threshold met; review:',main)
print('Picture initial deletion failure:',initial)
print('Repaired deletion but stale other-version evidence:',stale)
print('All pictured gates freshly supplied for candidate p3:',fresh)
print('Original failure preserved:',failed_records==failed_before,'history:',history)
print('These evidence IDs/states are constructed inputs, not test execution or human sign-off. Eligibility under a declared toy gate set does not deploy/approve anything, prove unknown-copy deletion or guarantee zero future faults.')
