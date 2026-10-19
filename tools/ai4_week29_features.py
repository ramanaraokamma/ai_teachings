import math
from statistics import mean


def features(length_cm, width, width_unit='cm'):
    if width_unit not in ('cm', 'mm'):
        raise ValueError('Need an explicit supported width unit')
    if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0
           for v in (length_cm, width)):
        raise ValueError('Need observed finite nonnegative dimensions')
    width_cm = width if width_unit == 'cm' else width / 10
    area = length_cm * width_cm
    ratio = length_cm / width_cm if width_cm != 0 else None
    return {'width_cm': width_cm, 'area_cm2': area, 'length_over_width': ratio}


def fit_area_mean(training):
    if not training:
        raise ValueError('Need nonempty training dimensions')
    return mean(features(length, width)['area_cm2'] for length, width in training)


training = [(2, 3), (4, 2), (6, 1)]  # Both dimensions cm.
training_mean = fit_area_mean(training)
query = features(5, 2)
print(training_mean, query['area_cm2'], query['area_cm2'] - training_mean)
print(features(12, 30, 'mm'))
print(features(5, 0))  # Zero area is computed; the ratio is unavailable.
# A missing observed dimension is not a measured zero; this contract rejects it.
# No label, future outcome or validation feature enters the fitted training mean.
