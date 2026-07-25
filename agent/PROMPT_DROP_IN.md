# Drop-in prompt (copy into Claude / Cursor / Codex / Grok)

English-only. Global product.

```text
You are in the x-algorithm-studio repo (English-only, global audience).

Follow docs/agent-loop.md end-to-end:

1) Read AGENTS.md (mandatory rules + non-goals).
2) Read docs/curriculum.md, docs/scoring.md, docs/pitfalls.md.
3) Run: make agent-smoke
   (or: make demo-fixture && make explain)
4) Read out/latest/report.html and out/latest/explain.json.
5) Teach-back in clear English (10 bullets):
   history → retrieval → multi-action scores → positives vs negatives.
   MUST NOT claim live production X or invent production weights.
6) Self-check agent/eval/checklist.md (need ≥5/6).
7) Then implement ONE of:
   - agent/tasks/05-weight-pack.md  (recommended: shows rank swaps)
   - agent/tasks/03-add-preset-user.md
   - improve extensions/scorers/explain.py (task 04 stretch)

Optimize for the human reaction:
"Hmm, so this is how posts get scored — that's why some things surface."

Respond in English only. Put new code under extensions/ or presets/ only.
```

## Shorter variant

```text
Read AGENTS.md + docs/agent-loop.md. Run make agent-smoke.
Explain For You ranking in 10 English bullets (public demo only),
pass agent/eval/checklist.md, then do agent/tasks/05-weight-pack.md.
```
