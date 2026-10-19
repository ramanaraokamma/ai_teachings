"""Sequential in-memory queue model; no durable store, broker or real effects."""
from copy import deepcopy

class MockWorker:
    def __init__(self, saved=None):
        self.jobs=deepcopy(saved or {})
        self.effects=[]
        self.deliveries=0
        self.acks=[]
    def accept(self,job_id,payload):
        if type(job_id) is not str or not job_id or type(payload) is not dict:
            raise ValueError('nonempty job ID and dictionary payload required')
        if job_id in self.jobs:
            if self.jobs[job_id]['payload']!=payload:raise ValueError('same ID has conflicting payload')
        else:self.jobs[job_id]={'payload':deepcopy(payload),'state':'pending','result':None}
        return {'job_id':job_id,'state':self.jobs[job_id]['state']}
    def deliver(self,job_id,*,crash_after_commit=False):
        self.deliveries+=1
        job=self.jobs.get(job_id)
        if job is None:return {'status':'review','reason':'unknown ID; reconcile first'}
        if job['state']=='completed':
            self.acks.append(job_id)
            return {'status':'return_existing','result':deepcopy(job['result'])}
        if job['state']!='pending':return {'status':'review','reason':'not a new pending job'}
        job['state']='running'
        # One indivisible classroom step represents a checked result plus recorded commit.
        # Real effect/status atomicity is an assumption, not implemented by this dictionary.
        result={'artifact':'checked fictional output for '+job_id}
        self.effects.append(job_id)
        job.update(state='completed',result=result)
        if crash_after_commit:return {'status':'simulated_crash_before_ack'}
        self.acks.append(job_id)
        return {'status':'completed','result':deepcopy(result)}

worker=MockWorker();payload={'task':'fictional conversion'}
accepted=worker.accept('J',payload)
assert accepted['state']=='pending' and worker.effects==[]
first=worker.deliver('J',crash_after_commit=True)
assert worker.jobs['J']['state']=='completed' and worker.acks==[]
# Copy a declared saved snapshot into another worker: no persistence is actually tested.
saved=deepcopy(worker.jobs);recovered=MockWorker(saved)
second=recovered.deliver('J')
assert second['status']=='return_existing' and recovered.effects==[] and recovered.acks==['J']
assert worker.effects==['J'] and worker.deliveries+recovered.deliveries==2
print('Main accepted:',accepted,'first delivery:',first,'redelivery:',second)
print('Two modeled deliveries; one original mock effect; redelivery adds zero effects.')
unknown=recovered.deliver('unknown')
assert unknown['status']=='review' and recovered.effects==[]
try:recovered.accept('J',{'task':'different'})
except ValueError:pass
else:raise AssertionError('conflicting ID accepted')
# A running snapshot cannot establish whether an external effect committed.
uncertain=MockWorker({'U':{'payload':{},'state':'running','result':None}})
assert uncertain.deliver('U')['status']=='review' and uncertain.effects==[]
# Losing all history makes prior completion unrecognizable: do not call this durable dedup.
lost=MockWorker();lost.accept('J',payload);lost.deliver('J')
assert len(worker.effects)+len(lost.effects)==2
# Separate pictured vocabulary; observed failure before checked output supplied explicitly.
picture_history=[{'id':'J12','state':'queued'},{'id':'J12','state':'running'},
                 {'id':'J12','state':'failed','reason':'observed crash before checked output'}]
assert all(item['state']!='succeeded' for item in picture_history)
print('Picture observed-failure history:',picture_history)
print('An unobserved crash may leave running/stale status; reconcile rather than invent failure or success.')
print('Pending/queued and completed/succeeded are paired classroom terms, not extra states in one machine.')
print('Sequential copied fixtures do not implement durability, atomic commits, concurrency, broker ordering, retries or exactly-once delivery.')
