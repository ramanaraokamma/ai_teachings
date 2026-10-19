"""Exact finite-population enumeration under a declared uniform sampling model."""
from itertools import combinations
from fractions import Fraction
from collections import Counter

def enumerate_means(records,size):
 if type(records) is not list or not records:raise ValueError('nonempty finite population required')
 if type(size) is not int or not 1<=size<=len(records):raise ValueError('valid exact sample size required')
 ids=[]
 for record in records:
  if type(record) is not dict or set(record)!={'id','value'}:raise ValueError('exact ID/value record required')
  if type(record['id']) is not str or not record['id'] or record['id'] in ids:raise ValueError('distinct nonempty population IDs required')
  if type(record['value']) is not int:raise ValueError('exact integer values required for this toy model')
  ids.append(record['id'])
 rows=[]
 for indices in combinations(range(len(records)),size):
  selected=[records[i] for i in indices]
  rows.append({'ids':tuple(r['id'] for r in selected),'values':tuple(r['value'] for r in selected),
               'mean':Fraction(sum(r['value'] for r in selected),size)})
 return rows
population=[{'id':'U1','value':1},{'id':'U2','value':1},{'id':'U3','value':3},{'id':'U4','value':3}]
rows=enumerate_means(population,2)
means=[r['mean'] for r in rows];frequencies=Counter(means)
# All six unordered ID pairs are equally likely under this explicitly declared model.
probabilities={value:Fraction(count,len(rows)) for value,count in sorted(frequencies.items())}
average_of_means=sum(means)/len(means)
population_mean=Fraction(sum(r['value'] for r in population),len(population))
assert means==[1,2,2,2,2,3] and average_of_means==population_mean==2
assert probabilities=={Fraction(1):Fraction(1,6),Fraction(2):Fraction(2,3),Fraction(3):Fraction(1,6)}
assert sum(probabilities.values())==1
assert len(enumerate_means(population,4))==1 and enumerate_means(population,4)[0]['mean']==2
# Separate picture: observed counts only, no probability model inferred for these samples.
picture_a=Fraction(3,4);picture_b=Fraction(2,4)
assert 100*(picture_a-picture_b)==25
print('Six unordered ID samples:',[(r['ids'],r['values'],str(r['mean'])) for r in rows])
print('Uniform-model sample-mean probabilities:',{str(k):str(v) for k,v in probabilities.items()})
print('Average sample mean:',average_of_means,'known finite-population mean:',population_mean)
print('Separate picture rates:',float(100*picture_a),float(100*picture_b),'difference: 25 percentage points')
print('Equal values retain distinct IDs. Enumerated samples are possibilities, not six independent observed experiments. Draws within a without-replacement sample are not independent.')
print('No random draw, live classifier, population inference or confidence interval is performed. The picture supplies no sampling probability model; it cannot borrow this finite-model probability.')
