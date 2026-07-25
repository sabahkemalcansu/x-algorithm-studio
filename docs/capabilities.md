# Capability set — what the public stack can teach

English product doc. This is the **capability map** agents must present to users
(simplified, honest). Built on public `xai-org/x-algorithm` ideas + this studio.

## A. What you can understand here

| Capability | In plain English | Where it shows up |
|------------|------------------|-------------------|
| **Personalization from history** | The system cares what *you* did before (likes, dwells, replies…) | Curriculum, aha report § user history |
| **Candidate retrieval** | First find a smaller set of posts that might fit | Phoenix retrieval / demo sports corpus |
| **Multi-action ranking** | Not one score — many P(like), P(dwell), P(block)… | Ranking head / results.json scores |
| **Positive vs negative weights** | Engagement lifts; rejection can bury | Scoring formula, ExplainScorer, weight packs |
| **Hard filters vs soft scores** | Mute/block/age/seen can drop posts *before* ML ranking | Full Home Mixer design (docs) |
| **In-network vs out-of-network** | Followed accounts (Thunder) vs global discovery (Phoenix) | System map |
| **Candidate isolation** | A post’s score doesn’t depend on which other posts are in the batch | Phoenix ranker design |
| **Diversity / author decay** | Avoid five posts from the same author in a row (full system) | Home Mixer scorers (concept) |
| **Explainability (studio)** | “Why is #1 on top?” via teaching drivers | `make explain` |
| **Weight experiments (studio)** | Same probs, different product weights → new order | `reweight.py` + `presets/weights/` |

## B. What this studio can *do* for you (product actions)

| Action | Command / path | Expectation |
|--------|----------------|-------------|
| Offline aha report | `make demo-fixture` | HTML lesson in English, no 3GB download |
| Score drivers | `make explain` | Top positive/negative contributions |
| Weight A/B | `reweight.py` + weight packs | Rank swaps for teaching |
| Agent curriculum | `AGENTS.md` + `docs/agent-loop.md` | Structured learning for coding agents |
| Safe extensions | `extensions/`, `presets/` | Build without forking vendor casually |
| Full mini model (optional) | `make vendor && make pull && make demo-native` | Needs git-lfs + ~3GB artifacts |

## C. What this is **not**

| Not a capability | Why |
|------------------|-----|
| Your live X For You | No live graph, no production weights |
| Guaranteed virality coach | Mechanism literacy ≠ growth hacks |
| Official X/xAI product | Community studio on public code |
| Full production stack one-click | Thunder/Home Mixer scale infra not shipped as SaaS |

## D. One-sentence capability pitch

> Learn how public For You-style ranking **retrieves**, **scores multi-actions**, and
> **penalizes negatives** — then run demos, explain ranks, and extend the studio.
