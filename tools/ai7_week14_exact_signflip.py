"""Exact tiny-n conditional sign-flip test, under explicitly assumed valid pairing/null."""
from itertools import product
from fractions import Fraction
from collections import Counter

def exact_rational(value):
 if type(value) is int or type(value) is Fraction:return Fraction(value)
 raise ValueError('use exact integers or Fraction values, not Boolean/inexact inputs')

def sign_flip_test(differences,alpha=Fraction(1,20)):
 """Assume independent paired units and conditionally independent equiprobable signs.
 Hold magnitudes fixed under the symmetric zero-effect null. Design assumptions
 cannot be verified from these numbers. Absolute-mean ties count inclusively.
 """
 if type(differences) not in (list,tuple) or not 1<=len(differences)<=16:
  raise ValueError('require 1 to 16 exact paired differences')
 values=[exact_rational(d) for d in differences];level=exact_rational(alpha)
 if not 0<level<1:raise ValueError('alpha must be between zero and one')
 n=len(values);observed_sum=sum(values);observed_absolute_mean=abs(observed_sum)/n
 rows=[]
 for signs in product((-1,1),repeat=n):
  signed=tuple(s*abs(d) for s,d in zip(signs,values));total=sum(signed)
  statistic=abs(total)/n
  rows.append({'signs':signs,'signed_differences':signed,'sum':total,'absolute_mean':statistic,
               'at_least_as_extreme':statistic>=observed_absolute_mean})
 extreme=sum(row['at_least_as_extreme'] for row in rows)
 p=Fraction(extreme,len(rows))
 return {'observed_sum':observed_sum,'observed_absolute_mean':observed_absolute_mean,
         'rows':rows,'extreme':extreme,'assignments':len(rows),'p':p,'alpha':level,
         'decision':'reject' if p<=level else 'do_not_reject'}
main=sign_flip_test([1,1,1])
assert main['observed_absolute_mean']==1 and main['extreme']==2 and main['assignments']==8 and main['p']==Fraction(1,4)
assert main['decision']=='do_not_reject'
# Separate picture: paired B-A times [-1,-2,-1], absolute sum ordering equivalent for fixed n.
picture=sign_flip_test([-1,-2,-1])
sum_counts=Counter(row['sum'] for row in picture['rows'])
assert sum_counts=={-4:1,-2:2,0:2,2:2,4:1} and picture['p']==Fraction(1,4)
# Scale invariance and inclusive ties require no arbitrary absolute epsilon.
scaled=sign_flip_test([Fraction(1,10**13)]*3)
assert scaled['p']==main['p'] and sign_flip_test([0,0,0])['p']==1
print('Main exact assignments:',[(r['signs'],str(r['sum']),str(r['absolute_mean']),r['at_least_as_extreme']) for r in main['rows']])
print('Main exact two-sided p:',main['p'],'decision at alpha 0.05:',main['decision'])
print('Picture signed-sum null counts:',{str(k):v for k,v in sorted(sum_counts.items())},'p:',picture['p'])
print('Exact tiny-scale check:',scaled['p'],'ties included; enumeration adds no new observed units.')
print('The p-value is a null-model tail probability, not the probability the null is true. Do not reject does not prove zero effect or practical unimportance.')
print('No actual random assignment, model experiment or significance claim for unpaired/correlated data is supplied. Exact arithmetic cannot verify pairing, independence, symmetry or exchangeability.')
