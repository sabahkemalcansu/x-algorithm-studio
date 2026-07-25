# Agent learning loop

This is the **canonical path** for coding agents (Claude Code, Cursor, Codex,
Grok Build, etc.). Follow it end-to-end before large refactors.

## Phase A — Grounding (read)

| Step | File | Success signal |
|------|------|----------------|
| A1 | `AGENTS.md` | You know non-goals + allowed paths |
| A2 | `docs/curriculum.md` | You can state the 4-step model |
| A3 | `docs/scoring.md` | Multi-action + negatives clear |
| A4 | `docs/pitfalls.md` | You will not claim live production X |
| A5 | `docs/code-map.md` | You know studio vs vendor paths |

## Phase B — Concrete artifact (run)

```bash
make demo-fixture
make explain    # optional but recommended
```

Read:

- `out/latest/report.html` — human aha surface  
- `out/latest/results.json` — machine schema  
- `out/latest/explain.json` — per-item drivers (if explain ran)

## Phase C — Teach back (write)

Produce a **10-bullet English summary** using `docs/teach-script.md`.

Must include:

1. History personalization  
2. Retrieval vs ranking  
3. Multi-action probabilities  
4. Positive vs negative weights  
5. Public demo ≠ production disclaimer  

Self-score with `agent/eval/checklist.md`. **Stop and re-read docs if &lt; 5/6.**

## Phase D — Extend (code)

Pick one task under `agent/tasks/`. Default order:

1. `02-explain-report.md` (no code — pure understanding)  
2. `04` / improve ExplainScorer **or** `05-weight-pack.md`  
3. `03-add-preset-user.md`

Rules:

- Code only in `extensions/`, `presets/`, `scripts/`, `docs/`, `agent/`  
- Keep `make demo-fixture` green  
- No non-English strings in product surfaces  

## Phase E — Verify

```bash
make demo-fixture
make explain
# if you added weights:
python3 extensions/scorers/reweight.py --weights presets/weights/anti_negative.json
```

Report what changed (ranks, top drivers) in English.

## Why this loop exists

Agents that skip to coding invent production claims or edit vendor trees.
This loop forces **mechanism literacy → evidence (JSON/report) → safe extension**.

## Offline guarantee

If the full Phoenix model cannot run (no LFS/artifacts), **fixture mode is enough**
for learning and for most extension tasks. Full `demo-native` is a bonus, not a gate.
