"""Supplied paired gains and practical thresholds, without inference or live timing."""
from math import isfinite
from statistics import mean
from fractions import Fraction

def finite_nonnegative(value):
 return type(value) in (int,float) and isfinite(value) and value>=0

def paired_gain(rows,minimum_useful_gain):
 if type(rows) is not list or not rows or not finite_nonnegative(minimum_useful_gain) or minimum_useful_gain<=0:
  raise ValueError('paired records and positive declared threshold required')
 ids=[];gains=[]
 for row in rows:
  if type(row) is not dict or set(row)!={'case_id','baseline_seconds','candidate_seconds'}:
   raise ValueError('exact paired case/timing fields required')
  if type(row['case_id']) is not str or not row['case_id'] or row['case_id'] in ids:raise ValueError('unique paired case IDs required')
  if not all(finite_nonnegative(row[k]) for k in ['baseline_seconds','candidate_seconds']):raise ValueError('finite nonnegative supplied times required')
  ids.append(row['case_id']);gains.append(row['baseline_seconds']-row['candidate_seconds'])
 average=mean(gains)
 return {'case_ids':ids,'gains_seconds':gains,'mean_gain_seconds':average,
         'minimum_useful_mean_gain':minimum_useful_gain,'meets_declared_mean_threshold':average>=minimum_useful_gain}
def error_reduction(a_errors,b_errors,total,minimum_per_thousand=10):
 if any(type(v) is not int for v in [a_errors,b_errors,total,minimum_per_thousand]) or total<=0 or minimum_per_thousand<=0:
  raise ValueError('exact integer counts and positive denominator/threshold required')
 if not 0<=a_errors<=total or not 0<=b_errors<=total:raise ValueError('valid error counts required')
 difference=Fraction(a_errors-b_errors,total)
 return {'A_error_rate':Fraction(a_errors,total),'B_error_rate':Fraction(b_errors,total),
         'reduction_percentage_points':100*difference,'fewer_errors_per_thousand':1000*difference,
         'relative_error_reduction':Fraction(a_errors-b_errors,a_errors) if a_errors else None,
         'meets_declared_threshold':1000*difference>=minimum_per_thousand}
rows=[{'case_id':'Q'+str(i+1),'baseline_seconds':a,'candidate_seconds':b}
      for i,(a,b) in enumerate(zip([10,12,8],[8,9,7]))]
main=paired_gain(rows,2)
assert main['gains_seconds']==[2,3,1] and main['mean_gain_seconds']==2 and main['meets_declared_mean_threshold']
picture=error_reduction(20,15,1000)
changed=error_reduction(20,8,1000)
assert picture['fewer_errors_per_thousand']==5 and picture['reduction_percentage_points']==Fraction(1,2) and not picture['meets_declared_threshold']
assert picture['relative_error_reduction']==Fraction(1,4)
assert changed['fewer_errors_per_thousand']==12 and changed['reduction_percentage_points']==Fraction(6,5) and changed['meets_declared_threshold']
assert error_reduction(20,10,1000)['meets_declared_threshold']
print('Main paired baseline-minus-candidate gains:',main)
print('Separate original supplied error-count comparison:',picture)
print('Changed supplied B error count:',changed)
print('Main mean threshold is inclusive and applies to the mean, not every case. The prior lesson used B-A; this gain definition deliberately uses A-B.')
print('These are descriptive supplied observations and fictional practical criteria, not actual timings, significance, uncertainty intervals, causal effects or complete deployment decisions. Quality/resources require their own evidence.')
