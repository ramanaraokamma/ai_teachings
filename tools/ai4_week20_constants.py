import math
from statistics import mean, median


def check_heights(values):
    if not values:
        raise ValueError('Need nonempty observed heights')
    if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('Need finite nonnegative heights in the declared unit')


def fit_constants(training):
    check_heights(training)
    return {'mean': mean(training), 'median': median(training)}


def evaluate(constants, targets):
    check_heights(targets)
    results = {}
    for name, value in constants.items():
        errors = [abs(y - value) for y in targets]
        results[name] = {'constant': value, 'absolute_errors': errors, 'mae': mean(errors)}
    return results


training = [2, 4, 6, 12]
validation = [4, 8]
constants = fit_constants(training)
print(constants)
print(evaluate(constants, validation))
# Investigate a supplied training-value change; validation stays the same.
changed_constants = fit_constants([2, 4, 6, 40])
print(changed_constants)
print(evaluate(changed_constants, validation))
