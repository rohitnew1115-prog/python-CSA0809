# Task 6 - College Fest Registration Desk

## Requirements and rules

Read one UTF-8 CSV per department. Each non-empty row has `register_number,name,department,email,events`; multiple events are separated with semicolons. Accept only five-field rows with non-empty values, a simple local-part/domain email shape, matching department and at least one event. The first valid registration number wins across all departments. Log malformed rows, invalid emails, duplicates, unreadable files and missing department files with the source name and, for records, line number. Continue after every recoverable error.

## Processing flow

```text
Five department CSV files -> read each file -> parse row with line number
  -> validate fields and email -> check register-number set
     -> invalid/duplicate: append reason to error log
     -> valid: add to clean master rows
  -> write clean_master_list.csv, event_*.csv, summary_report.txt, error_log.txt
```

## Package structure

- `fest_registration/reader.py`: UTF-8 file reading and file-level errors.
- `fest_registration/validator.py`: row and email validation; `InvalidRegistration`.
- `fest_registration/duplicate_checker.py`: set-based first-valid registration rule.
- `fest_registration/processor.py`: orchestration across CSE, ECE, EEE, MECH and CIVIL.
- `fest_registration/event_writer.py`: event-wise participant CSV files.
- `fest_registration/report.py`: event counts.
- `fest_registration/writer.py`: master, summary and error outputs.

## SIMATS algorithmic pseudocode

```text
ALGORITHM ProcessFestRegistrations
INPUT: department directory, ordered list [CSE, ECE, EEE, MECH, CIVIL]
OUTPUT: clean master CSV, one CSV per event, summary report, error log
BEGIN
    accepted <- empty list; seen <- empty set; errors <- empty list
    FOR each department in ordered list DO
        file <- department directory + department filename
        IF file cannot be opened THEN
            append filename and reason to errors; CONTINUE
        END IF
        FOR each non-empty row and its line number DO
            parse exactly five fields
            IF fields, department, email, or events are invalid THEN
                append filename, line number, and reason to errors; CONTINUE
            END IF
            IF register number is in seen THEN
                append filename, line number, and duplicate reason to errors; CONTINUE
            END IF
            add register number to seen; append registration to accepted
        END FOR
    END FOR
    write accepted rows to clean master CSV
    group accepted rows by each event and write one event CSV per group
    write event counts to summary report; write all errors to error log
END
```

## Demonstration

Run `python Task06/main.py` from the Assignment-4 directory. The five fixtures include clean rows, a duplicate register number, an invalid email and a damaged row. The default collector also expects all five department files and logs a missing file if one is absent. Generated files are under `output/`.

Run focused missing-file and invalid-record checks with `python -m unittest discover -s Task06/tests -v`. Run `python Task06/tests/missing_department_demo.py` to preserve a concrete four-missing-department error-log example in `output/missing_department_case/`.
