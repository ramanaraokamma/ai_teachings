from statistics import mean


def fit_training_line(training, candidates):
    if not training or not candidates:
        raise ValueError('Need nonempty training and declared candidate set')
    scored = []
    for m, b in candidates:
        sse = sum((y - (m * x + b)) ** 2 for x, y in training)
        scored.append(sse)
    best_index = min(range(len(candidates)), key=lambda i: scored[i])
    return candidates[best_index], scored


def evaluate(line, evaluation):
    if not evaluation:
        raise ValueError('No observed error average without evaluation records')
    m, b = line
    predictions = [m * x + b for x, y in evaluation]
    residuals = [y - p for (x, y), p in zip(evaluation, predictions)]
    return predictions, residuals, mean(abs(r) for r in residuals), mean(r*r for r in residuals)


# Caller must supply finite numeric pairs in declared day/cm units.
training = [(0, 1), (1, 3), (2, 5)]
candidates = [(1, 1), (2, 0), (2, 1)]
line, training_sse = fit_training_line(training, candidates)
validation = [(3, 6), (4, 10)]
print(training_sse, line)
print(evaluate(line, validation))
constant = mean(y for x, y in training)
print('training mean', constant, evaluate((0, constant), validation))
