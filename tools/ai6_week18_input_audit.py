"""Exact ASCII identifier contracts and local read-only dictionary lookup."""
import re
from copy import deepcopy

def valid_room_id(value):
    return type(value) is str and re.fullmatch(r'[A-Z][0-9]',value) is not None

def valid_picture_id(value):
    return type(value) is str and re.fullmatch(r'[a-z][0-9]',value) is not None

RECORDS={'A1':{'capacity':12,'source_id':'ROOM-A1'},
         'B2':{'capacity':7,'source_id':'ROOM-B2'}}
TRUSTED_ALLOWED=frozenset({'A1','D4'})

def lookup(value,allowed,records,calls):
    if not valid_room_id(value):return {'status':'invalid_input'}
    if value not in allowed:return {'status':'denied'}
    calls.append(value)  # local fixture lookup trace, not a network call
    record=records.get(value)
    if record is None:return {'status':'review','reason':'missing approved record'}
    if (type(record) is not dict or set(record)!={'capacity','source_id'} or type(record.get('capacity')) is not int
        or record['capacity']<0 or type(record.get('source_id')) is not str or not record['source_id']):
        return {'status':'review','reason':'invalid record fields'}
    return {'status':'answered','room_id':value,'capacity':record['capacity'],'source_id':record['source_id']}

before=deepcopy(RECORDS);calls=[]
normal=lookup('A1',TRUSTED_ALLOWED,RECORDS,calls)
rejected=lookup('delete_all()',TRUSTED_ALLOWED,RECORDS,calls)
denied=lookup('B2',TRUSTED_ALLOWED,RECORDS,calls)
missing=lookup('D4',TRUSTED_ALLOWED,RECORDS,calls)
assert normal=={'status':'answered','room_id':'A1','capacity':12,'source_id':'ROOM-A1'}
assert rejected=={'status':'invalid_input'} and denied=={'status':'denied'}
assert missing['status']=='review' and calls==['A1','D4'] and RECORDS==before
print('Main allowed/invalid/denied/missing fixtures:',normal,rejected,denied,missing)
print('Actual local lookup IDs:',calls,'records unchanged:',RECORDS==before)
# Do not trim, change case, coerce values or execute instruction-shaped data.
values=['A1','a1','A11','A1 ','A1\n','Ａ１','A١','delete_all()',None]
for value in values:print('Main shape fixture:',repr(value),valid_room_id(value))
assert [valid_room_id(v) for v in values]==[True,False,False,False,False,False,False,False,False]
# Separate pictured contract is lowercase, not the main uppercase contract.
picture=['h3','H3','h30','h3 ','z0']
assert [valid_picture_id(v) for v in picture]==[True,False,False,False,True]
print('Separate picture shapes:',[(repr(v),valid_picture_id(v)) for v in picture])
print('A valid shape does not grant access. No evaluation of input as code, SQL, shell or model instruction occurs.')
print('Trusted scope is a classroom fixture, not real authentication; these checks do not prove every injection boundary is protected.')
