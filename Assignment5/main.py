"""Run the Assignment 5 reproducible data and evidence pipeline."""
from pathlib import Path
import logging
import sys, csv
from Task03_Analysis_Visualisation.generate_data import generate
from Task03_Analysis_Visualisation.analysis import load_database
from Task03_Analysis_Visualisation.visualisation import make_charts
from Task08_Loops_vs_Libraries_SQL.benchmarking import run as run_benchmarks
from Task09_Final_Engineering_Decision.final_system import index_experiment, populate_supporting_tables

ROOT=Path(__file__).parent
def main(include_benchmarks=True):
    logging.basicConfig(level=logging.WARNING,format="%(levelname)s: %(message)s")
    data=generate(ROOT/"Task03_Analysis_Visualisation"/"data"/"synthetic_air_quality.csv")
    charts=make_charts(data,ROOT/"outputs"/"charts")
    db=ROOT/"database"/"air_quality.db"; db.parent.mkdir(exist_ok=True)
    con=load_database(data,db)
    populate_supporting_tables(con,ROOT/"Task05_AI_Applications"/"complaints.csv")
    before,after=index_experiment(con)
    con.close()
    evidence=ROOT/"outputs"/"reports"; evidence.mkdir(parents=True,exist_ok=True)
    with (evidence/"index_timing.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["query","before_index_seconds","after_index_seconds","repetitions"]); w.writerow(["station and month mean",f"{before:.8f}",f"{after:.8f}",30])
    print(f"Synthetic hourly readings: {12*90*24}")
    print("Charts:",", ".join(charts))
    print(f"Index median query seconds before={before:.8f} after={after:.8f}")
    if include_benchmarks:
        rows=run_benchmarks(ROOT/"Task08_Loops_vs_Libraries_SQL"/"benchmark_results")
        print(f"Benchmark measurements: {len(rows)} rows saved")
if __name__=="__main__": main(include_benchmarks="--skip-benchmarks" not in sys.argv)
