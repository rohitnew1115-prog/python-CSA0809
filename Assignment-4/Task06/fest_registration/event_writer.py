"""Write one CSV participant list for each event."""
import csv
from pathlib import Path


def write_event_files(output: Path, registrations):
    events = {}
    for row in registrations:
        for event in row["events"]:
            events.setdefault(event, []).append(row)
    output.mkdir(parents=True, exist_ok=True)
    for event, rows in sorted(events.items()):
        safe_name = "_".join(event.casefold().split())
        with (output / f"event_{safe_name}.csv").open("w", encoding="utf-8", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(["register_number", "name", "department", "email", "event"])
            for row in rows:
                writer.writerow([row[key] for key in ("register_number", "name", "department", "email")] + [event])
