"""Versioned local stub evaluation with explicit skipped rows and denominators."""
manifest={'suite':'ROOM-CAPACITY','case_version':'classroom-v1',
          'procedure_version':'fixed-lookup-stub-v1',
          'scoring':'exact nonnegative integer capacity equality',
          'skip_policy':'exclude from completed pass denominator; retain in planned coverage'}
cases=[{'id':f'C{i+1}','input':room,'expected':expected}
       for i,(room,expected) in enumerate(zip('ABCDEF',[12,8,10,6,4,2]))]
STUB={'A':12,'B':8,'C':10,'D':6,'E':5,'F':2}
def execute_fixture(cases):
    records=[]
    for case in cases:
        if case['id']=='C6':
            records.append({'id':'C6','status':'skipped','reason':'declared classroom skip'})
        else:
            records.append({'id':case['id'],'status':'completed','actual':STUB[case['input']]})
    return records

def summarize(cases,records):
    if not cases:raise ValueError('Need planned cases')
    if any(type(c) is not dict or set(c)!={'id','input','expected'}
           or type(c['id']) is not str or not c['id']
           or type(c['input']) is not str or not c['input'] for c in cases):
        raise ValueError('Invalid planned-case schema')
    for record in records:
        if (type(record) is not dict or record.get('status') not in ('completed','skipped')
            or type(record.get('id')) is not str or not record['id']):
            raise ValueError('Invalid result record')
        fields=({'id','status','actual'} if record['status']=='completed' else {'id','status','reason'})
        if set(record)!=fields:raise ValueError('Unexpected or missing result fields')
    ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate planned ID')
    if any(type(c['expected']) is not int or c['expected']<0 for c in cases):
        raise ValueError('Invalid reference capacity')
    result_ids=[r['id'] for r in records]
    if len(result_ids)!=len(set(result_ids)) or set(result_ids)!=set(ids):
        raise ValueError('Need exactly one explicit record for every planned ID')
    by_id={r['id']:r for r in records}
    ledger=[]
    for case in cases:
        record=by_id[case['id']]
        if record['status']=='skipped':
            if type(record.get('reason')) is not str or not record['reason']:raise ValueError('Skipped record needs a reason')
            ledger.append({**case,**record,'pass':None})
        elif record['status']=='completed':
            if 'actual' not in record:raise ValueError('Completed row missing actual output')
            actual=record['actual']
            passed=type(actual) is int and actual>=0 and actual==case['expected']
            ledger.append({**case,**record,'pass':passed})
        else:raise ValueError('Unknown result status')
    completed=sum(r['status']=='completed' for r in ledger)
    passes=sum(r['pass'] is True for r in ledger)
    return {'planned':len(cases),'completed':completed,'passed':passes,
            'failed':completed-passes,'skipped':len(cases)-completed,
            'coverage':completed/len(cases),
            'completed_pass_rate':passes/completed if completed else None,
            'ledger':ledger}

records=execute_fixture(cases)
summary=summarize(cases,records)
assert (summary['planned'],summary['completed'],summary['passed'],summary['failed'],summary['skipped'])==(6,5,4,1,1)
assert summary['completed_pass_rate']==.8 and summary['coverage']==5/6
assert records==execute_fixture(cases)  # same stub replay, not independent evidence
print('Manifest:',manifest)
for row in summary['ledger']:print('Raw case-level row:',row)
print('Completed pass rate:',summary['passed'],'/',summary['completed'])
print('Coverage:',summary['completed'],'/',summary['planned'])
try:summarize(cases,records[:-1])
except ValueError:print('Missing result record rejected; it is not silently a pass or a skip.')
else:raise AssertionError('Omitted planned case accepted')
all_skipped=[{'id':c['id'],'status':'skipped','reason':'not run'} for c in cases]
assert summarize(cases,all_skipped)['completed_pass_rate'] is None
# Separate supplied picture: correctness flags, not predicted class labels.
a=[1,1,0,1];b=[1,0,0,1]
assert sum(a)/4==.75 and sum(b)/4==.5
print('Separate full picture:',sum(a),'/4;',sum(b),'/4')
print('Selectively deleting known shared failure changes rates to 3/3 and 2/3; preserve the full original report.')
print('Local stub only: no real model run, broader quality estimate or runtime measurement.')
