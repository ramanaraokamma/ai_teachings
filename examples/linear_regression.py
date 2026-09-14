"""Fit a line to training pairs and evaluate a separate example."""
train = [(1, 3), (2, 5), (3, 7)]
if not train:
    raise ValueError("Training examples are required")
n = len(train)
x_mean = sum(x for x, y in train) / n
y_mean = sum(y for x, y in train) / n
num = sum((x - x_mean) * (y - y_mean) for x, y in train)
den = sum((x - x_mean) ** 2 for x, y in train)
if den == 0:
    raise ValueError("Distinct training ages are required")
slope = num / den
intercept = y_mean - slope * x_mean
test = [(4, 10)]
if not test:
    raise ValueError("Test examples are required for MAE")
preds = [slope * x + intercept for x, y in test]
mae = sum(abs(y - pred) for pred, (x, y) in zip(preds, test)) / len(test)
print(slope, intercept, preds, mae)
