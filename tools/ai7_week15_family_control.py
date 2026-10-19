"""Exact arithmetic on stipulated valid p-values, not a fitted statistical study."""
from fractions import Fraction

def bonferroni_family(values, family_size=None, alpha='0.05'):
 if not isinstance(values,(list,tuple)) or not values:raise ValueError('supply recorded p-values')
 if family_size is None:family_size=len(values)
 if type(family_size) is not int or family_size<len(values):raise ValueError('family must include all recorded tests')
 if type(alpha) not in (str,int,Fraction):raise ValueError('use exact decimal strings or fractions')
 level=Fraction(alpha)
 if not 0<level<1:raise ValueError('alpha must be between zero and one')
 if any(type(p) not in (str,int,Fraction) for p in values):raise ValueError('use exact p-value strings or fractions')
 ps=[Fraction(p) for p in values]
 if any(not 0<=p<=1 for p in ps):raise ValueError('p-values must lie in [0,1]')
 cutoff=level/family_size
 return {'family_size':family_size,'recorded_tests':len(ps),'missing_tests':family_size-len(ps),
         'cutoff':cutoff,'reject':[p<=cutoff for p in ps],
         'adjusted_p':[min(Fraction(1),p*family_size) for p in ps]}
main=bonferroni_family(['.009','.012','.3','.4','.8'])
picture_values=['.004','.012','.02','.08','.4','.9']
picture=bonferroni_family(picture_values)
changed=bonferroni_family(picture_values,10)
boundary=bonferroni_family(['.01','.2','.3','.4','.5'])
assert main['cutoff']==Fraction(1,100) and main['reject']==[True,False,False,False,False]
assert picture['cutoff']==Fraction(1,120) and picture['reject']==[True,False,False,False,False,False]
assert changed['cutoff']==Fraction(1,200) and changed['missing_tests']==4
assert boundary['reject'][0]
print('Main five-test decisions:',main)
print('Separate six-test picture:',picture)
print('Ten-test declared family, six supplied results:',changed)
print('Unknown four results stay unknown; no decision for them is fabricated.')
print('For valid individual tests, the union bound controls the chance of any false rejection at most alpha, without requiring independent tests.')
print('This arithmetic does not validate supplied p-values, establish effect magnitude or prove non-rejected nulls. No actual prompt experiment is run.')
