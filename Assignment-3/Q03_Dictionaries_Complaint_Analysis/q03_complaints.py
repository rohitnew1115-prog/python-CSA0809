"""Farmer help-line complaint analysis."""
import re
STOP={'not','high'}
calls=['seeds not received seeds delayed','fertiliser price high','seeds price high subsidy not received']
def frequent(texts,stop):
    counts={}
    for text in texts:
        for word in re.findall(r"[a-zA-Z]+",text.lower()):
            if word not in stop: counts[word]=counts.get(word,0)+1
    return counts
def topcounts(k): return sorted(frequent(calls,STOP).items(),key=lambda p:(-p[1],p[0]))[:k]
def main():
    print(topcounts(3)); print('tie rule: alphabetical order places price before received.')
    district_calls=[('Salem','seeds delayed'),('Erode','water shortage'),('Salem','fertiliser')]; by_district={}
    for district,text in district_calls: by_district.setdefault(district,[]).append(text)
    print('district groups:',by_district,'counts:',{k:len(v) for k,v in by_district.items()})
    crop_calls={'rice':['seed complaint'],'cotton':['pest complaint']}; print('crop groups:',crop_calls)
    print('edge tests:',frequent([],STOP),frequent(['SEEDS, seeds!!!'],STOP))
    print('dict expected O(n) average counting, O(d) space; repeated list.count per distinct word O(n*d). Hash lookup is average O(1), subject to collisions. Insertion order is guaranteed since Python 3.7; keys(), values(), items() are dynamic views.')
    print('deployment: dict counting for 100,000 daily complaints; Counter is concise and optimized; choose benchmarked version and normalize text consistently.')
if __name__=='__main__': main()
