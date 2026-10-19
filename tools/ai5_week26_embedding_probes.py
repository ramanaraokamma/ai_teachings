table = [[0, 0], [-1, -1], [2, 0],
         [1, 1], [0, 2], [0, 1]]
known = {"GO": 2, "TURN": 3, "STOP": 4, "WAIT": 5}

def distance2(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("Need equal nonempty dimensions")
    return sum((x - y)**2 for x, y in zip(a, b))

def nearest(query, candidates):
    if not candidates:
        raise ValueError("Need candidates")
    scores = {name: distance2(query, vector)
              for name, vector in candidates.items()}
    best = min(scores.values())
    return sorted(name for name, d in scores.items() if d == best)

candidates = {name: table[i] for name, i in known.items()
              if name != "GO"}
assert nearest(table[2], candidates) == ["TURN"]
# Complete lookup, masking and isolated row-update probes.
def lookup(ids):
    if any(type(i) is not int or not 0 <= i < len(table) for i in ids):
        raise ValueError('Token ID is outside this saved vocabulary')
    return [table[i][:] for i in ids]

def masked_vector_mean(vectors,mask):
    if not vectors or len(vectors)!=len(mask) or any(m not in (0,1) for m in mask):
        raise ValueError('Need aligned vectors and binary mask')
    width=len(vectors[0])
    if width==0 or any(len(v)!=width for v in vectors):
        raise ValueError('Need consistent nonempty vector dimensions')
    count=sum(mask)
    if count==0:
        raise ValueError('No real vectors')
    return [sum(v[j] for v,m in zip(vectors,mask) if m)/count for j in range(width)]

ids,mask=[2,4,0,0],[1,1,0,0]
vectors=lookup(ids)
print('table shape',len(table),len(table[0]),'sequence shape',len(vectors),len(vectors[0]))
print('looked-up sequence',vectors,'mask',mask)
print('masked mean',masked_vector_mean(vectors,mask))
print('incorrect all-slot mean',masked_vector_mean(vectors,[1,1,1,1]))
print('real UNK retained',masked_vector_mean(lookup([1,4,0,0]),mask))
regular={name:table[i] for name,i in known.items()}
query=[1,0]
print('query [1,0] squared distances',{name:distance2(query,v) for name,v in regular.items()})
print('all nearest ties',nearest(query,regular))
print('GO STOP / STOP GO same masked mean',masked_vector_mean(lookup([2,4]),[1,1]),masked_vector_mean(lookup([4,2]),[1,1]))
old=table[2][:]
target=[0,2]
gradient=[2*(e-t) for e,t in zip(old,target)]
new=[e-.25*g for e,g in zip(old,gradient)]
updated=[row[:] for row in table]
updated[2]=new
print('isolated GO-row gradient / new vector',gradient,new)
print('artificial objective before/after',distance2(old,target),distance2(new,target))
print('GO now collides with frozen TURN',updated[2]==updated[3])
assert table[2]==[2,0]  # Original saved table remains unchanged.
# Finite numeric components assumed. No semantic training dataset or quality result is supplied.
