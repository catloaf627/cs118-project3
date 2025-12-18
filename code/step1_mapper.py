#!/usr/bin/env python3
import os
import re
import sys

def load_stopwords():
    from nltk.corpus import stopwords  # type: ignore
    return set(stopwords.words('english'))

STOP_WORDS = load_stopwords()

# ---- Parsing helpers ----
RE_TOKEN = re.compile(r"[A-Za-z']+")
RE_META = re.compile(r"^\s*(Book|Author|Year)\s*:\s*(.*)\s*$", re.IGNORECASE)
RE_ALL_EQUALS = re.compile(r"^\s*=+\s*$")
# Normalize words containing the Unicode ligature 'œ' in "manœuvre(s)"
# to prevent incorrect tokenization into "man" + "oeuvre(s)"
RE_MANOEUVRE = re.compile(r"manœuvre(s)?", re.IGNORECASE)

def normalize_token(raw: str) -> str | None:
    # Skip the contraction "we'll" to avoid it being normalized to "well"
    if raw.lower() == "we'll":
        return None
    w = raw.lower().replace("'", "")
    if len(w) < 3:
        return None
    if not w.isalpha():
        return None
    if w in STOP_WORDS:
        return None
    return w

def toc_state_machine(line: str, in_toc: bool) -> tuple[bool, bool]:
    """
    Returns (should_skip_line, new_in_toc).
    Conservative: only skip explicit TOC header and obvious chapter listing lines.
    """
    s = line.strip()
    low = s.lower()

    if not in_toc:
        if low in ("contents", "table of contents"):
            return True, True
        return False, False

    # in_toc == True
    if s == "":
        # blank lines inside TOC: keep skipping but allow exit if TOC ends
        return True, True

    # Obvious TOC listing line heuristics
    # - starts with roman numeral / digit then punctuation
    # - or contains "chapter" and looks short-ish
    is_listing = bool(re.match(r"^\s*([ivxlcdm]+|\d+)\s*[\.\):\-]", low)) or \
                 ("chapter" in low and len(s) < 200)

    if is_listing:
        return True, True

    # First non-listing non-empty line => TOC ended; do NOT skip it
    return False, False

def main():
    in_toc = False

    for line in sys.stdin:
        line = line.rstrip("\n")
        line = RE_MANOEUVRE.sub(lambda m: "manoeuvre" + (m.group(1) or ""), line)

        # Skip separators of ======
        if RE_ALL_EQUALS.match(line):
            continue

        # Skip metadata lines (but we do not need year in step1)
        if RE_META.match(line):
            continue

        # TOC removal (if present)
        skip, new_in_toc = toc_state_machine(line, in_toc)
        if in_toc:
            if skip:
                continue
            else:
                in_toc = False
        else:
            if skip:
                in_toc = True
                continue

        # Tokenize and emit
        for tok in RE_TOKEN.findall(line):
            w = normalize_token(tok)
            if w is not None:
                sys.stdout.write(f"{w}\t1\n")

if __name__ == "__main__":
    main()
