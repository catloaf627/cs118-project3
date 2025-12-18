#!/usr/bin/env python3
import os
import re
import sys

# ---- Stopwords: prefer NLTK; fallback ----
FALLBACK_STOPWORDS = {
    'i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",
    'your','yours','yourself','yourselves','he','him','his','himself','she',"she's",'her','hers',
    'herself','it',"it's",'its','itself','they','them','their','theirs','themselves','what','which',
    'who','whom','this','that',"that'll",'these','those','am','is','are','was','were','be','been',
    'being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if',
    'or','because','as','until','while','of','at','by','for','with','about','against','between',
    'into','through','during','before','after','above','below','to','from','up','down','in','out',
    'on','off','over','under','again','further','then','once','here','there','when','where','why',
    'how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only',
    'own','same','so','than','too','very','s','t','can','will','just','don',"don't",'should',"should've",
    'now','d','ll','m','o','re','ve','y','ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",
    'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',"isn't",'ma','mightn',
    "mightn't",'mustn',"mustn't",'needn',"needn't",'shan',"shan't",'shouldn',"shouldn't",'wasn',"wasn't",
    'weren',"weren't",'won',"won't",'wouldn',"wouldn't"
}

def load_stopwords():
    try:
        from nltk.corpus import stopwords  # type: ignore
        return set(stopwords.words('english'))
    except Exception:
        return set(FALLBACK_STOPWORDS)

STOP_WORDS = load_stopwords()

# ---- Parsing helpers ----
RE_TOKEN = re.compile(r"[A-Za-z']+")
RE_META = re.compile(r"^\s*(Book|Author|Year)\s*:\s*(.*)\s*$", re.IGNORECASE)
RE_ALL_EQUALS = re.compile(r"^\s*=+\s*$")

def normalize_token(raw: str) -> str | None:
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
