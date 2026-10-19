"""Matched supplied regression experiments; final cases remain absent."""
train=[('T1',1,2),('T2',2,4)]
validation=[('V1',3,6),('V2',4,8)]
def predict(a,x):return max(0,a*x)
def mse(a,rows):
    if not rows:raise ValueError('Need evaluated rows')
    return sum((predict(a,x)-y)**2 for _,x,y in rows)/len(rows)
def fit(rate,updates=2):
    if rate<=0 or type(updates) is not int or updates<=0:
        raise ValueError('Need positive rate and integer update count')
    a=1.0
    history=[]
    for update in range(1,updates+1):
        if any(a*x<=0 for _,x,_ in train):
            raise ValueError('Restricted gradient needs positive preactivations')
        before=a
        gradient=sum(2*(a*x-y)*x for _,x,y in train)/len(train)
        a-=rate*gradient
        history.append((update,before,gradient,a,mse(a,train),mse(a,validation)))
    return {'rate':rate,'weight':a,'history':history,'validation_mse':mse(a,validation)}
runs=[fit(.1),fit(.2)]
selected=min(runs,key=lambda r:(r['validation_mse'],r['rate']))
assert [[r[3] for r in run['history']] for run in runs]==[[1.5,1.75],[2,2]]
assert [r['validation_mse'] for r in runs]==[.78125,0]
assert selected['rate']==.2
print('Baseline train/validation MSE:',mse(1,train),mse(1,validation))
for run in runs:
    print('Rate:',run['rate'],'history update,before,gradient,after,train MSE,valid MSE:',run['history'])
    print('Validation ID,prediction,squared error:',
          [(name,predict(run['weight'],x),(predict(run['weight'],x)-y)**2)
           for name,x,y in validation])
print('Selected using two distinct validation rows:',selected['rate'])
# Supported .3 probe is outside the prespecified .1/.2 candidate set.
probe=fit(.3)
assert [r[3] for r in probe['history']]==[2.5,1.75]
print('Supported .3 path, not a selection candidate:',probe['history'])
# Separate supplied picture entries are correctness flags, not class predictions.
a_flags=[1,1,0,1,0,1];b_flags=[1,1,1,1,0,1]
assert sum(a_flags)==4 and sum(b_flags)==5
print('Pictured changed case IDs:',[i+1 for i,(a,b) in enumerate(zip(a_flags,b_flags)) if a!=b])
print('Final evaluation not opened; no speed or seed-variation measurement.')
