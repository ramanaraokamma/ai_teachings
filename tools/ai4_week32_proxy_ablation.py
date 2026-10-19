# All values are synthetic. setting is audit metadata, absent from candidates.
training = []
for item_id, bit in [('T1', 1), ('T2', 1), ('T3', 0), ('T4', 0)]:
    training.append({'id': item_id, 'setting': 'greenhouse' if bit else 'desk',
                     'camera_code': bit, 'room_hint': bit, 'marker': bit, 'actual': bit})
validation = []
for plant, marker in [('P1', 1), ('P2', 0)]:
    for setting, room in [('greenhouse', 1), ('desk', 0)]:
        for camera in [1, 0]:
            validation.append({'id': f'{plant}-{setting}-{camera}', 'plant': plant,
                               'setting': setting, 'camera_code': camera,
                               'room_hint': room, 'marker': marker, 'actual': marker})


def fit_feature(rows, candidates):
    if not rows or not candidates:
        raise ValueError('Need training records and declared candidate inputs')
    errors = [sum(r[name] != r['actual'] for r in rows) for name in candidates]
    winner = min(range(len(candidates)), key=lambda i: errors[i])
    return candidates[winner], errors


def report(rows, predictions):
    if len(rows) != len(predictions):
        raise ValueError('Need same-case paired predictions')
    correct = sum(r['actual'] == p for r, p in zip(rows, predictions))
    positives = sum(r['actual'] == 1 for r in rows)
    found = sum(r['actual'] == p == 1 for r, p in zip(rows, predictions))
    return correct, len(rows), found, positives


for version, candidates in [('V1', ['camera_code', 'room_hint', 'marker']),
                            ('V2-camera-removed', ['room_hint', 'marker'])]:
    feature, errors = fit_feature(training, candidates)
    predictions = [r[feature] for r in validation]
    print(version, feature, errors, report(validation, predictions))
    for setting in ['greenhouse', 'desk']:
        subset = [r for r in validation if r['setting'] == setting]
        print(setting, report(subset, [r[feature] for r in subset]))
# Fixed rule: predict positive iff chosen binary input is1; first candidate wins ties.
# V2 removes camera but still selects room_hint, a setting proxy in this toy sample.
# Two new plant identities/four views each; no model of real fairness or disease.
