# Assignment 4 requirement map

| PDF item | Response / implementation | Execution evidence |
|---|---|---|
| Task 1.1 diagnosis | Nine practical defects and office consequences are listed in `report/Assignment4_Complete_Report.md`. | `Task01/solution.py`, `Task01/evidence/run.txt` |
| Task 1.2 repair | Parameterized paths, `with`, streamed input/output, `Decimal`, validation and rejected-line list. | `Task01/data/sample_mess_oct.txt`, `Task01/output/bill_report.csv` |
| Task 1.3 defence and complexity | Under-100-word defence and O(n) / O(L + k) comparison in the report. | Report section Task 1 |
| Task 2.1-2.2 model and operations | CSV schema, dictionary, reports, modes, encodings and methods explained. | `Task02/attendance.py` |
| Task 2.3 processing | `pathlib` discovery, validation, percentage/threshold CSVs and damaged-line log. | `Task02/output/` |
| Task 2.4 trace and complexity | Step-by-step dictionary trace and O(s × f × l) vs O(f × l) discussion. | Report section Task 2 |
| Task 3.1-3.3 failures, exception and try flow | Failure table, `InvalidRecord`, specific catches, `else`, `finally` and exception chaining. | `Task03/complete_code.py`, `Task03/attendance_exceptions.py` |
| Task 3 supplied code | TODOs completed; expected tuple matched exactly; missing file is handled. | `Task03/evidence/complete_code.txt` |
| Task 3.4 misuse | Separate controlled `NameError` hidden by `except Exception: pass`. | `Task03/broad_except_demo.py`, `Task03/evidence/broad_except.txt` |
| Task 4.1-4.2 forensic demo | Original truncation and missing separator retained; three daily fixtures run. | `Task04/legacy_demo.py`, `Task04/output/legacy_demo/returns.log` |
| Task 4.3-4.4 repair | Append mode, CSV newline handling, context managers and error log; rules and try/finally analysis. | `Task04/library_log.py`, `Task04/output/returns.log`, `Task04/output/errors.log` |
| Task 5.1 organizations | Same attendance utility as script, one imported module, three modules and package. | `Task05/organization_examples/`, `Task05/version_d_package/` |
| Task 5.2 streak feature | All versions report three consecutive absent days; changed-file counts are stated in report. | `Task05/evidence/` |
| Task 5.3 comparison | Comparison table, import forms, module cache, memory and change effort. | Report section Task 5 |
| Task 6 Stage 1-3 | Inputs/outputs, testable rules, email checks, set deduplication and error boundaries. | `Task06/README.md`, `Task06/fest_registration/` |
| Task 6 Stage 4 | Package responsibilities and SIMATS pseudocode. | `Task06/README.md` |
| Task 6 Stage 5 | Five department inputs, multi-event lists, invalid/duplicate/damaged rows, complete reports; missing-file case is tested. | `Task06/data/`, `Task06/output/`, tests |
| Final verification | All task commands and four Task 5 versions were executed; automated suite passed. | `screenshots/unittest.txt` and task `evidence/` logs |

## Complexity notes

- Task 1 input scan: O(n) time; O(L + k) working memory for longest line L and k rejected lines. Accepted bill rows are streamed to a temporary output.
- Task 2 one-pass aggregate: O(f × l) time and O(s) count storage; rereading per student costs O(s × f × l).
- Task 3 fixed-width parsing: O(n) time over n records; conditionals avoid exception construction when invalid values are common.
- Task 4 append processing: O(n) time, O(L) record memory, two file handles maximum.
- Task 5 all arrangements have the same record complexity; package import is a one-time cached load in `sys.modules`.
- Task 6 set-based deduplication: O(n) expected total time and O(n) identifier storage; list search can require O(n²) time.
