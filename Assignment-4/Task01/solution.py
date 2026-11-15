"""Task 1: diagnose and repair the hotel bill file processor."""
from pathlib import Path
import csv
import os
import tempfile
from decimal import Decimal, InvalidOperation

def diagnose():
    return ["Hard-coded machine path", "File handle is never closed", "Whole file loaded into memory", "Text iteration is not record iteration", "Unvalidated field count and amount conversion", "Bare except hides defects", "Repeated string concatenation", "Blank and rejected rows are not audited"]

def process_bills(input_path: Path, output_path: Path):
    total = Decimal("0.00")
    accepted_count = 0
    rejected = []
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(dir=output_path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(["Register", "Name", "Amount"])
            try:
                with input_path.open("r", encoding="utf-8", newline="") as source:
                    for line_no, raw in enumerate(source, 1):
                        if not raw.strip():
                            rejected.append(f"line {line_no}: empty record")
                            continue
                        try:
                            fields = next(csv.reader([raw]))
                            if line_no == 1 and [v.strip().lower() for v in fields] == ["register", "name", "amount"]:
                                continue
                            if len(fields) != 3:
                                raise ValueError(f"expected 3 fields, found {len(fields)}")
                            register, name, amount_text = (part.strip() for part in fields)
                            amount = Decimal(amount_text)
                            if not amount.is_finite():
                                raise ValueError("amount must be a finite decimal")
                            if not register or not name or amount < 0:
                                raise ValueError("empty identity or negative amount")
                            writer.writerow([register, name, f"{amount:.2f}"])
                            accepted_count += 1
                            total += amount
                        except (ValueError, csv.Error, InvalidOperation) as exc:
                            rejected.append(f"line {line_no}: {exc}: {raw.rstrip()}")
            except FileNotFoundError as exc:
                raise FileNotFoundError(f"bill input not found: {input_path}") from exc
            writer.writerow(["Total", "", f"{total:.2f}"])
        os.replace(temp_name, output_path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return total, accepted_count, rejected

if __name__ == "__main__":
    folder=Path(__file__).parent
    total, accepted_count, rejected=process_bills(folder/"data/sample_mess_oct.txt", folder/"output/bill_report.csv")
    print(f"Accepted {accepted_count} bills; total ${total:.2f}; rejected {len(rejected)}")
    for error in rejected: print(error)

