"""Local read-only plan audit; no model planning, booking, messaging or web calls."""
SAFE=['validate','retrieve','verify','answer']
PERMITTED=frozenset(SAFE)
SOURCE={'source_id':'ROOM-R','room_id':'B','capacity':12,'approved':True}

def run_plan(plan,request,source,events):
    if type(plan) is not list or any(type(step) is not str for step in plan):
        return {'status':'rejected_plan','reason':'invalid plan structure'}
    # Preflight rejects the entire unsafe proposal before any simulated step.
    if any(step not in PERMITTED for step in plan):
        return {'status':'rejected_plan','reason':'operation outside read-only scope'}
    if plan!=SAFE:
        return {'status':'rejected_plan','reason':'required order or stage missing'}
    validated=False;retrieved=None;verified=False
    for action in plan:
        if action not in PERMITTED:return {'status':'rejected_plan'}
        events.append(action)
        if action=='validate':
            if (type(request) is not dict or set(request)!={'room_id'}
                or type(request['room_id']) is not str or not request['room_id']):
                return {'status':'invalid_request'}
            validated=True
        elif action=='retrieve':
            if not validated:return {'status':'review','reason':'missing validation'}
            retrieved=source  # local injected fixture, not a network lookup
            if retrieved is None:return {'status':'review','reason':'missing approved evidence'}
            continue
        elif action=='verify':
            if (type(retrieved) is not dict or
                set(retrieved)!={'source_id','room_id','capacity','approved'} or
                retrieved['approved'] is not True or
                retrieved['room_id']!=request['room_id'] or
                type(retrieved['source_id']) is not str or not retrieved['source_id'] or
                type(retrieved['capacity']) is not int or retrieved['capacity']<0):
                return {'status':'review','reason':'evidence verification failed'}
            verified=True
        elif action=='answer':
            if not verified:return {'status':'review','reason':'missing verified evidence'}
            return {'status':'answered','room_id':retrieved['room_id'],
                    'capacity':retrieved['capacity'],'source_id':retrieved['source_id']}
    return {'status':'review'}

unsafe=['validate','retrieve','book','verify','answer']
unsafe_events=[]
rejected=run_plan(unsafe,{'room_id':'B'},SOURCE,unsafe_events)
assert rejected['status']=='rejected_plan' and unsafe_events==[]
safe_events=[]
answer=run_plan(list(SAFE),{'room_id':'B'},SOURCE,safe_events)
assert answer=={'status':'answered','room_id':'B','capacity':12,'source_id':'ROOM-R'}
assert safe_events==SAFE
missing_events=[]
missing=run_plan(list(SAFE),{'room_id':'B'},None,missing_events)
assert missing['status']=='review' and missing_events==['validate','retrieve']
wrong_events=[]
wrong=run_plan(['validate','retrieve','answer','verify'],{'room_id':'B'},SOURCE,wrong_events)
assert wrong['status']=='rejected_plan' and wrong_events==[]
print('Unsafe proposal rejected before all simulated work:',rejected,unsafe_events)
print('Separately safe read-only plan:',answer,safe_events)
print('Missing evidence runtime fallback:',missing,missing_events)
print('Wrong-order proposal:',wrong,wrong_events)
# Separate pictured tower-card policy permits conditional supported answering too.
def tower_reply(card):
    if card is None:return {'status':'unsupported','next':'request an approved card'}
    if card=={'source_id':'HEIGHT-CARD','height_m':24,'approved':True}:
        return {'status':'answered','height_m':24,'source_id':'HEIGHT-CARD'}
    return {'status':'review'}
assert tower_reply(None)['status']=='unsupported'
assert tower_reply({'source_id':'HEIGHT-CARD','height_m':24,'approved':True})['height_m']==24
print('Tower without/with supplied approved card:',tower_reply(None),tower_reply({'source_id':'HEIGHT-CARD','height_m':24,'approved':True}))
print('Fixtures only: the approved flag is supplied, not independent source verification; no external action executes.')
