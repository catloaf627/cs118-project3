The source code for this project is available at:  
https://github.com/catloaf627/cs118-project3

## How to Run

```bash
# Activate virtual environment
source /Users/yuqingwang/Desktop/cs118-project3/venv/bin/activate

# Prepare output directory
mkdir -p results
rm -f results/step1_* results/step2_*

# Step 1: Top-25 word count
python3 code/step1_mapper.py < cleaned_text.txt > results/step1_mapped.txt
LC_ALL=C sort results/step1_mapped.txt > results/step1_sorted.txt
python3 code/step1_reducer.py < results/step1_sorted.txt > results/step1_reduced.txt
head -25 results/step1_reduced.txt > results/step1_topwords.txt

# Step 2: Yearly analysis
export TOP_WORDS_FILE=results/step1_topwords.txt
python3 code/step2_mapper.py < cleaned_text.txt > results/step2_mapped.txt
LC_ALL=C sort results/step2_mapped.txt > results/step2_sorted.txt
python3 code/step2_reducer.py < results/step2_sorted.txt > results/step2_analysis.txt

# Preview results
cat results/step1_topwords.txt
head -60 results/step2_analysis.txt

## How to Run

During development, we identified and handled a small number of edge cases in tokenization to ensure the word counts match the intended semantics of the assignment and the provided input format.

### Handling the contraction "we'll"

The tokenizer removes ASCII apostrophes during normalization.  
As a result, the contraction `"we'll"` would be normalized to `"well"`, incorrectly inflating the count of the word **well**.

To prevent this, occurrences of `"we'll"` (both ASCII and Unicode forms) are explicitly skipped during normalization, ensuring that **well** is only counted when it appears as an actual word.

### Handling the word "manœuvre"

Some texts contain the word `"manœuvre"` (or `"manœuvres"`), which includes the Unicode ligature **œ**.  
Since the tokenizer only recognizes standard ASCII letters, this ligature would otherwise cause the word to be split into `"man"` and `"oeuvre(s)"`, incorrectly increasing the count of **man**.

To address this, `"manœuvre"` and `"manœuvres"` are normalized to `"manoeuvre"` and `"manoeuvres"` prior to tokenization, preventing **man** from being over-counted.

These fixes are intentionally minimal and localized, and do not affect the handling of other words or contractions.
