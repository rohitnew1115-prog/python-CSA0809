"""Create a short event count summary."""
from pathlib import Path


def write_summary(output: Path, registrations):
    counts = {}
    for registration in registrations:
        for event in registration["events"]:
            counts[event] = counts.get(event, 0) + 1
    lines = [f"{event}: {count}" for event, count in sorted(counts.items())]
    (output / "summary_report.txt").write_text("\n".join(lines) + ("\n" if lines else "No registrations\n"), encoding="utf-8")
