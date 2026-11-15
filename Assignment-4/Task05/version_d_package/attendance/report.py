"""Write attendance percentages and consecutive-absence report."""
from pathlib import Path
import csv


def write_reports(output: Path, percentages: dict[str, float], streaks: list[str]):
    output.mkdir(parents=True, exist_ok=True)
    with (output / "attendance_percentages.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["register_number", "percentage"])
        writer.writerows((register, f"{percent:.2f}") for register, percent in sorted(percentages.items()))
    (output / "absent_three_consecutive_days.txt").write_text(
        "\n".join(streaks) + ("\n" if streaks else ""), encoding="utf-8"
    )


__all__ = ["write_reports"]
