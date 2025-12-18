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
