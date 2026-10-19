"""Allowlisted metadata records from fictional fixtures; no real logs or secrets."""
import json
import re
POLICY={'access':'designated classroom reviewer',
        'retention':'delete mock records after this classroom exercise',
        'raw_text':'excluded'}

def event(trace_id,stage,status,duration_ms,error_category='none',source_id=None):
    if type(trace_id) is not str or not re.fullmatch(r'[A-Z][0-9]{1,8}',trace_id):
        raise ValueError('invalid trace ID format')
    if stage not in ('request','authorize','lookup','validate'):
        raise ValueError('invalid stage')
    if status not in ('ok','denied','review'):
        raise ValueError('invalid status')
    if type(duration_ms) is not int or duration_ms<0:
        raise ValueError('invalid duration')
    if error_category not in ('none','permission_denied','missing_source',
                              'invalid_request','dependency_failure','output_mismatch'):
        raise ValueError('invalid error category')
    record={'trace_id':trace_id,'stage':stage,'status':status,
            'duration_ms':duration_ms,'error_category':error_category}
    # The pictured retrieval policy explicitly permits this extra source-ID field.
    if source_id is not None:
        if stage!='lookup' or type(source_id) is not str or not re.fullmatch(r'C[0-9]{1,8}',source_id):
            raise ValueError('invalid retrieval source ID')
        record['source_id']=source_id
    return record

raw_mock={'trace_id':'R7','stage':'authorize','status':'denied','duration_ms':3,
          'error_category':'permission_denied',
          'passcode':'fictional-passcode-placeholder',
          'student_text':'fictional private question',
          'teacher_answer':'fictional private guide text'}
# Build the intended record; never serialize or print the entire raw_mock.
safe=event(raw_mock['trace_id'],raw_mock['stage'],raw_mock['status'],
           raw_mock['duration_ms'],raw_mock['error_category'])
trace=[event('R17','request','ok',240),
       event('R17','lookup','ok',80,source_id='C8'),
       event('R17','validate','ok',20)]
serialized=json.dumps([safe,*trace])
assert set(safe)=={'trace_id','stage','status','duration_ms','error_category'}
assert all(raw_mock[key] not in serialized for key in ['passcode','student_text','teacher_answer'])
assert {r['trace_id'] for r in trace}=={'R17'}
assert trace[0]['duration_ms']==240 and trace[1]['source_id']=='C8'
print('Declared classroom policy, not implemented controls:',POLICY)
print('Main minimized record:',safe)
for row in trace:print('Separate pictured trace metadata:',row)
print('The 240 ms request duration is one supplied fixture value, not a service average.')
print('Request span can include lookup/validation spans; do not add nested durations as independent work.')
print('Trace/source IDs remain linkable. Access control and deletion are declared, not enforced by this builder.')
