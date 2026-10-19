"""Pre-experiment plan and baseline only; candidate and final results absent."""
import json
plan={'id':'CAP33-v1','question':'Does two-update fitting beat the initial-weight baseline?',
      'prediction':'max(0,a*x)','bias':False,'baseline_weight':1.0,
      'candidate_initial_weight':1.0,'learning_rate':.1,'updates':2,
      'batch':'full training set','loss':'MSE',
      'validation_rule':'candidate MSE strictly less than baseline MSE',
      'final_rule':'frozen candidate MSE strictly less than same baseline MSE',
      'candidate_result':'not run','final_result':'not measured'}
training=[('T1',1,2),('T2',2,4)]
validation=[('V1',3,6),('V2',4,8)]
ledger=[]
for name,x,y in validation:
    pred=max(0,plan['baseline_weight']*x)
    ledger.append((name,x,y,pred,pred-y,(pred-y)**2))
baseline_mse=sum(r[-1] for r in ledger)/len(ledger)
assert baseline_mse==12.5
print(json.dumps(plan,indent=2))
print('Training IDs:',[r[0] for r in training])
print('Validation: ID,x,target,prediction,error,squared error',ledger)
print('Baseline validation MSE:',baseline_mse,'denominator:',len(validation))
print('Candidate criterion: MSE <',baseline_mse,'on these same validation rows')
print('Candidate has not been fitted by this script; hypothesis remains untested.')
print('Final inputs/targets intentionally absent from this planning script.')
# Separate supported example, not the main baseline:
assert ((2-5)**2+(4-7)**2)/2==9
