"""Local data-flow simulator with explicit, trusted caller-role input."""
SOURCES={'S':{'visibility':'student','time':'16:00'},
         'T':{'visibility':'teacher','time':'18:00'}}

def serve(request,caller_role,trace,*,draft=None,sources=SOURCES):
    trace.append('request_validator')
    if (not isinstance(request,dict) or set(request)!={'source_id'}
        or not isinstance(request['source_id'],str) or not request['source_id']):
        return {'status':'invalid_request'}
    trace.append('role_filter')
    if caller_role not in ('student','teacher'):
        return {'status':'denied'}
    allowed={key for key,meta in sources.items()
             if meta['visibility']=='student' or caller_role=='teacher'}
    key=request['source_id']
    if key in sources and key not in allowed:
        return {'status':'denied'}
    trace.append('source_lookup')
    if key not in allowed:
        return {'status':'review','reason':'No approved source'}
    record=sources[key]  # body read occurs only after authorization
    trace.append('draft')
    output=({'source_id':key,'time':record['time']} if draft is None else draft)
    trace.append('response_validator')
    if (not isinstance(output,dict) or set(output)!={'source_id','time'}
        or output['source_id']!=key or output['time']!=record['time']):
        return {'status':'review','reason':'Draft does not match approved evidence'}
    trace.append('result')
    return {'status':'answered',**output}

traces={}
for name,request,role,draft in [
 ('allowed',{'source_id':'S'},'student',None),
 ('restricted',{'source_id':'T'},'student',None),
 ('missing',{'source_id':'X'},'student',None),
 ('wrong_draft',{'source_id':'S'},'student',{'source_id':'S','time':'19:00'}),
 ('spoofed_request',{'source_id':'T','role':'teacher'},'student',None)]:
    trace=[]
    result=serve(request,role,trace,draft=draft)
    traces[name]=(trace,result)
    print(name,trace,result)
assert traces['allowed'][1]=={'status':'answered','source_id':'S','time':'16:00'}
assert traces['restricted']==(['request_validator','role_filter'],{'status':'denied'})
assert traces['spoofed_request']==(['request_validator'],{'status':'invalid_request'})
assert 'draft' not in traces['missing'][0]
assert traces['wrong_draft'][1]['status']=='review'
print('Simulation: role is supplied by a trusted test harness, not authenticated here.')
print('No model call, network, production access control or complete injection defense is demonstrated.')
