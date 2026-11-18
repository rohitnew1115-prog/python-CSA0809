"""Run small demonstrations and save actual console evidence as text."""
from pathlib import Path
from contextlib import redirect_stdout
import csv, io, sqlite3, tempfile, time
from Task02_Cleaning_Normalisation.cleaning import load_clean_csv
from Task03_Analysis_Visualisation.analysis import loop_daily_means,pandas_daily_means,sqlite_daily_means
from Task03_Analysis_Visualisation.visualisation import make_charts
from Task05_AI_Applications.sentiment import label,improved_label
from Task05_AI_Applications.summariser import summarize
from Task05_AI_Applications.chatbot import answer
from Task06_Cleaning_Pipeline.cleaning_pipeline import load_clean_text,min_max
from Task07_Adversarial_Data.adversarial_tests import run_cases
from Task09_Final_Engineering_Decision.final_system import create_db,station_average

ROOT=Path(__file__).parent
def main():
    out=ROOT/"outputs"/"reports"; out.mkdir(parents=True,exist_ok=True)
    sink=io.StringIO()
    with redirect_stdout(sink):
        sample=ROOT/"Task02_Cleaning_Normalisation"/"sample_data.csv"
        good,rejected=load_clean_csv(sample)
        clean_dir=ROOT/"outputs"/"cleaned_data"; clean_dir.mkdir(parents=True,exist_ok=True)
        with (clean_dir/"cleaned_sample.csv").open("w",newline="",encoding="utf-8") as f:
            fields=["station","date","hour","pm25","pm10","no2","co","temperature_c"]
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(good)
        print("Original CSV:")
        print(sample.read_text(encoding="utf-8"))
        print("Cleaned CSV rows:",good)
        print("Cleaned sample rows:",len(good)); print("Rejected rows and reasons:",rejected)
        print("Starter cleaned records:",load_clean_text()); print("Starter min-max:",min_max([48,95,121]))
        print("Cleaning >999 regression:",load_clean_text("station,date,pm25\nRohit,2026-10-01,1000\nRohit,2026-10-02,3\n"))
        for case,result in run_cases().items(): print("Adversarial",case+":",result)
        with tempfile.TemporaryDirectory() as td:
            con=create_db(Path(td)/"injection.db")
            con.executemany("INSERT INTO stations(station_name,area) VALUES(?,?)",[("Adyar","South"),("Guindy","West")])
            ids=dict(con.execute("SELECT station_name,station_id FROM stations"))
            rows=[("Adyar","2026-10-01",48.),("Guindy","2026-10-01",95.),("Guindy","2026-10-03",121.),("Adyar","2026-10-04",60.)]
            con.executemany("INSERT INTO readings(station_id,observed_at,pm25) VALUES(?,?,?)",[(ids[s],d,v) for s,d,v in rows]); con.commit()
            print("Station averages Adyar/Guindy:",station_average(con,"Adyar"),station_average(con,"Guindy"))
            october=con.execute("SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id) WHERE s.station_name=? AND r.observed_at>=? AND r.observed_at<?",("Adyar","2026-10-01","2026-11-01")).fetchone()[0]
            compare=list(con.execute("SELECT s.station_name,AVG(r.pm25) FROM readings r JOIN stations s USING(station_id) GROUP BY s.station_name ORDER BY s.station_name"))
            worst=con.execute("SELECT substr(observed_at,1,10),AVG(pm25) FROM readings GROUP BY substr(observed_at,1,10) ORDER BY AVG(pm25) DESC LIMIT 1").fetchone()
            print("October Adyar average:",october); print("Sample station comparison:",compare); print("Worst sampled day and mean:",worst)
            print("SQL injection result:",station_average(con,"Adyar' OR '1'='1")); con.close()
        bench=ROOT/"Task03_Analysis_Visualisation"/"data"/"synthetic_air_quality.csv"
        outputs=(loop_daily_means(bench),pandas_daily_means(bench),sqlite_daily_means(bench))
        print("Three-method daily means identical:",outputs[0]==outputs[1]==outputs[2],"groups:",len(outputs[0]))
        complaints=list(csv.DictReader((ROOT/"Task05_AI_Applications"/"complaints.csv").open(encoding="utf-8",newline="")))
        for fn,name in ((label,"baseline"),(improved_label,"improved")):
            agree=sum(fn(r["text"])==r["manual_label"] for r in complaints)
            print(f"{name.title()} manual-review agreement: {agree}/{len(complaints)} ({agree/len(complaints):.1%})")
        text=" ".join(r["text"] for r in complaints)
        start=time.perf_counter(); extracted=summarize(text,max_sentences=3); elapsed=time.perf_counter()-start
        first=text.partition(".")[0].strip()+"."
        print("Extractive summary (3 sentences):",extracted)
        print("First-sentence baseline:",first); print(f"Extractive runtime seconds: {elapsed:.8f}")
        db=sqlite3.connect(ROOT/"database"/"air_quality.db")
        print("Chatbot example:",answer("What is the PM2.5 in Adyar today?",db))
        print("Database row counts:",[(table,db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in ("stations","readings","complaints","sentiment_results","daily_summaries")])
        print("Database sample readings:",db.execute("SELECT s.station_name,r.observed_at,r.pm25 FROM readings r JOIN stations s USING(station_id) ORDER BY r.observed_at LIMIT 3").fetchall())
        index_rows=list(csv.DictReader((ROOT/"outputs"/"reports"/"index_timing.csv").open(encoding="utf-8")))
        print("Index timing evidence:",index_rows)
        bench_rows=list(csv.DictReader((ROOT/"Task08_Loops_vs_Libraries_SQL"/"benchmark_results"/"benchmark_results.csv").open(encoding="utf-8")))
        print("Benchmark result rows:",bench_rows)
        print("Monthly mean query on synthetic sample:",db.execute("SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id) WHERE s.station_name=? AND r.observed_at>=? AND r.observed_at<?",("Adyar","2026-01-01","2026-02-01")).fetchone()[0])
        db.close()
        print("Generated charts:",sorted(p.name for p in (ROOT/"outputs"/"charts").glob("*.png")))
    (out/"execution_evidence.txt").write_text(sink.getvalue(),encoding="utf-8")
    print(sink.getvalue())
if __name__=="__main__": main()
