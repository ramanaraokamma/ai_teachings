"""Pure fictional compatibility and mandatory-gate decisions; no release operations."""
from copy import deepcopy
READERS={'v1':{1},'v2':{1,2}}
RELEASES={'A':{'code':'v1','config':'cfg1','schema':1,'prompt':'p1','corpus':'c1','evidence':'eval-A'},
          'B':{'code':'v2','config':'cfg2','schema':2,'prompt':'p2','corpus':'c2','evidence':'eval-B'}}
def rollback_check(target_code,stored_schemas):
 if target_code not in READERS:raise ValueError('unknown target reader')
 if type(stored_schemas) is not list or not stored_schemas:
  raise ValueError('nonempty observed schema inventory required')
 if any(type(s) is not int or s not in (1,2) for s in stored_schemas):raise ValueError('unknown schema')
 incompatible=sorted(set(stored_schemas)-READERS[target_code])
 return {'status':'blocked' if incompatible else 'compatible_on_declared_schema_check',
         'incompatible_schemas':incompatible,'target_code':target_code}
GATES={'quality','privacy','compatibility','recovery'}
def release_decision(gates):
 if type(gates) is not dict or set(gates)!=GATES or any(type(v) is not bool for v in gates.values()):
  raise ValueError('complete explicit Boolean gate results required')
 failed=sorted(k for k,v in gates.items() if not v)
 return {'eligible_for_review':not failed,'failed_gates':failed}
def correctness(passed,total):
 if type(passed) is not int or type(total) is not int or total<=0 or not 0<=passed<=total:
  raise ValueError('valid integer pass count and positive denominator required')
 return 100*passed/total

stored=[1,2,2];before=deepcopy(stored)
main=rollback_check('v1',stored)
compatible_reader=rollback_check('v2',stored)
assert main['status']=='blocked' and main['incompatible_schemas']==[2]
assert compatible_reader['status']=='compatible_on_declared_schema_check' and stored==before
# Separate picture supplies correctness counts and a mandatory privacy failure.
quality_a=correctness(8,10);quality_b=correctness(9,10)
# This exercise declares a fictional quality threshold of 80 percent, not a universal rule.
initial_gates={'quality':quality_b>=80,'privacy':False,'compatibility':True,'recovery':True}
initial=release_decision(initial_gates)
assert quality_a==80 and quality_b==90 and initial['failed_gates']==['privacy']
# Fresh privacy evidence is only one gate: other gates may be incomplete or fail.
privacy_repaired_only=release_decision({'quality':True,'privacy':True,'compatibility':False,'recovery':True})
all_declared_pass=release_decision({key:True for key in GATES})
assert not privacy_repaired_only['eligible_for_review'] and all_declared_pass['eligible_for_review']
print('Main code-only rollback:',main,'compatible reader check:',compatible_reader)
print('Picture A/B correctness:',quality_a,quality_b,'B initial decision:',initial)
print('Privacy repaired but compatibility fails:',privacy_repaired_only)
print('All declared gates pass:',all_declared_pass,'not an automatic release or complete real-world assurance')
print('Release manifests:',RELEASES)
print('No migration, restoration, adapter, external-effect reversal or deployment is executed; source inventory unchanged:',stored==before)
