"""Invented development scores; no model or human-review run is claimed."""
from math import isfinite
rows = [('A', 'clear', .95, 1), ('B', 'blurred', .90, 0),
        ('C', 'clear', .80, 1), ('D', 'blurred', .60, 0),
        ('E', 'clear', .45, 0), ('F', 'blurred', .10, 1)]
def report(rows, cutoff):
    if not rows or not isfinite(cutoff) or not .5 <= cutoff <= 1:
        raise ValueError('Need rows and finite cutoff in [0.5,1]')
    ledger = []
    for name, condition, p1, label in rows:
        if not isfinite(p1) or not 0 <= p1 <= 1 or label not in (0,1):
            raise ValueError('Invalid score or binary reference')
        pred = int(p1 >= .5)
        confidence = max(p1, 1-p1)
        ledger.append((name, pred, confidence, pred == label,
                       confidence >= cutoff))
    accepted = [r for r in ledger if r[4]]
    return {'ledger': ledger, 'total': len(rows),
            'correct': sum(r[3] for r in ledger),
            'accepted': [r[0] for r in accepted],
            'deferred': [r[0] for r in ledger if not r[4]],
            'coverage': len(accepted)/len(rows),
            'accepted_accuracy': (sum(r[3] for r in accepted)/len(accepted)
                                  if accepted else None)}
for cutoff in [.5, .8, .95, .99]:
    print(cutoff, report(rows, cutoff))
r = report(rows, .8)
assert r['accepted'] == ['A','B','C','F']
assert r['deferred'] == ['D','E']
assert r['correct'] == 3 and r['accepted_accuracy'] == .5
assert report(rows,.99)['accepted_accuracy'] is None
confusion = {'TP':0, 'TN':0, 'FP':0, 'FN':0}
for _, _, p1, label in rows:
    pred = int(p1 >= .5)
    key = ('TP' if label else 'FP') if pred else ('FN' if label else 'TN')
    confusion[key] += 1
assert confusion == {'TP':2,'TN':1,'FP':2,'FN':1}
print('Confusion counts:', confusion)
for condition in ['clear','blurred']:
    group = [r for r in rows if r[1] == condition]
    print(condition, report(group,.8)['correct'], '/',len(group))
# Separate pictured scores: stricter cutoff keeps the confidently wrong case.
picture = [('A','toy',.9,0),('B','toy',.6,1),('C','toy',.2,0)]
assert report(picture,.8)['accepted_accuracy']==.5
assert report(picture,.85)['accepted_accuracy']==0
print('Picture cutoff .85:',report(picture,.85))
# No human review outcomes or controlled blur comparisons are supplied.
