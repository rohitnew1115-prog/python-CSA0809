"""Task 2: aggregate biometric attendance files for a month."""
from pathlib import Path
import csv

def process_month(input_dir: Path, output_dir: Path, roster: list[str], threshold: float=75.0):
    counts={student:[0,0] for student in roster}; errors=[]; files=sorted(input_dir.glob("*.csv"))
    for path in files:
        try:
            with path.open(encoding="utf-8", newline="") as source:
                for line, row in enumerate(csv.reader(source),1):
                    if not row: continue
                    try:
                        if len(row)!=3: raise ValueError(f"expected 3 fields, found {len(row)}")
                        reg, day, status=(v.strip() for v in row)
                        if reg not in counts: raise ValueError(f"unknown register {reg}")
                        from datetime import date
                        date.fromisoformat(day)
                        if status not in {"P","A"}: raise ValueError(f"invalid status {status!r}")
                        counts[reg][1]+=1
                        if status=="P": counts[reg][0]+=1
                    except ValueError as exc: errors.append(f"{path.name}:{line}: {exc}")
        except OSError as exc: errors.append(f"{path.name}: {exc}")
    output_dir.mkdir(parents=True,exist_ok=True)
    days=len(files)
    with (output_dir/"attendance_percentages.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["register_number","present","scheduled_days","percentage"]);
        for reg,(present,total) in counts.items(): w.writerow([reg,present,days,f"{present/days*100:.2f}" if days else "0.00"])
    with (output_dir/"below_75_percent.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["register_number","percentage"]);
        for reg,(present,total) in counts.items():
            percent=present/days*100 if days else 0
            if percent<threshold: w.writerow([reg,f"{percent:.2f}"])
    (output_dir/"damaged_lines.log").write_text("\n".join(errors)+("\n" if errors else ""),encoding="utf-8")
    return counts,errors,days

if __name__=="__main__":
    here=Path(__file__).parent
    counts,errors,days=process_month(here/"data",here/"output",["1925260050","1925260051","1925260052"])
    print(f"Processed {days} day(s), {sum(v[1] for v in counts.values())} records, {len(errors)} damaged row(s)")
