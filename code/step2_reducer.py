# step2_reducer.py
#!/usr/bin/env python3
import sys
from collections import defaultdict

years_seen = set()


# Load top words in the correct order
top_words = []
with open("results/step1_topwords.txt") as f:
    for line in f:
        w, _ = line.strip().split("\t")
        top_words.append(w)

# Aggregation structures
counts = defaultdict(int)   # per (word,year)
totals = defaultdict(int)   # per word

# Parse mapped data
for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 3:
        continue
    word, year, cnt = parts
    cnt = int(cnt)
    year = int(year)

    counts[(word, year)] += cnt
    totals[word] += cnt
    years_seen.add(year)


# Output results in top_words order
for word in top_words:
    if word not in totals:
        continue
    print(f"Word: {word} (Total: {totals[word]})")
    # sort years numeric ascending
    # for (w, y), cnt in sorted(counts.items()):
    #     if w == word:
    #         print(f"{y}: {cnt}")
    for y in sorted(years_seen):
        cnt = counts.get((word, y), 0)
        print(f"{y}: {cnt}")

    print()

