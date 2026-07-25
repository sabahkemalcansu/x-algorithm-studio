# Curriculum — 15 minutes to the For You mental model

## 0) What is this package?

**x-algorithm-studio** wraps the public `xai-org/x-algorithm` Phoenix demo so you can:

1. **Run** it (`make demo-fixture` offline, or full artifacts when available)
2. **Understand** it (aha HTML report + this curriculum)
3. **Extend** it (`extensions/`, `presets/`)

## 1) The problem

Millions of posts. Which ones first for *this* user?

Wrong intuition: “Highest likes / biggest account wins.”  
Right intuition here: “What will **this user** do?”

## 2) Two stages

### Retrieval — find candidates

Encode user history → search a large pool → keep top‑K similar / eligible items.  
Demo pool: sports corpus (~hundreds of thousands of posts in the public mini demo).

### Ranking — order them

A heavier model predicts **many** action probabilities per candidate, then combines them.

## 3) Product formula

```
FinalScore ≈ Σ (w_pos × P(positive_action))
           − Σ (w_neg × P(negative_action))
```

**Aha:** “Would get likes” is not enough if “would get blocked” is also high.

## 4) Candidate isolation

In ranking, candidates generally **don’t attend to each other** — only to user context.  
Scores stay stable across batches (cache-friendly, consistent).

## 5) Full system map (reading guide)

| Piece | Role |
|-------|------|
| Thunder | In-network (accounts you follow) |
| Phoenix retrieval | Out-of-network discovery |
| Phoenix ranker | Multi-action scoring |
| Home Mixer | Orchestration, filters, diversity |
| Filters | Mute, age, seen… (hard rules ≠ ML score) |

Studio demo emphasizes Phoenix-style retrieval→rank teaching surface.

## 6) Human sentences (use in reports)

1. It knows you from history.  
2. It gathers candidates.  
3. It predicts what you’ll do.  
4. Positives up, negatives down.  
5. “Famous / always on my feed” is not magic — high predicted fit + low rejection (demo-scale reading).

## 7) Responsible creator reading

- Optimize for **repeat genuine engagement**, not pure clickbait.  
- Spam patterns raise negative probability mass.  
- This is **literacy**, not a guaranteed growth hack.

## 8) Next

`docs/scoring.md` → `docs/code-map.md` → `make demo-fixture` → `agent/tasks/…`
