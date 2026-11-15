# Assignment 4 - Robust Data Processing with Files, Exceptions, Modules and Packages

| Student | Register number | Course outcome | Python |
|---|---|---|---|
| P ROHIT | 1925260050 | CO4 | 3.12.5 |

**Repository:** [python-CSA0809](https://github.com/rohitnew1115-prog/python-CSA0809)
**Libraries:** Python standard library only; no third-party dependencies. See `requirements.txt`.

This folder contains all six Assignment 4 tasks. Sample names use P ROHIT and Muruga Dharshini as requested. Each task includes input files and generated output. Run commands from this directory.

## Installation

Install Python 3.12 or later. No `pip install` step is required because the programs use only the standard library.

## Run each task

| Task | Command | Result |
|---|---|---|
| 1 - File processing | `python Task01/solution.py` | Decimal-safe bill report; invalid and empty lines are identified. |
| 2 - Attendance files | `python Task02/attendance.py` | Monthly percentages, below-75% list and damaged-line log. |
| 3 - Exceptions | `python Task03/complete_code.py` | Prints the exact expected tuple and logs missing-file handling. |
| 3 - Broad-except experiment | `python Task03/broad_except_demo.py` | Shows the controlled `NameError` hidden by `except Exception: pass`. |
| 4 - Original defective program | `python Task04/legacy_demo.py` | Preserves the overwrite and joined-record evidence. |
| 4 - Repaired log | `python Task04/library_log.py` | Appends all daily returns and logs a missing file. |
| 5A - Single script | `python Task05/organization_examples/single_script.py` | Attendance percentages and three-day absence results. |
| 5B - One module | `python Task05/organization_examples/module_app/main.py` | Same analysis through an imported module. |
| 5C - Three modules | `python Task05/organization_examples/grouped_app/main.py` | Same analysis through reader, stats and report modules. |
| 5D - Package | `python -m Task05.version_d_package.attendance` | Same analysis through an importable package. |
| 6 - Fest registration | `python Task06/main.py` | Clean master, event participant CSVs, summary and error log. |

Run the missing-department demonstration with `python Task06/tests/missing_department_demo.py`; its error log is saved under `Task06/output/missing_department_case/`.

Run the shared automated tests with `python -m unittest discover -s tests -v`, and Task 6 focused tests with `python -m unittest discover -s Task06/tests -v`.

## Repository structure

```text
Task01/                         Decimal-safe file processing
Task02/                         Biometric attendance processor and data
Task03/                         Custom exception, exact exercise and misuse demo
Task04/                         Original forensic example and repaired logger
Task05/organization_examples/   Versions A, B and C
Task05/version_d_package/       Version D package and sample attendance data
Task06/fest_registration/       Fest package modules
Task06/data/                    Five department fixtures
Task06/output/                  Generated master, event lists, summary and log
tests/                          Shared automated unittest suite
Task06/tests/                   Fest-package error-path tests
docs/assignment_checklist.md    Requirement-to-source mapping
report/Assignment4_Complete_Report.md
output/pdf/Assignment_4_Report.pdf
```

## Task result summary

1. Task 1 identifies the supplied defects and streams validated bill lines using `Decimal`; the sample total is **$2050.50**.
2. Task 2 processes all daily files, calculates percentages, and logs a damaged row with filename and line number.
3. Task 3 defines `InvalidRecord`, completes both supplied TODOs, matches the expected tuple, and isolates a broad-except demonstration.
4. Task 4 shows the original overwrite and missing separators, then preserves all six returns with append mode and logs the missing input.
5. Task 5 runs the same percentage and three-consecutive-absence report as a script, module, grouped modules and package.
6. Task 6 processes CSE, ECE, EEE, MECH and CIVIL fixtures, accepts **4** registrations and records **3** invalid/duplicate rows.

## Report and execution evidence

The full academic report is `report/Assignment4_Complete_Report.md`; the formatted PDF is `output/pdf/Assignment_4_Report.pdf`. Task execution logs are kept in each task's `evidence/` folder; this environment did not provide a screenshot-capture workflow.
