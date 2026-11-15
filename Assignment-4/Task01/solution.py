"""Task 1: diagnose and repair the hotel bill file processor."""
from pathlib import Path
import csv
import os
import tempfile

def diagnose():
    return ["Hard-coded machine path", "File handle is never closed", "Whole file loaded into memory", "Text iteration is not record iteration", "Unvalidated field count and amount conversion", "Bare except hides defects", "Repeated string concatenation", "Blank and rejected rows are not audited"]

def process_bills(input_path: Path, output_path: Path):
    total = 0.0
    accepted = []
    rejected = []
    try:
        with input_path.open("r", encoding="utf-8", newline="") as source:
            for line_no, raw in enumerate(source, 1):
                if not raw.strip():
                    continue
                try:
                    fields = next(csv.reader([raw]))
                    if line_no == 1 and [v.strip().lower() for v in fields] == ["register", "name", "amount"]:
                        continue
                    if len(fields) != 3:
                        raise ValueError(f"expected 3 fields, found {len(fields)}")
                    register, name, amount_text = (part.strip() for part in fields)
                    amount = float(amount_text)
                    if not register or not name or amount < 0:
                        raise ValueError("empty identity or negative amount")
                    accepted.append((register, name, amount))
                    total += amount
                except (ValueError, csv.Error) as exc:
                    rejected.append(f"line {line_no}: {exc}: {raw.rstrip()}")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"bill input not found: {input_path}") from exc
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = "Register,Name,Amount\n" + "".join(f"{r},{n},{a:.2f}\n" for r,n,a in accepted) + f"Total,,{total:.2f}\n"
    fd, temp_name = tempfile.mkstemp(dir=output_path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as target:
            target.write(text)
        os.replace(temp_name, output_path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return total, accepted, rejected

if __name__ == "__main__":
    folder=Path(__file__).parent
    total, accepted, rejected=process_bills(folder/"data/hotel_bills.csv", folder/"output/bill_report.csv")
    print(f"Accepted {len(accepted)} bills; total ${total:.2f}; rejected {len(rejected)}")
    for error in rejected: print(error)

