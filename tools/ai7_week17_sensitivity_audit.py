"""Sensitivity arithmetic on supplied summaries and unlabelled toy scores."""
from fractions import Fraction

def exact(value):
 if type(value) not in (str,int,Fraction):raise ValueError('use exact strings or fractions')
 result=Fraction(value)
 if not 0<=result<=1:raise ValueError('value must be in [0,1]')
 return result

def classify(scores,cutoff):
 if not isinstance(scores,(list,tuple)) or not scores:raise ValueError('scores required')
 boundary=exact(cutoff)
 return [exact(score)>=boundary for score in scores]
retrieval=[{'k':1,'recall':Fraction(4,10),'precision':Fraction(9,10)},
           {'k':3,'recall':Fraction(7,10),'precision':Fraction(7,10)},
           {'k':5,'recall':Fraction(8,10),'precision':Fraction(5,10)}]
scores=['.4','.6','.8'];before=scores[:]
picture={cutoff:classify(scores,cutoff) for cutoff in ['.5','.7','.6']}
assert picture['.5']==picture['.6']==[False,True,True]
assert picture['.7']==[False,False,True] and scores==before
# Labels are explicitly hypothetical, not supplied ground truth for the picture.
hypothetical_labels_A=[False,True,True]
hypothetical_labels_B=[False,False,True]
def correct_count(predictions,labels):
 if len(predictions)!=len(labels):raise ValueError('same cases required')
 return sum(a==b for a,b in zip(predictions,labels))
assert correct_count(picture['.5'],hypothetical_labels_A)==3
assert correct_count(picture['.7'],hypothetical_labels_B)==3
print('Supplied retrieval summary tradeoff:',retrieval)
print('Picture positive flags at each cutoff:',picture)
print('No reference labels are supplied; different explicitly hypothetical labels favor different cutoffs. More positives is not greater accuracy.')
print('Retrieval precision/recall are stipulated aggregate summaries; averaging convention and raw counts are not supplied. No raw relevance labels are reconstructed.')
print('Preserve the tested range and all results. Selection on these results needs separately reserved evaluation; no actual model run or beyond-range guarantee is supplied.')
