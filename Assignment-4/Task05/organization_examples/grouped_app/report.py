"""Grouped-module form: output formatter."""
def summary(percentages, streaks):
    attendance = "\n".join(f"{register}: {percent:.2f}%" for register, percent in sorted(percentages.items()))
    absent = ", ".join(streaks) if streaks else "none"
    return f"Attendance percentages:\n{attendance}\nAbsent for three consecutive days: {absent}"
