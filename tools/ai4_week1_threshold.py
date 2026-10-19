def predict(width, threshold):
    return int(width >= threshold)

def fit_threshold(training_rows, candidates):
    if not training_rows or not candidates:
        raise ValueError('training rows and candidates required')
    scored = []
    for threshold in candidates:
        mistakes = sum(predict(width, threshold) != label
                       for width, label in training_rows)
        scored.append((mistakes, threshold))
    # Tuple order implements fewest errors, then the smaller threshold.
    return min(scored)[1], scored

train = [(1, 0), (3, 0), (5, 1), (7, 1)]
threshold, scored = fit_threshold(train, [2, 4, 6])
print('training', scored)
print('frozen threshold', threshold)
# These rows are used only after selection in this complete classroom example.
test = [(2, 0), (6, 1)]
predictions = [predict(width, threshold) for width, label in test]
correct = sum(pred == label for pred, (width, label) in zip(predictions, test))
print('test predictions', predictions)
print('test correct', correct, 'of', len(test))
