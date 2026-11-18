"""Database schema setup, parameterized station query and measured index demo."""
from pathlib import Path
import sqlite3, time, statistics
import csv
from Task05_AI_Applications.sentiment import score,label

def create_db(path):
    con=sqlite3.connect(path); con.execute("PRAGMA foreign_keys=ON")
    schema=Path(__file__).parents[1]/"Task01_Data_Acquisition"/"schema.sql"
    con.executescript(schema.read_text(encoding="utf-8"))
    con.executescript("""
    CREATE TABLE IF NOT EXISTS complaints(complaint_id INTEGER PRIMARY KEY, station_id INTEGER REFERENCES stations(station_id), received_at TEXT NOT NULL, text TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS sentiment_results(complaint_id INTEGER PRIMARY KEY REFERENCES complaints(complaint_id), score INTEGER NOT NULL, label TEXT NOT NULL CHECK(label IN ('positive','negative','neutral')));
    CREATE TABLE IF NOT EXISTS daily_summaries(station_id INTEGER REFERENCES stations(station_id), day TEXT NOT NULL, mean_pm25 REAL, valid_readings INTEGER NOT NULL, PRIMARY KEY(station_id,day));
    """)
    return con

def station_average(con,name):
    return con.execute("SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id) WHERE s.station_name=?",(name,)).fetchone()[0]

def populate_supporting_tables(con, complaint_csv):
    con.execute("DELETE FROM sentiment_results"); con.execute("DELETE FROM complaints"); con.execute("DELETE FROM daily_summaries")
    with open(complaint_csv,newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f):
            con.execute("INSERT INTO complaints(complaint_id,received_at,text) VALUES(?,?,?)",(int(row["complaint_id"]),"2026-10-01T12:00:00",row["text"]))
            con.execute("INSERT INTO sentiment_results(complaint_id,score,label) VALUES(?,?,?)",(int(row["complaint_id"]),score(row["text"]),label(row["text"])))
    con.execute("""INSERT INTO daily_summaries(station_id,day,mean_pm25,valid_readings)
      SELECT station_id,substr(observed_at,1,10),AVG(pm25),COUNT(pm25) FROM readings
      GROUP BY station_id,substr(observed_at,1,10)""")
    con.commit()

def index_experiment(con,repeats=30):
    query="SELECT AVG(pm25) FROM readings WHERE station_id=? AND observed_at>=? AND observed_at<?"
    params=(1,"2026-01-01","2026-02-01")
    def timing():
        values=[]
        for _ in range(repeats):
            t=time.perf_counter(); con.execute(query,params).fetchone(); values.append(time.perf_counter()-t)
        return statistics.median(values)
    con.execute("DROP INDEX IF EXISTS idx_readings_station_time"); con.commit(); before=timing()
    con.execute("CREATE INDEX idx_readings_station_time ON readings(station_id,observed_at)"); con.commit(); after=timing()
    return before,after
