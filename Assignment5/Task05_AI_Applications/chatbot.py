"""Keyword rule chatbot that retrieves station readings from SQLite."""
import sqlite3
STATIONS=("Adyar","Guindy","Tambaram","Velachery","T Nagar","Anna Nagar","Perungudi","Royapuram","Manali","Kodungaiyur","Nungambakkam","Thiruvottiyur")
def answer(question, connection):
    q=question.casefold(); station=next((s for s in STATIONS if s.casefold() in q),None)
    if not station: return "Please name a monitoring station."
    metric="pm25" if "pm2.5" in q or "pm25" in q else "pm10" if "pm10" in q else None
    if not metric: return "Please ask for PM2.5 or PM10."
    row=connection.execute(f"SELECT r.{metric}, r.observed_at FROM readings r JOIN stations s USING(station_id) WHERE s.station_name=? ORDER BY r.observed_at DESC LIMIT 1",(station,)).fetchone()
    if not row: return f"No {metric.upper()} reading is available for {station}."
    return f"Latest {metric.upper()} at {station}: {row[0]:.1f} ug/m3 ({row[1]})."
