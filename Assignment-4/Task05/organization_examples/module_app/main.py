"""Entry point importing one user-defined module."""
from pathlib import Path
from reader import read, report
def main():
    rows=read(Path(__file__).parents[2]/"version_d_package"/"attendance"/"data")
    print("\n".join(report(rows)))
if __name__=="__main__": main()
