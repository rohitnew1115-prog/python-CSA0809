"""Create simple, labeled benchmark plots using Pillow (no hard-coded measurements)."""
from pathlib import Path
import csv
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'experiments'/'graphs'; OUT.mkdir(exist_ok=True)
def plot(path,title,series,xlabel,ylabel,log=False):
    w,h=900,520; im=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(im); left,top,right,bottom=90,70,850,430
    d.text((left,25),title,fill='black'); d.line((left,top,left,bottom),fill='black',width=2); d.line((left,bottom,right,bottom),fill='black',width=2)
    allvals=[v for _,vals in series for v in vals]; maxv=max(allvals) if allvals else 1
    if log: maxv=max(1,maxv)
    colors=['#1769aa','#d1495b','#2a9d8f','#f4a261','#6a4c93']
    count=max((len(vals) for _,vals in series),default=1)
    for si,(name,vals) in enumerate(series):
        pts=[]
        for i,v in enumerate(vals):
            x=(left+(right-left)*(si/max(1,len(series)-1))) if count==1 else left+(right-left)*(i/max(1,count-1)); y=bottom-(bottom-top)*(v/maxv); pts.append((int(x),int(y)))
        if len(pts)>1: d.line(pts,fill=colors[si%len(colors)],width=4)
        for x,y in pts: d.ellipse((x-5,y-5,x+5,y+5),fill=colors[si%len(colors)])
        d.text((left+si*145,455),name,fill=colors[si%len(colors)])
    d.text((left,bottom+25),xlabel,fill='black'); d.text((5,top),ylabel,fill='black'); im.save(path)
def read(file): return list(csv.DictReader((ROOT/'experiments'/file).open(encoding='utf-8')))
rain=list(csv.DictReader((ROOT/'Q01_Lists_and_Slicing'/'benchmark_results.csv').open(encoding='utf-8')))
plot(OUT/'q1_moving_average.png','Q1 Moving Average Runtime',[('naive',[float(r['naive_seconds']) for r in rain]),('running',[float(r['running_seconds']) for r in rain])],'Dataset sizes 365, 36,500, 365,000','Seconds')
rows=[r for r in read('benchmark_results.csv') if r['experiment']=='sensor']; sizes=[10000,100000,1000000]
plot(OUT/'q5_sensor_runtime.png','Q5 Sensor Cleaning Runtime',[(m,[float(next(r['seconds'] for r in rows if int(r['n'])==n and r['method']==m)) for n in sizes]) for m in ('loop','comprehension','filter')],'Readings 10k, 100k, 1m','Seconds')
rows=read('membership_results.csv'); plot(OUT/'q4_membership.png','Q4 Membership Check Runtime',[(m,[float(next(r['seconds'] for r in rows if int(r['n'])==n and r['method']==m)) for n in sizes]) for m in ('list','set')],'Registrations 10k, 100k, 1m','Seconds')
rows=read('timetable_index_results.csv'); plot(OUT/'q6_station_query.png','Q6 Timetable Station Query',[('scan',[float(rows[0]['seconds'])]),('indexed',[float(rows[1]['seconds'])])],'10,000 trains','Seconds')
rows=read('memory_results.csv'); ns=[10000,100000,1000000]
plot(OUT/'q5_sensor_memory.png','Q5 Sensor Comprehension Peak Memory',[('peak bytes',[float(next(r['bytes'] for r in rows if int(r['n'])==n)) for n in ns])],'Readings 10k, 100k, 1m','Bytes')
mem=read('tuple_list_memory.csv'); plot(OUT/'q2_list_tuple_memory.png','Q2 Shallow Container Memory at One Million Values',[(r['type'],[float(r['shallow_bytes'])]) for r in mem],'List versus tuple','Bytes')
