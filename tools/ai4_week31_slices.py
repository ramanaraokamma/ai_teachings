# Complete synthetic saved-output realization of camera A:2/20 and B:3/5 errors.
records = []
for i in range(1, 21):
    records.append({'id': f'A{i:02}',
                    'light': 'bright' if i <= 5 or 13 <= i <= 17 else 'dim',
                    'type': 'Alpha' if i <= 5 or 11 <= i <= 15 else 'Beta',
                    'camera': 'A', 'actual': 'spotted' if i <= 10 else 'healthy',
                    'prediction': 'spotted' if i <= 12 else 'healthy'})
for i in range(1, 6):
    records.append({'id': f'B{i:02}', 'light': 'dim', 'type': 'Beta', 'camera': 'B',
                    'actual': 'spotted' if i <= 3 else 'healthy',
                    'prediction': 'spotted' if i in (3, 4) else 'healthy'})


def summarize(rows):
    errors = sum(r['actual'] != r['prediction'] for r in rows)
    positives = sum(r['actual'] == 'spotted' for r in rows)
    found = sum(r['actual'] == r['prediction'] == 'spotted' for r in rows)
    return {'errors': errors, 'count': len(rows),
            'error_rate': errors / len(rows) if rows else None,
            'positive_found': found, 'positive_count': positives,
            'recall': found / positives if positives else None}


for field, groups in [('light', ['bright', 'dim']),
                      ('type', ['Alpha', 'Beta']), ('camera', ['A', 'B', 'C'])]:
    for group in groups:
        print(field, group, summarize([r for r in records if r[field] == group]))
print('pooled', summarize(records))
# Each case is one distinct fictional plant; groups partition within each field.
# Across fields the same cases recur, so do not sum lighting+type+camera counts.
# Inputs are complete resolved reference/prediction records, not model training.
