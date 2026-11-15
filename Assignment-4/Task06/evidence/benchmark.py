"""Small local comparison of list scans and set membership for duplicates."""
import time

COUNT = 5_000
keys = [f"R{index:05d}" for index in range(COUNT)]

start = time.perf_counter()
seen_list = []
for key in keys:
    if key not in seen_list:
        seen_list.append(key)
list_seconds = time.perf_counter() - start

start = time.perf_counter()
seen_set = set()
for key in keys:
    if key not in seen_set:
        seen_set.add(key)
set_seconds = time.perf_counter() - start

print(f"Registrations: {COUNT}")
print(f"List membership: {list_seconds:.4f} seconds; retained={len(seen_list)}")
print(f"Set membership:  {set_seconds:.4f} seconds; retained={len(seen_set)}")
