from statistics import mean

cases = {
    'P': ([7, 7, 7], [[7, 9, 8], [7, 9, 8], [7, 9, 8]]),
    'Q': ([1, 1, 1], [[8, 10, 9], [7, 9, 8], [7, 9, 8]]),
    'R': ([1, 2, 3], [[7, 9, 8], [5, 7, 6], [4, 6, 5]])
}
summary = {}
for case, (training_means, validation_repeats) in cases.items():
    summary[case] = []
    for size, training_mae, repeats in zip([10, 20, 40], training_means, validation_repeats):
        if not repeats:
            raise ValueError('No observed validation mean without repeats')
        result = (size, training_mae, mean(repeats), min(repeats), max(repeats))
        summary[case].append(result)
        print(case, result)
# Supplied synthetic loss records only: no classifier, sampling or fitting is run.
# The observed min/max across three repeats is not a confidence or future interval.
