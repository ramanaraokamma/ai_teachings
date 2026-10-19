# Synthetic plant IDs, background_red flag, available leaf_marker flag, toy label.
original = [('T1', 1, 1, 1), ('T2', 1, 1, 1),
            ('T3', 0, 0, 0), ('T4', 0, 0, 0)]
crossed_additions = [('T5', 0, 1, 1), ('T6', 0, 1, 1),
                     ('T7', 1, 0, 0), ('T8', 1, 0, 0)]
# Two held-out plants P1/P2, each observed on both backgrounds; four views.
validation = [('P1-red', 1, 1, 1), ('P1-grey', 0, 1, 1),
              ('P2-red', 1, 0, 0), ('P2-grey', 0, 0, 0)]


def fit_feature(training):
    if not training or len({r[0] for r in training}) != len(training):
        raise ValueError('Need nonempty uniquely identified training records')
    if any(type(v) is not int or v not in (0, 1) for r in training for v in r[1:]):
        raise ValueError('Need complete binary flags and toy labels')
    # Human-declared rule: predict 1 iff the chosen flag is 1.
    # Candidate order/background-first tie policy is fixed before validation.
    candidates = [1, 2]
    errors = [sum(r[index] != r[3] for r in training) for index in candidates]
    winner = min(range(len(candidates)), key=lambda i: errors[i])
    return candidates[winner], errors


def predict(flags, feature):
    if len(flags) != 2 or any(type(v) is not int or v not in (0, 1) for v in flags):
        raise ValueError('Need both observed flags in background/marker order')
    return flags[feature - 1]


for version, training in [('V1', original), ('V2', original + crossed_additions)]:
    feature, errors = fit_feature(training)
    predictions = [predict(r[1:3], feature) for r in validation]
    correct = sum(p == r[3] for p, r in zip(predictions, validation))
    print(version, feature, errors, predictions, correct, len(validation))
# This toy marker perfectly tracks the toy label by construction, not in real use.
# Validation is visible development evidence; no untouched final test is supplied.
