"""Sequential in-memory effect stubs and trusted approval fixtures; no sending."""
from copy import deepcopy

class MockLedger:
    def __init__(self,trusted_approvals):
        self._approvals=deepcopy(trusted_approvals)
        self.committed={}
        self.effects=[]

    def submit(self,actor, key,payload,approval_id):
        if any(type(v) is not str or not v for v in [actor, key,approval_id]):
            raise ValueError('invalid actor, key or approval identifier')
        if (type(payload) is not dict or set(payload)!={'operation','version','destination','body'}
            or any(type(v) is not str or not v for v in payload.values())):
            raise ValueError('invalid payload schema')
        approval=self._approvals.get(approval_id)
        expected={'actor':actor,'key':key,'payload':payload}
        if approval!=expected:
            raise PermissionError('matching trusted approval required')
        slot=(actor, key)
        if slot in self.committed:
            original,result=self.committed[slot]
            if original!=payload:raise ValueError('idempotency payload conflict')
            return deepcopy(result)
        result={'operation_id':key,'status':'committed_stub'}
        # This appends a local record only; no provider effect is executed.
        self.effects.append(deepcopy(payload))
        self.committed[slot]=(deepcopy(payload),deepcopy(result))
        return deepcopy(result)

payload={'operation':'send','version':'v1','destination':'D','body':'fictional message'}
changed={**payload,'version':'v2'}
approvals={'A1':{'actor':'operator','key':'K','payload':payload},
           'A2':{'actor':'operator','key':'K','payload':changed}}
ledger=MockLedger(approvals)
first=ledger.submit('operator','K',payload,'A1')
retry=ledger.submit('operator','K',dict(payload),'A1')
assert first==retry and len(ledger.effects)==1
print('Same approved operation retried:',first,retry,'effect stubs:',len(ledger.effects))
try:ledger.submit('operator','K',changed,'A1')
except PermissionError:print('Changed version with old approval rejected before another effect.')
else:raise AssertionError('Stale approval accepted')
try:ledger.submit('operator','K',changed,'A2')
except ValueError:print('Same key/different approved payload rejected as an idempotency conflict.')
else:raise AssertionError('Payload conflict accepted')
for actor, key,approval_id in [('other-actor','K','A1'),('operator','K2','A1')]:
    try:ledger.submit(actor, key,payload,approval_id)
    except PermissionError:pass
    else:raise AssertionError('Approval borrowed for a different actor or operation key')
first['status']='changed returned copy'
assert ledger.submit('operator','K',payload,'A1')['status']=='committed_stub'
assert len(ledger.effects)==1
# Separate desk picture, its own exact approval and operation.
desk={'operation':'reserve','version':'v1','destination':'desk4','body':'fictional desk request'}
desk_ledger=MockLedger({'D1':{'actor':'desk-operator','key':'K9','payload':desk}})
desk_ledger.submit('desk-operator','K9',desk,'D1')
desk_ledger.submit('desk-operator','K9',desk,'D1')
try:desk_ledger.submit('desk-operator','K10',{**desk,'destination':'desk5'},'D1')
except PermissionError:pass
else:raise AssertionError('Desk5 borrowed desk4 approval')
assert len(desk_ledger.effects)==1
print('Separate desk K9 duplicates:',len(desk_ledger.effects),'stub; K10 denied')
# A new process/ledger instance has no remembered commits in this in-memory mock.
restarted=MockLedger(approvals)
restarted.submit('operator','K',payload,'A1')
assert len(ledger.effects)+len(restarted.effects)==2
print('Fresh in-memory ledger forgets the old commit; two instances recorded two separate stubs.')
print('No real actor verification, approval signature, persistence, concurrency safety, delivery or crash-safe exactly-once guarantee.')
