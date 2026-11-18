"""Min-max scaling with defined behavior for empty and constant data."""
def min_max(values):
    values = list(values)
    if not values:
        return []
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [round((value - low) / (high - low), 3) for value in values]
