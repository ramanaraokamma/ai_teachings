"""Fit a threshold using training data, then evaluate untouched examples."""
train = [(0, 0), (1, 0), (4, 1), (5, 1)]
values = sorted({x for x, y in train})
if len(values) < 2:
    raise ValueError("Two distinct training values are required")
candidates = [(a + b) / 2 for a, b in zip(values, values[1:])]


def errors(threshold):
    return sum(int(x >= threshold) != y for x, y in train)


threshold = min(candidates, key=errors)
test = [(2, 0), (3, 1)]
predictions = [int(x >= threshold) for x, y in test]
correct = sum(pred == y for pred, (x, y) in zip(predictions, test))
print(threshold, predictions, correct, len(test))
