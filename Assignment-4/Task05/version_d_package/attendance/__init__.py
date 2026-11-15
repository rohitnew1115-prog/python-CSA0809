"""Attendance processing package."""
from .reader import read_attendance
from .stats import summarize
from .report import write_reports

__all__ = ["read_attendance", "summarize", "write_reports"]
