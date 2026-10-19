def build_report(record):
    # Short fictional classroom records, not arbitrary text or live measurements.
    fields = {'source_id', 'cups', 'days', 'losses_ml', 'initial_ml'}
    if type(record) is not dict or set(record) != fields:
        raise ValueError('exact record fields required')
    if type(record['source_id']) is not str or not record['source_id']:
        raise ValueError('source ID required')
    for key in ['cups', 'days']:
        if type(record[key]) is not int or record[key] < 1:
            raise ValueError('positive integer counts required')
    losses = record['losses_ml']
    initial = record['initial_ml']
    for values, minimum in [(losses, 0), (initial, 1)]:
        if values is not None:
            if type(values) is not list or len(values) != record['cups']:
                raise ValueError('one value per cup required')
            if any(type(x) is not int or x < minimum for x in values):
                raise ValueError('integer mL values outside the toy contract')
    if initial is not None and losses is None:
        raise ValueError('initial values do not supply losses')
    if initial is not None and any(x > y for x, y in zip(losses, initial)):
        raise ValueError('loss cannot exceed initial volume')
    half = None
    if losses is not None and initial is not None:
        half = all(2 * loss == start for loss, start in zip(losses, initial))
    return {'source_id': record['source_id'],
            'procedure': {'cups': record['cups'], 'days': record['days']},
            'losses_ml': losses, 'all_lost_half': half}

E2 = {'source_id': 'E2', 'cups': 3, 'days': 4,
      'losses_ml': None, 'initial_ml': None}
E3 = {'source_id': 'E3', 'cups': 3, 'days': 4,
      'losses_ml': [1, 2, 3], 'initial_ml': None}
print(build_report(E2))
print(build_report(E3))
