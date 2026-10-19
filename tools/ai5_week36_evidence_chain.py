"""Replay the supplied capstone evidence chain; no population claim."""
train=[(1,2),(2,4)]
validation=[(3,6),(4,8)]
final=[(5,10),(6,12),(-1,-2),(-2,-4)]
def predict(weight,x):return max(0,weight*x)
def mse(weight,rows):return sum((predict(weight,x)-y)**2 for x,y in rows)/len(rows)
records=[]
for rate in [.1,.2]:
    weight=1.0
    history=[]
    for update in [1,2]:
        assert all(weight*x>0 for x,_ in train)
        gradient=sum(2*(weight*x-y)*x for x,y in train)/len(train)
        weight-=rate*gradient
        history.append((update,gradient,weight))
    records.append({'rate':rate,'history':history,'weight':weight,
                    'validation_mse':mse(weight,validation)})
selected=min(records,key=lambda r:(r['validation_mse'],r['rate']))
frozen_weight=selected['weight']
assert frozen_weight==2 and selected['rate']==.2
# No updates or choices below this point use the final targets.
final_ledger=[(x,y,predict(1,x),predict(frozen_weight,x),
               (predict(1,x)-y)**2,(predict(frozen_weight,x)-y)**2)
              for x,y in final]
baseline_mse=mse(1,final)
candidate_mse=mse(frozen_weight,final)
negative_mse=mse(frozen_weight,[(x,y) for x,y in final if x<0])
assert (baseline_mse,candidate_mse,negative_mse)==(20.25,5,10)
print('Validation selection records:',records)
print('Frozen final: x,target,baseline,candidate,baseline squared error,candidate squared error',final_ledger)
print('Final MSE baseline/candidate:',baseline_mse,candidate_mse)
print('Negative-input MSE, 2 rows:',negative_mse)
print('Scope: two positive validation rows; four constructed final rows.')
print('Unmeasured: timing, energy, fitted-line comparison, independent revised-model performance.')
# Separate supported comparison: not the main scores.
absolute=8-2;relative=absolute/8
assert (absolute,relative)==(6,.75)
print('Separate supported reduction:',absolute,'MSE units;',100*relative,'% relative MSE reduction')
# Pictured neuron: an activation, not a probability or an accuracy percentage.
def neuron(second):
    z=2*.5+second*(-1)+.2
    return z,max(0,z)
assert abs(neuron(1)[0]-.2)<1e-12 and neuron(2)[1]==0
print('Picture original z/output:',neuron(1),'changed:',neuron(2))
