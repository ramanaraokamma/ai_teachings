"""Virtual caller-wait arithmetic only: no sleep, network, remote abort or undo."""
from math import isfinite,isclose

def duration(value):
    return type(value) in (int,float) and isfinite(value) and value>=0

def waiting_bound(attempts,per_attempt,gaps):
    if type(attempts) is not int or attempts<1 or len(gaps)!=attempts-1:
        raise ValueError('invalid attempt budget/gap count')
    if not duration(per_attempt) or any(not duration(g) for g in gaps):
        raise ValueError('durations must be finite and nonnegative')
    return attempts*per_attempt+sum(gaps)

def simulate(outcomes,attempts,per_attempt,gaps,cancel_before_attempt=None):
    bound=waiting_bound(attempts,per_attempt,gaps)
    if cancel_before_attempt is not None and (type(cancel_before_attempt) is not int or not 1<=cancel_before_attempt<=attempts):
        raise ValueError('invalid cancellation boundary')
    elapsed=0;events=[]
    for index in range(attempts):
        number=index+1
        # This model only places cancellation before a next attempt/backoff begins.
        if number==cancel_before_attempt:
            return {'status':'cancelled','elapsed_s':elapsed,'events':events,'bound_s':bound}
        if index:
            elapsed+=gaps[index-1]
            events.append({'kind':'gap','seconds':gaps[index-1],'elapsed_s':elapsed})
        if index>=len(outcomes):raise ValueError('missing supplied outcome fixture')
        waited,status=outcomes[index]
        if (not duration(waited) or waited>per_attempt or
            status not in ('timeout','transient','success','auth_error','permission_error','invalid_request')):
            raise ValueError('invalid caller-wait outcome')
        if status=='timeout' and waited!=per_attempt:
            raise ValueError('timeout fixture must reach its declared wait cap')
        elapsed+=waited
        events.append({'kind':'attempt','number':number,'status':status,
                       'caller_wait_s':waited,'elapsed_s':elapsed})
        if status=='success':return {'status':'success','elapsed_s':elapsed,'events':events,'bound_s':bound}
        if status not in ('timeout','transient'):
            return {'status':'nonretryable','elapsed_s':elapsed,'events':events,'bound_s':bound}
    return {'status':'budget_exhausted','elapsed_s':elapsed,'events':events,'bound_s':bound}

main=simulate([(4,'timeout')]*3+[(.1,'success')],3,4,[1,2])
assert main['elapsed_s']==15 and main['status']=='budget_exhausted'
assert len([e for e in main['events'] if e['kind']=='attempt'])==3
print('Main virtual wait trace:',main)
picture=simulate([(1,'timeout'),(.4,'success')],2,1,[0])
cancelled=simulate([(1,'timeout'),(.4,'success')],2,1,[0],cancel_before_attempt=2)
assert picture['status']=='success' and isclose(picture['elapsed_s'],1.4)
assert cancelled['status']=='cancelled' and cancelled['elapsed_s']==1
assert len([e for e in cancelled['events'] if e['kind']=='attempt'])==1
print('Separate picture without cancellation:',picture)
print('Cancellation after first timeout:',cancelled)
nonretryable=simulate([(.2,'permission_error'),(.2,'success')],3,4,[1,2])
assert nonretryable['status']=='nonretryable' and nonretryable['elapsed_s']==.2
assert len(nonretryable['events'])==1
print('Non-transient failure stops immediately:',nonretryable)
print('Timeout/cancellation of caller waiting does not prove remote work stopped or a committed effect was undone.')
print('Only declared boundary cancellation is modeled; no real asynchronous cancellation, overhead or wall-clock measurement.')
