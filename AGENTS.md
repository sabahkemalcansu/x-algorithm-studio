# AGENTS.md — x-algorithm-studio

You are working in **x-algorithm-studio**: a community package that makes the
public [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) Phoenix demo
easy to **run**, easy to **understand**, and safe to **extend**.

## Mission (in order)

1. **Understand** the ranking mental model (not “most likes win”).
2. **Run** `make demo-fixture` (always) or full `make demo-native` if artifacts exist.
3. **Explain** in plain **English** using `docs/teach-script.md` tone.
4. **Extend** only under `extensions/`, `presets/`, `docs/`, `scripts/`, `agent/`.

## Hard non-goals

- Do **not** claim this is live X production ranking or a user’s real timeline.
- Do **not** invent production weight values.
- Do **not** rewrite `vendor/x-algorithm` casually; treat it as pinned upstream.
- Do **not** give spammy “game the algorithm” playbooks; teach **mechanism literacy**.

## Mandatory read order

1. `docs/curriculum.md`
2. `docs/scoring.md`
3. `docs/code-map.md`
4. `docs/pitfalls.md`
5. `out/latest/report.html` **or** generate via `make demo-fixture`
6. `extensions/README.md` before coding extensions

## Mental model (must internalize)

```
User history
  → retrieve candidates (similarity / sources)
  → predict P(actions): like, reply, dwell, block, mute, …
  → Final ≈ Σ w_pos·P(pos) − Σ w_neg·P(neg)
  → filters / diversity (full system)
  → ranked feed
```

Demo focus: public **mini Phoenix** retrieval → ranking on a **sports** corpus + example user.

## Commands

```bash
make doctor
make demo-fixture    # offline aha report (preferred first step)
make open
make vendor && make pull && make demo-native   # full model when possible
```

## Teaching target (human reaction)

> “Hmm — so this kind of post scores like this; that’s why some posts surface
> and some accounts *feel* big — scoring and predicted engagement, not magic.”

## Safe extension points

| Path | Purpose |
|------|---------|
| `extensions/scorers/` | Explain layers, post-processors |
| `extensions/filters/` | Demo filters |
| `presets/users/` | Alternate histories |
| `presets/weights/` | Teaching weight packs |
| `scripts/` | DX only |
| `docs/` | Curriculum |

## After learning — pick a task

- `agent/tasks/01-summarize.md`
- `agent/tasks/02-explain-report.md`
- `agent/tasks/03-add-preset-user.md`
- `agent/tasks/04-explain-scorer.md`

Self-check: `agent/eval/checklist.md`.

## Output quality bar

- Separate **retrieval** vs **ranking**
- Mention **multi-action** + **negative** weights
- One sentence on **candidate isolation** if asked about the transformer
- Always include the **public demo ≠ production** disclaimer
