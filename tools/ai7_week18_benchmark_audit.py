"""Source-identity and coverage audit on explicitly fictional metadata/summaries."""
from collections import Counter
from fractions import Fraction

def audit_sources(rows):
 if not isinstance(rows,(list,tuple)) or not rows:raise ValueError('nonempty records required')
 if any(not isinstance(r,dict) or not isinstance(r.get('row_id'),str) or not r['row_id'] or not isinstance(r.get('source_id'),str) or not r['source_id'] for r in rows):raise ValueError('row and source IDs required')
 if len({r['row_id'] for r in rows})!=len(rows):raise ValueError('row IDs must be unique')
 counts=Counter(r['source_id'] for r in rows)
 return {'rows':len(rows),'unique_source_ids':len(counts),'source_weights':dict(counts),
         'extra_rows_beyond_one_per_source':len(rows)-len(counts)}
# Metadata construction illustrates the stated three-copy/eight-source arrangement.
rows=[{'row_id':f'R{i+1}','source_id':s} for i,s in enumerate(['S1','S1','S1','S2','S3','S4','S5','S6','S7','S8'])]
before=[r.copy() for r in rows];main=audit_sources(rows)
assert main['rows']==10 and main['unique_source_ids']==8 and main['source_weights']['S1']==3
assert main['extra_rows_beyond_one_per_source']==2 and rows==before
indoor=Fraction(9,10);outdoor_initial=None;outdoor_added=Fraction(2,4)
pooled_changed=Fraction(9+2,10+4)
assert indoor==Fraction(9,10) and outdoor_added==Fraction(1,2) and pooled_changed==Fraction(11,14)
print('Supplied-source metadata arrangement:',main)
print('Indoor supplied rate:',indoor,'initial outdoor rate:',outdoor_initial)
print('Changed supplied outdoor slice:',outdoor_added,'pooled descriptive count:',pooled_changed)
print('Do not substitute the pooled 11/14 for outdoor 2/4, or call unmeasured outdoor performance zero.')
print('IDs distinguish declared source identities; they cannot prove independent sampling, eligibility or correct labels. No rows are silently deleted, no outcomes per source invented, and no real photo collection/model evaluation occurs.')
