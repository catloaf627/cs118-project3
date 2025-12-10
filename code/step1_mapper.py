#!/usr/bin/env python3
import sys
import re
import string
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english'))

in_content = False

for line in sys.stdin:
    line = line.strip()

    # Start marker
    if '*** START OF' in line:
        in_content = True
        continue

    # End marker
    if '*** END OF' in line:
        in_content = False
        break

    if not in_content:
        continue

    # Extract alphabetic words
    words = re.findall(r"[a-zA-Z]+", line)
    for w in words:
        w = w.lower()
        if len(w) >= 3 and w not in STOP_WORDS:
            sys.stdout.write(w + "\t1\n")
