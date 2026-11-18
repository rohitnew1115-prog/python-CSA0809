"""Small-data daily means, database loading and query helpers."""
from __future__ import annotations
import csv, sqlite3
from collections import defaultdict
from pathlib import Path
import pandas as pd

def loop_daily_means(path):
    totals, counts = defaultdict(float), defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("pm25") in (None, ""):
                continue
            key = (row["station"], row["date"])
            totals[key] += float(row["pm25"]); counts[key] += 1
    return {k: round(totals[k] / counts[k], 6) for k in sorted(totals)}

def pandas_daily_means(path):
    frame = pd.read_csv(path)
    result = frame.groupby(["station", "date"], as_index=False)["pm25"].mean()
    return {(r.station, r.date): round(float(r.pm25), 6) for r in result.itertuples()}

def sqlite_daily_means(path):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings(station TEXT, date TEXT, pm25 REAL)")
    with open(path, newline="", encoding="utf-8") as f:
        rows = [(r["station"], r["date"], float(r["pm25"])) for r in csv.DictReader(f) if r.get("pm25")]
    con.executemany("INSERT INTO readings VALUES(?,?,?)", rows)
    result = {(a, b): round(c, 6) for a, b, c in con.execute("SELECT station,date,AVG(pm25) FROM readings GROUP BY station,date ORDER BY station,date")}
    con.close()
    return result

def load_database(csv_path, db_path):
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys=ON")
    schema = Path(__file__).parents[1] / "Task01_Data_Acquisition" / "schema.sql"
    con.executescript(schema.read_text(encoding="utf-8"))
    con.executescript("""
    CREATE TABLE IF NOT EXISTS complaints(complaint_id INTEGER PRIMARY KEY, station_id INTEGER REFERENCES stations(station_id), received_at TEXT NOT NULL, text TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS sentiment_results(complaint_id INTEGER PRIMARY KEY REFERENCES complaints(complaint_id), score INTEGER NOT NULL, label TEXT NOT NULL CHECK(label IN ('positive','negative','neutral')));
    CREATE TABLE IF NOT EXISTS daily_summaries(station_id INTEGER REFERENCES stations(station_id), day TEXT NOT NULL, mean_pm25 REAL, valid_readings INTEGER NOT NULL, PRIMARY KEY(station_id,day));
    """)
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    stations = sorted({r["station"] for r in rows})
    con.executemany("INSERT OR IGNORE INTO stations(station_name,area) VALUES(?,?)", [(s, s + " area") for s in stations])
    idmap = dict(con.execute("SELECT station_name,station_id FROM stations"))
    con.executemany("INSERT OR IGNORE INTO readings(station_id,observed_at,pm25,pm10,no2,co,temperature_c,source_file) VALUES(?,?,?,?,?,?,?,?)",
        [(idmap[r["station"]], r["date"]+"T"+r["hour"].zfill(2)+":00:00", float(r["pm25"]),float(r["pm10"]),float(r["no2"]),float(r["co"]),float(r["temperature_c"]),"synthetic") for r in rows])
    con.commit(); return con
