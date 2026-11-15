"""Q7: Evidence-based iterative redesign of Q6 staircase counter."""
from functools import lru_cache
import time
@lru_cache(maxsize=None)
def ways_memo(n): return 1 if n<=1 else ways_memo(n-1)+ways_memo(n-2)
def ways_iterative_counted(n):
    if n<0: raise ValueError("n must be non-negative")
    if n<=1: return 1,0
    a,b=1,2; iterations=0
    for _ in range(3,n+1): a,b=b,a+b; iterations+=1
    return b,iterations
def main():
    print("Diagnosis: plain recursion repeats subproblems exponentially; memo reduces repeated work but depth still grows with n.")
    print("Objective: same answers through n=1000, no recursion-limit changes, O(1) algorithmic auxiliary space.")
    print("Prediction: n=1000 requires 998 loop updates; memo recursion may fail at interpreter depth limit.")
    print(" n | same result | memo time(s) | loop time(s) | iterations | memo status")
    for n in (10,20,25,30,100,1000):
        ways_memo.cache_clear(); mr=None; mt=None; status="completed"
        try:
            t=time.perf_counter(); mr=ways_memo(n); mt=time.perf_counter()-t
        except RecursionError: status="RecursionError"
        t=time.perf_counter(); ir,iters=ways_iterative_counted(n); it=time.perf_counter()-t
        same=(mr==ir) if mr is not None else "not comparable"
        print(f"{n:4} | {str(same):12} | {mt if mt is not None else '-':>12} | {it:12.9f} | {iters:10} | {status}")
        if mr is not None: assert mr==ir
        assert iters==max(n-2,0)
    print("Evaluation: exact equality for completed comparisons; n=1000 loop succeeds in 998 updates. Q7 objective achieved.")
    print("Trade-off: iterative form is less directly recursive but removes O(n) cache and call stack; both recurrence counts are O(n).")
if __name__ == '__main__': main()
