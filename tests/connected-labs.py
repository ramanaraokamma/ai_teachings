"""Keep existing code drafts aligned while choosing the new main lesson example."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from sync_connected_labs import sync_labs
w=next(w for w in json.loads((R/'content/programme.json').read_text())['weeks'] if w['id']=='ai-2/5')
old=[w['sections'][2]['blocks'][11]['text'],w['sections'][7]['blocks'][8]['text']];entry={'labs':[{'title':str(i),'code':code} for i,code in enumerate(old)]};original=copy.deepcopy(entry)
w=copy.deepcopy(w);w['sections'][13]['blocks'].append({'type':'code','text':'# RESERVED assessment code'})
new=sync_labs(w,entry)
assert entry==original and [l['code'] for l in new['labs'][:2]]==old
assert sum(bool(l.get('primary')) for l in new['labs'])==1
assert 'while count > 3' in next(l['code'] for l in new['labs'] if l.get('primary'))
assert all('RESERVED' not in l['code'] for l in new['labs'])
assert sync_labs(w,new)==new
print('Primary while example, stable draft indices, reserved-code exclusion and repeat sync verified.')
