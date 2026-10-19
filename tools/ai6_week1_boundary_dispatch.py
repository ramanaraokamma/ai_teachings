"""Local deterministic simulation of a read-only timetable service."""
from copy import deepcopy
SCHEDULE={'Tuesday':'16:00'}
SOURCE='public-schedule-classroom-v1'

def dispatch(operations,schedule):
    if not isinstance(operations,list) or not operations:
        raise ValueError('Need a nonempty list of structured operations')
    results=[]
    for operation in operations:
        if not isinstance(operation,dict) or not isinstance(operation.get('action'),str):
            raise ValueError('Every operation needs a string action')
        action=operation['action']
        # The contract only authorizes reads; requests cannot extend this allowlist.
        if action!='read_schedule':
            results.append({'action':action,'status':'out_of_scope'})
            continue
        day=operation.get('day')
        if not isinstance(day,str) or not day:
            raise ValueError('A schedule read needs a nonempty day string')
        if day not in schedule:
            results.append({'action':action,'day':day,'status':'review',
                            'reason':'No supplied schedule entry'})
        else:
            results.append({'action':action,'day':day,'status':'answered',
                            'time':schedule[day],'source':SOURCE})
    return results

before=deepcopy(SCHEDULE)
request=[{'action':'read_schedule','day':'Tuesday'},
         {'action':'move_schedule','day':'Tuesday','new_day':'Wednesday'}]
result=dispatch(request,SCHEDULE)
assert result[0]['time']=='16:00' and result[1]['status']=='out_of_scope'
assert dispatch([{'action':'read_schedule','day':'Wednesday'}],SCHEDULE)[0]['status']=='review'
assert dispatch([{'action':'email_user'}],SCHEDULE)[0]['status']=='out_of_scope'
assert SCHEDULE==before
print('Mixed request:',result)
print('Missing Wednesday:',dispatch([{'action':'read_schedule','day':'Wednesday'}],SCHEDULE))
print('Snapshot unchanged:',SCHEDULE==before)
print('Simulation only: no natural-language parser, network, authentication, email, edit or reviewer outcome.')
