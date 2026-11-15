"""Version A: reading, attendance statistics, streaks and report in one script."""
from pathlib import Path
import csv
from datetime import date, timedelta

def main():
    data = Path(__file__).parents[1] / "version_d_package" / "attendance" / "data"
    rows = []
    for path in sorted(data.glob("*.csv")):
        with path.open(encoding="utf-8", newline="") as source:
            rows.extend(row for row in csv.reader(source) if len(row) == 3 and row[2] in {"P", "A"})
    per_student = {}
    for register, day_text, status in rows:
        per_student.setdefault(register, {})[date.fromisoformat(day_text)] = status
    for register, days in sorted(per_student.items()):
        pct = 100 * sum(value == "P" for value in days.values()) / len(days)
        longest = run = 0
        previous = None
        for day in sorted(days):
            run = run + 1 if previous and day == previous + timedelta(days=1) and days[day] == days[previous] == "A" else (1 if days[day] == "A" else 0)
            longest = max(longest, run)
            previous = day
        print(f"{register}: attendance={pct:.2f}% absent_3_consecutive={longest >= 3}")

if __name__ == "__main__":
    main()
