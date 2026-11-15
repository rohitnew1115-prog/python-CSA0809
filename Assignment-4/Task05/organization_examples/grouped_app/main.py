"""Main importing three task modules."""
from pathlib import Path
from reader import read
from stats import summarize
from report import summary
def main():
    rows=read(Path(__file__).parents[2]/"version_d_package"/"attendance"/"data")
    percentages,streaks=summarize(rows)
    print(summary(percentages,streaks))
if __name__=="__main__": main()
