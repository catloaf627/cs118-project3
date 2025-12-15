#helper_func.py
#!/usr/bin/python3

import re
import string
from nltk.corpus import stopwords

# Load NLTK English stopwords
STOP_WORDS = set(stopwords.words('english'))


# =============================================================================
# GUTENBERG HEADER/FOOTER DETECTION
# =============================================================================

def is_start_marker(line):
    """
    Check if this line marks the START of actual book content.
    Gutenberg uses "*** START OF" to indicate where the book begins.
    """
    patterns = [
        r'\*\*\* START OF',
        r'\*\*\*START OF',
    ]
    return any(re.search(p, line, re.IGNORECASE) for p in patterns)


def is_end_marker(line):
    """
    Check if this line marks the END of actual book content.
    Gutenberg uses "*** END OF" to indicate where the book ends.
    Everything after this is license/legal text.
    """
    patterns = [
        r'\*\*\* END OF',
        r'\*\*\*END OF',
    ]
    return any(re.search(p, line, re.IGNORECASE) for p in patterns)


# =============================================================================
# TABLE OF CONTENTS DETECTION
# =============================================================================

def is_table_of_contents(line):
    """
    Check if this line is a TOC header (e.g., "Contents", "Table of Contents").
    """
    patterns = [
        r'^contents?:?$',           # "Content", "Contents", "Content:", "Contents:"
        r'^table of contents:?$',
    ]
    line_lower = line.lower().strip()
    return any(re.match(p, line_lower, re.IGNORECASE) for p in patterns)


def is_toc_entry(line):
    """
    Check if this line looks like a TOC entry (numbered chapter listing).
    TOC entries typically start with numbers, roman numerals, or chapter headings.
    """
    line_stripped = line.strip().lower()
    
    toc_entry_patterns = [
        r'^[ivxlc]+\.?\s',           # Roman numerals: "II. ...", "XIV ..."
        r'^\d+\.?\s',                 # Arabic numerals: "1. ...", "12 ..."
        r'^chapter\s+[ivxlc\d]+',     # "Chapter I", "Chapter 12"
        r'^part\s+[ivxlc\d]+',        # "Part I", "Part 2"
        r'^prologue',                 # "Prologue"
        r'^epilogue',                 # "Epilogue"
        r'^appendix',                 # "Appendix"
        r'^preface',                  # "Preface"
        r'^introduction',             # "Introduction"
    ]
    return any(re.match(p, line_stripped) for p in toc_entry_patterns)


# =============================================================================
# WORD CLEANING
# =============================================================================

def clean_word(word):
    """
    Clean and normalize a word for analysis.
    
    Returns:
        Cleaned word (lowercase, stripped of punctuation) if valid,
        None if word should be filtered out.
    
    Filtering criteria:
        - Minimum length of 3 characters
        - Must be alphabetic only (no numbers or special characters)
        - Must not be a stop word
    """
    # Remove surrounding punctuation (including smart quotes, dashes)
    word = word.strip(string.punctuation + '""''—–')
    word = word.lower()
    
    # Filter out invalid words
    if not word or len(word) < 3 or word in STOP_WORDS:
        return None
    
    if not word.isalpha():
        return None
    
    return word