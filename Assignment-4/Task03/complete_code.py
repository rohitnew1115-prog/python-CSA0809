"""TODO-completed version of the supplied Complete the Code program."""
import os
import tempfile


class InvalidRecord(Exception):
    """Raised when a line is not a valid three-field P/A record."""


def parse_line(line):
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {parts[2]!r}")
    return tuple(parts)


def summarise(path):
    present, absent, errors = 0, 0, []
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
    return present, absent, errors


def main():
    data = "192311001,2026-10-08,P\n192311002,2026-10-08,A\n" \
           "192311003,2026-10-08\n192311004,2026-10-08,L\n"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write(data)
            temporary_path = tmp.name
        print(summarise(temporary_path))
    finally:
        if temporary_path is not None:
            os.remove(temporary_path)
    try:
        summarise("this_file_does_not_exist.csv")
    except FileNotFoundError as exc:
        output = os.path.join(os.path.dirname(__file__), "output", "missing_file.log")
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w", encoding="utf-8") as log:
            log.write(f"Handled missing input: {exc}\n")


if __name__ == "__main__":
    main()
