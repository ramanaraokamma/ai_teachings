def build_counts(pairs, labels):
    if len(labels) != 2 or len(set(labels)) != 2:
        raise ValueError('Declare exactly two distinct labels in axis order')
    ids = [item_id for item_id, actual, predicted in pairs]
    if len(ids) != len(set(ids)):
        raise ValueError('Repeated evaluation ID: review the source')
    index = {label: i for i, label in enumerate(labels)}
    counts = [[0, 0], [0, 0]]
    for item_id, actual, predicted in pairs:
        if actual not in index or predicted not in index:
            raise ValueError('Missing, unresolved or unsupported label')
        counts[index[actual]][index[predicted]] += 1
    total = sum(sum(row) for row in counts)
    correct = counts[0][0] + counts[1][1]
    return counts, correct, total


# The complete printed C01–C20 fixture, with reference first in every pair.
pairs = [(f'C{i:02}', 'spotted', 'spotted') for i in range(1, 5)]
pairs += [('C05', 'spotted', 'healthy')]
pairs += [(f'C{i:02}', 'healthy', 'spotted') for i in range(6, 9)]
pairs += [(f'C{i:02}', 'healthy', 'healthy') for i in range(9, 21)]
labels = ['spotted', 'healthy']
counts, correct, total = build_counts(pairs, labels)
print(labels, counts)
print(correct, total, correct / total if total else 'unavailable')
# Empty evaluation has zero counts but no observed accuracy, never an invented 0%.
