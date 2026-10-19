import math


def summarize(records):
    if not records:
        raise ValueError('No observed residual mean without matched records')
    if len({item_id for item_id, observed, predicted in records}) != len(records):
        raise ValueError('Repeated case ID')
    residuals = []
    for item_id, observed, predicted in records:
        for value in (observed, predicted):
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError('Need finite nonnegative heights in the same declared unit')
        residuals.append(observed - predicted)
    return residuals, sum(residuals) / len(residuals), sum(abs(r) for r in residuals) / len(residuals)


# Matched case ID, observed day-7 height cm, supplied predicted height cm.
records = [('R1', 3, 4), ('R2', 5, 4), ('R3', 6, 8),
           ('R4', 10, 8), ('R5', 8, 12), ('R6', 16, 12)]
print(summarize(records))
# Semantic pairing, measurement truth and units still require source checking.
