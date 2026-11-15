"""Task 4: append each day's returned books and preserve forensic errors."""
from pathlib import Path
import csv

def append_returns(input_path: Path, log_path: Path, error_path: Path):
    errors=[]; written=0
    try:
        log_path.parent.mkdir(parents=True,exist_ok=True)
        with input_path.open("r",encoding="utf-8",newline="") as source:
            with log_path.open("a",encoding="utf-8",newline="") as log:
                writer=csv.writer(log)
                for line_number,row in enumerate(csv.reader(source),1):
                    if not row: continue
                    if len(row)!=2:
                        errors.append(f"{input_path.name}:{line_number}: expected 2 fields, found {len(row)}"); continue
                    writer.writerow([value.strip() for value in row]); written+=1
    except UnicodeDecodeError as exc: errors.append(f"{input_path.name}: encoding error: {exc}")
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
    log.parent.mkdir(parents=True,exist_ok=True); log.write_text("",encoding="utf-8")
    errors.parent.mkdir(parents=True,exist_ok=True); errors.write_text("",encoding="utf-8")
    results=run_days([here/"data/day1.csv",here/"data/day2.csv",here/"data/day3.csv"],log,errors)
    missing=append_returns(here/"data/missing.csv",log,errors)
    print(f"Processed 3 daily files; appended {sum(n for n,_ in results)} returns; logged {sum(len(e) for _,e in results)+len(missing[1])} error(s)")
