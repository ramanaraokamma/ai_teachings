"""Closed-object validation; no coercion, room lookup or booking."""
def nonnegative_integer(value):
    return type(value) is int and value >= 0

def validate_request(value):
    if type(value) is not dict or set(value)!={'room_id','requested_count'}:
        raise ValueError('request fields')
    if type(value['room_id']) is not str or not value['room_id']:
        raise ValueError('room ID')
    if not nonnegative_integer(value['requested_count']):
        raise ValueError('requested count')
    return dict(value)

probes=[('valid',{'room_id':'B','requested_count':2}),
        ('Boolean',{'room_id':'B','requested_count':True}),
        ('string',{'room_id':'B','requested_count':'2'}),
        ('negative',{'room_id':'B','requested_count':-2}),
        ('extra field',{'room_id':'B','requested_count':2,'book':True}),
        ('missing count',{'room_id':'B'}),
        ('empty ID',{'room_id':'','requested_count':2}),
        ('nonobject',['B',2])]
results=[]
for name,value in probes:
    try:
        output=validate_request(value)
        results.append((name,'valid',output))
    except ValueError as error:
        results.append((name,'invalid',str(error)))
print('Python isinstance(True,int):',isinstance(True,int))
print('Contract exact type(True) is int:',type(True) is int)
for result in results:print(result)
assert results[0][1]=='valid' and all(r[1]=='invalid' for r in results[1:])
original={'room_id':'B','requested_count':2}
validated=validate_request(original)
assert validated==original and validated is not original
# A nonempty string is all this contract requires: whitespace also passes.
assert validate_request({'room_id':' ','requested_count':2})['room_id']==' '
# Whether that ID exists, is authorized, or has room capacity is not checked here.
# Do not silently add trimming, numeric conversion, or a room-ID format rule.
print('Schema-valid does not establish room existence, authority, capacity, or count truth.')
