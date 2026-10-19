import math


def losses(residuals):
    if not residuals:
        raise ValueError('No observed average loss without records')
    if any(type(r) not in (int, float) or not math.isfinite(r) for r in residuals):
        raise ValueError('Need finite matched residuals in one declared unit')
    mae = sum(abs(r) for r in residuals) / len(residuals)
    mse = sum(r * r for r in residuals) / len(residuals)
    return {'mae': mae, 'mse': mse, 'rmse': math.sqrt(mse)}


training_heights = [5, 7, 9]  # Fit the constant before evaluating new cases.
baseline = sum(training_heights) / len(training_heights)
observed = [10, 10, 10]      # E1, E2, E3, three different fictional objects.
candidate = [10, 10, 4]     # Supplied predictions; candidate fitting not given.
baseline_predictions = [baseline] * len(observed)
for name, predictions in [('candidate', candidate), ('mean baseline', baseline_predictions)]:
    residuals = [y - p for y, p in zip(observed, predictions)]
    print(name, residuals, losses(residuals))
# Length/order/unit identity is declared by the supplied matched E1–E3 fixture.
# Different losses can rank the same fixed predictions differently.
