"""Repeat an explicitly specified ASCII string-length rule; no trained model."""

def labels(strings,strict=False):
 if not isinstance(strings,(list,tuple)) or any(not isinstance(s,str) for s in strings) or type(strict) is not bool:
  raise ValueError('string sequence and Boolean boundary flag required')
 return [{'input':s,'character_count':len(s),'label':'long' if (len(s)>4 if strict else len(s)>=4) else 'short'} for s in strings]
inputs=['oak','pine','willow'];original=labels(inputs);changed=labels(inputs,True)
assert [r['character_count'] for r in original]==[3,4,6]
assert [r['label'] for r in original]==['short','long','long']
assert [r['label'] for r in changed]==['short','short','long']
assert labels(['oak '])[0]['label']=='long' # No whitespace trimming under this method.
assert inputs==['oak','pine','willow']
print('Original explicit inclusive length rule:',original)
print('Changed strict greater-than-four rule:',changed)
print('Whitespace boundary probe:',labels(['oak ']))
print('Method: Python len on the supplied ASCII strings, no stripping or preprocessing. Long is an arbitrary string-length label, not botanical meaning.')
print('This demonstrates repeatable computation only. It supplies no missing code/data/split for the main AI report, no learned-model evidence and no independent study reproduction.')
