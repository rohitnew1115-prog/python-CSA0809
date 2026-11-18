"""Reproducible median timing study for loops, pandas and SQLite GROUP BY."""
from __future__ import annotations
import csv, sqlite3, time, timeit, cProfile, pstats, io, statistics, sys, re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Task03_Analysis_Visualisation.generate_data import generate
from Task03_Analysis_Visualisation.analysis import loop_daily_means, pandas_daily_means
import pandas as pd
import matplotlib.pyplot as plt

def sql_daily_means(path):
    con=sqlite3.connect(":memory:"); con.execute("CREATE TABLE readings(station TEXT,date TEXT,pm25 REAL)")
    with open(path,newline="",encoding="utf-8") as f:
        con.executemany("INSERT INTO readings VALUES(?,?,?)",((r["station"],r["date"],float(r["pm25"])) for r in csv.DictReader(f)))
    return {(a,b):round(c,6) for a,b,c in con.execute("SELECT station,date,AVG(pm25) FROM readings GROUP BY station,date ORDER BY station,date")}

def measured(func,path,repeats=3):
    times=[]; result=None
    for _ in range(repeats):
        t=time.perf_counter(); result=func(path); times.append(time.perf_counter()-t)
    shallow=sys.getsizeof(result)+sum(sys.getsizeof(k)+sys.getsizeof(v) for k,v in result.items())
    return statistics.median(times),shallow,result

def run(outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True); rows=[]
    for count in (1,12,100):
        path=out/f"synthetic_{count}_stations.csv"
        generate(path,stations=[f"Station {i:03d}" for i in range(count)],days=365)
        with open(path,"rb") as f: size=len(f.read())
        loop_t,loop_mem,loop=measured(loop_daily_means,path)
        pandas_t,pandas_mem,pandas_result=measured(pandas_daily_means,path)
        sql_t,sql_mem,sql_result=measured(sql_daily_means,path)
        assert loop==pandas_result==sql_result
        pandas_frame_bytes=int(pd.read_csv(path).memory_usage(index=True,deep=True).sum())
        for method,seconds,memory in (("CSV loops",loop_t,loop_mem),("Pandas groupby",pandas_t,pandas_frame_bytes),("SQLite GROUP BY",sql_t,sql_mem)):
            rows.append({"stations":count,"rows":count*8760,"csv_bytes":size,"method":method,"median_seconds":round(seconds,6),"approx_measured_state_bytes":memory,"memory_measurement":"aggregation output object; Pandas uses full DataFrame deep size","repeats":3,"correctness":"identical"})
    csv_path=out/"benchmark_results.csv"
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    fig,ax=plt.subplots(figsize=(8,4.8))
    for method in ("CSV loops","Pandas groupby","SQLite GROUP BY"):
        selected=[r for r in rows if r["method"]==method]
        ax.plot([r["rows"] for r in selected],[r["median_seconds"] for r in selected],marker="o",label=method)
    ax.set(title="Daily mean benchmark by data size",xlabel="Hourly input rows",ylabel="Median elapsed time (seconds)")
    ax.set_xscale("log"); ax.grid(alpha=.25); ax.legend(); fig.tight_layout()
    fig.savefig(out.parents[1]/"outputs"/"charts"/"benchmark_comparison.png",dpi=150); plt.close(fig)
    # Isolated timeit repeat and cProfile evidence on the 1-station input.
    path=out/"synthetic_1_stations.csv"
    timer=timeit.repeat(lambda:loop_daily_means(path),number=1,repeat=5)
    (out/"timeit_results.txt").write_text("loop_daily_means repeat seconds (5 runs): "+", ".join(f"{x:.6f}" for x in timer)+"\n",encoding="utf-8")
    prof=cProfile.Profile(); prof.enable(); loop_daily_means(path); prof.disable()
    prof.dump_stats(out/"loop_profile.prof")
    stream=io.StringIO(); pstats.Stats(prof,stream=stream).sort_stats("cumulative").print_stats(20)
    report=re.sub(r"[A-Za-z]:\\Users\\[^\\]+", "<python-user-dir>", stream.getvalue())
    report=report.replace(str(Path(__file__).resolve().parents[1]), ".")
    (out/"profile_report.txt").write_text(report,encoding="utf-8")
    # Keep the reproducible generator and measurements, not tens of megabytes of disposable input CSVs.
    for count in (1,12,100):
        (out/f"synthetic_{count}_stations.csv").unlink(missing_ok=True)
    return rows

if __name__=="__main__":
    root=Path(__file__).parent/"benchmark_results"; result=run(root)
    for row in result: print(row)
