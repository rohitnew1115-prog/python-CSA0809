# Task 6 - Design Challenge College Fest Registration Desk

Inputs: one CSV per department with `register_number,name,department,email,event`. Outputs: `master_registrations.csv`, one CSV per event, `summary.txt`, `errors.log`. Rules: fields required; email must have a local part and dotted domain; one registration per student (first valid row wins); event names are normalized; malformed lines, duplicate registration and missing files are logged; processing continues.

Flow: discover department CSV files -> parse row -> validate fields/email -> check registration set -> add accepted row -> write sorted master and event lists -> write counts and rejection log. Expected O(n) processing with hash-set duplicate detection.

Pseudocode: for file in sorted(files), for row with line number: parse; validate; if register in seen reject; else add to seen and accepted. Write each result to a temporary file then replace destination.
