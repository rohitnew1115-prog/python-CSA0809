"""Controlled malformed input cases. Each response is captured, never crashes."""
import csv, io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Task02_Cleaning_Normalisation.cleaning import REQUIRED

def inspect_csv(data, encoding="utf-8", delimiter=None):
    try:
        text=data.decode(encoding)
        if not text.strip(): return "ERROR: empty file"
        sample=text[:4096]
        try: dialect=csv.Sniffer().sniff(sample,delimiters=",;\t")
        except csv.Error: return "ERROR: unable to detect CSV delimiter"
        if delimiter is not None: dialect.delimiter=delimiter
        reader=csv.DictReader(io.StringIO(text),dialect=dialect)
        fields=set(reader.fieldnames or [])
        missing=sorted(REQUIRED-fields)
        if missing: return "ERROR: missing required columns: "+", ".join(missing)
        return f"OK: {sum(1 for _ in reader)} data rows"
    except UnicodeError as exc: return f"ERROR: unsupported encoding ({exc.__class__.__name__})"
    except (OSError,csv.Error) as exc: return f"ERROR: cannot read CSV ({exc})"

def run_cases():
    header=b"station,date,hour,pm25,pm10,no2,co,temperature,temperature_unit\nAdyar,2026-10-01,0,48,70,17,.3,25,C\n"
    missing=b"station,date,pm25\nAdyar,2026-10-01,48\n"
    wrong=b"station|date|hour|pm25|pm10|no2|co|temperature|temperature_unit\nAdyar|2026-10-01|0|48|70|17|.3|25|C\n"
    utf16="station,date,hour,pm25,pm10,no2,co,temperature,temperature_unit\nAdyar,2026-10-01,0,48,70,17,.3,25,C\n".encode("utf-16")
    return {"missing column":inspect_csv(missing),"wrong delimiter":inspect_csv(wrong),"different encoding (UTF-16)":inspect_csv(utf16),"empty file":inspect_csv(b"")}
if __name__=="__main__":
    for case,result in run_cases().items(): print(f"{case}: {result}")
    from Task09_Final_Engineering_Decision.final_system import create_db
    import tempfile, os
    path=tempfile.mktemp(suffix=".db"); con=create_db(path)
    print("SQL injection Adyar' OR '1'='1:",con.execute("SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id) WHERE s.station_name=?",("Adyar' OR '1'='1",)).fetchone()[0])
    con.close(); os.unlink(path)
