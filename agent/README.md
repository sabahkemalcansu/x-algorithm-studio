# Agent pack (global / English)

This folder turns **x-algorithm-studio** into a drop-in curriculum for coding agents.

## Fast path

1. Open the repo root in Claude Code, Cursor, Codex, or Grok Build.  
2. Paste [`PROMPT_DROP_IN.md`](PROMPT_DROP_IN.md).  
3. Agent follows `AGENTS.md` → `docs/agent-loop.md`.  
4. Humans verify with [`eval/checklist.md`](eval/checklist.md).

## Layout

```text
PROMPT_DROP_IN.md   # copy-paste for social / README
tasks/              # graded practice
eval/               # checklist + golden rubric
```

## Design goals

| Goal | How |
|------|-----|
| Agent *actually* learns the mechanism | Mandatory read order + fixture evidence |
| Safe coding | Extensions only; vendor read-only |
| Global audience | English only |
| Measurable | checklist ≥5/6 before “ready to extend” |

## Offline first

Agents must succeed with `make demo-fixture` alone. Full Phoenix artifacts are optional.
