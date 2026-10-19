rows = [('T01', .9, 1), ('T02', .8, 1), ('T03', .7, 1),
        ('T04', .6, 0), ('T05', .5, 1), ('T06', .4, 0),
        ('T07', .3, 1), ('T08', .2, 0), ('T09', .1, 0), ('T10', .0, 0)]


def evaluate(rows, threshold):
    if not 0 <= threshold <= 1:
        raise ValueError('Threshold outside declared 0..1 range')
    if len({i for i, score, actual in rows}) != len(rows):
        raise ValueError('Duplicate case ID')
    tp = fp = fn = tn = 0
    for item_id, score, actual in rows:
        if not 0 <= score <= 1 or actual not in (0, 1):
            raise ValueError('Need declared-range score and observed binary outcome')
        prediction = int(score >= threshold)
        tp += int(actual == 1 and prediction == 1)
        fp += int(actual == 0 and prediction == 1)
        fn += int(actual == 1 and prediction == 0)
        tn += int(actual == 0 and prediction == 0)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    accuracy = (tp + tn) / len(rows) if rows else None
    return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'precision': precision, 'recall': recall, 'accuracy': accuracy}


for threshold in [.4, .7]:
    print(threshold, evaluate(rows, threshold))
# These are development comparisons, not untouched final-test conclusions.
