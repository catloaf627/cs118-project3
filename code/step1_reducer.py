#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    word, count = parts
    counts[word] += int(count)

# Sort by count descending
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

for word, count in sorted_counts:
    print(f"{word}\t{count}")
