"""Supplied fictional monitoring counts; no live telemetry or causal inference."""
from fractions import Fraction

def window(eligible,passes,failures,missing,threshold=80):
 values=[eligible,passes,failures,missing]
 if any(type(v) is not int or v<0 for v in values) or passes+failures+missing!=eligible:
  raise ValueError('nonnegative exact counts must cover all eligible cases')
 if type(threshold) is not int or not 0<=threshold<=100:raise ValueError('integer percent threshold required')
 observed=passes+failures
 observed_rate=Fraction(passes,observed) if observed else None
 complete=eligible>0 and missing==0
 quality_alert=(100*observed_rate<threshold) if complete else None
 return {'eligible':eligible,'passes':passes,'failures':failures,'missing':missing,
         'observed_rate':observed_rate,'complete':complete,'quality_alert':quality_alert,
         'coverage_alert':missing>0 or eligible==0}
def pct(rate):return None if rate is None else float(100*rate)
reference=window(20,18,2,0);current=window(20,14,6,0)
drop_pp=100*(reference['observed_rate']-current['observed_rate'])
assert pct(reference['observed_rate'])==90 and pct(current['observed_rate'])==70 and drop_pp==20
assert not reference['quality_alert'] and current['quality_alert']
# Same rubric, supplied slice denominators, fully observed outcomes in each recorded week.
slices_a={'clear':window(20,18,2,0),'ambiguous':window(10,8,2,0)}
slices_b={'clear':window(20,19,1,0),'ambiguous':window(10,4,6,0)}
total_a=window(30,26,4,0);total_b=window(30,23,7,0)
assert [pct(slices_a[k]['observed_rate']) for k in ['clear','ambiguous']]==[90,80]
assert [pct(slices_b[k]['observed_rate']) for k in ['clear','ambiguous']]==[95,40]
no_ambiguous=window(0,0,0,0)
assert no_ambiguous['observed_rate'] is None and no_ambiguous['quality_alert'] is None
# Missing outcomes are reported, never silently counted as passes or failures.
incomplete=window(20,14,4,2)
assert incomplete['observed_rate']==Fraction(14,18) and incomplete['quality_alert'] is None and incomplete['coverage_alert']
exact_boundary=window(10,8,2,0)
assert exact_boundary['quality_alert'] is False
print('Main reference/current:',pct(reference['observed_rate']),pct(current['observed_rate']),'drop in percentage points:',float(drop_pp))
print('Picture clear/ambiguous A:',[pct(slices_a[k]['observed_rate']) for k in ['clear','ambiguous']])
print('Picture clear/ambiguous B:',[pct(slices_b[k]['observed_rate']) for k in ['clear','ambiguous']])
print('Picture totals A/B:',pct(total_a['observed_rate']),pct(total_b['observed_rate']))
print('Zero ambiguous slice:',no_ambiguous,'incomplete example:',incomplete)
print('Same rubric and constructed complete counts do not establish a stable trend, comparable case difficulty or cause. Check case mix, versions and instrumentation.')
