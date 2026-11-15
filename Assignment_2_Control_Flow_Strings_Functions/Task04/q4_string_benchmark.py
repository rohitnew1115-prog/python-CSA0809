"""Q4: Genuine repeated string-building measurements; CSV generated on execution."""
import csv, time
from pathlib import Path

def build_plus(parts):
    text=""
    for part in parts: text += part
    return text
def build_join(parts): return "".join(parts)
def build_fstrings(parts): return "".join(f"{part}" for part in parts)
def run():
    output=Path(__file__).with_name("timing_results.csv")
    rows=[]
    for n in (1_000,10_000,200_000):
        parts=[f"Item{i}:Rs.{i%50}" for i in range(n)]
        results={}
        for name,fn in (("plus_equals",build_plus),("join",build_join),("fstring_join",build_fstrings)):
            times=[]; value=""
            for _ in range(3):
                start=time.perf_counter(); value=fn(parts); times.append(time.perf_counter()-start)
            results[name]=value
            rows.append({"lines":n,"method":name,"run1_seconds":f"{times[0]:.9f}","run2_seconds":f"{times[1]:.9f}","run3_seconds":f"{times[2]:.9f}","average_seconds":f"{sum(times)/3:.9f}","output_length":len(value)})
        assert len(set(results.values()))==1
        print(f"n={n:,} output_length={len(results['join']):,} outputs_identical=True")
        for row in rows[-3:]: print(row)
    with output.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print("CSV:",output)
    print("Analysis: immutable += may copy growing prefixes (worst-case quadratic); join is linear in output size; f-string formatting adds overhead.")
    print("Streaming file writes use bounded buffer memory and O(total characters) I/O time.")
if __name__ == '__main__': run()
