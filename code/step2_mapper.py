#!/usr/bin/env python3
import sys
import re
import string
import helper_func as hf

# load top words
TOP_WORDS = set()
with open("results/step1_topwords.txt") as f:
    for line in f:
        w, _ = line.strip().split("\t")
        TOP_WORDS.add(w)

KNOWN_DATES = {
    # Sherlock Holmes
    'study in scarlet': 1887,
    'sign of the four': 1890,
    'adventures of sherlock holmes': 1892,
    'memoirs of sherlock holmes': 1894,
    'hound of the baskervilles': 1902,
    'return of sherlock holmes': 1905,
    'valley of fear': 1915,
    'his last bow': 1917,
    'bruce-partington plans': 1908,
    # Edgar Allan Poe
    'edgar allan poe': 1845,
    'works of edgar allan poe': 1845,
    # Agatha Christie
    'mysterious affair at styles': 1920,
    'murder on the links': 1923,
    'poirot investigates': 1924,
    'secret adversary': 1922,
    'man in the brown suit': 1924,
    # Father Brown by Chesterton
    'innocence of father brown': 1911,
    'wisdom of father brown': 1914,
    # Others
    'moonstone': 1868,
    'mystery of the yellow room': 1907,
    'secret of the night': 1914,
    'red house mystery': 1922,
    'whose body': 1923,
    'hand in the dark': 1920,
}

# same header/footer handling as step1
in_content = False
current_year = None
in_toc = False
emitted = set()

for line in sys.stdin:
    line = line.strip()

    if '*** START OF' in line:
        in_content = True
        continue
    if '*** END OF' in line:
        in_content = False
        current_year = None
        continue

    if not in_content and current_year == None:
        # detect title to assign year
        if 'Title:' in line:
            low = line.lower()
            for title in KNOWN_DATES:
                if title in low:
                    current_year = KNOWN_DATES[title]
                    break
        continue

    # if not current_year:
    #     continue

    if in_content:
        # Table of Contents detection
        if hf.is_table_of_contents(line):
            in_toc = True
            continue
            
        if in_toc and hf.is_toc_entry(line):
            continue
        else:
            in_toc = False

        words = re.findall(r"[a-zA-Z]+", line)
        for w in words:
            w = w.lower()
            if w in TOP_WORDS:
                print(f"{w}\t{current_year}\t1")
                emitted.add(w)

        for w in TOP_WORDS:
            if w not in emitted:
                print(f"{w}\t{current_year}\t0")
