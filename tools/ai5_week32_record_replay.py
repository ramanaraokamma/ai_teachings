"""Replay the supplied toy run; emit an in-memory record, not a final test."""
import hashlib
import json
import platform

def content_hash(value):
    payload=json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

manifest=[{'id':'T1','role':'training','x':1.0,'target':2.0},
          {'id':'T2','role':'training','x':2.0,'target':4.0},
          {'id':'V1','role':'validation','x':3.0,'target':6.0}]
config={'run_id':'NN32-A','architecture':'ReLU(a*x); no bias',
        'initial_weight':1.0,'learning_rate':.1,'full_batch_updates':2,
        'loss':'mean squared error','preprocessing':'none',
        'random_operations':'none',
        'selection':'minimum validation MSE, earlier update wins ties'}

def predict(a,x):
    return max(0.0,a*x)

def mse(a,rows):
    if not rows:
        raise ValueError('MSE needs at least one row')
    return sum((predict(a,r['x'])-r['target'])**2 for r in rows)/len(rows)

def replay(data,config):
    training=[r for r in data if r['role']=='training']
    validation=[r for r in data if r['role']=='validation']
    if not training or not validation:
        raise ValueError('Need separate training and validation rows')
    if len({r['id'] for r in data})!=len(data):
        raise ValueError('Duplicate data ID')
    a=config['initial_weight']
    baseline={'weight':a,'training_mse':mse(a,training),
              'validation_mse':mse(a,validation)}
    checkpoints=[]
    for update in range(1,config['full_batch_updates']+1):
        # This deliberately restricted gradient requires all training a*x > 0.
        if any(a*r['x']<=0 for r in training):
            raise ValueError('Outside the supplied positive-preactivation gradient')
        gradient=sum(2*(a*r['x']-r['target'])*r['x'] for r in training)/len(training)
        a-=config['learning_rate']*gradient
        predictions=[{'id':r['id'],'role':r['role'],
                      'prediction':predict(a,r['x']),
                      'squared_error':(predict(a,r['x'])-r['target'])**2}
                     for r in data]
        checkpoints.append({'update':update,'gradient_before':gradient,'weight':a,
                            'training_mse':mse(a,training),
                            'validation_mse':mse(a,validation),
                            'prediction_rows':predictions})
    selected=min(checkpoints,key=lambda r:(r['validation_mse'],r['update']))
    return {'baseline':baseline,'checkpoints':checkpoints,
            'selected_update':selected['update'],
            'selected_weight':selected['weight']}

result=replay(manifest,config)
assert result['baseline']['validation_mse']==9
assert [(r['weight'],r['training_mse'],r['validation_mse'])
        for r in result['checkpoints']]==[(1.5,.625,2.25),(1.75,.15625,.5625)]
assert result==replay(manifest,config)  # replay, not new independent evidence
record={'config':config,'data_manifest':manifest,'data_sha256':content_hash(manifest),
        'config_sha256':content_hash(config),'python_version':platform.python_version(),
        'result':result,'final_evaluation':'not measured','runtime':'not measured',
        'peak_memory':'not measured','energy':'not measured',
        'provenance':'constructed classroom regression rows'}
print(json.dumps(record,indent=2))
# A hash detects changed serialized content; it does not establish label quality.
changed=[dict(r) for r in manifest]
changed[-1]['target']=7.0
assert content_hash(changed)!=content_hash(manifest)
assert content_hash(manifest)==record['data_sha256']
print('Changed validation target detected; original manifest retained.')
# Save the exact code separately with its own hash when creating an actual run folder.
