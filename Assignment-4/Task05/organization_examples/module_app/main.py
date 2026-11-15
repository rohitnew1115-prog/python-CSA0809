"""Entry point importing one user-defined module."""
from pathlib import Path
from reader import read
def main(): print(f"Valid records: {len(read(Path(__file__).parents[2]/'attendance_package/data'))}")
if __name__=="__main__": main()
