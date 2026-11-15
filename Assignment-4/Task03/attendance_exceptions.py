"""Task 3: strict attendance parsing and explicit exception boundaries."""
from pathlib import Path

class InvalidRecord(ValueError):
    def __init__(self, message: str, source: str, line_number: int):
        super().__init__(f"{source}:{line_number}: {message}")
        self.source=source; self.line_number=line_number

def parse_line(raw: str, source: str, line_number: int):
    fields=raw.rstrip("\r\n").split(".")
    if len(fields)!=3: raise InvalidRecord(f"expected 3 fields, found {len(fields)}",source,line_number)
    reg, day, status=(f.strip() for f in fields)
    if not reg: raise InvalidRecord("empty register number",source,line_number)
    from datetime import date
    try: date.fromisoformat(day)
    except ValueError as exc: raise InvalidRecord(f"invalid date {day!r}",source,line_number) from exc
    if status not in {"P","A"}: raise InvalidRecord(f"invalid status {status!r}",source,line_number)
    return reg,day,status

def process_file(path: Path):
    valid=[]; errors=[]; source=None
    try:
        source=path.open("r",encoding="utf-8")
        for line_number,raw in enumerate(source,1):
            if not raw.strip(): continue
            try: valid.append(parse_line(raw,path.name,line_number))
            except InvalidRecord as exc: errors.append(str(exc))
    except OSError as exc:
        raise RuntimeError(f"cannot read attendance file {path}") from exc
    finally:
        if source is not None: source.close()
    return valid,errors

if __name__=="__main__":
    p=Path(__file__).parent/"data/attendance.txt"
    try:
        rows,errors=process_file(p); print(f"valid={len(rows)} rejected={len(errors)}")
        for error in errors: print(error)
    except RuntimeError as exc: print(exc)
