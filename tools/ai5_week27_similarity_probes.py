from math import sqrt

def unit(v):
    if not v:
        raise ValueError("Need a nonempty vector")
    length = sqrt(sum(x*x for x in v))
    if length == 0:
        raise ValueError("Zero vector has no direction")
    return [x / length for x in v]

def cosine(a, b):
    if len(a) != len(b):
        raise ValueError("Need matching dimensions")
    ua, ub = unit(a), unit(b)
    return sum(x*y for x, y in zip(ua, ub))

q = [3, 4]
for name, v in [("A", [6, 8]), ("B", [3, 0]),
                ("C", [-3, -4])]:
    print(name, round(cosine(q, v), 6))
# Complete raw/unit comparison and explicit zero-candidate policy.
from math import isfinite

def distance2(a,b):
    if not a or len(a)!=len(b):
        raise ValueError('Need equal nonempty dimensions')
    return sum((x-y)**2 for x,y in zip(a,b))

def cosine_rank(query,candidates,tolerance=1e-9):
    unit(query)  # Reject an empty or zero query, not an invented zero cosine.
    if not isfinite(tolerance) or tolerance<0:
        raise ValueError('Need nonnegative finite tie tolerance')
    scores={};excluded=[]
    for name,vector in candidates.items():
        if not vector or len(vector)!=len(query):
            raise ValueError('Candidate dimensions must match query')
        if all(x==0 for x in vector):
            excluded.append(name)
        else:
            scores[name]=cosine(query,vector)
    if not scores:
        return [],excluded,scores  # Explicit no-comparison result.
    best=max(scores.values())
    return sorted(n for n,c in scores.items() if abs(c-best)<=tolerance),excluded,scores

candidates={'A':[6,8],'B':[3,0],'C':[-3,-4]}
print('query unit vector',unit(q))
for name,v in candidates.items():
    c=cosine(q,v)
    d=distance2(unit(q),unit(v))
    print(name,'raw d2 / cosine / unit d2 / 2-2cos',
          round(distance2(q,v),6),round(c,6),round(d,6),round(2-2*c,6))
print('raw winner',min(candidates,key=lambda n:distance2(q,candidates[n])))
print('cosine winners',cosine_rank(q,candidates)[0])
print('zero candidate report',cosine_rank(q,{'Z':[0,0],'B':[3,0]}))
print('only zero candidate: no comparison',cosine_rank(q,{'Z':[0,0]}))
print('perpendicular nonzero cosine',round(cosine(q,[-4,3]),6))
print('positive/negative scaling cosines',round(cosine(q,[6,8]),6),round(cosine(q,[-3,-4]),6))
print('same unit vector, different totals',sum(q),sum(candidates['A']))
# Caller supplies finite moderate components and the intended candidate roles.
# Per-vector normalization fits no dataset mean or spread. No task-quality score is supplied.
