"""Generate 12 stations x 90 days of reproducible synthetic hourly readings."""
import csv, math, random
from datetime import date, timedelta
from pathlib import Path

STATIONS = ["Adyar", "Guindy", "Tambaram", "Velachery", "T Nagar", "Anna Nagar", "Perungudi", "Royapuram", "Manali", "Kodungaiyur", "Nungambakkam", "Thiruvottiyur"]
FIELDS = ["station","date","hour","pm25","pm10","no2","co","temperature_c"]

def generate(path, stations=STATIONS, start=date(2026,1,1), days=90, seed=1925260050):
    rng=random.Random(seed); path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for sidx,station in enumerate(stations):
            for day in range(days):
                d=start+timedelta(days=day)
                seasonal=8*math.sin(day/18)+4*math.cos(day/7)
                for hour in range(24):
                    rush=18 if hour in (8,9,18,19) else 0
                    pm=max(3, 28+sidx*.22+seasonal+rush+rng.gauss(0,7))
                    temp=27+5*math.sin((hour-6)*math.pi/12)+3*math.sin(day/30)+rng.gauss(0,1.4)
                    w.writerow({"station":station,"date":d.isoformat(),"hour":hour,"pm25":round(pm,2),"pm10":round(pm*1.65+rng.random()*8,2),"no2":round(max(1,pm*.42+rng.gauss(0,5)),2),"co":round(max(.05,pm*.009+rng.random()*.2),3),"temperature_c":round(temp,2)})
    return path

if __name__ == "__main__":
    target=Path(__file__).parent/"data"/"synthetic_air_quality.csv"
    generate(target); print(f"Wrote synthetic data to {target}")
