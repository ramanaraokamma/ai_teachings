"""Controlled integration fixtures and recorded adapter calls; no network."""
ACCESS={'S':'student','T':'teacher'}
DATA={'S':{'source_id':'S','room_id':'B','capacity':12},
      'T':{'source_id':'T','room_id':'STAFF','capacity':4}}

def storage_fixture(mode='normal'):
    calls=[]
    def lookup(key):
        calls.append(key)
        if mode=='missing':return None
        if mode=='failure':raise RuntimeError('mock dependency failed')
        return dict(DATA[key])
    return lookup,calls

def permitted(role,key):
    return role in ('student','teacher') and key in ACCESS and (role=='teacher' or ACCESS[key]=='student')

def service(request,role,lookup,events):
    events.append('validate_request')
    if type(request) is not dict or set(request)!={'source_id'} or type(request['source_id']) is not str:
        return {'status':'invalid_request'}
    key=request['source_id']
    events.append('authorize')
    if not permitted(role,key):return {'status':'denied'}
    events.append('lookup')
    try:record=lookup(key)
    except RuntimeError:return {'status':'review','reason':'dependency failure'}
    if record is None:return {'status':'review','reason':'missing source'}
    events.append('draft_stub')
    output=dict(record)  # local stub, not a model-generated answer
    events.append('validate_response')
    if (set(output)!={'source_id','room_id','capacity'} or output['source_id']!=key
        or type(output['room_id']) is not str or not output['room_id']
        or type(output['capacity']) is not int or output['capacity']<0):
        return {'status':'review','reason':'response/source mismatch'}
    return {'status':'answered',**output}

lookup,calls=storage_fixture();events=[]
denied=service({'source_id':'T'},'student',lookup,events)
assert denied=={'status':'denied'} and calls==[] and 'lookup' not in events
print('Correct denied result AND empty lookup trace:',denied,calls,events)
# Deliberate broken order: a final refusal does not undo earlier fixture access.
bad_lookup,bad_calls=storage_fixture()
def broken_order(request,role,lookup):
    lookup(request['source_id'])
    return {'status':'denied'} if not permitted(role,request['source_id']) else {'status':'unverified'}
bad=broken_order({'source_id':'T'},'student',bad_lookup)
assert bad==denied and bad_calls==['T']
print('Deliberate hidden failure detected: same denial but lookup calls:',bad_calls)
trials={}
for mode in ['normal','missing','failure']:
    lookup,calls=storage_fixture(mode);events=[]
    result=service({'source_id':'S'},'student',lookup,events)
    trials[mode]=(result,calls,events)
    print(mode,result,calls,events)
assert trials['normal'][0]=={'status':'answered','source_id':'S','room_id':'B','capacity':12}
assert all('draft_stub' not in trials[m][2] for m in ['missing','failure'])
# Separate pictured catalogue adapter and identifier agreement.
catalogue={'M':'map','N':'notebook'}
def catalogue_reply(requested,returned):
    if returned!=requested:return {'status':'review','reason':'adapter identifier mismatch'}
    return {'status':'answered','source_id':returned,'item':catalogue[returned]}
assert catalogue_reply('N','N')=={'status':'answered','source_id':'N','item':'notebook'}
assert catalogue_reply('N','M')['status']=='review'
print('Catalogue correct/wrong adapter:',catalogue_reply('N','N'),catalogue_reply('N','M'))
print('These mock interactions do not measure live provider availability, model behaviour or all runtime failures.')
