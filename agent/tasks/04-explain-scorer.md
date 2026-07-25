# Task 04 — ExplainScorer

## Status

**Shipped.** Baseline lives at `extensions/scorers/explain.py`.

## Goal (for agents improving it)

After `make demo-fixture`:

```bash
make explain
# or: python3 extensions/scorers/explain.py
```

You should see top drivers for ranks 1..5 and `out/latest/explain.json`.

## Stretch improvements (pick one)

1. Load weights from `presets/weights/*.json` via `--weights`.  
2. Add a one-line English “story” per item (“high dwell, low block”).  
3. Emit Markdown for README demos.  

## Acceptance

- `make explain` stays green  
- Weights labeled **teaching-only / not production**  
- No vendor edits  
- English-only strings
