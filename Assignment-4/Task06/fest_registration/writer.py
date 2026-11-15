"""Write the clean master file, event lists, summary and error log."""
import csv
from pathlib import Path
from .event_writer import write_event_files
from .report import write_summary

FIELDS = ["register_number", "name", "department", "email", "events"]


def write_outputs(output: Path, registrations, errors):
    output.mkdir(parents=True, exist_ok=True)
    rows = sorted(registrations, key=lambda row: row["register_number"])
    with (output / "clean_master_list.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "events": ";".join(row["events"])})
    # Keep the earlier filename available for users who already used it.
    with (output / "master_registrations.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "events": ";".join(row["events"])})
    write_event_files(output, rows)
    write_summary(output, rows)
    (output / "summary.txt").write_text((output / "summary_report.txt").read_text(encoding="utf-8"), encoding="utf-8")
    (output / "error_log.txt").write_text("\n".join(errors) + ("\n" if errors else "No errors\n"), encoding="utf-8")
    (output / "errors.log").write_text("\n".join(errors) + ("\n" if errors else ""), encoding="utf-8")
