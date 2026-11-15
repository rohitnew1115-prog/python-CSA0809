"""Task 4: append each day's returned books and preserve forensic errors."""
from pathlib import Path
import csv

def append_returns(input_path: Path, log_path: Path, error_path: Path):
    errors=[]; written=0
    try:
        with input_path.open(encoding="utf-8",newline="") as source:
            rows=list(csv.reader(source))
        with log_path.open("a",encoding="utf-8",newline="") as log:
            for row in rows:
                if not row: continue
                if len(row)!=2:
                    errors.append(f"{input_path.name}: malformed row {row!r}"); continue
                log.write(",".join(v.strip() for v in row)+"\n"); written+=1
    except OSError as exc: errors.append(f"{input_path.name}: {exc}")
    error_path.parent.mkdir(parents=True,exist_ok=True)
    if errors:
        with error_path.open("a",encoding="utf-8") as f:
            for error in errors: f.write(error+"\n")
    return written,errors

def run_days(paths, log_path: Path, error_path: Path):
    return [append_returns(Path(p),log_path,error_path) for p in paths]

if __name__=="__main__":
    here=Path(__file__).parent; log=here/"output/returns.log"; errors=here/"output/errors.log"
    results=run_days([here/"data/day1.csv",here/"data/day2.csv",here/"data/missing.csv"],log,errors)
    print(f"Processed {len(results)} daily files; appended {sum(n for n,_ in results)} returns; errors {sum(len(e) for _,e in results)}")
