# X launch notes (draft)

## One-liner

One command to *see* how the open For You ranking works — or drop the repo into Claude/Cursor/Grok so your agent learns it and extends it.

## Thread skeleton

1. x-algorithm has huge stars. Running it still hurts (LFS, 3GB, JAX).  
2. **x-algorithm-studio**: `make demo-fixture` → plain-language aha report in minutes.  
3. Screenshot: #1 vs low rank (positives vs block).  
4. Mental model: history → retrieve → multi-action score → rank.  
5. **Agent door**: paste `agent/PROMPT_DROP_IN.md` into your coding agent.  
6. Disclaimer: public demo ≠ live production feed. Not affiliated with X/xAI.  
7. Link + star/fork CTA.

## Pin comment

```text
Human: make demo-fixture && make open
Agent: open agent/PROMPT_DROP_IN.md
```
