#!/usr/bin/env python3
import sys

def flush_word(word: str, total: int, year_counts: list[tuple[int, int]]):
    # Expected format:
    # Word: holmes (Total: 887)
    # 1887: 156
    sys.stdout.write(f"Word: {word} (Total: {total})\n")
    for y, c in year_counts:
        sys.stdout.write(f"{y}: {c}\n")

def main():
    current_word = None
    current_year = None
    current_count = 0

    # Accumulators per word (years are few; safe)
    word_total = 0
    years_list: list[tuple[int, int]] = []

    def commit_year(y: int, c: int):
        nonlocal word_total, years_list
        word_total += c
        years_list.append((y, c))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        w, y_s, c_s = parts
        try:
            y = int(y_s)
            c = int(c_s)
        except ValueError:
            continue

        if current_word is None:
            current_word, current_year, current_count = w, y, c
            continue

        if w == current_word and y == current_year:
            current_count += c
        else:
            # commit previous (word,year)
            commit_year(current_year, current_count)

            # word changed: flush whole block
            if w != current_word:
                years_list.sort(key=lambda t: t[0])  # year ascending
                flush_word(current_word, word_total, years_list)
                # reset word accumulators
                word_total = 0
                years_list = []

            current_word, current_year, current_count = w, y, c

    # finalize last
    if current_word is not None and current_year is not None:
        commit_year(current_year, current_count)
        years_list.sort(key=lambda t: t[0])
        flush_word(current_word, word_total, years_list)

if __name__ == "__main__":
    main()
