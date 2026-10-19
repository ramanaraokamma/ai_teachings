"""Deterministic read-only capstone over supplied room and garden dictionaries."""
from copy import deepcopy
import re
VERSION='c1'
ROOMS={'A':{'id':'A','approved':True,'capacity':12,'version':'c1','source_id':'REG-A'},
       'B':{'id':'B','approved':False,'capacity':8,'version':'c1','source_id':'REG-B'}}

def output(status,resource_id,capacity=None,source_id=None):
 if status not in {'supported','review','denied','invalid_input'}:raise ValueError('unknown status')
 if status=='supported':
  if type(capacity) is not int or capacity<0 or type(source_id) is not str or not source_id:
   raise ValueError('supported output needs exact nonnegative integer capacity and source')
 elif capacity is not None or source_id is not None:raise ValueError('unsupported output must have null claims')
 return {'status':status,'resource_id':resource_id,'capacity':capacity,'source_id':source_id}

def serve(request,trusted_role,records,trace,logs):
 rid=None
 def finish(status,capacity=None,source_id=None):
  result=output(status,rid,capacity,source_id)
  logs.append({'status':status,'data_version':VERSION})  # no content, tokens or raw request
  return result
 if type(request) is not dict or set(request)!={'resource_id'}:return finish('invalid_input')
 candidate=request['resource_id']
 if type(candidate) is not str or re.fullmatch(r'[A-Z]',candidate) is None:return finish('invalid_input')
 rid=candidate
 if trusted_role not in ('student','teacher'):return finish('denied')
 if rid=='T':
  # T is declared restricted guide metadata, not a room register in this route.
  return finish('denied' if trusted_role=='student' else 'review')
 trace.append({'operation':'room_lookup','resource_id':rid})
 record=records.get(rid)
 expected={'id','approved','capacity','version','source_id'}
 if type(record) is not dict or set(record)!=expected:return finish('review')
 if record['id']!=rid or record['version']!=VERSION or record['approved'] is not True:return finish('review')
 if type(record['capacity']) is not int or record['capacity']<0:return finish('review')
 if type(record['source_id']) is not str or not record['source_id']:return finish('review')
 return finish('supported',record['capacity'],record['source_id'])

before=deepcopy(ROOMS);trace=[];logs=[]
a=serve({'resource_id':'A'},'student',ROOMS,trace,logs)
b=serve({'resource_id':'B'},'student',ROOMS,trace,logs)
t=serve({'resource_id':'T'},'student',ROOMS,trace,logs)
assert a['status']=='supported' and a['capacity']==12 and a['source_id']=='REG-A'
assert b['status']=='review' and b['capacity'] is None and t['status']=='denied'
assert [e['resource_id'] for e in trace]==['A','B'] and ROOMS==before
assert serve({'resource_id':'A','role':'teacher'},'student',ROOMS,[],[])['status']=='invalid_input'
assert serve({'resource_id':'A'},'unknown',ROOMS,[],[])['status']=='denied'
# Separate garden picture; exact structured operations, not natural-language parsing.
GARDEN={'G1':{'approved':True,'claim':'fictional garden card one'},
        'G2':{'approved':True,'claim':'Mint needs regular watering.'},
        'G3':{'approved':True,'claim':'fictional garden card three'}}
def garden_reply(operations,records):
 if operations!=['read_G2','edit_G2']:raise ValueError('use exact supplied two-operation fixture')
 record=records.get('G2');supported=type(record) is dict and record.get('approved') is True and type(record.get('claim')) is str
 return {'answer_status':'supported' if supported else 'review',
         'claim':record['claim'] if supported else None,'source_id':'G2' if supported else None,
         'edit_status':'denied','effects':[]}
garden_before=deepcopy(GARDEN)
picture=garden_reply(['read_G2','edit_G2'],GARDEN)
missing=garden_reply(['read_G2','edit_G2'],{k:v for k,v in GARDEN.items() if k!='G2'})
assert picture['source_id']=='G2' and missing['claim'] is None
assert picture['edit_status']==missing['edit_status']=='denied' and GARDEN==garden_before
print('Main A/B/T:',a,b,t,'lookup trace:',trace,'minimal log:',logs[:3])
print('Separate garden picture:',picture,'missing G2:',missing)
print('No booking, send or edit tool exists. Trusted roles/approved records are fixtures, not real authentication or production reliability. No model, live register or independent gardening advice is used.')
