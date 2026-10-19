"""Summarize supplied durations and fictional costs; no benchmark or provider calls."""
from math import isfinite
from statistics import mean,median

def nonnegative(value):return type(value) in (int,float) and isfinite(value) and value>=0

def summarize(rows):
 if type(rows) is not list or not rows:raise ValueError('nonempty measured-case fixture required')
 ids=[];durations=[];successes=[]
 for row in rows:
  if type(row) is not dict or set(row)!={'case_id','seconds','success'}:raise ValueError('exact supplied fields required')
  if type(row['case_id']) is not str or not row['case_id'] or row['case_id'] in ids:raise ValueError('unique case ID required')
  if not nonnegative(row['seconds']) or type(row['success']) is not bool:raise ValueError('valid duration and success flag required')
  ids.append(row['case_id']);durations.append(row['seconds']);successes.append(row['success'])
 return {'case_ids':ids,'durations':durations,'count':len(rows),'passes':sum(successes),
         'mean_seconds':mean(durations),'median_seconds':median(durations),'max_seconds':max(durations)}
def compare(a,b):
 sa=summarize(a);sb=summarize(b)
 if sa['case_ids']!=sb['case_ids']:raise ValueError('same ordered case IDs required for paired fixture')
 return sa,sb

def cost_means(count,total_seconds,total_cost):
 if type(count) is not int or count<=0 or not all(nonnegative(v) for v in [total_seconds,total_cost]):
  raise ValueError('positive count and finite nonnegative totals required')
 return {'count':count,'mean_seconds':total_seconds/count,'mean_cost_units':total_cost/count}
def rows(durations):return [{'case_id':'Q'+str(i+1),'seconds':s,'success':True} for i,s in enumerate(durations)]
a,b=compare(rows([1,1,1,9]),rows([2,2,2,2]))
assert (a['mean_seconds'],a['median_seconds'],a['max_seconds'],a['passes'])==(3,1,9,4)
assert (b['mean_seconds'],b['median_seconds'],b['max_seconds'],b['passes'])==(2,2,2,4)
picture_a=cost_means(6,18,12);picture_b=cost_means(6,12,18)
mean_budget=2
assert picture_a['mean_cost_units']<=mean_budget and picture_b['mean_cost_units']>mean_budget
# Added failure probe, separate from the reserved independent C/D case.
failed_rows=rows([2,2,2,2]);failed_rows[-1]['success']=False
failed=summarize(failed_rows)
assert failed['count']==4 and failed['passes']==3 and len(failed['durations'])==4
print('Main all-pass A:',a,'B:',b)
print('Separate picture average time/cost A:',picture_a,'B:',picture_b)
print('Mean budget at most 2 fictional units: A passes, B fails. Individual per-request cap cannot be inferred from totals.')
print('Separate failure probe retains all four durations and reports quality:',failed)
print('Duration scope is supplied request-start-to-final-outcome fixture time, including failed outcomes. No actual timer, repeated trials, confidence interval, currency pricing or universal winner is provided.')
