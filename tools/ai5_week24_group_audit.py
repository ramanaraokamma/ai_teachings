# Complete fictional provenance audit. No model is trained and no new score is claimed.
from copy import deepcopy
from itertools import product

def difference(x):
    return x[0][0]+x[1][0]-x[0][1]-x[1][1]
def label(x):
    return int(difference(x)>0)
def swap_rows(x):
    return [x[1][:],x[0][:]]
def swap_columns(x):
    return [row[::-1] for row in x]

# Every binary 2x2 pattern checks the known mathematical rule, not unknown real labels.
for bits in product([0,1],repeat=4):
    x=[list(bits[:2]),list(bits[2:])]
    assert label(swap_rows(x))==label(x)
    assert difference(swap_columns(x))==-difference(x)
    expected=0 if difference(x)==0 else 1-label(x)
    assert label(swap_columns(x))==expected
print('all 16 binary patterns: row swaps preserve labels; column swaps require the declared rule')

sources = {
    'P': ([[1,0],[0,0]], 'training'),
    'Q': ([[0,1],[0,0]], 'training'),
    'R': ([[1,0],[1,0]], 'validation'),
    'S': ([[0,1],[0,1]], 'final'),
    'T': ([[1,1],[0,0]], 'final'),
}
inventory=[]
for group,(image,split) in sources.items():
    for transform,pixels in [('original',deepcopy(image)),('row_swap',swap_rows(image))]:
        inventory.append({'id':group+'-'+transform,'source':group,'parent':None if transform=='original' else group+'-original',
                          'split':split,'transform':transform,'pixels':pixels,'label':label(pixels)})
retained=[r for r in inventory if r['split']=='training' or r['transform']=='original']

def audit(records):
    groups={};pixels={}
    for r in records:
        groups.setdefault(r['source'],set()).add(r['split'])
        key=tuple(tuple(row) for row in r['pixels'])
        pixels.setdefault(key,[]).append((r['id'],r['split']))
    shared_groups={g:sorted(s) for g,s in groups.items() if len(s)>1}
    duplicate_pixels=[pairs for pairs in pixels.values() if len({split for _,split in pairs})>1]
    return shared_groups,duplicate_pixels

for split in ['training','validation','final']:
    part=[r for r in retained if r['split']==split]
    print(split,'groups / retained records',len({r['source'] for r in part}),len(part))
print('retained / excluded',len(retained),len(inventory)-len(retained))
print('clean recorded-group / exact-pixel overlaps',audit(retained))

bad_group=deepcopy(retained)
next(r for r in bad_group if r['id']=='P-row_swap')['split']='validation'
print('new filename does not repair shared source:',audit(bad_group)[0])

alias=deepcopy(next(r for r in retained if r['id']=='P-row_swap'))
alias.update(id='claimed-U-original',source='claimed-U',parent=None,split='validation',transform='original')
print('different claimed source, same pixels:',audit(retained+[alias]))
print('Audit only: exact pixels do not prove real-object identity; missing provenance still needs review.')
print('Any affected fitting/selection must be rerun after a justified split repair; no repaired score is supplied.')
