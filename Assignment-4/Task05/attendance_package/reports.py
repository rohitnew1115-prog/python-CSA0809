from pathlib import Path
import csv
def write_reports(output: Path, percentages: dict[str,float], streaks: list[str]):
    output.mkdir(parents=True,exist_ok=True)
    with (output/"attendance_percentages.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["register_number","percentage"]); w.writerows((r,f"{p:.2f}") for r,p in sorted(percentages.items()))
    (output/"absent_three_consecutive_days.txt").write_text("\n".join(streaks)+("\n" if streaks else ""),encoding="utf-8")
