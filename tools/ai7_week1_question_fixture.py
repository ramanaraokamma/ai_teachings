"""Added constructed retrieval snapshot for a bounded research question, no live retrieval."""
from fractions import Fraction
CORPUS={'R'+str(i) for i in range(1,11)}
# Relevance labels are a supplied classroom rubric, not real annotator judgments.
RELEVANT={'Q1':{'R1','R2'},'Q2':{'R3'},'Q3':{'R4','R5'},'Q4':{'R6'},'Q5':{'R7','R8'}}
A={'Q1':['R1','R9','R10'],'Q2':['R3','R9','R10'],'Q3':['R4','R9','R10'],
   'Q4':['R6','R9','R10'],'Q5':['R7','R9','R10']}
B={'Q1':['R1','R2','R9'],'Q2':['R3','R9','R10'],'Q3':['R4','R5','R9'],
   'Q4':['R9','R10','R8'],'Q5':['R7','R8','R10']}

def score_snapshot(ranking,labels,corpus,cutoff=3):
 if type(cutoff) is not int or cutoff!=3:raise ValueError('this classroom protocol fixes cutoff at exactly three')
 if not ranking or set(ranking)!=set(labels):raise ValueError('matched nonempty query IDs and supplied labels required')
 counts={}
 for query,ids in ranking.items():
  if type(ids) is not list or len(ids)!=cutoff or len(set(ids))!=cutoff or not set(ids)<=corpus:
   raise ValueError('exact unique eligible top-k records required')
  if type(labels[query]) is not set or not labels[query]<=corpus:raise ValueError('eligible relevance set required')
  counts[query]=sum(rid in labels[query] for rid in ids)
 return {'counts':counts,'mean_relevant_in_top3':Fraction(sum(counts.values()),len(counts)),
         'queries':len(counts),'cutoff':cutoff}
a=score_snapshot(A,RELEVANT,CORPUS);b=score_snapshot(B,RELEVANT,CORPUS)
assert list(a['counts'].values())==[1,1,1,1,1] and list(b['counts'].values())==[2,1,2,0,2]
assert a['mean_relevant_in_top3']==1 and b['mean_relevant_in_top3']==Fraction(7,5)
assert b['counts']['Q4']<a['counts']['Q4']
print('Bounded question: On these five fixed queries, with corpus c1 and supplied relevance rules, does B return more relevant records in the top three on average than A?')
print('Added constructed snapshot A:',a,'B:',b)
print('B has larger mean here, but worsens Q4; no universal usefulness, causal mechanism, deployment impact or learner outcome follows.')
print('All rankings and labels are supplied fictional inputs; no retriever, model, child, human annotator or experiment was run. These revealed cases are practice, not a fresh reserved evaluation.')
