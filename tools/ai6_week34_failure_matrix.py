"""Complete four-case baseline failure matrix and supplied component-failure fixtures."""
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

# Expected outputs and allowed lookups are declared before executing the baseline.
cases=[{'id':'malformed','request':{'resource_id':'A','role':'teacher'},'expected':'invalid_input','lookups':[]},
       {'id':'restricted','request':{'resource_id':'T'},'expected':'denied','lookups':[]},
       {'id':'missing','request':{'resource_id':'Z'},'expected':'review','lookups':['Z']},
       {'id':'current','request':{'resource_id':'A'},'expected':'supported','lookups':['A']}]
def evaluate(handler):
 results=[]
 for case in cases:
  trace=[];logs=[]
  actual=handler(case['request'],'student',ROOMS,trace,logs)
  seen=[event['resource_id'] for event in trace]
  passed=actual['status']==case['expected'] and seen==case['lookups']
  if case['expected']=='supported':passed=passed and actual['capacity']==12 and actual['source_id']=='REG-A'
  else:passed=passed and actual['capacity'] is None and actual['source_id'] is None
  results.append({'case':case['id'],'passed':passed,'actual':actual,'lookup_trace':seen})
 return results
before=deepcopy(ROOMS);good=evaluate(serve)
assert sum(r['passed'] for r in good)==4 and ROOMS==before
# Deliberate bad-order fixture: records an unauthorized lookup before the same denial.
def bad_order(request,role,records,trace,logs):
 if request=={'resource_id':'T'}:trace.append({'operation':'restricted_lookup','resource_id':'T'})
 return serve(request,role,records,trace,logs)
bad=evaluate(bad_order)
assert sum(r['passed'] for r in bad)==3 and bad[1]['actual']['status']=='denied' and not bad[1]['passed']
# Separate pictured fallback; no actual retrieval provider, drafting model or timeout.
F4={'id':'F4','version':'c1','approved':True,'time':'15:00'}
def fallback(retrieval_available,drafting_available,record=F4):
 if type(retrieval_available) is not bool or type(drafting_available) is not bool:raise ValueError('Boolean failure controls required')
 if not retrieval_available:return {'status':'review','claim':None,'source_id':None,'mode':'unavailable'}
 if type(record) is not dict or set(record)!={'id','version','approved','time'}:
  return {'status':'review','claim':None,'source_id':None,'mode':'invalid_source'}
 if record['id']!='F4' or record['version']!='c1' or record['approved'] is not True or record['time']!='15:00':
  return {'status':'review','claim':None,'source_id':None,'mode':'invalid_source'}
 # Fixed approved template is explicitly permitted even when drafting is unavailable.
 return {'status':'supported','claim':'The club time is '+record['time']+'.','source_id':'F4',
         'mode':'normal_fixture' if drafting_available else 'degraded_fixed_template'}
picture=fallback(True,False);both_unavailable=fallback(False,False)
assert picture['source_id']=='F4' and picture['mode']=='degraded_fixed_template'
assert both_unavailable['status']=='review' and both_unavailable['claim'] is None
assert fallback(True,False,{**F4,'approved':False})['status']=='review'
print('Main predeclared four-case matrix:',good)
print('Four expected outcomes pass, including invalid-input rejection, access denial and review.')
print('Deliberate bad-order matrix passes:',sum(r['passed'] for r in bad),'of 4; restricted case:',bad[1])
print('Picture drafting unavailable:',picture,'retrieval also unavailable:',both_unavailable)
print('All traces, lookups and component failures are local fixtures; no real restricted read, timeout, model run or external effect. These cases do not cover every failure interaction.')
