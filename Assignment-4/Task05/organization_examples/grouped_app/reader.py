"""Grouped-module form: input reader."""
from pathlib import Path
import csv
def read(folder):
    rows=[]
    for path in Path(folder).glob("*.csv"):
        with path.open(encoding="utf-8",newline="") as f: rows.extend(row for row in csv.reader(f) if len(row)==3 and row[2] in {"P","A"})
    return rows
