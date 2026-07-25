# x-algorithm-studio

**Run · Understand · Extend**

> One click to see how X’s **public** For You (Phoenix) demo ranks posts —  
> **or** drop this repo into Claude / Cursor / Codex / Grok and let the agent learn it, then build on top.

Not affiliated with X or xAI.  
Does **not** reconstruct your live timeline or production weights.  
Built on [`xai-org/x-algorithm`](https://github.com/xai-org/x-algorithm) (Apache-2.0).

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

1. Open this folder in Claude Code, Cursor, Codex, or Grok Build.  
2. Paste the prompt in [`agent/PROMPT_DROP_IN.md`](agent/PROMPT_DROP_IN.md).  
3. Agent must read `AGENTS.md` → `docs/curriculum.md` → explain → optional extension task.

Eval rubric: [`agent/eval/checklist.md`](agent/eval/checklist.md).

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
