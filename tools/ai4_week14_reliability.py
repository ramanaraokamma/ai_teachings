# Fictional score p(positive), observed binary outcome. Bins declared in advance.
rows = [(f'L{i:02}', 0.2, int(i <= 2)) for i in range(1, 11)]
rows += [(f'M{i:02}', 0.5, int(i <= 7)) for i in range(1, 11)]
rows += [(f'H{i:02}', 0.8, int(i <= 6)) for i in range(1, 11)]
bins = [('low', 0.0, 0.35), ('middle', 0.35, 0.65), ('high', 0.65, 1.0)]
for name, left, right in bins:
    selected = [(p, y) for item_id, p, y in rows
                if left <= p and (p < right or right == 1.0 and p <= right)]
    if not selected:
        print(name, 'no observations')
        continue
    mean_score = sum(p for p, y in selected) / len(selected)
    positives = sum(y for p, y in selected)
    frequency = positives / len(selected)
    print(name, len(selected), round(mean_score, 3), positives, round(frequency, 3))
# These groups describe p(positive), not the correctness rate of chosen labels.
# No calibrator is fitted, and no population guarantee follows from ten cases/bin.
