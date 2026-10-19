"""Fictional incident evidence and controlled reproductions, no live log access."""
from copy import deepcopy

main_events=[{'time':'09:00','kind':'corpus_update','version':'c2'},
             {'time':'09:05','kind':'response','source_version':'c1','weight_version':'w7'},
             {'time':'09:06','kind':'containment','action':'cache_disabled'}]
weight_before='w7';weight_at_response='w7'
before=deepcopy(main_events)
assert weight_before==weight_at_response
# A deliberately buggy query-only cache is one candidate mechanism, not the proven live bug.
source={'c1':'old fictional answer','c2':'new fictional answer'}
cached={'query':'q','source_version':'c1','answer':source['c1']}
def candidate_response(cache_enabled):
 if type(cache_enabled) is not bool:raise ValueError('Boolean controlled condition required')
 return deepcopy(cached) if cache_enabled else {'query':'q','source_version':'c2','answer':source['c2']}
with_cache=candidate_response(True);without_cache=candidate_response(False)
assert with_cache['source_version']=='c1' and without_cache['source_version']=='c2'
assert main_events==before

def locate_mismatch(current_version,retrieved_version,drafted_room,records):
 if current_version not in records or retrieved_version not in records:
  return {'observed':'incomplete source evidence','next_test':'obtain permitted missing version metadata'}
 if retrieved_version!=current_version:
  return {'observed':'stale evidence version','next_test':'reproduce version selection/cache behavior'}
 if drafted_room!=records[retrieved_version]['room']:
  return {'observed':'draft differs from retrieved record','next_test':'inspect context handoff and answer construction'}
 return {'observed':'no supplied version/room mismatch','next_test':'inspect other reported symptoms'}
# Separate picture timeline and a changed trace; no model generates either draft.
records={'5':{'room':'C'},'6':{'room':'D'}}
picture_events=[('14:00','version 6 publishes room D'),('14:05','version 5 used, room C drafted'),
                ('14:06','user reports mismatch')]
picture=locate_mismatch('6','5','C',records)
changed=locate_mismatch('6','6','C',records)
assert picture['observed']=='stale evidence version'
assert changed['observed']=='draft differs from retrieved record'
assert locate_mismatch('6','missing','C',records)['observed']=='incomplete source evidence'
print('Main supplied timeline:',main_events)
print('Reliable declared weight version unchanged:',weight_before==weight_at_response)
print('Controlled candidate fixture, enabled/disabled:',with_cache,without_cache)
print('Picture ordered events:',picture_events)
print('Picture evidence localization:',picture,'changed trace:',changed)
print('Candidate reproduction supports a possible mechanism in this fixture; chronology alone does not prove the real incident cause.')
print('Containment may proceed promptly while authorized minimized evidence is captured. No private payloads, actual systems, model runs or live repairs are used.')
