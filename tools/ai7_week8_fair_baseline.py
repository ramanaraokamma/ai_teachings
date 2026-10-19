"""Constructed same-procedure/different-source comparison, not a model benchmark."""
from fractions import Fraction
from copy import deepcopy
CURRENT={'V':'E','W':'B','X':'D'}
OLD={'V':'C','W':'B','X':'A'}
CASES=['V','W','X'];TRUTH=deepcopy(CURRENT)

def evaluate(source,cases,truth):
 if type(source) is not dict or type(cases) is not list or not cases or len(set(cases))!=len(cases):
  raise ValueError('supplied source and unique matched cases required')
 if set(cases)!=set(truth):raise ValueError('complete fixed judged cases required')
 outputs=[{'case':case,'answer':source.get(case),'correct':source.get(case)==truth[case]} for case in cases]
 return {'outputs':outputs,'correct':sum(row['correct'] for row in outputs),'count':len(cases)}
# A and B intentionally use the identical lookup function; only information changes.
a_old=evaluate(OLD,CASES,TRUTH);b_current=evaluate(CURRENT,CASES,TRUTH)
a_aligned=evaluate(CURRENT,CASES,TRUTH)
assert a_old['correct']==1 and b_current['correct']==a_aligned['correct']==3

def conditions(case_ids,source_version,*,test_labels_seen=False):
 return {'case_ids':list(case_ids),'source_version':source_version,'scoring':'fixed-rubric-v1',
         'test_labels_seen':test_labels_seen,'budget_policy':'not supplied'}
def compare_conditions(a,b):
 required={'case_ids','source_version','scoring','test_labels_seen','budget_policy'}
 if type(a) is not dict or type(b) is not dict or set(a)!=required or set(b)!=required:
  raise ValueError('complete declared condition records required')
 if type(a['test_labels_seen']) is not bool or type(b['test_labels_seen']) is not bool:
  raise ValueError('explicit test-label exposure flags required')
 issues=[]
 for name in ['case_ids','source_version','scoring']:
  if a[name]!=b[name]:issues.append('mismatched '+name)
 if a['test_labels_seen'] or b['test_labels_seen']:issues.append('test answer-key exposure')
 if a['budget_policy']=='not supplied' or b['budget_policy']=='not supplied':issues.append('resource policy not supplied')
 elif a['budget_policy']!=b['budget_policy']:issues.append('mismatched resource policy')
 return issues
unequal=compare_conditions(conditions(CASES,'old'),conditions(CASES,'current'))
assert 'mismatched source_version' in unequal
# Separate picture: aggregate correctness, same eight cases/sources, no tuning on test.
picture_a=Fraction(6,8);picture_b=Fraction(7,8)
assert 100*picture_a==75 and 100*picture_b==Fraction(175,2)
assert 100*(picture_b-picture_a)==Fraction(25,2)
picture_ids=['P'+str(i) for i in range(1,9)]
leaked=compare_conditions(conditions(picture_ids,'same'),conditions(picture_ids,'same',test_labels_seen=True))
assert 'test answer-key exposure' in leaked
print('Added same-procedure old/current source results:',a_old,b_current)
print('Align both to current sources:',a_aligned,b_current,'not a claim about real model equality')
print('Declared-condition issues:',unequal)
print('Separate picture percentages:',float(100*picture_a),float(100*picture_b),'net count difference: one; paired flips unknown')
print('Picture answer-key-exposure variant issues:',leaked)
print('Current task evidence is permitted source material, distinct from hidden evaluation labels. These local fixtures do not measure runtime budgets, real model quality, statistical significance or broad advantage.')
