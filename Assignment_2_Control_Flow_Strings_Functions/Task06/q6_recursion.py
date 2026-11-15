"""Q6: Temple staircase recursive and memoised solutions with measured calls."""
from functools import lru_cache
import sys, time
naive_calls=0; memo_calls=0
def ways_naive(n):
    global naive_calls
    naive_calls += 1
    if n <= 1: return 1
    return ways_naive(n-1)+ways_naive(n-2)
@lru_cache(maxsize=None)
def ways_memo(n):
    global memo_calls
    memo_calls += 1
    if n <= 1: return 1
    return ways_memo(n-1)+ways_memo(n-2)
def ways_iterative(n):
    if n < 0: raise ValueError("n must be non-negative")
    if n <= 1: return 1
    a,b=1,2
    for _ in range(3,n+1): a,b=b,a+b
    return b
def main():
    global naive_calls, memo_calls
    print("n -> ways for 1..6")
    for n in range(1,7): assert ways_memo(n)==ways_iterative(n); print(n,ways_memo(n))
    print("n=5 call tree: W5 -> W4,W3; W4 -> W3,W2; each W3 -> W2,W1 (repeated W3 and W2).")
    for n in (10,20,25,30):
        naive_calls=0; start=time.perf_counter(); answer=ways_naive(n); elapsed=time.perf_counter()-start; calls=naive_calls
        memo_calls=0; ways_memo.cache_clear(); mstart=time.perf_counter(); cached=ways_memo(n); melapsed=time.perf_counter()-mstart
        assert answer==cached==ways_iterative(n)
        print(f"n={n} ways={answer} naive_calls={calls} memo_misses={memo_calls} naive_s={elapsed:.6f} memo_s={melapsed:.6f}")
    assert ways_naive(25)==121393 and naive_calls>0
    # The exact n=25 count is recorded independently, without changing the verified answer.
    naive_calls=0; assert ways_naive(25)==121393; print("Expected check n=25: ways=121393, plain calls=",naive_calls); assert naive_calls==242785
    print("Python recursion limit:",sys.getrecursionlimit())
    try:
        ways_memo.cache_clear(); memo_calls=0; value=ways_memo(1000); print("memo n=1000 completed",len(str(value)),"digits")
    except RecursionError as e: print("memo n=1000 RecursionError:",e)
    result=ways_iterative(1000); print("iterative n=1000 digits:",len(str(result)))
    print("Naive O(2^n) time/O(n) stack; memo O(n) time and O(n) cache+stack; iterative O(n) time/O(1) auxiliary space.")
    print("Deployment recommendation: iterative for n up to 1000; memoization helps moderate n but recursion depth remains.")
if __name__ == '__main__': main()


