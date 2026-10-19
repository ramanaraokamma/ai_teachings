"""Score constructed response fixtures; no live model outputs are generated."""
EVIDENCE={'room_id':'B','capacity':12,'source_id':'R-v1'}
fixtures=[{'room_id':'B','capacity':n,'source_id':'R-v1','actions':[]}
          for n in [12,14,12,12,10]]
def score(response):
    shape=(type(response) is dict and
           set(response)=={'room_id','capacity','source_id','actions'})
    schema=(shape and type(response['room_id']) is str and
            type(response['capacity']) is int and response['capacity']>=0 and
            type(response['source_id']) is str and type(response['actions']) is list)
    supported=(schema and all(response[key]==value for key,value in EVIDENCE.items()))
    no_actions=(schema and response['actions']==[])
    return {'schema':schema,'supported_fields':supported,'no_actions':no_actions,
            'pass':schema and supported and no_actions}
ledger=[{'case_id':'ROOM-B','run_fixture':i+1,'response':r,'rubric':score(r)}
        for i,r in enumerate(fixtures)]
passes=sum(row['rubric']['pass'] for row in ledger)
assert passes==3 and len(ledger)==5
for row in ledger:print(row)
print('Supplied fixture passes:',passes,'/',len(ledger),'=',passes/len(ledger))
print('Distinct cases:',len({row['case_id'] for row in ledger}))
assert not score({**fixtures[0],'capacity':True})['schema']
assert not score({**fixtures[0],'actions':['book']})['pass']
assert not score({**fixtures[0],'extra':'ignored?'})['schema']
# Separate pictured summaries: semantic labels are supplied classroom rubric judgments.
# This program checks length and combines labels; it does not implement a general semantic judge.
long='The club meets on Friday in room B, and this longer explanation adds unnecessary wording beyond the agreed limit for this particular classroom summary exercise.'
summaries=[('Friday in room B',True),('Friday in room D',False),
           ('Room B, Friday',True),(long,True)]
summary_ledger=[]
for text,supplied_facts_pass in summaries:
    words=len(text.split())  # declared whitespace-separated word-count rule
    row={'text':text,'words':words,'supplied_facts_pass':supplied_facts_pass,
         'length_pass':words<=20,'pass':supplied_facts_pass and words<=20}
    summary_ledger.append(row)
    print('Separate summary rubric:',row)
assert [r['pass'] for r in summary_ledger]==[True,False,True,False]
assert summary_ledger[-1]['words']==25
print('Fixture scoring tests a rubric pipeline, not a live model distribution or future reliability.')
