"""Local access-aware/versioned cache fixtures with virtual minute timestamps."""
from copy import deepcopy
from math import isfinite

def finite_nonnegative(value):
    return type(value) in (int,float) and isfinite(value) and value>=0

def cache_key(query,role,corpus_version,procedure_version):
    if any(type(v) is not str or not v for v in [query,role,corpus_version,procedure_version]):
        raise ValueError('nonempty key fields required')
    if role not in ('student','teacher'):raise ValueError('unknown trusted role fixture')
    return query,role,corpus_version,procedure_version

class FixtureCache:
    def __init__(self):self.entries={}
    def put(self,query,role,corpus_version,procedure_version,value,saved_at):
        if not finite_nonnegative(saved_at):raise ValueError('invalid virtual save time')
        key=cache_key(query,role,corpus_version,procedure_version)
        self.entries[key]={'saved_at':saved_at,'value':deepcopy(value)}
    def get(self,query,role,corpus_version,procedure_version,now,ttl,*,currently_allowed):
        if type(currently_allowed) is not bool:raise ValueError('trusted permission fixture required')
        if not currently_allowed or role not in ('student','teacher'):
            return {'status':'denied'}
        if not finite_nonnegative(now) or not finite_nonnegative(ttl) or ttl<=0:
            raise ValueError('finite nonnegative time and positive TTL required')
        key=cache_key(query,role,corpus_version,procedure_version)
        entry=self.entries.get(key)
        if entry is None:return {'status':'miss','reason':'no matching context key'}
        age=now-entry['saved_at']
        if age<0:return {'status':'miss','reason':'invalid negative age'}
        if age>=ttl:return {'status':'miss','reason':'expired'}
        return {'status':'hit','age_minutes':age,'value':deepcopy(entry['value'])}

cache=FixtureCache();query='room information';ttl=5
cache.put(query,'teacher','c1','p1',{'answer':'fictional teacher-only detail'},0)
teacher_hit=cache.get(query,'teacher','c1','p1',4,ttl,currently_allowed=True)
student_miss=cache.get(query,'student','c1','p1',4,ttl,currently_allowed=True)
revoked=cache.get(query,'teacher','c1','p1',4,ttl,currently_allowed=False)
expired=cache.get(query,'teacher','c1','p1',5,ttl,currently_allowed=True)
assert teacher_hit['status']=='hit' and student_miss['status']=='miss'
assert revoked=={'status':'denied'} and expired=={'status':'miss','reason':'expired'}
assert cache.get(query,'teacher','c2','p1',1,ttl,currently_allowed=True)['status']=='miss'
assert cache.get(query,'teacher','c1','p2',1,ttl,currently_allowed=True)['status']=='miss'
print('Main role/current-permission/expiry results:',teacher_hit['status'],student_miss,revoked,expired)
# Separate pictured source versions; trusted publication context chooses current v5.
openings={'4':'09:00','5':'09:30'};current_version='5';lookups=[]
picture=FixtureCache();room='map-room opening'
picture.put(room,'student','4','p1',{'opening':'09:00','source_version':'4'},0)
first=picture.get(room,'student',current_version,'p1',1,ttl,currently_allowed=True)
assert first['status']=='miss'
lookups.append(current_version)  # local source fixture lookup, not a network call
picture.put(room,'student',current_version,'p1',
            {'opening':openings[current_version],'source_version':current_version},1)
next_request=picture.get(room,'student',current_version,'p1',2,ttl,currently_allowed=True)
assert next_request['status']=='hit' and next_request['value']['opening']=='09:30' and lookups==['5']
print('Picture current-version first miss:',first)
print('Picture later matching fresh hit:',next_request,'source fixture lookups:',lookups)
# Deliberate hypothetical publication fault: same version label, changed source value.
silent_edit={'5':'09:45'}
assert next_request['value']['opening']!=silent_edit['5']
print('A silent unversioned edit would not be detected by this matching key/TTL alone.')
print('Expired/mismatched entries may remain in memory; serving validity is not proof of retention deletion.')
print('Roles, permissions, approved versions and cached authorized values are supplied fixtures; no real authentication, clock, provider or distributed cache.')
