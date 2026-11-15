"""Attendance percentages and three-day absence analysis."""
from collections import defaultdict
from datetime import date, timedelta


def summarize(rows):
    by_student = defaultdict(dict)
    for register, day_text, status in rows:
        by_student[register][date.fromisoformat(day_text)] = status
    percentages, streaks = {}, []
    for register, days in by_student.items():
        percentages[register] = 100 * sum(status == "P" for status in days.values()) / len(days)
        run = longest = 0
        previous = None
        for day in sorted(days):
            run = run + 1 if previous and day == previous + timedelta(days=1) and days[day] == days[previous] == "A" else (1 if days[day] == "A" else 0)
            longest = max(longest, run)
            previous = day
        if longest >= 3:
            streaks.append(register)
    return percentages, sorted(streaks)
