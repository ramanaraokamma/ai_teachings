# Complete fictional paper expo ledger; this is not a fitted classifier.
records = [
    {'id': f'R{i:02}', 'reference': 'clear' if i <= 8 else 'blocked',
     'candidate': 'clear' if i <= 7 or 9 <= i <= 10 else 'blocked',
     'baseline': 'clear'} for i in range(1, 13)
]
def audit(rows, field):
    if not rows or len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Need nonempty uniquely identified records')
    cells = [0, 0, 0, 0]  # TN, FP, FN, TP; blocked positive
    for r in rows:
        if r['reference'] not in ('clear', 'blocked') or r[field] not in ('clear', 'blocked'):
            raise ValueError('Missing reference or prediction; do not guess')
        cells[2 * (r['reference'] == 'blocked') + (r[field] == 'blocked')] += 1
    tn, fp, fn, tp = cells
    return {'cells': cells, 'correct': tn + tp, 'total': len(rows),
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / (tp + fn) if tp + fn else None,
            'errors': [r['id'] for r in rows if r[field] != r['reference']]}
print('candidate', audit(records, 'candidate'))
print('baseline', audit(records, 'baseline'))
print('Paper arithmetic reproduced; actual training/code/split provenance remains unprovided.')
