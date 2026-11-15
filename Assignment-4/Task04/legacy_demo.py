"""Faithful copy of the defective library example from the assignment PDF."""
from pathlib import Path
import os


def save_returns(books):
    log = open("returns.log", "w", encoding="utf-8")
    for book in books:
        log.write(book)
    log.close()


def process(day_file):
    try:
        books = open(day_file, encoding="utf-8").read().split("\n")
        save_returns(books)
    except FileNotFoundError:
        print("missing")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    evidence = here / "output" / "legacy_demo" / "returns.log"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    original_cwd = Path.cwd()
    try:
        os.chdir(evidence.parent)
        evidence.write_text("", encoding="utf-8")
        for day in (here / "data/day1.csv", here / "data/day2.csv", here / "data/day3.csv"):
            process(day)
        process(here / "data/missing.csv")
        print(evidence.read_text(encoding="utf-8"))
    finally:
        os.chdir(original_cwd)
