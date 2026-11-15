"""Rainfall list and slicing study."""
from random import Random
from time import perf_counter

def moving_naive(values, window=7):
    return [sum(values[i:i+window]) / window for i in range(len(values)-window+1)]

def moving_running(values, window=7):
    if len(values) < window: return []
    total = sum(values[:window]); out = [total/window]
    for i in range(window, len(values)):
        total += values[i] - values[i-window]; out.append(total/window)
    return out

def main():
    rng=Random(1925260050); readings=[0.0 if rng.random()<0.08 else round(rng.uniform(0,35),1) for _ in range(365)]
    weekly=[sum(readings[i:i+7]) for i in range(0,len(readings),7)]
    wet=max(enumerate(weekly,1),key=lambda p:p[1]); dry=min(enumerate(weekly,1),key=lambda p:p[1])
    print('days:',len(readings),'weeks:',len(weekly)); print('wettest week:',wet,'driest week:',dry)
    print('first 7-day averages:',moving_running(readings)[:5]); print('dry days:',[i+1 for i,x in enumerate(readings) if x==0])
    print('empty/fewer than 7:',moving_running([]),moving_running([1,2,3]))
    print('slices:',readings[7:14],readings[-7:-1],readings[::7])
    print('pseudocode: initialize sum of first 7; emit mean; for each next reading add incoming and subtract outgoing; emit mean.')
    print('complexity: naive additions = 7*(n-6); running-sum additions = 7+(n-7), plus subtractions; both O(n) output space, running total O(1) extra.')
    print('late insertion: list.insert(i,x) is O(n) due to shifting; useful for a small year, costly for frequent arbitrary inserts.')
    print('date-key dict: O(7) average per window lookup, O(n) storage; sparse/missing dates require explicit policy; list has compact contiguous day access.')
if __name__=='__main__': main()
