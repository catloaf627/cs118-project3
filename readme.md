# CS118 Project 3 – MapReduce Word Trend Analysis

This project analyzes word usage and publication-year trends across 25 detective fiction novels using a two-stage MapReduce pipeline in Python.

---

## Step 1 – Word Ranking
- Remove Project Gutenberg headers and footers
- Remove table-of-contents sections
- Normalize words (lowercase, alphabetic only, min length 3)
- Filter English stopwords via NLTK
- Count word frequencies across all novels
- Sort in descending order
- Output the Top-25 most frequent words

## Step 2 – Year-based Trend Analysis
- Determine publication year from stored title→year mapping
- Only track the Top-25 words from Step 1
- Aggregate occurrences by publication year
- Produce time-series trend data (similar to Google Ngram)

---

## Project Structure

cs118-project3/
│
├── code/
│   ├── step1_mapper.py        # Extract, clean, filter, emit (word,1)
│   ├── step1_reducer.py       # Aggregate & sort by freq desc
│   ├── step2_mapper.py        # Emit (word,year,1) for Top-25 only
│   └── step2_reducer.py       # Aggregates & formats year trends
│
├── data/                      # 25 raw Project Gutenberg .txt books
│
├── results/
│   ├── step1_reduced.txt      # Full sorted word frequency list
│   ├── step1_topwords.txt     # Top 25 most frequent words
│   └── step2_analysis.txt     # Year-by-year trend results
│
└── venv/                      # Python virtual environment

---

## How to Run

### Setup
source venv/bin/activate
pip install nltk
python3 -c "import nltk; nltk.download('stopwords')"

### Step 1
python3 code/step1_mapper.py < results/combined_input.txt > results/step1_mapped.txt
python3 code/step1_reducer.py < results/step1_mapped.txt > results/step1_reduced.txt
head -25 results/step1_reduced.txt > results/step1_topwords.txt

### Step 2
python3 code/step2_mapper.py < results/combined_input.txt > results/step2_mapped.txt
python3 code/step2_reducer.py < results/step2_mapped.txt > results/step2_analysis.txt

---

## Files to Submit

### Output Results:
results/step1_reduced.txt  
results/step1_topwords.txt  
results/step2_analysis.txt  

### Code:
code/step1_mapper.py  
code/step1_reducer.py  
code/step2_mapper.py  
code/step2_reducer.py  

---

## Dependencies
- Python 3.x
- nltk (stopwords data)

---

## Author
Group 12
CS118 Cloud Computing – Fall 2025  
Tufts University
```
