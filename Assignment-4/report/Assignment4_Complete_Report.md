# Assignment 4: Robust Data Processing with Files, Exceptions, Modules and Packages

**Course outcome:** CO4 - Design and implement Python programs using file handling, error handling, modules and packages to process and analyse data.  
**Student:** P ROHIT  
**Register number:** 1925260050  
**Course:** CSA0809 - Python Programming  
**Python:** 3.12.5  
**Repository:** [python-CSA0809](https://github.com/rohitnew1115-prog/python-CSA0809) (`Assignment-4/`)

## Introduction and objectives

This work implements the six assignment tasks using small, runnable Python programs. The examples use P ROHIT and Muruga Dharshini as requested. The programs use the Python standard library, UTF-8 text, context managers, record validation, recoverable error logs and modular design. Each task has input data and generated output in its folder. The report records observed program output and the automated test results.

The objectives are to process records without losing data, retain a useful trace of invalid input, select appropriate file operations, use a custom exception, compare program organizations, and build a multi-file registration workflow that continues after a bad record or missing department file.

## Task 1 - File-Processing Design Review: Diagnose and Repair a Poor Script (6 marks)

### 1.1 Diagnosis

| Defect in supplied script | Practical consequence in a hostel office |
|---|---|
| Hard-coded `C:\\Users\\Office\\Desktop\\mess_oct.txt` | The script fails on another workstation or after the file is moved. |
| File is opened without `with` and never explicitly closed | The handle can remain open, delaying flushes and blocking later file operations. |
| `read()` loads all input at once | Memory grows with the full month file instead of one record. |
| `int(parts[2])` rejects paise such as `1250.50` | Bill totals are lost or inaccurate for decimal charges. |
| Bare `except: pass` hides unrelated bugs and invalid rows | Staff see neither the cause nor which student's charge was omitted. |
| Repeated `report = report + ...` copies a growing string | Large reports waste time and memory. |
| `split('\n')` can produce a final empty item | The empty item is handled as a mysterious error rather than a known blank line. |
| No rejected-record list or audit trail | Invalid bills disappear without a review path. |
| Fields and amounts are not validated before use | Missing columns, blank identity, negative amounts or non-finite values can corrupt totals. |

### 1.2 Repaired program and run

`Task01/solution.py` accepts input and output paths, reads one line at a time, validates three fields, parses amounts as `Decimal`, records rejected rows, writes the accepted rows as they are processed, and atomically replaces the report after a complete run. The sample `Task01/data/sample_mess_oct.txt` contains two valid decimal bills, one malformed record and one blank record.

Command: `python Task01/solution.py`

Observed result: `Accepted 2 bills; total $2050.50; rejected 2`. The rejected rows are recorded in the terminal output. `Task01/output/bill_report.csv` contains both valid bills and the exact total.

### 1.3 Design defence (under 100 words)

The corrected program reads each bill as one line, closes both files with context managers, and writes accepted rows to a temporary report as it goes. It does not retain the whole input or the accepted rows in memory. Its additional memory is one line plus the rejected-line list, which grows only with invalid rows. `Decimal` preserves cents, validation rejects bad records explicitly, and atomic replacement prevents a partial report from replacing the previous good report. This makes a 50,000-line file predictable to process and leaves invalid data available for review.

### Alternative concept and complexity

With `read()` or `readlines()`, processing remains O(n) time for n input characters/records, but the input copy occupies O(n) memory. Iterating over the file also takes O(n) time while holding O(L) input memory, where L is the longest line. This implementation additionally retains O(k) memory for k rejected records because the specification asks for a rejected-line list. Accepted output rows are streamed to a temporary file. A line count does not change the asymptotic time of validation.

**Measured experiment:** `Task01/evidence/benchmark.py` generated 50,000 rows (1,250,000 input bytes). In the recorded Python 3.12.5 run, `read()+splitlines()` took 0.0683 s and peaked at 4,854,249 traced bytes; line iteration took 0.0362 s and peaked at 34,501 traced bytes. These are one local run, not universal timings; the memory difference demonstrates the expected input-storage behavior.

## Task 2 - Biometric Attendance Files (8 marks)

### 2.1 Data model

Each daily UTF-8 CSV record is `register_number,YYYY-MM-DD,status`, where status is `P` or `A`. `Task02/attendance.py` initializes a dictionary keyed by each roster registration number and accumulates present counts. The monthly percentage is `present / scheduled daily files * 100`. The summary CSV includes register number, present count, scheduled days and percentage. A second CSV lists students below 75%; a log retains the filename, line number and reason for each damaged line. An empty file, missing directory, unreadable file or invalid encoding is recorded without terminating other files.

### 2.2 File-operation choices

| Operation | Use and reason |
|---|---|
| `r` mode | Read existing daily records without changing the source evidence. |
| `w` mode | Rebuild the monthly reports from the current input set, avoiding stale totals. |
| `a` mode | Appropriate for a persistent incident log when each run should preserve history; this task regenerates its log with the reports. |
| UTF-8 | Explicit, portable decoding for input and output text. A decode failure is logged. |
| `read()` | Suitable for small one-off text; not used for daily attendance because it loads the entire file. |
| `readline()` | Useful when a caller needs one line on demand; the implementation uses iteration for concise line numbering. |
| File iteration | Streams daily records and supplies one row at a time. |
| `write()` / CSV writer | Writes results; `csv.writer` handles delimiters and line endings safely. |

### 2.3 Monthly-processing algorithm

```text
ALGORITHM ProcessMonth
INPUT: directory of daily CSV files, roster, threshold 75
OUTPUT: attendance summary, below-threshold report, damaged-line log
BEGIN
    initialize present count to zero for each roster register
    discover daily files with pathlib and sort them
    FOR each file DO
        try to open as UTF-8 CSV
        IF file cannot be read THEN log filename and reason; CONTINUE
        FOR each row with line number DO
            IF row is blank THEN CONTINUE
            IF field count, register, date, or status is invalid THEN
                log filename, line number, and reason; CONTINUE
            END IF
            increment present count when status is P
        END FOR
        log an empty file when no non-blank row was found
    END FOR
    calculate each percentage using the number of discovered daily files
    write summary CSV and separate below-75-percent CSV
    write damaged-line log
END
```

### 2.4 Trace

For `day2.csv`, the valid row `1925260051,2026-10-02,P` increments that student's present count from 0 to 1. The next row is `BAD,ROW`; it has two fields, so no attendance count changes. The processor adds `day2.csv:4: expected 3 fields, found 2` to `damaged_lines.log` and continues with the next daily file. The three sample files contain nine valid records and one damaged row.

### Alternative concept and complexity

Rereading all f files for each of s students costs O(s × f × l), where l is the average number of lines per file. Reading every file once and updating a dictionary costs O(f × l). The dictionary requires O(s) count storage, while the rereading approach can use O(1) count memory if it calculates one student's total at a time. The one-pass approach avoids repeated disk I/O and is appropriate for this monthly report.

## Task 3 - Error Handling in the Attendance Processor (9 marks)

### 3.1 Failure table

| Failure | Typical exception or condition | Handling strategy |
|---|---|---|
| Missing folder | `FileNotFoundError` / absent path | Check the input directory and report the folder problem. |
| Missing file | `FileNotFoundError` | Catch at the file boundary, preserve the cause with `raise ... from ...`, and report it. |
| Permission denied | `PermissionError` | Catch specifically, identify the file, continue with other files. |
| Wrong encoding | `UnicodeDecodeError` | Log the filename and encoding failure; do not treat text as a valid record. |
| Damaged CSV syntax | `csv.Error` | Record the affected source and continue if the reader can recover. |
| Empty file | No rows | Treat as a data-quality condition and report it; it is not necessarily a Python exception. |
| Missing or extra fields | Custom `InvalidRecord`; low-level parsing can also cause `IndexError` | Check field count before indexing and catch `InvalidRecord` per row. |
| Invalid status | Custom `InvalidRecord` | Accept only `P` or `A`; retain line number and message. |
| Invalid date or data type | `ValueError` | Validate the date or number at the record boundary and report the specific row. |
| Unexpected programmer typo | `NameError` | Do not swallow it with a broad handler; allow it to surface during development. |

### 3.2 Custom exception

`InvalidRecord(Exception)` is defined in `Task03/complete_code.py`. `parse_line()` raises it when the input does not have exactly three comma-separated fields or its status is not `P` or `A`. `summarise()` catches it for one line and stores `(line_number, message)`, so one damaged record does not discard the valid rows.

### 3.3 Complete the Code and full try statement

`Task03/complete_code.py` keeps the supplied data and program purpose, completes both TODOs and catches a missing input at the call site. `summarise()` uses `with`, the record loop uses `try/except`, successful records are processed in `else`, and the temporary demonstration file is removed in `finally`. The fuller `Task03/attendance_exceptions.py` adds specific permission and encoding handlers and wraps file errors with `raise ... from ...` so the original cause remains available.

Command: `python Task03/complete_code.py`

Observed output, matching the required tuple exactly:

```text
(1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])
```

The second missing-file check is caught and written to `Task03/output/missing_file.log`; it does not alter the required stdout line.

### 3.4 Misuse experiment

`Task03/broad_except_demo.py` deliberately references `line_numer` after defining `line_number`. With `except Exception: pass`, the resulting `NameError` is swallowed and the program prints `Program continued; the NameError was hidden.` This controlled experiment is isolated from the normal attendance processor.

### Alternative concept and complexity

Exception-based validation and conditional validation both take O(1) work per record for a fixed number of fields, or O(n) across n rows. When invalid rows are rare, the exception path stays out of normal work and communicates exceptional cases clearly. When invalid rows are common, raising and constructing exceptions has more overhead than checking field count and status with `if` statements. Conditional validation is then preferable for routine, expected invalid values. Neither approach removes the need to report the rejected row.

## Task 4 - File and Exception Forensics (7 marks)

### 4.1 Defects in the original library program

Opening `returns.log` with `w` truncates the previous day's history on every call. `write(b)` adds no separator, so adjacent book records are joined. If a write raises before `close()`, the handle is not reliably closed and buffered data may not be flushed. The `except FileNotFoundError` only prints `missing`; it does not save the error in a log. Other write and decoding errors are not handled.

### 4.2 Forensic evidence

`Task04/legacy_demo.py` preserves the defective implementation and runs it on `day1.csv`, `day2.csv` and `day3.csv`. Its generated evidence is `Task04/output/legacy_demo/returns.log`. Only the final day's records remain and those records are joined together. The missing-file case is separately demonstrated in the repaired run and recorded in `errors.log`.

### 4.3 Repair and 4.4 prevention

`Task04/library_log.py` streams CSV rows, uses nested `with` statements, opens the return log in append mode, writes proper CSV rows with newlines, validates fields, and appends errors to a separate log. The demonstration resets generated outputs once, appends all six valid returns from the three sample days, and records a missing-file error.

Two prevention rules:

1. Open every file with a context manager so it closes on both successful and exceptional paths.
2. Decide explicitly whether the output is a replacement report (`w`) or a historical log (`a`), and write a record delimiter for every record.

### Alternative concept and complexity

Manual `open()`/`close()` inside `try/finally` has the same O(n) processing time and O(L) line memory as a context manager. The context manager expresses cleanup directly and reliably closes the resource as control exits its block. In this implementation at most two files are open at once (one input and one output); a failed write still closes both. Manual code can achieve the same resource count only if every path reaches the `finally` block.

## Task 5 - The Same Utility Organised Four Ways (7 marks)

### 5.1 Four organizations

- **A - Single script:** `Task05/organization_examples/single_script.py` contains reading, percentage and absence-streak analysis, and output formatting.
- **B - One imported module:** `module_app/main.py` calls the reusable `module_app/reader.py` functions.
- **C - Three modules:** `grouped_app/reader.py`, `stats.py` and `report.py` divide input, calculations and display; `main.py` coordinates them.
- **D - Package:** `version_d_package/attendance/` contains `__init__.py`, `reader.py`, `stats.py`, `report.py` and a package entry point.

Each version reads the same daily attendance sample and reports each student's percentage and whether they were absent on three consecutive days. The observed sample identifies registers `1925260051` and `1925260052` as absent for three consecutive days.

### 5.2 Change effort

The new streak requirement touches **one file** in A, **two files** in B (module logic and main/report call), **four files** in C (reader, statistics, report and main as the presentation changes), and **two files** in D (statistics and report module). A and B require changes to a file that has more responsibilities; C and D isolate the statistical rule. The exact count is based on the checked-in implementation.

### 5.3 Comparison

| Organization | Readability | Reuse and testing | Naming conflicts | Adding the streak report |
|---|---|---|---|---|
| One script | Simple while short; crowded as features grow | Functions can be tested, but importing the script risks mixing application flow and logic | Low initially; global names share one file | Change the main script (1 file). |
| One imported module | Reusable logic is separate from the main entry point | Module functions can be imported and tested independently | Module name can collide with another top-level module | Change module and main (2 files). |
| Three modules | Input, calculation and display responsibilities are visible | Each module can be tested and reused independently | Generic names may collide unless imported through a package or unique path | Change reader, stats, report and main (4 files). |
| Package | Clear boundaries plus a namespace | Best isolation for reuse and focused tests | Package-qualified names reduce collisions | Change stats and report (2 files). |

`import attendance.stats` binds the package name `attendance`; access the function as `attendance.stats.percentage(...)`. `from attendance import stats` binds the submodule name `stats`; access it as `stats.percentage(...)`. `from attendance.stats import percentage` binds the function directly; it is concise but can obscure its source and can collide with another local `percentage` name.

### Alternative concept and complexity

Keeping every function in one script avoids package-loading work but makes it harder to locate a particular responsibility as the file grows. Imports execute a module once per process; Python stores the loaded module in `sys.modules`, so later imports reuse it. Loading a package has a small one-time startup cost and uses memory for its module objects and imported names. All four organizations read n rows in O(n) time; checking consecutive days is O(s × d) for s students and d dates in this simple ordered scan. The package does not change the core data complexity; it lowers the maintenance cost of locating a function and containing changes.

## Task 6 - College Fest Registration Desk (13 marks)

### Stage 1: Problem interpretation and testable requirements

Inputs are five UTF-8 CSV files for CSE, ECE, EEE, MECH and CIVIL. Each non-empty record has register number, name, department, email and semicolon-separated events. Outputs are a clean master CSV, one participant CSV per event, an event-count summary and an error log.

The program must: process all five departments; require five non-empty fields; check a simple email form using string methods; require the row department to match its source file; split and retain each requested event; accept only the first valid use of a register number; report duplicate, malformed, invalid-email, missing-file and unreadable-file cases with source and line where applicable; and continue to the next row or file after each recoverable error.

### Stage 2: Flow

```text
Five department files
        |
        v
Read file (missing/unreadable -> error_log.txt; continue)
        |
        v
Parse record and retain line number
        |
        v
Validate field count, department, email, events
       / \
  invalid   valid
    |         |
    v         v
log reason  check register-number set
              / \
        duplicate  new register
           |           |
           v           v
        log reason   clean master rows
                         |
                         v
         master CSV + event CSVs + summary report
```

### Stage 3: design decisions

`duplicate_checker.accept_once()` checks a set, giving expected O(1) membership per record. Email validation uses `split("@")`, `count`, `startswith`, `endswith` and whitespace checks; no external package is used. `reader.py` catches file-level errors. `validator.py` raises `InvalidRegistration` for one malformed row. `processor.py` catches that row exception and proceeds. Missing department files are logged explicitly for the fixed list of five departments.

### Stage 4: package and pseudocode

Package: `Task06/fest_registration/` with `reader.py`, `validator.py`, `processor.py`, `duplicate_checker.py`, `event_writer.py`, `report.py`, `writer.py` and `__init__.py`. Its responsibilities and SIMATS-style `ALGORITHM`, `INPUT`, `OUTPUT`, `BEGIN`, `FOR`, `IF`, `CONTINUE` and `END` pseudocode are documented in `Task06/README.md`.

### Stage 5: implementation and observed result

The five input fixtures demonstrate clean registration rows, multi-event entries, a repeated register number, an invalid email and a damaged row. The default processor expects five files; removing any file from a test copy produces a filename-specific missing-file entry while processing the rest. `Task06/tests/missing_department_demo.py` creates a persistent missing-file example in `Task06/output/missing_department_case/error_log.txt`. The generated master retains the first valid entry for register `1925260050`; event CSVs split semicolon-delimited event choices. Observed run: **4 accepted registrations, 3 rejected rows**. Outputs include `clean_master_list.csv`, `event_*.csv`, `summary_report.txt` and `error_log.txt`.

### Alternative concept and complexity

Searching a list of prior registration numbers for each row can require O(n) comparisons per row, or O(n²) total across n records. A set uses expected O(1) membership and insertion, producing O(n) average total time. Both approaches store up to O(n) registration identifiers; the set uses additional hash-table overhead. The fixed input order makes first-valid-registration-wins deterministic.

**Measured experiment:** `Task06/evidence/benchmark.py` checked 5,000 unique registration keys. In the recorded local run, list membership took 0.1291 s and set membership took 0.0012 s; both retained all 5,000 keys. This small measurement supports, but does not replace, the average-case complexity analysis.

## Execution and verification record

All six task programs, the four Task 5 organizations, the supplied Task 3 complete-code program, the isolated broad-exception experiment and the Task 6 package were executed from the `Assignment-4` directory. The observed Task 3 tuple matched exactly. The Task 4 repaired run preserved six returns and logged the missing input. Task 6 generated its master, five event participant files, summary and row-level error log.

Automated verification command: `python -m unittest discover -s tests -v`  
Observed result: **6 shared tests passed**, plus **1 focused Task 6 test passed** with `python -m unittest discover -s Task06/tests -v`. The tests cover decimal bills and missing inputs, monthly attendance and damaged data, exact Task 3 parsing and exception chaining, append-only returns, consecutive absence, and Task 6 duplicate/email/damaged/missing-department handling.

The project uses Python 3.12.5 and the standard library only. Terminal output logs are stored under task evidence folders because this workspace did not provide a screenshot capture workflow.

## Conclusion

The six implementations demonstrate streaming file handling, decimal-safe totals, monthly aggregation, precise exception boundaries, append-only logging, four code organizations and a modular multi-department registration pipeline. Invalid records are visible in logs, and recoverable input problems do not stop the remaining work. The repository includes the runnable sources, sample data, generated reports, tests, README and this report.
