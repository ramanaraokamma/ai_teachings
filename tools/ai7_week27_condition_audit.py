"""Condition-specific descriptive rates from stipulated summaries."""
from fractions import Fraction

def rate(correct,total):
 if type(correct) is not int or type(total) is not int or total<1 or not 0<=correct<=total:raise ValueError('valid count and positive denominator required')
 return Fraction(correct,total)
main_current=rate(9,10);main_outdated=rate(5,10)
indoor=rate(7,8);outdoor=rate(3,8);pooled=rate(10,16)
assert 100*(main_current-main_outdated)==40
assert 100*(indoor-outdoor)==50 and pooled==Fraction(5,8)
# Reserved independent case is deliberately not solved by this practice program.
print('Main current/outdated rates:',main_current,main_outdated,'gap in percentage points:',100*(main_current-main_outdated))
print('Separate indoor/outdoor rates:',indoor,outdoor,'pooled:',pooled)
print('Pooled 62.5% hides indoor 87.5% versus outdoor 37.5%; it is not the rate for either slice.')
print('No individual case outcomes, cause, significance, stable population rate or universal robustness is supplied. Frozen-model/rubric claims are exercise assumptions, not code-verified controls.')
print('No model is run and no new condition is collected. Keep baseline, metric, eligibility and conditions aligned in any proposed follow-up.')
