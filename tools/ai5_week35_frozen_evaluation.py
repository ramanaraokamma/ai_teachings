"""Supplied frozen-case evaluation; never use this script to tune the candidate."""
final=[('F1',5,10),('F2',6,12),('F3',-1,-2),('F4',-2,-4)]
def predict(a,x):return max(0,a*x)
def evaluate(weight,rows):
    if not rows:raise ValueError('Need evaluated cases')
    ledger=[(name,x,y,predict(weight,x),(predict(weight,x)-y)**2)
            for name,x,y in rows]
    return ledger,sum(r[-1] for r in ledger)/len(ledger)
baseline,baseline_mse=evaluate(1,final)
candidate,candidate_mse=evaluate(2,final)
assert [r[-1] for r in baseline]==[25,36,4,16]
assert [r[-1] for r in candidate]==[0,0,4,16]
assert baseline_mse==20.25 and candidate_mse==5
assert candidate_mse<baseline_mse
negative=[r for r in final if r[1]<0]
positive=[r for r in final if r[1]>0]
assert evaluate(2,negative)[1]==10 and evaluate(2,positive)[1]==0
print('Frozen baseline:',baseline,'MSE:',baseline_mse)
print('Frozen candidate:',candidate,'MSE:',candidate_mse)
print('Candidate positive MSE:',evaluate(2,positive)[1], 'negative MSE:',evaluate(2,negative)[1])
print('Strict aggregate criterion passes; negative-target representational failure remains.')
# Proposed signed output: known-case regression check only, not fresh final evidence.
revision=[(name,2*x,(2*x-y)**2) for name,x,y in final]
assert all(error==0 for _,_,error in revision)
print('Hand-proposed signed-output check on already revealed rows:',revision)
print('Revision has not been independently fitted/selected/evaluated here.')
