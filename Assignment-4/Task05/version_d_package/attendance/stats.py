from collections import defaultdict
def summarize(rows):
    stats=defaultdict(lambda:[0,0]); daily=defaultdict(dict)
    for reg,day,status in rows:
        stats[reg][1]+=1; stats[reg][0]+=status=="P"; daily[reg][day]=status
    percentages={r:(p/t*100 if t else 0) for r,(p,t) in stats.items()}
    streaks=[]
    from datetime import date,timedelta
    for reg,days in daily.items():
        ordered=sorted(date.fromisoformat(d) for d in days); longest=run=0; previous=None
        for day in ordered:
            run=run+1 if previous and day==previous+timedelta(days=1) and days[previous.isoformat()] == "A" and days[day.isoformat()] == "A" else (1 if days[day.isoformat()] == "A" else 0)
            longest=max(longest,run); previous=day
        if longest>=3: streaks.append(reg)
    return percentages,streaks
