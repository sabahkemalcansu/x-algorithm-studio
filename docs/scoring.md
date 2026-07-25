# Scoring deep dive (teaching)

## Multi-action head

Instead of one “relevance” logit, the ranker predicts many actions, for example:

**Positive-leaning:** favorite/like, reply, repost, quote, click, profile click, video view, dwell, share, follow…

**Negative-leaning:** not interested, block, mute, report…

Exact action set follows upstream model/config (public mini model documents ~19 action types).

## Weighted sum

Home Mixer–style serving combines probabilities:

```
final = Σ w_i * P(action_i)
```

with **positive** and **negative** weights. Studio aha reports emphasize this shape even when using illustrative finals in fixtures.

## Why #1 vs #8 (teaching example)

| | High rank | Low rank |
|--|-----------|----------|
| P(favorite) | high | low/mid |
| P(dwell) | high | low |
| P(block) | low | higher |
| Story | fits history, worth time | weak fit or spammy |

## Isolation reminder

Candidate A’s score should not depend on whether B is in the same batch (isolation mask). That’s a ranking-systems design choice, not a social UI detail.

## What we do **not** know from the public demo alone

- Exact production weights on live X  
- Full candidate sources mix at scale  
- Ads / policy stacks interaction in production  

Teach mechanism, not false precision.
