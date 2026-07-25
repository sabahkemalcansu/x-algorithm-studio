# Agent pack (global / English)

This folder turns **x-algorithm-studio** into a drop-in curriculum for coding agents.

## Fast path (for humans)

1. Open the repo in Claude Code, Cursor, Codex, or Grok Build.  
2. Paste **[`PROMPT_DROP_IN.md`](PROMPT_DROP_IN.md)** into the agent.  
3. You should receive a **guided first message**:  
   Welcome → what/why → expectations → capabilities → Questions / Demo / Build.  
4. Pick a path; the agent deepens from there (`SESSION_PROTOCOL.md` + `docs/agent-loop.md`).  
5. Quality bar: [`eval/checklist.md`](eval/checklist.md).

If the agent skips the welcome and jumps into code, re-paste the short prompt in `PROMPT_DROP_IN.md`.

## Layout

```text
PROMPT_DROP_IN.md      # what users paste (entry)
SESSION_PROTOCOL.md    # mandatory first-turn host script
FIRST_TURN_EXAMPLE.md  # gold-standard welcome tone
tasks/                 # graded practice after Build
eval/                  # checklist + golden rubric
```

## Design goals

| Goal | How |
|------|-----|
| Product-feeling session | SESSION_PROTOCOL welcome flow |
| Agent *actually* learns | agent-loop + fixture evidence + checklist |
| Safe coding | Extensions only; vendor read-only |
| Global audience | English only |
| Measurable grasp | checklist ≥5/6; can restate 4-step model |

## Offline first

Agents must succeed with `make demo-fixture` alone. Full Phoenix artifacts are optional.
