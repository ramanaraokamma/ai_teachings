"""Count supplied query runs and plant groups; no experiment or model training."""
from collections import Counter
from copy import deepcopy
query_runs=[{'query_id':'Q'+str(q),'run':r} for q in range(1,4) for r in range(1,5)]
assert len(query_runs)==12 and len({row['query_id'] for row in query_runs})==3
views=[{'view_id':f'P{p}-v{v}','plant_id':f'P{p}'} for p in range(1,5) for v in range(1,4)]
before=deepcopy(views)
train_ids={'P1','P2'};eval_ids={'P3','P4'}
train=[row for row in views if row['plant_id'] in train_ids]
evaluation=[row for row in views if row['plant_id'] in eval_ids]

def audit_split(train,evaluation):
 for rows in (train,evaluation):
  if type(rows) is not list or not rows:raise ValueError('two nonempty view-record lists required')
  for row in rows:
   if type(row) is not dict or set(row)!={'view_id','plant_id'} or any(type(v) is not str or not v for v in row.values()):
    raise ValueError('exact nonempty view/plant metadata required')
 all_rows=train+evaluation
 if not all_rows or len({r['view_id'] for r in all_rows})!=len(all_rows):
  raise ValueError('nonempty unique view identities across split required')
 train_plants={r['plant_id'] for r in train};eval_plants={r['plant_id'] for r in evaluation}
 return {'train_views':len(train),'eval_views':len(evaluation),'distinct_plants':len(train_plants|eval_plants),
         'train_plants':sorted(train_plants),'eval_plants':sorted(eval_plants),
         'shared_plants':sorted(train_plants&eval_plants),
         'disjoint_for_new_plant_goal':not bool(train_plants&eval_plants),
         'independence':'not established from IDs alone'}
valid=audit_split(train,evaluation)
assert valid['train_views']==valid['eval_views']==6 and valid['shared_plants']==[]
# Move one actual view, rather than duplicate it: plant identity still crosses the boundary.
moved=next(r for r in train if r['view_id']=='P1-v1')
leaky_train=[r for r in train if r['view_id']!='P1-v1']
leaky_eval=evaluation+[moved]
leaky=audit_split(leaky_train,leaky_eval)
assert leaky['train_views']==5 and leaky['eval_views']==7 and leaky['shared_plants']==['P1']
assert not leaky['disjoint_for_new_plant_goal'] and views==before
print('Main query measurements:',len(query_runs),'distinct query contexts:',len({r['query_id'] for r in query_runs}))
print('Picture four plant IDs, views per plant:',dict(Counter(r['plant_id'] for r in views)))
print('Group-correct split:',valid)
print('One P1 view moved into evaluation:',leaky)
print('No actual images, classifier runs, randomized assignments or human responses are used. Disjoint IDs check leakage for this declared goal, not independence, representativeness or broad new-plant reliability.')
