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

def load_top_words() -> set[str]:
    # Handout suggests env var TOP_WORDS_FILE
    path = os.environ.get("TOP_WORDS_FILE", "results/step1_topwords.txt")
    top = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # step1 output format: "word count"
                parts = line.split()
                if parts:
                    top.add(parts[0].lower())
    except FileNotFoundError:
        # If not found, fail loudly; step2 depends on it
        sys.stderr.write(f"ERROR: TOP_WORDS_FILE not found: {path}\n")
        sys.exit(1)
    return top

def toc_state_machine(line: str, in_toc: bool) -> tuple[bool, bool]:
    s = line.strip()
    low = s.lower()

    if not in_toc:
        if low in ("contents", "table of contents"):
            return True, True
        return False, False

    if s == "":
        return True, True

    is_listing = bool(re.match(r"^\s*([ivxlcdm]+|\d+)\s*[\.\):\-]", low)) or \
                 ("chapter" in low and len(s) < 200)

    if is_listing:
        return True, True

    return False, False

def main():
    top_words = load_top_words()

    current_year: int | None = None
    in_toc = False

    for line in sys.stdin:
        line = line.rstrip("\n")
        line = RE_MANOEUVRE.sub(lambda m: "manoeuvre" + (m.group(1) or ""), line)

        # Skip ===== separators
        if RE_ALL_EQUALS.match(line):
            continue

        # Handle metadata
        m = RE_META.match(line)
        if m:
            key = m.group(1).strip().lower()
            val = (m.group(2) or "").strip()
            if key == "year":
                try:
                    current_year = int(val)
                except ValueError:
                    current_year = None
            # Always skip metadata lines as "metadata"
            continue

        # TOC removal if present
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

        # If we haven't seen a Year yet, we cannot emit step2 keys
        if current_year is None:
            continue

        for tok in RE_TOKEN.findall(line):
            w = normalize_token(tok)
            if w is None:
                continue
            if w in top_words:
                sys.stdout.write(f"{w}\t{current_year}\t1\n")

if __name__ == "__main__":
    main()
