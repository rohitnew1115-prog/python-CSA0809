"""Task 5 organization 1: one self-contained script."""
from pathlib import Path
import csv
def main():
    total=0; present=0
    for path in (Path(__file__).parents[1]/"attendance_package/data").glob("*.csv"):
        with path.open(encoding="utf-8",newline="") as stream:
            for row in csv.reader(stream):
                if len(row)==3 and row[2] in {"P","A"}: total+=1; present += row[2]=="P"
    print(f"valid={total} attendance={present/total*100:.2f}%" if total else "No records")
if __name__=="__main__": main()
