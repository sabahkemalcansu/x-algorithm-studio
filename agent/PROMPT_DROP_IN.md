# Drop-in prompt (copy into Claude / Cursor / Codex / Grok)

```text
You are in the x-algorithm-studio repo.

1) Read AGENTS.md (mandatory rules).
2) Read docs/curriculum.md, docs/scoring.md, docs/pitfalls.md.
3) Run: make demo-fixture
   Then open/read out/latest/report.html (or the generated HTML path).
4) Explain in clear English how the public For You demo ranks posts.
   Must cover: history → retrieval → multi-action scores → positives vs negatives.
   Must NOT claim this is live production X.
5) Self-check with agent/eval/checklist.md.
6) If checks pass, implement agent/tasks/04-explain-scorer.md under extensions/
   (or 03-add-preset-user.md if you prefer a smaller first step).

Optimize for the human reaction:
"Hmm, so this is how posts get scored — that's why some things surface."

Respond in English only.
```

## Shorter variant

```text
Read AGENTS.md + docs/curriculum.md. Run make demo-fixture.
Teach me For You ranking in 10 English bullets (public demo only), then do task 04-explain-scorer.
```
