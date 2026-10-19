def fit_majority(labels):
    if not labels or any(label not in {'clear', 'blocked'} for label in labels):
        raise ValueError('Need nonempty resolved clear/blocked training labels')
    # The tie policy is declared before looking at validation labels.
    return 'blocked' if labels.count('blocked') > labels.count('clear') else 'clear'


def score(references, predictions):
    if not references or len(references) != len(predictions):
        raise ValueError('Need nonempty, same-case paired labels and predictions')
    if any(label not in {'clear', 'blocked'} for label in references + predictions):
        raise ValueError('Unresolved or unsupported label')
    correct = sum(actual == predicted for actual, predicted in zip(references, predictions))
    blocked_total = references.count('blocked')
    blocked_found = sum(actual == predicted == 'blocked'
                        for actual, predicted in zip(references, predictions))
    return {'correct': correct, 'total': len(references),
            'blocked_found': blocked_found, 'blocked_total': blocked_total,
            'blocked_recall': blocked_found / blocked_total if blocked_total else None}


training = ['clear', 'clear', 'blocked', 'clear', 'blocked', 'clear']
constant = fit_majority(training)
# V1–V4 share this fixed order, available feature and resolved reference label.
feature = [7, 2, 4, 1]
reference = ['blocked', 'clear', 'blocked', 'clear']
majority_predictions = [constant] * len(reference)
# Teacher-declared rule, fixed before this comparison; not fitted on validation.
rule_predictions = ['blocked' if value >= 6 else 'clear' for value in feature]
print(constant, majority_predictions, score(reference, majority_predictions))
print(rule_predictions, score(reference, rule_predictions))
