"""Exact expected-value/error tests for two supplied pure components."""
def remaining(capacity,used):
    if type(capacity) is not int or type(used) is not int:
        raise ValueError('capacity/used type')
    if not 0<=used<=capacity:
        raise ValueError('capacity/used range')
    return capacity-used

def room_label(number):
    if type(number) is not int or number<=0:
        raise ValueError('positive room number')
    return 'Room '+str(number)

def check(function,args,expected):
    try:
        actual=('value',function(*args))
    except ValueError:
        actual=('error','ValueError')
    return {'input':args,'expected':expected,'actual':actual,'passed':actual==expected}

cases=[((12,5),('value',7)),((12,12),('value',0)),((0,0),('value',0)),
       ((12,13),('error','ValueError')),((12,-2),('error','ValueError')),
       ((12,'5'),('error','ValueError')),((True,0),('error','ValueError'))]
records=[check(remaining,args,expected) for args,expected in cases]
for record in records:print('Remaining:',record)
assert all(r['passed'] for r in records)
formatter=[check(room_label,(7,),('value','Room 7')),
           check(room_label,(12,),('value','Room 12')),
           check(room_label,(0,),('error','ValueError'))]
for record in formatter:print('Formatter:',record)
assert all(r['passed'] for r in formatter)
assert remaining(12,5)==remaining(12,5)  # repeated call, not new service evidence
# Finite property sweep, not an exhaustive proof for every integer.
for capacity in range(9):
    for used in range(capacity+1):
        value=remaining(capacity,used)
        assert 0<=value<=capacity and value+used==capacity
# Deliberate wrong copy: tests should detect a changed outcome.
def off_by_one(capacity,used):
    return capacity-used-1
fault=check(off_by_one,(12,5),('value',7))
assert not fault['passed'] and fault['actual']==('value',6)
print('Deliberate defect detected:',fault)
print('Unit cases do not test live room data, authorization, network, model or full integration.')
