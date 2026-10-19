"""Pure sandbox-policy/quota decisions on fixtures, not an actual sandbox."""
from math import isfinite

MAIN_PAIRS=frozenset({('read','fixtures'),('write','outputs')})
def permitted(operation,resource):
    # Abstract resource handles, not filesystem paths or network addresses.
    return type(operation) is str and type(resource) is str and (operation,resource) in MAIN_PAIRS

def admit_batch(queued,additional,maximum=10):
    if any(type(v) is not int or v<0 for v in [queued,additional,maximum]) or queued>maximum:
        raise ValueError('invalid queue counts')
    projected=queued+additional
    return {'admit':projected<=maximum,'current':queued,'additional':additional,
            'projected':projected,'maximum':maximum,'policy':'all-or-nothing'}

def audit_picture(elapsed_s,output_bytes,network_attempted):
    if (type(elapsed_s) not in (int,float) or not isfinite(elapsed_s) or elapsed_s<0
        or type(output_bytes) is not int or output_bytes<0 or type(network_attempted) is not bool):
        raise ValueError('invalid supplied trial measurements')
    violations=[]
    if network_attempted:violations.append('network prohibited')
    if elapsed_s>2:violations.append('time limit exceeded')
    if output_bytes>20_000_000:violations.append('output limit exceeded')
    return {'within_declared_limits':not violations,'violations':violations}

requests=[('read','fixtures'),('write','outputs'),('network','public_web'),
          ('write','outside'),('write','fixtures')]
assert [permitted(op,res) for op,res in requests]==[True,True,False,False,False]
print('Main abstract operation/resource decisions:',[(op,res,permitted(op,res)) for op,res in requests])
assert admit_batch(8,2)['admit'] and not admit_batch(8,3)['admit']
print('Main queue admission fixtures:',admit_batch(8,2),admit_batch(8,3))
a=audit_picture(1,2_000_000,False)
b=audit_picture(1,2_000_000,True)
slow=audit_picture(3,2_000_000,False)
assert a['within_declared_limits'] and b['violations']==['network prohibited']
assert slow['violations']==['time limit exceeded']
assert audit_picture(2,20_000_000,False)['within_declared_limits']
assert audit_picture(2,20_000_001,False)['violations']==['output limit exceeded']
print('Separate picture A/B/changed A:',a,b,slow)
print('Unit convention: 1 MB = 1,000,000 bytes; 2 seconds and 20 MB are inclusive maxima.')
print('No job is executed, queued, stopped or isolated. No file/network operation or timer is used.')
print('These checks do not resolve paths/symlinks, atomically reserve queue space, or prove isolation or output truth.')
