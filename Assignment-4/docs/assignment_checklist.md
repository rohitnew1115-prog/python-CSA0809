# Assignment 4 checklist

| Question | Requirement and response | Implementation | Verification |
|---|---|---|---|
| Task 1.1 Diagnose the Script (2) | Identifies hard-coded path, unclosed handle, whole-file memory load, malformed unpacking, unguarded amount conversion, repeated string concatenation, blank final record and silent rejection. | Task01/solution.py, diagnose() | Unit tests and CLI |
| Task 1.2 Repair the Design (3) | Parameterized path; context manager; line streaming; specific exceptions; rejected-row list; incremental report; missing file reported. | Task01/solution.py | Unit tests and CLI |
| Task 1.3 Design Defence (1) | Streaming keeps O(1) record memory; simpler than read-all for 50,000 lines. | Report | Review |
| Task 2.1 Model the Data (2) | CSV schema, dictionary counts keyed by registration, percentage and output files. | Task02/attendance.py | Unit tests |
| Task 2.2 Design the File Operations (2) | pathlib discovery, UTF-8 readers/writers, context managers and explicit missing-file errors. | Task02/attendance.py | Unit tests |
| Task 2.3 Design the Processing (3) | Month-wide aggregation; P/A validation; below-75% list and damaged-row log. | Task02/attendance.py | Unit tests |
| Task 2.4 Trace (1) | Valid, absent, damaged, empty and missing input behavior is shown. | Task02/data, outputs | CLI + tests |
| Task 3.1 Identify Failures (3) | Enumerates missing paths, permission, encoding, value/date/status/field count, empty file and line number risks. | Task03/attendance_exceptions.py | Tests |
| Task 3.2 Custom Exception (2) | InvalidRecord stores source and line and is raised on malformed data. | Task03/attendance_exceptions.py | Tests |
| Task 3.3 Complete try statement (3) | Specific catches; finally cleanup; exception chaining at file boundary. | Task03/attendance_exceptions.py | Tests |
| Task 3.4 Misuse Experiment (1) | Documents broad-catch masking and demonstrates a deliberately wrong name in a test-only example. | docs/assignment_checklist.md | Review |
| Task 4.1 Locate Defects (2) | `w` truncates earlier days; missing newline merges records; no error log; exceptions stop processing. | Task04/library_log.py | Tests |
| Task 4.2 Construct Evidence (2) | Three-day fixture has append, newline, and missing-file conditions. | Task04/data | CLI |
| Task 4.3 Repair Program (2) | Append mode, normalized newline, report and error log. | Task04/library_log.py | Tests |
| Task 4.4 Prevent Recurrence (1) | Atomic output, context manager, explicit append policy and regression test. | Task04/library_log.py | Tests |
| Task 5.1 Four Organisations (3) | Standalone script, one imported module, grouped modules and package are shown with `__main__` guard. | Task05/organization_examples; Task05/attendance_package | CLI and import checks |
| Task 5.2 Change Requirement (2) | Adds second report of students absent three consecutive days and files changed. | Task05/attendance_package/reports.py | Tests |
| Task 5.3 Compare Organisations (2) | Four forms produce same results; package maintains lower change coupling. | Report | Review |
| Task 6 Stage 1 (2) | Inputs, outputs and validation rules specified. | Task06/README.md | Review |
| Task 6 Stage 2 (2) | Input-to-validation-to-deduplication-to-outputs flow documented. | Task06/README.md | Review |
| Task 6 Stage 3 (2) | Duplicate registration, invalid email, damaged line and missing file decisions stated. | Task06/fest_package/processor.py | Tests |
| Task 6 Stage 4 (4) | Package structure, focused modules and pseudocode included. | Task06/fest_package | Import tests |
| Task 6 Stage 5 (3) | Clean master/event lists, summary, error log; tolerant continuation demonstrated. | Task06/main.py | CLI + tests |

## Task 1.1: diagnosed defects
The file path is fixed to one machine; `open` has no context manager; `read()` loads all 50,000 lines; iterating the text iterates characters rather than records; unpacking does not validate columns; numeric conversion can terminate the program; a bare `except` hides all failures; string concatenation is repeatedly quadratic; blank lines are not skipped and bad records disappear without audit.

## Task 1.3: design defence
A line iterator holds only the current record, so auxiliary memory is O(1) with respect to the number of lines (the report itself is accumulated in a list here for one final atomic write; this can also be streamed to a temporary output). `read()`/`readlines()` require O(n) input memory. For 50,000 rows, a simple streaming loop has predictable memory and clear per-row recovery.

## Task 2.4 trace
The sample contains valid P/A entries and one malformed row. Valid entries increment counts; malformed input is recorded with its file and line; students below 75% appear in the separate roster report; missing files are reported without discarding prior valid rows. Empty input creates valid empty reports.

## Task 3.4 misuse experiment
Replacing `except ValueError` with bare `except` makes a misspelled variable (`line_numer`) look like an ordinary rejected record, hiding a programming defect. Catch only expected input errors; unexpected exceptions should remain visible.

## Task 4.1 forensic findings
Opening the log with `w` on every daily run truncates earlier returns. Writing without a newline fuses adjacent records. A missing input file terminates the run, and there is no per-file error evidence.

## Task 5.3 complexity and effort
For n records over d files, reading and counting costs O(n); consecutive-day checks cost O(s*d) for s students in the straightforward matrix. All organizations share this algorithmic complexity. A package adds import/module loading overhead once, negligible for this workload, while reducing the cost and risk of changing one concern because reader, statistics and report writer are isolated.

## Task 6 flow and key decisions
Department files -> parse and validate each line -> log malformed rows -> reject invalid email -> reject repeated registration number -> retain valid registrations -> atomically write master list, event lists and summary. A set provides expected O(1) duplicate checks, compared with O(n) search per input and O(n^2) total for a list. On an error the pipeline continues to other lines and files; generated outputs report rejected records.
