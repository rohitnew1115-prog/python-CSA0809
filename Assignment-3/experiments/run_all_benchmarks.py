"""Reproducible benchmark suite for Assignment 3; CSVs contain measured values."""
from pathlib import Path
import csv, random, statistics, time, timeit, tracemalloc, sys, re
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'experiments'; OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'Q01_Lists_and_Slicing')); from q01_rainfall import moving_naive,moving_running
sys.path.insert(0,str(ROOT/'Q03_Dictionaries_Complaint_Analysis')); from q03_complaints import frequent
sys.path.insert(0,str(ROOT/'Q05_List_Comprehension_Sensor_Readings')); from q05_sensor_readings import loop_valid,comp_valid,functional_valid
def measure(fn, repeats=3):
    vals=[]
    for _ in range(repeats):
        start=time.perf_counter(); fn(); vals.append(time.perf_counter()-start)
    return statistics.mean(vals)
def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def main():
    rng=random.Random(1925260050); rows=[]; memory_rows=[]; rain_rows=[]
    for n in (365,36500,365000):
        x=[rng.random()*35 for _ in range(n)]
        naive=measure(lambda:moving_naive(x),2 if n>100000 else 3); running=measure(lambda:moving_running(x))
        rain_rows.append({'n':n,'naive_seconds':naive,'running_seconds':running,'naive_additions':7*max(0,n-6),'running_additions':7+max(0,n-7) if n>=7 else 0,'running_subtractions':max(0,n-7)})
    write_csv(ROOT/'Q01_Lists_and_Slicing'/'benchmark_results.csv',rain_rows)
    for n in (1000,10000,100000):
        vocab=('seed','price','complaint','subsidy','water','crop','delayed','received')
        texts=[' '.join(vocab[(i+j)%len(vocab)] for j in range(4)) for i in range(n)]; words=[w for t in texts for w in t.split()]; distinct=set(words)
        # This keeps the documented O(n*d) baseline measurable at 100,000 records.
        list_time=measure(lambda:[words.count(w) for w in distinct])
        def dict_word_count():
            counts={}
            for word in words: counts[word]=counts.get(word,0)+1
            return counts
        dict_time=measure(dict_word_count)
        from collections import Counter
        counter_time=measure(lambda:Counter(words))
        rows.append({'experiment':'complaints','n':n,'method':'dict','seconds':dict_time})
        rows.append({'experiment':'complaints','n':n,'method':'list_count','seconds':list_time})
        rows.append({'experiment':'complaints','n':n,'method':'Counter','seconds':counter_time})
    for n in (10000,100000,1000000):
        vals=[rng.uniform(-8,10) for _ in range(n)]
        for name,fn in [('loop',loop_valid),('comprehension',comp_valid),('filter',functional_valid)]:
            rows.append({'experiment':'sensor','n':n,'method':name,'seconds':measure(lambda:fn(vals))})
        outputs=[loop_valid(vals),comp_valid(vals),functional_valid(vals)]
        assert outputs[0]==outputs[1]==outputs[2]
        tracemalloc.start(); comp_valid(vals); _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
        memory_rows.append({'experiment':'sensor_output','n':n,'method':'comprehension_peak','bytes':peak})
    write_csv(OUT/'benchmark_results.csv',rows)
    write_csv(OUT/'memory_results.csv',memory_rows)
    # membership workloads
    reg=[]
    for n in (10000,100000,1000000):
        values=[str(i) for i in range(n)]; s=set(values); probes=[str(i) for i in (0,n//7,n//3,n//2,2*n//3, n-1)]
        for method,container in [('list',values),('set',s)]:
            reg.append({'n':n,'method':method,'seconds':measure(lambda:[q in container for q in probes],1)})
    write_csv(OUT/'membership_results.csv',reg)
    # tuple/list measurements
    vals=list(range(1_000_000)); tuple_rows=[{'type':'list','shallow_bytes':sys.getsizeof(vals)},{'type':'tuple','shallow_bytes':sys.getsizeof(tuple(vals))}]
    write_csv(OUT/'tuple_list_memory.csv',tuple_rows)
    # small reproducible benchmark of timetable indexed vs scan
    railway=ROOT/'Q06_Nested_Data_Railway_Timetable'/'q06_railway.py'
    # generic synthetic schedule queries
    sched=[{'stops':[('S'+str(j%100),'06:00','06:05') for j in range(10)],'days':{'Mon'}} for _ in range(10000)]
    index={}
    for i,t in enumerate(sched):
        for st,a,d in t['stops']: index.setdefault(st,[]).append(i)
    q=lambda:[i for i,t in enumerate(sched) if any(s=='S50' for s,a,d in t['stops']) and 'Mon' in t['days']]
    indexed=lambda:index.get('S50',[])
    write_csv(OUT/'timetable_index_results.csv',[{'n':len(sched),'method':'scan','seconds':measure(q),'index_bytes_shallow':0},{'n':len(sched),'method':'index','seconds':measure(indexed),'index_bytes_shallow':sys.getsizeof(index)}])
    rain=rain_rows
    sensor=[r for r in rows if r['experiment']=='sensor']
    complaints=[r for r in rows if r['experiment']=='complaints']
    membership=reg
    lines=['# Experimental investigation summary','','Environment: Python 3.12.5; fixed seed 1925260050. Times are averages from repeated `time.perf_counter()` measurements and can vary by machine. The CSV files are the raw measured values.','','## Moving averages','']
    for r in rain: lines.append(f"- n={r['n']}: naive {r['naive_seconds']:.6f}s; running sum {r['running_seconds']:.6f}s; additions {r['naive_additions']} vs {r['running_additions']} (plus {r['running_subtractions']} subtractions).")
    lines+=['','## Complaint counting','','The three methods consume the same pre-tokenized list with eight distinct words. The list-count method is a deliberately small-vocabulary O(n*d) baseline.']
    for n in (1000,10000,100000):
        vals=[r for r in complaints if int(r['n'])==n]; lines.append(f"- n={n}: "+'; '.join(f"{r['method']} {float(r['seconds']):.6f}s" for r in vals)+'.')
    lines+=['','## Sensor cleaning','']
    for n in (10000,100000,1000000):
        vals=[r for r in sensor if int(r['n'])==n]; lines.append(f"- n={n}: "+'; '.join(f"{r['method']} {float(r['seconds']):.6f}s" for r in vals)+'.')
    lines+=['','## Membership and index trade-off','','See `membership_results.csv`, `timetable_index_results.csv`, and `memory_results.csv` for measured membership times, station query times, and tracemalloc peak bytes. `tuple_list_memory.csv` reports shallow container sizes only; the one million integer objects are not included in either size.']
    (OUT/'experiment_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Benchmark CSVs written under',OUT)
if __name__=='__main__': main()
