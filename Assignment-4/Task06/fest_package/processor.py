from pathlib import Path
import csv,re
REQUIRED=5
def valid_email(value): return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",value))
def collect(folder: Path):
    accepted=[]; errors=[]; seen=set()
    for path in sorted(folder.glob("*.csv")):
        try:
            with path.open(encoding="utf-8",newline="") as source:
                for number,row in enumerate(csv.reader(source),1):
                    if not row: continue
                    try:
                        if len(row)!=REQUIRED: raise ValueError(f"expected {REQUIRED} fields, found {len(row)}")
                        reg,name,dept,email,event=(x.strip() for x in row)
                        if not all((reg,name,dept,email,event)): raise ValueError("empty required field")
                        if not valid_email(email): raise ValueError(f"invalid email {email!r}")
                        if reg in seen: raise ValueError(f"duplicate registration {reg}")
                        seen.add(reg); accepted.append({"register_number":reg,"name":name,"department":dept,"email":email,"event":event})
                    except ValueError as exc: errors.append(f"{path.name}:{number}: {exc}")
        except OSError as exc: errors.append(f"{path.name}: {exc}")
    return accepted,errors
