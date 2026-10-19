import math

def compare_paired(actual, estimated, boundary):
    # Caller must supply matching cases in the same order and the same units.
    if len(actual) != len(estimated) or not actual:
        raise ValueError('nonempty equal-length paired values required')
    for value in list(actual) + list(estimated) + [boundary]:
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError('finite nonnegative numeric values required')
    actual_classes = [int(value > boundary) for value in actual]
    predicted_classes = [int(value > boundary) for value in estimated]
    errors = [abs(pred - ref) for ref, pred in zip(actual, estimated)]
    correct = sum(ref == pred for ref, pred in zip(actual_classes, predicted_classes))
    return {'actual_classes': actual_classes,
            'predicted_classes': predicted_classes,
            'correct': correct, 'cases': len(actual),
            'absolute_errors': errors, 'mae': sum(errors) / len(errors)}

actual = [4, 7, 9]
estimated = [5, 6, 10]
for boundary in [6, 7]:
    result = compare_paired(actual, estimated, boundary)
    print('boundary', boundary, 'cm')
    print('classes', result['actual_classes'], result['predicted_classes'])
    print('correct', result['correct'], 'of', result['cases'])
    print('MAE', round(result['mae'], 2), 'cm')
