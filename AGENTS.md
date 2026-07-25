# AGENTS.md — x-algorithm-studio

You are working in **x-algorithm-studio**: a community package that makes the
public [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) Phoenix demo
easy to **run**, easy to **understand**, and safe to **extend**.

**Language policy:** English only (docs, reports, code comments, user-facing
explanations). This product targets a global audience.

## Mission (strict order)

### On a new human session (drop-in / first message)

0. **Host the user** — follow `agent/SESSION_PROTOCOL.md` **before** deep tooling:
   Welcome (from `OWNER.md`) → what/why → expectations → capabilities → CTAs  
   (Questions / Demo / Build).  
   See `agent/FIRST_TURN_EXAMPLE.md` for tone.

### Then (after they choose a path)

1. **Understand** the ranking mental model (not “most likes win”).
2. **Run** `make demo-fixture` / `make agent-smoke` when demo or build is chosen.
3. **Explain** in plain English (`docs/teach-script.md` tone).
4. **Self-check** against `agent/eval/checklist.md` (need ≥5/6) before “fully grasped”.
5. **Extend** only under allowed paths (below).
6. **Re-run** fixture/report or `make explain` after code changes.

Full technical loop: `docs/agent-loop.md`.  
Capability map for §4 of the welcome: `docs/capabilities.md`.

## Hard non-goals

- Do **not** claim this is live X production ranking or a user’s real timeline.
- Do **not** invent production weight values as fact.
- Do **not** rewrite `vendor/x-algorithm` casually; treat it as pinned upstream.
- Do **not** write spammy “game the algorithm” playbooks; teach **mechanism literacy**.
- Do **not** add non-English product UI or docs.

## Mandatory read order

1. `docs/curriculum.md`
2. `docs/scoring.md`
3. `docs/code-map.md`
4. `docs/pitfalls.md`
5. `docs/agent-loop.md`
6. Generate or open `out/latest/report.html` via `make demo-fixture`
7. `extensions/README.md` before coding extensions

## Mental model (must internalize)

```
User history
  → retrieve candidates (similarity / sources)
  → predict P(actions): like, reply, dwell, block, mute, …
  → Final ≈ Σ w_pos·P(pos) − Σ w_neg·P(neg)
  → filters / diversity (full system)
  → ranked feed
```

Demo focus: public **mini Phoenix** retrieval → ranking on a **sports** corpus
+ example user. Studio also ships an offline **fixture** so agents can learn
without 3GB artifacts.

## Commands

```bash
make doctor
make demo-fixture    # offline aha report (preferred first step)
make open            # open HTML report
make explain         # run ExplainScorer on out/latest/results.json
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
| `docs/` | Curriculum (English) |
| `agent/` | Tasks & eval |

**Forbidden for casual edits:** `vendor/x-algorithm/**` (read-only unless
intentionally bumping the pin).

## Built-in extension: ExplainScorer

After `make demo-fixture`:

```bash
make explain
# or: python3 extensions/scorers/explain.py
```

Writes human-readable drivers to stdout and `out/latest/explain.json`.

## After learning — pick a task

| Task | File | Outcome |
|------|------|---------|
| Summarize | `agent/tasks/01-summarize.md` | 10 English bullets |
| Explain report | `agent/tasks/02-explain-report.md` | #1 vs low rank story |
| Preset user | `agent/tasks/03-add-preset-user.md` | new history JSON |
| ExplainScorer | `agent/tasks/04-explain-scorer.md` | already shipped — improve or fork |
| Weight pack | `agent/tasks/05-weight-pack.md` | teaching reweight experiment |

Self-check: `agent/eval/checklist.md`  
Concept rubric: `agent/eval/golden-summary.md`

## Output quality bar

- Separate **retrieval** vs **ranking**
- Mention **multi-action** + **negative** weights
- One sentence on **candidate isolation** if asked about the transformer
- Always include the **public demo ≠ production** disclaimer
- English only

## Drop-in entry (what humans share)

| File | Who uses it |
|------|-------------|
| `agent/PROMPT_DROP_IN.md` | **Paste this into the coding agent** |
| `agent/SESSION_PROTOCOL.md` | Agent must execute on first turn |
| `OWNER.md` | Welcome credit + thanks |
| `docs/capabilities.md` | Capability set for welcome §4 |

Humans should say: “Paste `agent/PROMPT_DROP_IN.md` into Claude/Cursor/Grok.”
