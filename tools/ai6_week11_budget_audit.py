"""Exact count-based objectives on constructed request-check fixtures."""
def objective(eligible,failures,target_percent):
    if (type(eligible) is not int or eligible<=0 or type(failures) is not int
        or not 0<=failures<=eligible or type(target_percent) is not int
        or not 0<=target_percent<=100):
        raise ValueError('Need positive eligible count,valid failures,integer percent')
    successes=eligible-failures
    allowed_failures=((100-target_percent)*eligible)//100
    return {'eligible':eligible,'successes':successes,'failures':failures,
            'allowed_failures':allowed_failures,'success_rate':successes/eligible,
            'meets':100*successes>=target_percent*eligible,
            'remaining_budget':allowed_failures-failures}

WINDOW={'id':'W-A','start':'fictional day 09:00','end':'fictional day 10:00',
        'scope':'supplied user-request ledger assigned to this window'}
requests=[]
for i in range(1,201):
    checks={'schema':True,'support_or_correct_refusal':True,'time_contract':True}
    if i in [196,199,200]:checks['support_or_correct_refusal']=False
    if i in [197,199]:checks['schema']=False
    if i in [198,200]:checks['time_contract']=False
    requests.append({'id':f'R{i:03}','eligible':True,
                     'kind':'correct_refusal' if i==10 else 'answer', 'checks':checks})
# Predeclared separate health-check events are not user requests in this toy policy.
excluded=[{'id':f'H{i}','eligible':False,'reason':'internal health check'} for i in range(1,4)]
failed=[r for r in requests if not all(r['checks'].values())]
criterion_failures=sum(not value for r in requests for value in r['checks'].values())
report=objective(len(requests),len(failed),98)
assert report['successes']==195 and report['allowed_failures']==4
assert not report['meets'] and report['remaining_budget']==-1
assert len(failed)==5 and criterion_failures==7  # overlapping checks count once/request
assert requests[9]['kind']=='correct_refusal' and all(requests[9]['checks'].values())
print('Window manifest:',WINDOW)
print('Constructed window W-A: 200 eligible requests; 3 separate health checks excluded by the declared rule.')
print('Failed request IDs:',[r['id'] for r in failed],'failed criteria:',criterion_failures)
print('Count-based objective:',report)
print('Excluded records:',excluded)
# Separate pictured window and a counterfactual copy, not a relabelled original.
picture_original=objective(100,3,98)
picture_counterfactual=objective(100,2,98)
assert not picture_original['meets'] and picture_counterfactual['meets']
print('Picture original:',picture_original)
print('Separate counterfactual copy:',picture_counterfactual)
assert picture_original['failures']==3  # original history is preserved
assert objective(12,0,98)['allowed_failures']==0
assert not objective(12,1,98)['meets']
print('At 98% over 12 requests, the maximum integer failure count is 0, not a rounded-up fraction.')
print('Synthetic check flags only: no actual reliability interval, timing measurement or future guarantee.')
