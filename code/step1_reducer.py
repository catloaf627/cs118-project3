#!/usr/bin/env python3
import sys

def main():
    current_word = None
    current_count = 0
    totals = []  # list[(word, count)]

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        word, cnt_s = parts
        try:
            cnt = int(cnt_s)
        except ValueError:
            continue

        if current_word is None:
            current_word = word
            current_count = cnt
        elif word == current_word:
            current_count += cnt
        else:
            totals.append((current_word, current_count))
            current_word = word
            current_count = cnt

    if current_word is not None:
        totals.append((current_word, current_count))

    # Sort by frequency desc; tie-break by word ascending for determinism
    totals.sort(key=lambda x: (-x[1], x[0]))

    # Handout expected format for results: "word count" separated by spaces
    for w, c in totals:
        sys.stdout.write(f"{w} {c}\n")

if __name__ == "__main__":
    main()
