# Task 4 Debugging and profiling plan

Use a temporary `print()` while developing a narrow branch; thousands of prints add formatting and console I/O overhead and can distort timing. Replace persistent diagnostics with `logging` (`DEBUG` detail during development, `WARNING` for rejected rows, `ERROR` for failed input) so output can be filtered or silenced by log level. Add assertions for internal invariants such as 0 <= hour < 24 and uniqueness of station-hour keys. Run `pdb` with a breakpoint at the validation boundary to inspect a malformed row and step through exception handling.

Example: `logger.debug("row=%d station=%r", row_number, station)`; `assert 0 <= hour < 24`; `breakpoint()`; `logger.warning("invalid PM2.5 at row %d", row_number)`. Do not log personally identifying complaint text.

Use `time.perf_counter()` around complete stages, `timeit.repeat()` for isolated functions after warm-up, and `cProfile` for call-level attribution. The benchmark runner writes `cProfile` output and uses three measured repetitions. Keep log level at WARNING and remove `breakpoint()` in production. Profiling hooks can be omitted from scheduled runs. For n rows, a streaming grouping pass is O(n) time and O(g) aggregation state for g station-day groups; retaining all row objects is O(n) memory.
