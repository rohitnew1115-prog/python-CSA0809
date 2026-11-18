# Task 2 Cleaning and normalization

`cleaning.py` validates required fields, date formats, hourly range, duplicates, numeric types, nonnegative sensor limits and units. Missing values stay `None`; invalid rows are returned with reasons. Fahrenheit is normalized to Celsius. `normalisation.py` scales values to 0–1 and returns an empty list or zeros for empty and constant inputs.
