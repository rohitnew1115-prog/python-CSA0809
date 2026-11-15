from pathlib import Path
import csv
def read_attendance(folder: Path):
    rows=[]; errors=[]
    for path in sorted(folder.glob("*.csv")):
        with path.open(encoding="utf-8",newline="") as f:
            for line,row in enumerate(csv.reader(f),1):
                if not row: continue
                try:
                    if len(row)!=3: raise ValueError("expected register,date,status")
                    reg,day,status=(x.strip() for x in row)
                    from datetime import date; date.fromisoformat(day)
                    if status not in {"P","A"}: raise ValueError("status must be P or A")
                    rows.append((reg,day,status))
                except ValueError as exc: errors.append(f"{path.name}:{line}: {exc}")
    return rows,errors
