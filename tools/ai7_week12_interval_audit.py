"""Known-sigma normal interval arithmetic and separate supplied-interval interpretation."""
from math import sqrt,isfinite
from statistics import NormalDist

def finite_real(value):
 if type(value) not in (int,float):return False
 try:return isfinite(value)
 except OverflowError:return False

def known_sigma_interval(mean,sigma,n,critical=1.96):
 """Assume independent normal sampling with known positive population sigma.
 Numeric checks cannot verify those design/model assumptions.
 """
 if not finite_real(mean) or not finite_real(sigma) or sigma<=0:
  raise ValueError('finite mean and known positive sigma required')
 if type(n) is not int or n<1 or not finite_real(critical) or critical<=0:
  raise ValueError('positive exact n and finite positive critical required')
 try:
  se=sigma/sqrt(n);margin=critical*se;lower=mean-margin;upper=mean+margin
 except OverflowError:raise ValueError('settings exceed this floating-point calculation')
 if not all(isfinite(v) for v in [se,margin,lower,upper]):raise ValueError('nonfinite result')
 return {'standard_error':se,'margin':margin,'lower':lower,'upper':upper,'critical':critical,
         'theoretical_normal_coverage':2*NormalDist().cdf(critical)-1}
main=known_sigma_interval(10,2,16)
assert main['standard_error']==0.5 and abs(main['margin']-0.98)<1e-12
assert abs(main['lower']-9.02)<1e-12 and abs(main['upper']-10.98)<1e-12
assert abs(main['theoretical_normal_coverage']-0.95)<0.00001
# Separate supplied intervals; no standard error or raw-data fitting is inferred.
def locate_zero(lower,upper,estimate):
 if not all(finite_real(v) for v in [lower,upper,estimate]) or lower>upper or not lower<=estimate<=upper:
  raise ValueError('ordered finite supplied bounds containing the estimate required')
 return {'contains_zero':lower<=0<=upper,
         'direction':'all negative' if upper<0 else 'all positive' if lower>0 else 'includes zero'}
picture=locate_zero(-1.4,-0.2,-0.8)
changed=locate_zero(-1.4,0.3,-0.8)
assert picture=={'contains_zero':False,'direction':'all negative'} and changed['contains_zero']
print('Main known-sigma interval:',main)
print('Separate supplied B-A time interval:',picture,'changed supplied interval:',changed)
print('Negative B-A means B has lower mean time under this convention, not every request is faster.')
print('Critical 1.96 is rounded: theoretical normal-model coverage is approximately 95 percent. No repeated-sample coverage experiment was run.')
print('Confidence concerns the procedure under assumptions, not a 95 percent probability assigned to a fixed unknown mean after observing this interval. Zero inclusion does not prove equality.')
print('The calculation does not verify normality, independence, known sigma or unbiased sampling; an interval does not repair bias, prove causality or establish practical value.')
