"""Reproducible memory/time comparison on 50,000 synthetic bill rows."""
from pathlib import Path
import tempfile
import time
import tracemalloc


ROWS = 50_000
RECORD = "1925260050,P ROHIT,1.25\n"


def measure(path, read_all):
    tracemalloc.start()
    start = time.perf_counter()
    with path.open("r", encoding="utf-8") as source:
        if read_all:
            count = sum(1 for line in source.read().splitlines() if line)
        else:
            count = sum(1 for line in source if line.strip())
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return count, elapsed, peak


with tempfile.TemporaryDirectory() as temp:
    sample = Path(temp) / "fifty_thousand.txt"
    with sample.open("w", encoding="utf-8") as target:
        for _ in range(ROWS):
            target.write(RECORD)
    read_all = measure(sample, True)
    streamed = measure(sample, False)
    print(f"Rows: {ROWS}; input bytes: {sample.stat().st_size}")
    print(f"read()+splitlines(): rows={read_all[0]}, seconds={read_all[1]:.4f}, peak_bytes={read_all[2]}")
    print(f"line iteration: rows={streamed[0]}, seconds={streamed[1]:.4f}, peak_bytes={streamed[2]}")
