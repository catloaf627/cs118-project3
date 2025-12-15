# step1_reducer.py
# #!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    word, count = parts
    counts[word] += int(count)

# ✅ REQUIRED: count DESC, word ASC
# sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))


for word, count in sorted_counts:
    print(f"{word}\t{count}")
