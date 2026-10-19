# Complete synthetic saved-output record for arithmetic replay, not model training.
references = ['clear' if i % 2 else 'blocked' for i in range(1, 21)]
predictions = {}
for seed, mistakes in [(11, 6), (22, 4), (33, 8)]:
    predictions[seed] = [('blocked' if y == 'clear' else 'clear') if i < mistakes else y
                         for i, y in enumerate(references)]
accuracies = []
for seed in [11, 22, 33]:
    correct = sum(y == p for y, p in zip(references, predictions[seed]))
    accuracies.append(correct / len(references))
    print(seed, correct, len(references))
print('mean', round(sum(accuracies) / len(accuracies), 6))
print('range percentage points', round(100 * (max(accuracies) - min(accuracies)), 6))
# Seeds label supplied run records here; no classifier or random process is rerun.
