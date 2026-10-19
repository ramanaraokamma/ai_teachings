"""Supplied frozen extractor; fit only the target threshold on training rows."""
from math import isfinite
train = [('T1', [1, 1], 0), ('T2', [1, 3], 0),
         ('T3', [4, 2], 1), ('T4', [5, 3], 1)]
validation = [('V1', [2, 1], 0), ('V2', [3, 4], 1)]
def feature(x):
    if len(x) != 2 or any(not isfinite(v) or v < 0 for v in x):
        raise ValueError('Need two finite nonnegative counts')
    return max(0, x[0] + x[1])
def predict(x, threshold):
    return int(feature(x) >= threshold)
def errors(threshold):
    return sum(predict(x, threshold) != y for _, x, y in train)
candidates = [3, 5, 7]
best = min(candidates, key=lambda t: (errors(t), t))
counts = {y: sum(label == y for _, _, label in train) for y in (0, 1)}
baseline = min(counts, key=lambda y: (-counts[y], y))
ledger = [(name, feature(x), y, predict(x, best), baseline)
          for name, x, y in validation]
head_correct = sum(pred == y for _, _, y, pred, _ in ledger)
baseline_correct = sum(base == y for _, _, y, _, base in ledger)
assert [errors(t) for t in candidates] == [1, 0, 1]
assert (best, baseline, head_correct, baseline_correct) == (5, 0, 2, 1)
assert predict([2, 3], best) == 1  # equality belongs to class 1
print('Threshold mistakes:', [(t, errors(t)) for t in candidates])
print('Training label counts:', counts, 'baseline:', baseline)
print('Validation: name, h, label, head, baseline', ledger)
print('Correct on same two rows:', head_correct, baseline_correct)
# Different target: first count exceeds second. Both original features collide.
u, v = [1, 3], [3, 1]
assert feature(u) == feature(v) == 4
# This repair is hand supplied, not trained or independently evaluated.
def supplied_repair(x):
    return int(max(0, x[0] - x[1]) >= 1)
assert (supplied_repair(u), supplied_repair(v)) == (0, 1)
print('Collision h:', feature(u), feature(v), 'supplied repair:',
      supplied_repair(u), supplied_repair(v))
