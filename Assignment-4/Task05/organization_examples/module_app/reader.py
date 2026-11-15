"""Reusable attendance reader and report logic for Version B."""
from pathlib import Path
import csv
from datetime import date, timedelta
def read(folder):
    rows=[]
    for path in sorted(Path(folder).glob("*.csv")):
        with path.open(encoding="utf-8",newline="") as source: rows.extend(row for row in csv.reader(source) if len(row)==3 and row[2] in {"P","A"})
    return rows

def report(rows):
    grouped={}
    for reg,day_text,status in rows: grouped.setdefault(reg,{})[date.fromisoformat(day_text)]=status
    lines=[]
    for reg,days in sorted(grouped.items()):
        pct=100*sum(status=="P" for status in days.values())/len(days); run=longest=0; previous=None
        for day in sorted(days):
            run=run+1 if previous and day==previous+timedelta(days=1) and days[day]==days[previous]=="A" else (1 if days[day]=="A" else 0)
            longest=max(longest,run); previous=day
        lines.append(f"{reg}: attendance={pct:.2f}% absent_3_consecutive={longest>=3}")
    return lines
