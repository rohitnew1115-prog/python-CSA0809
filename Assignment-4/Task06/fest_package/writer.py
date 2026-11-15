from pathlib import Path
import csv,os,tempfile
def _atomic_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True); fd,name=tempfile.mkstemp(dir=path.parent,text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)
def write_outputs(output: Path, rows, errors):
    fields=["register_number","name","department","email","event"]
    sorted_rows=sorted(rows,key=lambda r:(r["event"].casefold(),r["register_number"]))
    _atomic_csv(output/"master_registrations.csv",sorted_rows,fields)
    for event in sorted({r["event"] for r in rows}): _atomic_csv(output/f"event_{event.lower().replace(' ','_')}.csv",[r for r in sorted_rows if r["event"]==event],fields)
    counts={}
    for row in rows: counts[row["event"]]=counts.get(row["event"],0)+1
    (output/"summary.txt").write_text("\n".join(f"{k}: {v}" for k,v in sorted(counts.items()))+"\n",encoding="utf-8")
    (output/"errors.log").write_text("\n".join(errors)+("\n" if errors else ""),encoding="utf-8")
