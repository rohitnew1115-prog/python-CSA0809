# Experimental investigation summary

Environment: Python 3.12.5; fixed seed 1925260050. Times are averages from repeated `time.perf_counter()` measurements and can vary by machine. The CSV files are the raw measured values.

## Moving averages

- n=365: naive 0.000220s; running sum 0.000075s; additions 2513 vs 365 (plus 358 subtractions).
- n=36500: naive 0.013774s; running sum 0.004841s; additions 255458 vs 36500 (plus 36493 subtractions).
- n=365000: naive 0.141505s; running sum 0.064801s; additions 2554958 vs 365000 (plus 364993 subtractions).

## Complaint counting

The three methods consume the same pre-tokenized list with eight distinct words. The list-count method is a deliberately small-vocabulary O(n*d) baseline.
- n=1000: dict 0.000335s; list_count 0.000366s; Counter 0.000220s.
- n=10000: dict 0.004395s; list_count 0.003434s; Counter 0.002476s.
- n=100000: dict 0.045950s; list_count 0.050003s; Counter 0.029051s.

## Sensor cleaning

- n=10000: loop 0.001164s; comprehension 0.000956s; filter 0.001286s.
- n=100000: loop 0.011743s; comprehension 0.012576s; filter 0.014591s.
- n=1000000: loop 0.126918s; comprehension 0.120759s; filter 0.154527s.

## Membership and index trade-off

See `membership_results.csv`, `timetable_index_results.csv`, and `memory_results.csv` for measured membership times, station query times, and tracemalloc peak bytes. `tuple_list_memory.csv` reports shallow container sizes only; the one million integer objects are not included in either size.
