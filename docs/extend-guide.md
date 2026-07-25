# Extend guide

## Rules

1. Put new code under `extensions/` or `presets/`.  
2. Don’t break `make demo-fixture`.  
3. Keep Apache attribution / NOTICE.  
4. Document the teaching value in a short README blurb.

## Ideas

- **ExplainScorer** — top 3 drivers per item (fav/dwell/block contributions)  
- **Preset users** — “NBA-only fan”, “casual” histories  
- **Weight packs** — `engagement_max.toml` vs `anti_negative.toml` (post-hoc teaching reweight)  
- **Bilingual report** — `--lang en` already supported in renderer  

## Contract for post-hoc reweight (teaching)

If you re-rank fixture/live JSON:

```text
new_final = sum(w[a] * scores[a] for a in scores)
```

Write before/after ranks into `out/latest/` and re-run `make report`.
