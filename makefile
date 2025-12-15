# ========================
# CS118 Project 3 Makefile
# ========================

PYTHON = python3
CODE_DIR = code
RESULTS_DIR = results
DATA_DIR = data
INPUT = cleaned_text.txt

STEP1_MAPPER = $(CODE_DIR)/step1_mapper.py
STEP1_REDUCER = $(CODE_DIR)/step1_reducer.py
STEP2_MAPPER = $(CODE_DIR)/step2_mapper.py
STEP2_REDUCER = $(CODE_DIR)/step2_reducer.py

# Step2 intermediate/output files
STEP2_MAPPED  = $(RESULTS_DIR)/step2_mapped.txt
STEP2_SORTED  = $(RESULTS_DIR)/step2_sorted.txt
STEP2_ANALYSIS = $(RESULTS_DIR)/step2_analysis.txt

.PHONY: all clean step1 step2

all: step1 step2
	@echo "✅ Pipeline finished successfully."

# ------------------------
# Step 1: Word Rankings
# ------------------------
step1:
	@echo "▶ Running Step 1 (Word Rankings)..."
	@mkdir -p $(RESULTS_DIR)
	@rm -f $(RESULTS_DIR)/step1_*.txt
	$(PYTHON) $(STEP1_MAPPER) < $(INPUT) > $(RESULTS_DIR)/step1_mapped.txt
	LC_ALL=C sort $(RESULTS_DIR)/step1_mapped.txt > $(RESULTS_DIR)/step1_sorted.txt
	$(PYTHON) $(STEP1_REDUCER) < $(RESULTS_DIR)/step1_sorted.txt > $(RESULTS_DIR)/step1_reduced.txt
	head -25 $(RESULTS_DIR)/step1_reduced.txt > $(RESULTS_DIR)/step1_topwords.txt
	@echo "✔ Step 1 done: $(RESULTS_DIR)/step1_topwords.txt"

# ------------------------
# Step 2: Year-Based Analysis
# ------------------------
step2: step1
	@echo "▶ Running Step 2 (Year-Based Analysis)..."
	@mkdir -p $(RESULTS_DIR)
	@rm -f $(STEP2_MAPPED) $(STEP2_SORTED) $(STEP2_ANALYSIS)

	@for f in $(DATA_DIR)/* ; do \
		export map_input_file=$$f ; \
		$(PYTHON) $(STEP2_MAPPER) < $$f >> $(STEP2_MAPPED) ; \
	done

	LC_ALL=C sort $(STEP2_MAPPED) > $(STEP2_SORTED)
	$(PYTHON) $(STEP2_REDUCER) < $(STEP2_SORTED) > $(STEP2_ANALYSIS)

	@echo "✔ Step 2 done: $(STEP2_ANALYSIS)"

# ------------------------
# Clean all generated files
# ------------------------
clean:
	@rm -f $(RESULTS_DIR)/*.txt
	@echo "🧹 Cleaned results directory."