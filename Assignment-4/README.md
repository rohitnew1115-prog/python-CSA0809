# Assignment 4 - Robust Data Processing

**Student:** P ROHIT  
**Registration number:** 1925260050  
**Course:** CSA0809 - Python Programming

Six independently runnable tasks implement the SIMATS Assignment 4 requirements for file processing, data validation, exceptions, modules, packages, and dependable reporting. Python standard library only; tested on Python 3.12.5.

## Run

From this folder, run `python Task01/solution.py` through `python Task06/main.py`. Each task reads its included sample data and writes outputs below its `output/` folder. Task 5 package: `python -m Task05.attendance_package`; Task 5 organization examples: run scripts in `Task05/organization_examples/`; Task 6: `python Task06/main.py`. Run all tests with `python -m unittest discover -s tests -v`.

## Structure

- `Task01/solution.py`: diagnose/repair the hotel bill script and streaming report.
- `Task02/attendance.py`: daily biometric files, monthly attendance, low-attendance and damaged-line reports.
- `Task03/attendance_exceptions.py`: strict three-field parser and custom exception.
- `Task04/library_log.py`: append-only daily return log and forensic reproductions.
- `Task05/attendance_package/`: importable reader, statistics, reports, CLI; consecutive-absence report.
- `Task06/fest_package/`: event registration validation, duplicate handling, clean lists, summary and error log.
- `tests/`: unittest cases for normal and failure paths.
- `docs/assignment_checklist.md`: question-by-question mapping and analytical responses.
- `report/Assignment_4_Report.pdf`: submission report matching Assignment 3 PDF styling.
- `data/`: realistic input files; `outputs/`: generated evidence.

## Data formats

Attendance CSV: `register_number,date,status` where status is P or A. Task 3 additionally demonstrates the supplied dotted `register.date.status` record. Task 6 input CSV: `register_number,name,department,email,event`; event is one line per registered event.

## Error handling

Files are opened with UTF-8 and context managers. Invalid rows are logged with file and line number while valid rows continue. Task 3 raises `InvalidRecord` for record-level defects and preserves the cause when wrapping file errors. Outputs are written to temporary files and atomically replaced where a complete report must not be truncated.

