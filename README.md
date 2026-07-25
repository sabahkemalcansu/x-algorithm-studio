# x-algorithm-studio

**Run · Understand · Extend**

> One click to see how X’s **public** For You (Phoenix) demo ranks posts —  
> **or** drop this repo into Claude / Cursor / Codex / Grok and let the agent learn it, then build on top.

Not affiliated with X or xAI.  
Does **not** reconstruct your live timeline or production weights.  
Built on [`xai-org/x-algorithm`](https://github.com/xai-org/x-algorithm) (Apache-2.0).  
**Language:** English only (docs, report UI, agent prompts).

---

## Two doors

| Door | Command / action | You get |
|------|------------------|---------|
| **Human — one click** | `make demo-fixture` (offline) or `make demo` | Plain-language **aha report** |
| **Agent — one paste** | Open repo + [`agent/PROMPT_DROP_IN.md`](agent/PROMPT_DROP_IN.md) | Agent learns curriculum → can extend |

---

## Quick start (understand in 2 minutes, offline)

No 3GB download required:

```bash
git clone <your-fork-or-path> x-algorithm-studio
cd x-algorithm-studio
make doctor
make demo-fixture
make open
```

You’ll get `out/latest/report.html`:

- one-sentence mental model  
- 4 steps: remember → retrieve → score → rank  
- why #1 beats a lower item (positive vs negative signals)  
- honest disclaimer  

---

## Full Phoenix demo (real mini model)

Needs ~3GB artifacts, git-lfs, and Python/uv (or later Docker fat image):

```bash
make vendor    # clone xai-org/x-algorithm
make pull      # LFS / extract artifacts into ~/.cache/x-algorithm-studio
make demo-native
make open
```

See upstream `phoenix/README.md` if LFS fails.

---

## For coding agents (the big unlock)

**Global product — English only.**

### What users do

1. Open this folder in Claude Code, Cursor, Codex, or Grok Build.  
2. Paste **[`agent/PROMPT_DROP_IN.md`](agent/PROMPT_DROP_IN.md)** (the whole copy block).  

### What they should see first (product session)

The agent’s **first reply** must follow [`agent/SESSION_PROTOCOL.md`](agent/SESSION_PROTOCOL.md):

1. **Welcome** — owner + thanks ([`OWNER.md`](OWNER.md))  
2. **What this is / why it exists**  
3. **What you can do / what to expect**  
4. **Capability set** ([`docs/capabilities.md`](docs/capabilities.md))  
5. **Continue** — Questions · Demo · Build  

Example tone: [`agent/FIRST_TURN_EXAMPLE.md`](agent/FIRST_TURN_EXAMPLE.md).

### After they pick a path

| Path | Agent does |
|------|------------|
| Questions | Teach from curriculum / scoring / capabilities |
| Demo | `make demo-fixture` (+ `make explain`) and walk the report |
| Build | `make agent-smoke` → extension task under `extensions/` / `presets/` |

Deeper technical loop: [`docs/agent-loop.md`](docs/agent-loop.md).  
Eval: [`agent/eval/checklist.md`](agent/eval/checklist.md) (≥5/6 = solid grasp).

```bash
make agent-smoke   # fixture report + ExplainScorer
make explain       # why #1 ranked up (teaching weights)
```

---

## What you’re looking at

Public demo shape:

```text
sample user history (sports)
  → retrieve candidates from sports corpus
  → Phoenix multi-action probabilities
  → ranked list + aha report
```

**Aha, not magic:** posts surface when predicted positive engagement is high and negative (block/mute/…) is low — for *that* user history.

---

## Layout

```text
scripts/          doctor, pull, run, aha renderer
fixtures/         offline sample_results.json
vendor/           x-algorithm (on make vendor)
docs/             curriculum, scoring, code-map
agent/            drop-in prompt, tasks, eval
extensions/       safe place to build
out/              generated reports (gitignored)
```

---

## Marketing one-liner (X)

> 26k people starred the algorithm. Almost nobody runs it.  
> **x-algorithm-studio**: one command to *see* how ranking works —  
> or drop it into your coding agent and *extend* it.

---

## License

Apache-2.0. Upstream `x-algorithm` remains under its Apache-2.0 terms; see `NOTICE`.
