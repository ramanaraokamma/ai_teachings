# Complete supplied-vocabulary encoder and separate sensor-mask investigation.
VOCAB = {'GO':2,'TURN':3,'STOP':4}

def encode(events):
    if not 1<=len(events)<=4:
        raise ValueError('Need one to four real events')
    if any(e in ('PAD','UNK') for e in events):
        raise ValueError('Reserved markers are not events')
    ids=[VOCAB.get(e,1) for e in events]
    return ids+[0]*(4-len(ids)),[1]*len(ids)+[0]*(4-len(ids))

def last_event(ids,mask):
    if len(ids)!=4 or len(mask)!=4 or any(m not in (0,1) for m in mask):
        raise ValueError('Need four IDs and a binary right-padding mask')
    n=sum(mask)
    if n==0 or mask!=[1]*n+[0]*(4-n):
        raise ValueError('Need real events followed by padding')
    if any(i not in (1,2,3,4) for i in ids[:n]) or any(i!=0 for i in ids[n:]):
        raise ValueError('Real IDs and padding IDs violate the schema')
    token_id=ids[n-1]
    # This demonstration declares review when the final event identity is unknown.
    answer='review' if token_id==1 else 'yes' if token_id==4 else 'no'
    return n-1,token_id,answer

def masked_mean(values,mask):
    if not values or len(values)!=len(mask) or any(m not in (0,1) for m in mask):
        raise ValueError('Need aligned measurements and a binary mask')
    real=[v for v,m in zip(values,mask) if m]
    if not real:
        raise ValueError('No real measurements')
    return sum(real)/len(real)

for events in [['GO','STOP'],['STOP','GO'],['WAIT','GO'],['PAUSE','GO'],['GO','WAIT']]:
    ids,mask=encode(events)
    print(events,'IDs',ids,'mask',mask,'final position/ID/result',last_event(ids,mask))
values,mask=[0,4,0,0],[1,1,0,0]
print('sensor masked mean',masked_mean(values,mask))
print('incorrect all-slot mean',sum(values)/len(values))
wrong_real=[v for v in values if v!=0]
print('incorrect discard-zero mean',sum(wrong_real)/len(wrong_real))
print('padding-only numeric changes leave masked mean',masked_mean([0,4,999,-7],mask))
print('count collision',['GO','TURN','STOP'],['STOP','TURN','GO'],'both counts',[1,1,1])
# Assume actual event strings and numeric sensor measurements. Missing input needs review.
# Token IDs are names; this program never treats their average as a measurement.
