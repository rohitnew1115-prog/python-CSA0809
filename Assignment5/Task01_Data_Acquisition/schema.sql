PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL UNIQUE,
    area TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
);
CREATE TABLE IF NOT EXISTS readings (
    reading_id INTEGER PRIMARY KEY,
    station_id INTEGER NOT NULL REFERENCES stations(station_id),
    observed_at TEXT NOT NULL,
    pm25 REAL CHECK (pm25 IS NULL OR pm25 BETWEEN 0 AND 999),
    pm10 REAL CHECK (pm10 IS NULL OR pm10 BETWEEN 0 AND 999),
    no2 REAL CHECK (no2 IS NULL OR no2 BETWEEN 0 AND 1000),
    co REAL CHECK (co IS NULL OR co BETWEEN 0 AND 100),
    temperature_c REAL CHECK (temperature_c IS NULL OR temperature_c BETWEEN -80 AND 70),
    source_file TEXT NOT NULL DEFAULT 'synthetic',
    UNIQUE (station_id, observed_at)
);
CREATE INDEX IF NOT EXISTS idx_readings_station_time ON readings(station_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_readings_time ON readings(observed_at);
