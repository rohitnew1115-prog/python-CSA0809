from pathlib import Path
from .reader import read_attendance
from .stats import summarize
from .reports import write_reports
def main():
    base=Path(__file__).parent; rows,errors=read_attendance(base/"data"); percentages,streaks=summarize(rows); write_reports(base/"output",percentages,streaks)
    (base/"output/errors.log").write_text("\n".join(errors)+("\n" if errors else ""),encoding="utf-8")
    print(f"Read {len(rows)} records; errors {len(errors)}; three-day absences {len(streaks)}")
if __name__=="__main__": main()
