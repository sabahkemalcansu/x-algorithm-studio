# Task 05 — Weight pack experiment

## Goal

Show how **product weights** change order even when model probabilities stay fixed.

## Steps

1. `make demo-fixture`
2. Note top-3 from `out/latest/results.json`
3. Run:

```bash
python3 extensions/scorers/reweight.py \
  --weights presets/weights/anti_negative.json \
  --output out/latest/results_anti_negative.json

python3 extensions/scorers/reweight.py \
  --weights presets/weights/engagement_max.json \
  --output out/latest/results_engagement_max.json
```

4. Compare top-5 post_ids across default / anti_negative / engagement_max.
5. Write a short English paragraph: what changed and why (look at high-block items).

## Acceptance

- Two reweighted JSON files exist under `out/latest/`
- You explain at least one rank swap using P(block) or P(dwell)
- You state weights are **teaching-only**, not production X
