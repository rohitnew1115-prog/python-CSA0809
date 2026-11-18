"""Assignment starter-shaped PM2.5 cleaning function plus safe scaling."""
import csv, logging
from pathlib import Path
LOG=logging.getLogger(__name__)
RAW="""station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""
def load_clean_text(text=RAW):
    records=[]
    for row in csv.DictReader(text.splitlines()):
        value=(row.get("pm25") or "").strip()
        try:
            if not value or value.upper()=="NA": continue
            number=float(value)
            if number<0 or number>999: continue
        except (ValueError,TypeError):
            continue
        records.append((row["station"],row["date"],number))
    return records
def load_clean_file(path):
    text=Path(path).read_text(encoding="utf-8-sig")
    return load_clean_text(text)
def min_max(values):
    vals=list(values)
    if not vals: return []
    low,high=min(vals),max(vals)
    return [0.0 for _ in vals] if low==high else [round((v-low)/(high-low),3) for v in vals]
if __name__=="__main__":
    print("Cleaned records:",load_clean_text())
    print("Normalised values:",min_max([48,95,121]))
    assert load_clean_text("station,date,pm25\nRohit,2026-10-01,1000\nRohit,2026-10-02,3\n")==[("Rohit","2026-10-02",3.0)]
    print("Above-999 test: passed")
