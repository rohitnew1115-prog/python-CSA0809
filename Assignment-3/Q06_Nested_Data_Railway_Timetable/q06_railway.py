"""Nested timetable and station-day index demonstration."""
from collections import defaultdict
TIMETABLE={
 '12601':{'name':'Chennai Mail','stops':[('Chennai','06:00','06:10'),('Katpadi','08:15','08:20'),('Bengaluru','11:00','11:10')],'days':{'Mon','Tue','Wed','Thu','Fri','Sat'}},
 '12602':{'name':'Coastal Express','stops':[('Chennai','07:00','07:05'),('Katpadi','09:00','09:05'),('Mysuru','13:00','13:10')],'days':{'Mon','Wed','Fri'}},
 '12603':{'name':'Southern Link','stops':[('Coimbatore','05:30','05:35'),('Chennai','10:00','10:10'),('Katpadi','12:00','12:05')],'days':{'Tue','Thu','Sat'}},
 '12604':{'name':'Hill City','stops':[('Chennai','08:00','08:05'),('Salem','11:00','11:05'),('Bengaluru','15:00','15:10')],'days':{'Sun','Tue'}},
 '12605':{'name':'Delta Passenger','stops':[('Thanjavur','04:00','04:05'),('Chennai','12:00','12:05'),('Katpadi','14:00','14:05')],'days':{'Mon','Tue','Wed','Thu','Fri','Sat','Sun'}}}
def query(station,day,data=TIMETABLE):
    found=[]
    for no,t in data.items():
        if day in t['days']:
            for s,a,d in t['stops']:
                if s.casefold()==station.casefold(): found.append((d,no,t['name']))
    return sorted(found,key=lambda x:x[0])
def build_index(data):
    idx=defaultdict(list)
    for no,t in data.items():
        for s,a,d in t['stops']: idx[s.casefold()].append((no,t['name'],d,t['days']))
    return idx
def main():
    print('nested example:',TIMETABLE['12601']); print('third station departure:',TIMETABLE['12601']['stops'][2][2])
    print('Katpadi Monday:',query('Katpadi','Mon')); print('unknown/day-filter/empty:',query('Atlantis','Mon'),query('Mysuru','Tue'),query('Any','Mon',{}))
    for no,t in TIMETABLE.items(): print(no,t['name'],[(s,a,d) for s,a,d in t['stops']],sorted(t['days']))
    idx=build_index(TIMETABLE); print('indexed Katpadi:',[(no,n,d) for no,n,d,days in idx.get('katpadi',[]) if 'Mon' in days])
    print('dictionary train metadata lookup; list preserves route order; tuple is fixed station-time record; set supports running-day membership. Scan O(T*S); station index O(matches) average query after O(total stops) build, uses O(total stops) extra memory.')
    print('flat list scan also O(total stops); index accelerates repeated station lookup at storage/build cost. Missing station/data returns empty result.')
if __name__=='__main__': main()
