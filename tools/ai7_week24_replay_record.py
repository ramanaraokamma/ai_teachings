"""Replay a tiny self-contained calculation in memory; no external experiment."""
import hashlib
import sys
from fractions import Fraction
SCRIPT='''from fractions import Fraction

def mean_csv(text):
    parts=text.strip().split(',')
    if not parts or any(not p.strip() for p in parts):
        raise ValueError('nonempty comma-separated integer values required')
    values=[int(p) for p in parts]
    return Fraction(sum(values),len(values))
'''
namespace={};exec(SCRIPT,namespace)
def record(run_id,data_text):
 if not isinstance(run_id,str) or not run_id:raise ValueError('run ID required')
 if not isinstance(data_text,str):raise ValueError('explicit input bytes required')
 data_bytes=data_text.encode('utf-8');script_bytes=SCRIPT.encode('utf-8')
 return {'run_id':run_id,'data_text':data_text,'script_text':SCRIPT,
         'data_sha256':hashlib.sha256(data_bytes).hexdigest(),
         'script_sha256':hashlib.sha256(script_bytes).hexdigest(),
         'python_runtime':sys.version,'dependencies':'Python standard library only',
         'metric':'exact arithmetic mean of parsed integers','randomness':'none used',
         'raw_output':str(namespace['mean_csv'](data_text))}
original=record('demo-original','2,4,6\n');changed=record('demo-changed','2,4,9\n')
assert original['raw_output']=='4' and changed['raw_output']=='5'
assert original['data_sha256']!=changed['data_sha256'] and original['script_sha256']==changed['script_sha256']
assert record('demo-replay',original['data_text'])['raw_output']==original['raw_output']
print('Original local in-memory run record:',original)
print('Changed local in-memory run record:',changed)
print('Changed input gets a different run ID; original record retained. Hashes describe these exact bytes only.')
print('This is an actual tiny local calculation, not an independent reproduction of an AI model, evidence of good sampling or proof that the recorded formula answers a scientific question.')
