# scorers/

Teaching-time post-processors for `out/latest/results.json`.

| Script | Purpose |
|--------|---------|
| `explain.py` | Top drivers per item (illustrative weights) |
| `reweight.py` | Re-rank with a weight pack under `presets/weights/` |

```bash
make demo-fixture
make explain

python3 extensions/scorers/reweight.py \
  --weights presets/weights/anti_negative.json
```

**Disclaimer:** These weights are for education. They are **not** production X weights.
