# Task 1 Data acquisition design

Station files use a header row and one row per station-hour: `station,date,hour,pm25,pm10,no2,co,temperature,temperature_unit`. The station identifier and timestamp form the natural record key. Accepted date formats are ISO `YYYY-MM-DD` and `DD/MM/YYYY`; hours are integers 0 through 23.

The sample data in `../Task02_Cleaning_Normalisation/sample_data.csv` includes valid and intentionally invalid synthetic examples: a blank field, `NA`, a negative PM2.5 value, an impossible PM2.5 value, a duplicate timestamp, a Fahrenheit temperature, a malformed date, a nonnumeric PM10 value, and a missing-column case in the adversarial fixtures. None represents a real measurement.

CSV is portable and good for exchange or append-only archives. It has no constraints or query indexes, so repeated analytical questions scan all n rows (O(n)); loading a DataFrame uses memory proportional to the full dataset. SQLite uses a normalized station table and readings table; foreign keys prevent orphan readings, and `(station_id, observed_at)` prevents duplicate station-hours. Indexed filters are roughly O(log n + k), with k matching rows, and aggregations scan the selected rows. CSV is simpler for transfer; SQLite is preferable for repeat queries and integrity.

CSV-to-database mapping: station name is resolved to `stations.station_id`; date and hour become ISO `observed_at`; PM2.5, PM10, NO2, CO and normalized Celsius map directly to readings columns; source filename is retained for provenance.

## Example SQL

```sql
-- Station average during October
SELECT AVG(r.pm25) FROM readings r JOIN stations s USING (station_id)
WHERE s.station_name = ? AND r.observed_at >= ? AND r.observed_at < ?;
-- Compare station means
SELECT s.station_name, AVG(r.pm25) FROM readings r JOIN stations s USING (station_id)
GROUP BY s.station_name ORDER BY AVG(r.pm25) DESC;
-- Worst air-quality day (highest daily mean)
SELECT substr(observed_at,1,10) AS day, AVG(pm25) AS mean_pm25
FROM readings WHERE pm25 IS NOT NULL GROUP BY day ORDER BY mean_pm25 DESC LIMIT 1;
```

An index changes lookup work from a full scan toward logarithmic key navigation plus result processing, but adds disk space and slows inserts slightly. SQLite is embedded, transactional, portable and suitable for this coursework and a small deployment; a service database is appropriate when multiple concurrent writers, replication or operational availability become requirements.
