# Pitfalls (agents & humans)

## Do not say

- “This *is* your X For You right now.”  
- “We have production weights.”  
- “Do X spam pattern to go viral for sure.”  
- “Upstream accepts our PR” (xAI repos are contribution-closed).

## Do say

- “Public mini Phoenix demo / mechanism.”  
- “Illustrative scores in fixture mode.”  
- “Negatives can dominate positives.”  
- “Filters are hard rules; scores are soft ranking.”

## Common confusions

| Confusion | Correction |
|-----------|------------|
| Ranking = retrieval | Retrieval finds candidates; ranking orders a smaller set |
| One engagement score | Multi-action probabilities + weights |
| More likes always win | Not if block/mute risk is high for that user |
| Studio replaces x-algorithm | Studio **runs & teaches** the public surface |

## Fixture vs live

- `make demo-fixture` → teaching numbers, always works  
- `make demo-native` → real mini model when artifacts resolve  
