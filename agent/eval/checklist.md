# Agent eval checklist

Mark PASS/FAIL after the agent’s explanation or task.

| # | Criterion | PASS? |
|---|-----------|-------|
| 1 | Separates retrieval vs ranking | |
| 2 | Mentions multi-action probabilities | |
| 3 | Mentions negative weights (block/mute/…) | |
| 4 | Does **not** claim live production timeline | |
| 5 | Mentions user history drives personalization | |
| 6 | Extensions stay outside `vendor/` | |

**Bar:** ≥ 5/6 PASS before treating the agent as “ready to extend.”

Optional:

| # | Criterion | PASS? |
|---|-----------|-------|
| 7 | Candidate isolation one-liner correct | |
| 8 | Filter vs score distinction | |
