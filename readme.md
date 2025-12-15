# CS118 Project 3 — MapReduce Text Analysis

## Overview

This project implements a two-stage MapReduce-style text analysis pipeline using Python and GNU Make.

* **Step 1** computes global word frequencies from a cleaned text corpus and outputs the top 25 most frequent words.
* **Step 2** performs a year-based analysis on those top words, computing how often each word appears in texts from different publication years.

All pipeline steps are orchestrated using the provided `Makefile`.

---

## Input Data

### `cleaned_text.txt`

The input text has already been **pre-cleaned** and provided by the course staff.
Key characteristics of the cleaned input:

* Gutenberg headers and footers are removed
* Each book is clearly separated using delimiter lines:

  ```
  ======================================================================
  Book: <Book Title>
  Author: <Author Name>
  Year: <Publication Year>
  ======================================================================
  ```
* The `======` delimiter lines are **not part of the actual content** and should not be counted as text

This file is used directly as input for **Step 1**.

---

## Directory Structure

```
.
├── code/
│   ├── step1_mapper.py
│   ├── step1_reducer.py
│   ├── step2_mapper.py
│   └── step2_reducer.py
├── data/
│   └── (individual book files for Step 2)
├── results/
│   └── (generated output files)
├── cleaned_text.txt
├── Makefile
└── README.md
```

---

## Step 1: Word Rankings

**Goal:**
Compute the top 25 most frequent words in the cleaned text corpus.

### Processing Flow

1. `step1_mapper.py`

   * Reads `cleaned_text.txt`
   * Extracts alphabetic words
   * Normalizes to lowercase
   * Filters stopwords
   * Emits `(word, 1)` pairs

2. The intermediate output is **sorted lexicographically** using Unix `sort`.

3. `step1_reducer.py`

   * Aggregates word counts
   * Sorts results by:

     * Frequency (descending)
     * Word (ascending, for ties)

4. The top 25 words are saved to:

   ```
   results/step1_topwords.txt
   ```

---

## Step 2: Year-Based Analysis

**Goal:**
For each of the top 25 words from Step 1, compute how frequently it appears in texts published in different years.

### Processing Flow

1. `step2_mapper.py`

   * Reads individual book files from the `data/` directory
   * Extracts the publication year for each book
   * Emits `(word, year, 1)` only for words that appear in `step1_topwords.txt`

2. All mapper outputs are concatenated into:

   ```
   results/step2_mapped.txt
   ```

3. The intermediate data is sorted by word and year.

4. `step2_reducer.py`

   * Aggregates counts per `(word, year)`
   * Outputs a formatted, human-readable analysis to:

     ```
     results/step2_analysis.txt
     ```

---

## Using the Makefile

### Run the Entire Pipeline

```bash
make
```

This will run **Step 1 followed by Step 2** and generate all results in the `results/` directory.

---

### Run Step 1 Only

```bash
make step1
```

Outputs:

* `results/step1_mapped.txt`
* `results/step1_sorted.txt`
* `results/step1_reduced.txt`
* `results/step1_topwords.txt`

---

### Run Step 2 Only

```bash
make step2
```

Note: `step2` automatically depends on `step1`.

Outputs:

* `results/step2_mapped.txt`
* `results/step2_sorted.txt`
* `results/step2_analysis.txt`

---

### Clean Generated Files

```bash
make clean
```

Removes all `.txt` files from the `results/` directory.

---

## Output Summary

| File                 | Description                                 |
| -------------------- | ------------------------------------------- |
| `step1_topwords.txt` | Top 25 most frequent words                  |
| `step2_analysis.txt` | Year-based frequency analysis for top words |

---

## Notes

* All sorting is performed with `LC_ALL=C` to ensure deterministic ordering.
* The pipeline is designed to match the autograder’s expectations for both **order-sensitive** (Step 1) and **order-insensitive** (Step 2) test
---


