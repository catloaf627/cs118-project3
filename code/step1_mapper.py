#!/usr/bin/env python3
import sys
import re
import string
from nltk.corpus import stopwords
import helper_func as hf

STOP_WORDS = set(stopwords.words('english'))

in_content = False
in_toc = False

for line in sys.stdin:
    line = line.strip()

    # Start marker
    if hf.is_start_marker(line):
        in_content = True
        continue

    # End marker
    if hf.is_end_marker(line):
        in_content = False
        continue

    if not in_content:
        continue

    # Table of Contents detection
    if hf.is_table_of_contents(line):
        in_toc = True
        continue
        
    if in_toc and hf.is_toc_entry(line):
        continue
    else:
        in_toc = False

    # Extract alphabetic words
    words = re.findall(r"[a-zA-Z]+", line)
    for w in words:
        w = w.lower()
        if len(w) >= 3 and w not in STOP_WORDS:
            sys.stdout.write(w + "\t1\n")

