"""Main importing three task modules."""
from pathlib import Path
from reader import read
from statistics import present_percent
from report import summary
def main():
    rows=read(Path(__file__).parents[2]/"attendance_package/data"); print(summary(rows,present_percent(rows)))
if __name__=="__main__": main()
