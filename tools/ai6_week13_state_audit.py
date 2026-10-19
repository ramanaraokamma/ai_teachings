"""Explicit state transitions and lookup-entry budgets; no real agent/tools."""
BASE={'ready':{'looking_up'},'looking_up':{'review','done'},
      'review':{'done'},'done':set()}

def step(state,target,attempts,policy,maximum=2,authorized_review_evidence=False):
    if (type(attempts) is not int or attempts<0 or type(maximum) is not int
        or maximum<=0 or attempts>maximum or type(authorized_review_evidence) is not bool):
        raise ValueError('invalid counter or evidence flag')
    if type(state) is not str or type(target) is not str:
        raise ValueError('state names must be strings')
    if state not in policy or target not in policy.get(state,set()):
        raise ValueError('transition not declared')
    if state=='review' and target=='done' and not authorized_review_evidence:
        raise ValueError('authorized review evidence required')
    next_attempts=attempts+int(target=='looking_up')
    if next_attempts>maximum:raise ValueError('lookup-entry budget exhausted')
    return target,next_attempts

def audit(path,policy=BASE,maximum=2,authorized_review_evidence=False):
    if not path or path[0]!='ready':raise ValueError('trace must start ready')
    state='ready';attempts=0;prefix=['ready']
    for index,target in enumerate(path[1:],1):
        before=state
        try:state,attempts=step(state,target,attempts,policy,maximum,authorized_review_evidence)
        except ValueError as error:
            return {'valid':False,'complete':False,'first_invalid_step':index,
                    'from':before,'to':target,'reason':str(error),
                    'accepted_prefix':prefix,'lookup_entries':attempts}
        prefix.append(state)
    return {'valid':True,'complete':state=='done','accepted_prefix':prefix,
            'lookup_entries':attempts}

proposed=['ready','looking_up','review','looking_up','done']
original=audit(proposed)
assert not original['valid'] and original['first_invalid_step']==3
assert original['lookup_entries']==1 and original['reason']=='transition not declared'
print('Main invalid proposal, original graph:',original)
waiting=audit(['ready','looking_up','review'])
assert waiting['valid'] and not waiting['complete']
without_evidence=audit(['ready','looking_up','review','done'])
with_evidence=audit(['ready','looking_up','review','done'],authorized_review_evidence=True)
assert not without_evidence['valid'] and with_evidence['valid'] and with_evidence['complete']
print('Valid but incomplete prefix:',waiting)
print('Review completion without/with supplied authorized-evidence flag:',without_evidence,with_evidence)
# Explicit graph revision: do not mutate the original or reset the counter.
revised={state:set(targets) for state,targets in BASE.items()}
revised['review'].add('looking_up')
revised_trace=audit(proposed,policy=revised)
assert revised_trace['valid'] and revised_trace['lookup_entries']==2
third=['ready','looking_up','review','looking_up','review','looking_up','done']
exhausted=audit(third,policy=revised)
assert not exhausted['valid'] and exhausted['reason']=='lookup-entry budget exhausted'
assert BASE['review']=={'done'}
print('Separately revised graph permits two entries:',revised_trace)
print('Third entry denied even with revised arrow:',exhausted)
assert not audit(['ready','looking_up','done','looking_up'])['valid']
# Separate picture checks finite parcel paths, not parcel data or an autonomous loop.
parcel={'idle':{'querying'},'querying':{'checking'},'checking':{'complete'},'complete':set()}
def parcel_path(path,arrows):
    return bool(path) and path[0]=='idle' and path[-1]=='complete' and all(b in arrows.get(a,set()) for a,b in zip(path,path[1:]))
assert parcel_path(['idle','querying','checking','complete'],parcel)
assert not parcel_path(['idle','querying','complete'],parcel)
parcel_retry={state:set(targets) for state,targets in parcel.items()}
parcel_retry['checking'].add('querying')
assert not parcel_path(['idle','querying','complete'],parcel_retry)
print('Parcel retry arrow does not authorize querying directly to complete.')
print('Local trace audit only. Evidence flag is a supplied trusted fixture, not real evidence verification; no actual lookup occurs.')
