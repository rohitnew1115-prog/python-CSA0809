"""Reusable validation and cleaning for synthetic station CSV exports."""
from __future__ import annotations
import csv
import logging
from datetime import datetime
from pathlib import Path

LOG = logging.getLogger(__name__)
REQUIRED = {"station", "date", "hour", "pm25", "pm10", "no2", "co", "temperature", "temperature_unit"}
LIMITS = {"pm25": (0, 999), "pm10": (0, 999), "no2": (0, 1000), "co": (0, 100), "temperature": (-80, 70)}

def parse_date(value: str) -> str:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"unsupported date format: {value!r}")

def _number(raw: str | None, field: str) -> float | None:
    if raw is None or raw.strip().upper() in {"", "NA", "N/A", "NULL"}:
        return None
    value = float(raw)
    lo, hi = LIMITS[field]
    if not lo <= value <= hi:
        raise ValueError(f"{field} outside accepted range {lo}..{hi}")
    return value

def clean_rows(rows):
    """Return normalized dict rows and a list of (row number, reason)."""
    good, rejected, seen = [], [], set()
    for line, row in enumerate(rows, start=2):
        try:
            station = (row.get("station") or "").strip()
            if not station:
                raise ValueError("missing station")
            date = parse_date(row.get("date") or "")
            hour = int(row.get("hour", ""))
            if hour not in range(24):
                raise ValueError("hour outside 0..23")
            key = (station.casefold(), date, hour)
            if key in seen:
                raise ValueError("duplicate station timestamp")
            clean = {"station": station, "date": date, "hour": hour}
            invalid_pm25 = False
            for field in ("pm25", "pm10", "no2", "co"):
                try:
                    clean[field] = _number(row.get(field), field)
                except (ValueError, TypeError, OverflowError) as exc:
                    clean[field] = None
                    rejected.append((line, f"invalid {field}: {exc}"))
                    if field == "pm25": invalid_pm25 = True
            raw_temp = row.get("temperature")
            unit = (row.get("temperature_unit") or "C").strip().upper()
            temp = None
            if raw_temp is not None and raw_temp.strip().upper() not in {"", "NA", "N/A", "NULL"}:
                try:
                    parsed_temp = float(raw_temp)
                    if unit == "F": parsed_temp = (parsed_temp - 32) * 5 / 9
                    elif unit != "C": parsed_temp = float("nan")
                    if -80 <= parsed_temp <= 70: temp = parsed_temp
                    else: rejected.append((line, f"temperature outside accepted range: {parsed_temp}"))
                except (ValueError, TypeError, OverflowError) as exc:
                    rejected.append((line, f"invalid temperature: {exc}"))
            clean["temperature_c"] = round(temp, 3) if temp is not None else None
            if invalid_pm25:
                continue
            if clean["pm25"] is None:
                raise ValueError("missing or invalid PM2.5")
            seen.add(key)
            good.append(clean)
        except (ValueError, TypeError, OverflowError) as exc:
            rejected.append((line, str(exc)))
            LOG.warning("Rejected row %d: %s", line, exc)
    return good, rejected

def load_clean_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError("input CSV is missing or empty")
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
            missing = sorted(REQUIRED - set(reader.fieldnames or []))
            raise ValueError(f"missing required columns: {missing}")
        return clean_rows(reader)
