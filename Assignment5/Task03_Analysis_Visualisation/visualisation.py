"""Create four labeled plots from the deterministic synthetic dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def make_charts(csv_path, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["month"] = df.date.dt.to_period("M").astype(str)
    daily = df.groupby(["station", "date"], as_index=False).pm25.mean()
    monthly = df.groupby("month").pm25.mean()
    fig, ax = plt.subplots(figsize=(8,4.5)); monthly.plot(ax=ax, marker="o", color="#145a7a")
    ax.set(title="Monthly mean PM2.5 trend (synthetic)", xlabel="Month", ylabel="Mean PM2.5 (µg/m³)"); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/"monthly_pm25_trend.png", dpi=150); plt.close(fig)
    stations = df.groupby("station").pm25.mean().sort_values()
    fig, ax = plt.subplots(figsize=(8,5)); stations.plot.barh(ax=ax, color="#3c879a")
    ax.set(title="Station comparison", xlabel="Mean PM2.5 (µg/m³)", ylabel="Monitoring station"); ax.grid(axis="x",alpha=.25); fig.tight_layout(); fig.savefig(out/"station_comparison.png",dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4.5)); ax.scatter(df.temperature_c,df.pm25,s=7,alpha=.35,color="#bc5a35",label="Hourly reading")
    ax.set(title="Temperature and PM2.5 relationship",xlabel="Temperature (°C)",ylabel="PM2.5 (µg/m³)"); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/"temperature_vs_pm25.png",dpi=150); plt.close(fig)
    worst = df.nlargest(12,"pm25").sort_values("pm25")
    fig, ax = plt.subplots(figsize=(8,5)); ax.barh(worst.station+" "+worst.date.dt.strftime("%m-%d")+" "+worst.hour.astype(str)+":00",worst.pm25,color="#9c3d3d")
    ax.set(title="Worst air-quality hours",xlabel="PM2.5 (µg/m³)",ylabel="Station, date and hour"); ax.grid(axis="x",alpha=.25); fig.tight_layout(); fig.savefig(out/"worst_air_quality_hours.png",dpi=150); plt.close(fig)
    return ["monthly_pm25_trend.png","station_comparison.png","temperature_vs_pm25.png","worst_air_quality_hours.png"]
