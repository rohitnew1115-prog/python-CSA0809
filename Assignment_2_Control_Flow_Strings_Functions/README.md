# Assignment 2 — Control Flow, Strings and Functions

**Student:** P ROHIT  
**Register number:** 1925260050 
**Course:** Python Programming   
**Python:** 3.12.5 (execution environment)

Seven independent, executable programs implement the assignment screenshots. The supplied guide and correction sheet informed edge-case handling; the screenshots remain the primary specification.

## Requirements and run

Python 3.10+ is recommended (Q1 uses `match`). Standard library only; no external runtime dependencies. Install with `python -m pip install -r requirements.txt` (the file is intentionally empty of third-party packages).

```powershell
python Task01/q1_subsidy.py
python Task02/q2_otp.py
python Task03/q3_vehicle_validator.py
python Task04/q4_string_benchmark.py
python Task05/q5_functions_scope.py
python Task06/q6_recursion.py
python Task07/q7_redesign.py
```

## Questions

1. Subsidy slabs and four decision designs; tests 100, 101, 200, 201 and eight households.
2. OTP attempts: blank entries do not count; break, continue, pass and loop-else demonstrated; extra two attempts supported.
3. String-only vehicle registration normalisation, validation and receipt format; regex is discussed only as an alternative.
4. Repeated +=, join and f-string based generation timed three times at 1k, 10k and 200k parts. Actual per-run measurements and averages are in `Task04/timing_results.csv`.
5. Canteen orders, mutable default bug and fix, return values and variable scopes.
6. Naive recursion, memoisation and staircase recurrence; checks the required n=25 expected result and call count.
7. Iterative redesign compares identical inputs through 1000 and records time and update counts.

## Results and evidence

Each `TaskNN/output.txt` contains captured output from a successful execution. `evidence/` holds authentic run logs organized by question; graphical terminal screenshots were not available in this environment, so no synthetic screenshots were created. `graphs/` contains plots generated from the recorded Q4 and Q7 measurements. Q7 actual timings are in `Task07/comparison_results.csv`. The full academic report, including code appendices and analysis, is `report/Assignment_2_Final_Report.pdf`.

## Repository layout

`Task01`–`Task07` contain one independent program and task notes each; `report/` has the PDF; `evidence/Q1`–`Q7` store run logs; `graphs/` contains measurement charts. Replace student placeholders before submission. Create the required GitHub repository as `CSACS<RegisterNumber>_Assignment2` only after entering the actual register number.
