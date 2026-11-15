"""UTF-8, line-numbered department CSV reader."""
import csv
from pathlib import Path


def read_department(path: Path):
    """Return (records, errors), retaining line numbers and file-level faults."""
    records, errors = [], []
    try:
        with path.open("r", encoding="utf-8", newline="") as source:
            for line_number, row in enumerate(csv.reader(source), 1):
                if row:
                    records.append((line_number, row))
    except FileNotFoundError:
        errors.append(f"{path.name}: missing department file")
    except PermissionError as exc:
        errors.append(f"{path.name}: permission denied: {exc}")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.name}: invalid UTF-8: {exc}")
    except csv.Error as exc:
        errors.append(f"{path.name}: invalid CSV: {exc}")
    except OSError as exc:
        errors.append(f"{path.name}: file error: {exc}")
    return records, errors
