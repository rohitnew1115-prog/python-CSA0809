"""Task 5 organization 2: reusable reader module."""
from pathlib import Path
import csv
def read(folder):
    rows=[]
    for path in Path(folder).glob("*.csv"):
        with path.open(encoding="utf-8",newline="") as source: rows.extend(row for row in csv.reader(source) if len(row)==3 and row[2] in {"P","A"})
    return rows
