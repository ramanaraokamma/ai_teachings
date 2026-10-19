"""Audit symbolic environment configuration; no real endpoint, token or deployment."""
from copy import deepcopy
ENVIRONMENTS={
 'development':{'store':'dev-fixtures','namespace':'dev-mock','credential':'dev-reader','room':'D'},
 'staging':{'store':'stage-fixtures','namespace':'stage-mock','credential':'stage-reader','room':'Z'},
 'production':{'store':'approved-school','namespace':'prod-mock','credential':'prod-reader','room':'A'}}
# Symbolic authority metadata comes from the trusted harness, not a client claim.
CREDENTIALS={v['credential']:{'environment':e,'store':v['store'],'operation':'read'}
             for e,v in ENVIRONMENTS.items()}
STORES={v['store']:{'room':v['room'],'fictional':True} for v in ENVIRONMENTS.values()}
FIELDS={'environment','store','namespace','credential','operation'}
def audit(config):
 if type(config) is not dict or set(config)!=FIELDS:raise ValueError('exact config fields required')
 if any(type(v) is not str or not v for v in config.values()):raise ValueError('nonempty string fields required')
 env=config['environment']
 if env not in ENVIRONMENTS:return {'status':'blocked','reason':'unknown environment'}
 expected=ENVIRONMENTS[env];authority=CREDENTIALS.get(config['credential'])
 if config['store']!=expected['store']:return {'status':'blocked','reason':'store crosses environment'}
 if config['namespace']!=expected['namespace']:return {'status':'blocked','reason':'namespace crosses environment'}
 if config['credential']!=expected['credential'] or authority is None:
  return {'status':'blocked','reason':'credential crosses environment or is unknown'}
 if authority['environment']!=env or authority['store']!=config['store'] or authority['operation']!=config['operation']:
  return {'status':'blocked','reason':'credential authority does not match operation/context'}
 return {'status':'allowed_fixture_read','environment':env}
def read_fixture(config,calls):
 verdict=audit(config)
 if verdict['status']!='allowed_fixture_read':return verdict
 calls.append(config['store'])
 return {**verdict,'record':deepcopy(STORES[config['store']])}
def config_for(env):
 rule=ENVIRONMENTS[env]
 return {'environment':env,'store':rule['store'],'namespace':rule['namespace'],
         'credential':rule['credential'],'operation':'read'}

before=deepcopy(STORES);calls=[];stage=config_for('staging')
main_bad={**stage,'store':ENVIRONMENTS['production']['store']}
main=read_fixture(main_bad,calls)
assert main['status']=='blocked' and calls==[]
picture=read_fixture(stage,calls)
assert picture['record']['room']=='Z' and calls==['stage-fixtures']
changed=read_fixture({**stage,'credential':'prod-reader'},calls)
assert changed['status']=='blocked' and calls==['stage-fixtures']
assert audit({**stage,'namespace':'prod-mock'})['status']=='blocked'
assert audit({**stage,'operation':'write'})['status']=='blocked'
assert audit({**stage,'environment':'stage'})['status']=='blocked'
assert STORES==before
print('Main staging badge with production store:',main)
print('Picture valid rehearsal:',picture,'changed production credential:',changed)
print('Only successful local fixture read:',calls,'all source stores unchanged:',STORES==before)
print('All environments, records and credential IDs are fictional; production here is another dictionary.')
print('A label or symbolic allowlist is not network/IAM isolation. No real credentials, endpoints, secrets, promotion or deployment are accessed.')
