"""Three inspectable read-only demonstration cases; no external service or model."""
from copy import deepcopy
CARD_VERSION='fixture-c1'
CARDS={'V7':{'id':'V7','approved':True,'version':CARD_VERSION,'club':'V','room':'E'}}

def demonstrate(card_id,operation,records):
 if type(card_id) is not str or not card_id or type(operation) is not str:
  raise ValueError('explicit fixture card and operation required')
 trace=[]
 if operation!='read':
  return {'status':'denied','room':None,'source_id':None,'trace':trace,'effects':[]}
 trace.append({'operation':'read','card_id':card_id})
 card=records.get(card_id)
 fields={'id','approved','version','club','room'}
 if type(card) is not dict or set(card)!=fields or card['id']!=card_id or card['approved'] is not True or card['version']!=CARD_VERSION:
  return {'status':'review','room':None,'source_id':None,'trace':trace,'effects':[]}
 if type(card['room']) is not str or not card['room'] or type(card['club']) is not str or not card['club']:
  return {'status':'review','room':None,'source_id':None,'trace':trace,'effects':[]}
 return {'status':'supported','room':card['room'],'source_id':card_id,'trace':trace,'effects':[]}

before=deepcopy(CARDS)
# Declare the cases and exact output/trace requirements before running the fixture.
cases=[{'id':'supported','card':'V7','operation':'read','expected':'supported','expected_room':'E','expected_source':'V7','reads':['V7']},
       {'id':'legitimate-review','card':'V8','operation':'read','expected':'review','expected_room':None,'expected_source':None,'reads':['V8']},
       {'id':'denied-send','card':'V7','operation':'send','expected':'denied','expected_room':None,'expected_source':None,'reads':[]}]
results=[]
for case in cases:
 actual=demonstrate(case['card'],case['operation'],CARDS)
 passed=(actual['status']==case['expected'] and actual['room']==case['expected_room'] and
         actual['source_id']==case['expected_source'] and
         [e['card_id'] for e in actual['trace']]==case['reads'] and actual['effects']==[])
 results.append({'case':case['id'],'passed_expected_contract':passed,'actual':actual})
assert all(r['passed_expected_contract'] for r in results) and CARDS==before
assert demonstrate('V7','read',{})['status']=='review'
assert demonstrate('V7','read',{'V7':{**CARDS['V7'],'approved':False}})['status']=='review'
# Evidence inventory says explicitly what this local demonstration never measured.
evidence={'fixture_version':CARD_VERSION,'expected_case_passes':3,'cases':3,
          'output_status_counts':{'supported':1,'review':1,'denied':1},
          'network_availability':'not measured','production_authentication':'not implemented',
          'time_and_resource_measurements':'not measured','rollback_rehearsal':'not run',
          'audience_or_operator_signoff':'not supplied'}
print('Complete supported/review/denied demonstration:',results)
print('Evidence and missing-measurement inventory:',evidence)
print('Three expected-contract case passes do not mean three supported answers, broad reliability, production security or release approval.')
print('No email, edit, booking or other side-effect tool exists. Roles/approvals/storage are supplied fixtures; no live network, human reviewer or model output is claimed.')
