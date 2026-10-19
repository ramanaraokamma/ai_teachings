"""Trusted classroom session fixtures; no login protocol or real identities."""
RESOURCES={'lesson':{'role':'student','body':'fictional student lesson'},
           'guide':{'role':'teacher','body':'fictional teacher guide'}}

def may_read(role,resource_role):
    if role not in ('student','teacher') or resource_role not in ('student','teacher'):
        return False
    return role=='teacher' or resource_role=='student'

def read_request(trusted_session,request,trace):
    trace.append('check_trusted_session_fixture')
    if not trusted_session or trusted_session.get('role') not in ('student','teacher'):
        return {'status':'denied'}
    trace.append('authorize_read')
    key=request.get('resource_id')
    if key not in RESOURCES:
        return {'status':'denied'}
    role=trusted_session['role']  # request.get('role') is never consulted
    if not may_read(role,RESOURCES[key]['role']):
        return {'status':'denied'}
    trace.append('read_allowed_body')
    return {'status':'answered','source_id':key,'text':RESOURCES[key]['body']}

student_session={'actor':'fictional-learner','role':'student'}
trace=[]
spoofed=read_request(student_session,{'resource_id':'guide','role':'teacher'},trace)
assert spoofed=={'status':'denied'} and 'read_allowed_body' not in trace
assert student_session['role']=='student'
print('Student with client-claimed teacher role:',trace,spoofed)
public_trace=[]
public=read_request(student_session,{'resource_id':'lesson'},public_trace)
assert public['status']=='answered'
print('Student allowed read:',public_trace,public)
unknown_trace=[]
assert read_request(student_session,{'resource_id':'unknown'},unknown_trace)=={'status':'denied'}
assert not may_read('administrator','teacher') and not may_read('teacher','unknown')
# Separate museum authorization decision only: no editing is executed.
def museum_allowed(trusted_role,action,resource):
    return resource=='C' and ((trusted_role=='volunteer' and action=='read')
                            or (trusted_role=='curator' and action in ('read','edit')))
assert museum_allowed('volunteer','read','C')
assert not museum_allowed('volunteer','edit','C')
assert museum_allowed('curator','edit','C')
print('Museum volunteer read/edit:',museum_allowed('volunteer','read','C'),museum_allowed('volunteer','edit','C'))
print('Museum curator edit permission:',museum_allowed('curator','edit','C'))
print('Permission decisions only; real authentication, session expiry and write execution are absent.')
