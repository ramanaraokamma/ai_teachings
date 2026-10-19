"""Declared toy analysis plan versus post-result changes; no actual preregistration/study."""
from copy import deepcopy
from fractions import Fraction
from statistics import mean
from math import isfinite
VALID={'supported','unsupported','abstain','timeout'}

def summarize(rows):
 if type(rows) is not list or not rows:raise ValueError('nonempty complete-case fixture required')
 ids=[];counts={state:0 for state in VALID};durations=[]
 for row in rows:
  if type(row) is not dict or set(row)!={'case_id','outcome','seconds'}:raise ValueError('exact case fields required')
  if type(row['case_id']) is not str or not row['case_id'] or row['case_id'] in ids:raise ValueError('unique IDs required')
  if row['outcome'] not in VALID:raise ValueError('declared outcome category required')
  if type(row['seconds']) not in (int,float) or not isfinite(row['seconds']) or row['seconds']<0:
   raise ValueError('finite nonnegative supplied duration required')
  ids.append(row['case_id']);counts[row['outcome']]+=1;durations.append(row['seconds'])
 return {'case_ids':ids,'counts':counts,'supported_rate':Fraction(counts['supported'],len(rows)),
         'mean_seconds':mean(durations),'denominator':len(rows)}
# Plan is recorded in code before evaluating these fully revealed practice fixtures.
plan={'primary':'supported_rate','direction':'B>A','failure_rule':'all planned cases stay in denominator',
      'secondary':['mean_seconds','unsupported_count','abstention_count','timeout_count']}
saved_plan=deepcopy(plan)
def rows(outcomes,seconds):return [{'case_id':'Q'+str(i+1),'outcome':v,'seconds':seconds} for i,v in enumerate(outcomes)]
a=summarize(rows(['supported']*4+['unsupported','timeout'],3))
b=summarize(rows(['supported']*4+['abstain','timeout'],2))
assert a['case_ids']==b['case_ids'] and a['supported_rate']==b['supported_rate']==Fraction(2,3)
primary_pattern=b['supported_rate']>a['supported_rate']
assert not primary_pattern and b['mean_seconds']<a['mean_seconds']
revision={'stage':'post_results','proposed_new_claim':'B is faster','status':'exploratory revision, not original primary'}
assert plan==saved_plan
# Separate pictured strict reduction question: supplied changed-case tie, no model is scored.
picture={'reserved_case_count_in_scenario':10,'A_unsupported':2,'B_unsupported':2,
         'friendlier_wording':'qualitative scenario description, not a measured primary metric'}
assert not picture['B_unsupported']<picture['A_unsupported']
print('Original declared toy plan:',plan)
print('Added practice A:',a,'B:',b,'strict primary improvement observed:',primary_pattern)
print('Post-result claim record:',revision,'original plan unchanged:',plan==saved_plan)
print('Separate pictured unsupported-count tie:',picture)
print('Abstention is not a supported answer. Fewer unsupported claims can coexist with unchanged support and more abstention; retain all outcomes.')
print('This script defines/evaluates supplied fixtures in order, not a real preregistration or reserved study. No significance, power, population equality, model experiment or human scoring is established.')
