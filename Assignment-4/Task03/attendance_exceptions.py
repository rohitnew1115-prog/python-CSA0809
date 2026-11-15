"""Task 3: custom record errors and the supplied Complete the Code exercise."""
from pathlib import Path
import tempfile
from datetime import date


class InvalidRecord(Exception):
    """Raised when an attendance record is not three fields with P/A status."""


def parse_line(line):
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    try:
        date.fromisoformat(parts[1])
    except ValueError as exc:
        raise InvalidRecord(f"invalid date {parts[1]!r}") from exc
    if parts[2] not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {parts[2]!r}")
    return tuple(parts)


def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, 1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"attendance file not found: {path}") from exc
    except PermissionError as exc:
        raise PermissionError(f"permission denied: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"attendance file is not UTF-8: {path}") from exc
    return present, absent, errors


def run_supplied_example():
    data = (
        "192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n192311004,2026-10-08,L\n"
    )
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write(data)
        print(summarise(tmp.name))
    finally:
        if tmp is not None:
            Path(tmp.name).unlink(missing_ok=True)


if __name__ == "__main__":
    run_supplied_example()
    try:
        summarise(Path(__file__).parent / "data" / "does_not_exist.csv")
    except FileNotFoundError as exc:
        (Path(__file__).parent / "output" / "missing_file.log").parent.mkdir(parents=True, exist_ok=True)
        (Path(__file__).parent / "output" / "missing_file.log").write_text(str(exc) + "\n", encoding="utf-8")
