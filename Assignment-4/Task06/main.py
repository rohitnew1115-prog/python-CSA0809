from pathlib import Path
from fest_package.processor import collect
from fest_package.writer import write_outputs
def main():
    base=Path(__file__).parent; rows,errors=collect(base/"data"); write_outputs(base/"output",rows,errors)
    print(f"Accepted {len(rows)} registrations; rejected {len(errors)} rows")
if __name__=="__main__": main()
