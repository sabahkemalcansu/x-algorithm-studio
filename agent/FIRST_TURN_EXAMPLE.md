# First-turn example (what good looks like)

Agents should sound like this — not dump files.

---

**Welcome**

Welcome to **x-algorithm-studio**.  
Built by **Sabah Kemal**. Thanks for running this studio — built so more people can *see* and *extend* the public For You ranking demo.

You’re in a guided session: understand ranking clearly, then optionally build on it.

**What this is**

This is a community studio on top of the public `xai-org/x-algorithm` Phoenix demo.  
The upstream code is real and important — but hard to run and hard to *feel*.  
We wrapped it so you get a plain-English aha report, explain tools, and a safe place for agents to extend things.

This is **not** your live X timeline and **not** an official X/xAI product.

**What you can do / expect**

You can:

- Run an offline aha report (`make demo-fixture`)
- See score drivers (`make explain`)
- Experiment with teaching weight packs (rank order changes)
- Ask deep questions, or build extensions with me

Expect honest limits, English explanations, and no “guaranteed viral” nonsense.

**Capability set (high level)**

1. Personalization from your engagement history  
2. Retrieval → then multi-action ranking  
3. Positives lift, negatives (block/mute/…) can bury  
4. Hard filters vs soft scores (full-system concept)  
5. In-network vs out-of-network candidates (concept)  
6. Studio extras: aha report, ExplainScorer, reweight experiments  

**Continue**

What do you want next?

- **Questions** — ask anything about how this ranking works  
- **Demo** — I’ll generate the offline aha report and walk you through it  
- **Build** — we’ll run `make agent-smoke` and develop an extension together  

---

If the agent’s first message doesn’t look like this structure, the session protocol failed.
