def feature(image):
    return image[0][0] + image[1][0] - image[0][1] - image[1][1]

train = [([[1, 0], [0, 0]], 1),
         ([[1, 0], [1, 0]], 1),
         ([[0, 1], [0, 0]], -1),
         ([[0, 1], [0, 1]], -1)]
valid = [([[0, 0], [1, 0]], 1),
         ([[0, 0], [0, 1]], -1)]

def mse(a, rows):
    return sum((a * feature(x) - t)**2 for x, t in rows) / len(rows)

a, checkpoints = 0.0, [0.0]
for _ in range(2):
    gradient = sum(2 * (a * feature(x) - t) * feature(x)
                   for x, t in train) / len(train)
    a -= 0.1 * gradient
    checkpoints.append(a)
for step, value in enumerate(checkpoints):
    print(step, round(value, 6), round(mse(value, train), 6),
          round(mse(value, valid), 6))
# Select using validation MSE only; exact ties keep the earlier checkpoint.
best_index = min(range(len(checkpoints)), key=lambda i: (mse(checkpoints[i],valid),i))
selected = checkpoints[best_index]
positive = sum(t == 1 for _,t in train)
negative = sum(t == -1 for _,t in train)
baseline_class = 1 if positive > negative else 0  # Declared class-0 tie rule.

def prediction(weight, image):
    d = feature(image)
    hidden = [max(0,d),max(0,-d)]
    score = weight*(hidden[0]-hidden[1])
    return d,hidden,score,int(score > 0)

def audit(weight, rows, ids, baseline):
    if len(rows) != len(ids) or not rows:
        raise ValueError('Need one ID per nonempty supplied case list')
    ledger = []
    for name,(image,target) in zip(ids,rows):
        d,h,score,pred = prediction(weight,image)
        ledger.append({'id':name,'d':d,'hidden':h,'score':score,
                       'class':int(target==1),'prediction':pred,'baseline':baseline})
    return ledger

print('selected checkpoint / weight', best_index,round(selected,6))
print('training class counts 1/0', positive,negative,'frozen baseline',baseline_class)
for split,rows,ids in [('training',train,['A','B','C','D']),('validation',valid,['E','F'])]:
    ledger = audit(selected,rows,ids,baseline_class)
    for row in ledger:
        print(split,{**row,'score':round(row['score'],6)})  # Display rounding only.
    correct = sum(r['prediction']==r['class'] for r in ledger)
    base_correct = sum(r['baseline']==r['class'] for r in ledger)
    print(split,'candidate / baseline correct / total',correct,base_correct,len(ledger))
# This public boundary probe is not one of the teacher-held final cases.
empty_pattern = [[0,0],[0,0]]
print('public equal-column-sum probe d/hidden/score/class',prediction(selected,empty_pattern))
print('Final cases absent. Save selected parameters and protocol before teacher release.')
# Fixed kernels, no bias/pooling; only a was fitted. Finite valid binary images assumed.
