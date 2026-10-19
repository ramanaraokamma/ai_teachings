"""Declared comparison controls and a deliberately paper-only toy rule."""
from collections import Counter
from copy import deepcopy
A={'method':'A','corpus':'c1','queries':['Q1','Q2','Q3'],'cutoff':3,'rubric':'r1','environment':'toy-local'}
B={'method':'B','corpus':'c2','queries':['Q4','Q5','Q6'],'cutoff':3,'rubric':'r1','environment':'toy-local'}
def unintended_changes(a,b):
 fields={'method','corpus','queries','cutoff','rubric','environment'}
 if type(a) is not dict or type(b) is not dict or set(a)!=fields or set(b)!=fields:
  raise ValueError('complete declared control records required')
 return [field for field in ['corpus','queries','cutoff','rubric','environment'] if a[field]!=b[field]]
main_changes=unintended_changes(A,B)
matched_B={**deepcopy(A),'method':'B'}
assert main_changes==['corpus','queries'] and unintended_changes(A,matched_B)==[]
# Separate picture metadata: H1 and S1 recur; these four rows are not four leaf objects.
original=[{'leaf_id':'H1','condition':'healthy','paper':'white'},
          {'leaf_id':'S1','condition':'spotted','paper':'blue'}]
crossed=[{'leaf_id':leaf,'condition':condition,'paper':paper}
         for leaf,condition in [('H1','healthy'),('S1','spotted')] for paper in ['white','blue']]
COMBINATIONS={(condition,paper) for condition in ['healthy','spotted'] for paper in ['white','blue']}
def design_cells(rows):
 if type(rows) is not list or not rows:raise ValueError('nonempty supplied metadata required')
 cells=Counter()
 for row in rows:
  if type(row) is not dict or set(row)!={'leaf_id','condition','paper'}:
   raise ValueError('exact leaf/condition/paper metadata required')
  if type(row['leaf_id']) is not str or not row['leaf_id'] or (row['condition'],row['paper']) not in COMBINATIONS:
   raise ValueError('declared leaf and cell values required')
  cells[(row['condition'],row['paper'])]+=1
 return {'cells':dict(cells),'missing_cells':sorted(COMBINATIONS-set(cells)),
         'records':len(rows),'leaf_ids':len({r['leaf_id'] for r in rows})}
def paper_only_rule(paper):
 if paper not in ('white','blue'):raise ValueError('known paper fixture required')
 return 'healthy' if paper=='white' else 'spotted'
def evaluate_rule(rows):
 design_cells(rows)
 return [{'leaf_id':r['leaf_id'],'condition':r['condition'],'paper':r['paper'],
          'prediction':paper_only_rule(r['paper']),'correct':paper_only_rule(r['paper'])==r['condition']} for r in rows]
before=deepcopy(crossed)
original_cells=design_cells(original);crossed_cells=design_cells(crossed)
original_results=evaluate_rule(original);crossed_results=evaluate_rule(crossed)
assert len(original_cells['missing_cells'])==2 and crossed_cells['missing_cells']==[]
assert sum(r['correct'] for r in original_results)==2 and sum(r['correct'] for r in crossed_results)==2
assert len(crossed_results)==4 and crossed_cells['leaf_ids']==2 and crossed==before
print('Main unintended declared changes:',main_changes,'matched-design fields:',unintended_changes(A,matched_B))
print('Original versus crossed cells:',original_cells,crossed_cells)
print('Deliberately paper-only rule on coupled records:',original_results)
print('Same toy rule on crossed records:',crossed_results)
print('The rule fits original2/2 yet only2/4 crossed, illustrating an alternative explanation. It does not reveal what an actual trained model uses internally.')
print('All conditions/labels are supplied fictional metadata. No photos, collection, classifier training, randomization, network timings or real causal experiment is performed. Matching listed fields does not prove all confounders controlled.')
