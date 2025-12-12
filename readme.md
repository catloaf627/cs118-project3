# CS118 Project 3 — What To Do After Every Code Change

### Step 0: Activate the virtual environment (if you opened a new terminal)

```bash
cd ~/Desktop/cs118-project3
source venv/bin/activate
```

---

### Step 1: Delete all old outputs (mandatory)

```bash
rm -f results/step1_mapped.txt
rm -f results/step1_reduced.txt
rm -f results/step1_topwords.txt
rm -f results/step2_mapped.txt
rm -f results/step2_analysis.txt
```

Purpose: prevent mixing **new code** with **old results**.

---

### Step 2: Re-run Step 1 Mapper (per file)

```bash
for f in data/*; do
  python3 code/step1_mapper.py < "$f" >> results/step1_mapped.txt
done
```

---

### Step 3: Re-run Step 1 Reducer

```bash
python3 code/step1_reducer.py < results/step1_mapped.txt > results/step1_reduced.txt
```

---

### Step 4: Re-generate Top 25 (always required)

```bash
head -25 results/step1_reduced.txt > results/step1_topwords.txt
```

---

### Step 5: Sanity-check Step 1 (critical)

```bash
cat results/step1_topwords.txt
```

Verify all of the following:

* Exactly 25 lines
* **No proper names** (e.g., holmes, drebber, ferrier)
* Mostly function words (said, one, man, would, could, upon, ...)

⚠️ If Step 1 is wrong, **do NOT proceed to Step 2**.

---

### Step 6: Re-run Step 2 Mapper (per file)

```bash
for f in data/*; do
  python3 code/step2_mapper.py < "$f" >> results/step2_mapped.txt
done
```

---

### Step 7: Re-run Step 2 Reducer (final output)

```bash
python3 code/step2_reducer.py < results/step2_mapped.txt > results/step2_analysis.txt
```

---

### Step 8: Sanity-check Step 2 output

```bash
head -40 results/step2_analysis.txt
```

Verify:

* Each block starts with `Word:`
* Word order exactly matches `step1_topwords.txt`
* Years are in ascending order

---

## One-line Debugging Rule

> **Change code → delete old results → run Step 1 → check Top25 →
> only then run Step 2**

---

## After Debugging (Ready to Submit)

Only these files are submitted to the autograder:

```
results/step1_topwords.txt
results/step2_analysis.txt
```

All other files are intermediate and should not be submitted.
