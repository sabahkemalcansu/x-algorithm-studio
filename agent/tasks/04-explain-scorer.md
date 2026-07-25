# Task 04 — ExplainScorer (first real extension)

## Goal

Add `extensions/scorers/explain.py` that:

1. Loads `out/latest/results.json`  
2. For each item, computes simple contributions:  
   `contrib_favorite = 2.0 * P(favorite)`, `contrib_dwell = 1.5 * P(dwell)`, `contrib_block = -3.0 * P(block)`  
   (teaching weights — label them as illustrative)  
3. Prints top 3 drivers per item for ranks 1..5  
4. Optionally writes `out/latest/explain.json`

## Acceptance

- `python3 extensions/scorers/explain.py` runs after `make demo-fixture`  
- Output is human-readable  
- README blurb under `extensions/scorers/`  

Do not modify vendor.
