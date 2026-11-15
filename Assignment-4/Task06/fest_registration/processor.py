"""Orchestrate department reading, validation and duplicate rejection."""
from pathlib import Path
from .duplicate_checker import accept_once
from .reader import read_department
from .validator import InvalidRegistration, validate_row


DEFAULT_DEPARTMENTS = ("CSE", "ECE", "EEE", "MECH", "CIVIL")


def collect(folder: Path, departments=DEFAULT_DEPARTMENTS):
    accepted, errors, seen = [], [], set()
    for department in departments:
        path = Path(folder) / f"department_{department.casefold()}.csv"
        records, file_errors = read_department(path)
        errors.extend(file_errors)
        for line_number, raw in records:
            try:
                record = validate_row(raw)
                if record["department"].casefold() != department.casefold():
                    raise InvalidRegistration(f"department must be {department}")
                if not accept_once(record["register_number"], seen):
                    raise InvalidRegistration(f"duplicate registration {record['register_number']}")
                accepted.append(record)
            except InvalidRegistration as exc:
                errors.append(f"{path.name}:{line_number}: {exc}")
    return accepted, errors
