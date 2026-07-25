#!/usr/bin/env python3
"""ExplainScorer — teaching breakdown of multi-action scores.

Uses *illustrative* weights (not production X weights) to show which signals
drive each ranked item. English-only output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


# Illustrative teaching weights only — label them as such in all output.
DEFAULT_WEIGHTS: dict[str, float] = {
    "favorite": 2.0,
    "like": 2.0,
    "reply": 1.2,
    "repost": 1.5,
    "dwell": 1.5,
    "click": 1.0,
    "video_view": 1.0,
    "share": 1.3,
    "block": -3.0,
    "mute": -2.5,
    "not_interested": -2.0,
    "report": -3.5,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_results(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def contributions(
    scores: dict[str, float], weights: dict[str, float]
) -> list[tuple[str, float, float, float]]:
    """Return list of (action, prob, weight, contrib) sorted by |contrib| desc."""
    rows: list[tuple[str, float, float, float]] = []
    seen_like = False
    for action, prob in scores.items():
        key = action.lower()
        # avoid double-counting like/favorite if both present
        if key == "like" and "favorite" in {k.lower() for k in scores}:
            continue
        w = weights.get(key, 0.0)
        if w == 0.0:
            continue
        p = float(prob)
        rows.append((key, p, w, p * w))
    rows.sort(key=lambda r: abs(r[3]), reverse=True)
    return rows


def explain_item(item: dict[str, Any], weights: dict[str, float], top_k: int = 3) -> dict[str, Any]:
    scores = {k: float(v) for k, v in (item.get("scores") or {}).items()}
    parts = contributions(scores, weights)
    top = parts[:top_k]
    recon = sum(c for *_, c in parts)
    return {
        "rank": item.get("rank"),
        "post_id": item.get("post_id"),
        "author_id": item.get("author_id"),
        "hint": item.get("hint"),
        "final_reported": item.get("final"),
        "final_reconstructed_teaching": round(recon, 4),
        "top_drivers": [
            {
                "action": a,
                "probability": round(p, 4),
                "weight": w,
                "contribution": round(c, 4),
                "direction": "positive" if c >= 0 else "negative",
            }
            for a, p, w, c in top
        ],
        "all_contributions": [
            {
                "action": a,
                "probability": round(p, 4),
                "weight": w,
                "contribution": round(c, 4),
            }
            for a, p, w, c in parts
        ],
    }


def format_human(ex: dict[str, Any]) -> str:
    lines = [
        f"#{ex['rank']}  post={ex['post_id']}  "
        f"reported_final={ex['final_reported']}  "
        f"teaching_recon={ex['final_reconstructed_teaching']}"
        + (f"  ({ex['hint']})" if ex.get("hint") else "")
    ]
    for d in ex["top_drivers"]:
        sign = "+" if d["contribution"] >= 0 else ""
        lines.append(
            f"    {sign}{d['contribution']:.3f}  "
            f"{d['action']}: P={d['probability']:.2f} × w={d['weight']}"
            f"  [{d['direction']}]"
        )
    return "\n".join(lines)


def main() -> None:
    root = project_root()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--input",
        type=Path,
        default=root / "out" / "latest" / "results.json",
        help="results.json path",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=root / "out" / "latest" / "explain.json",
        help="write machine-readable explain JSON",
    )
    ap.add_argument("--top-k-items", type=int, default=5, help="how many ranks to print")
    ap.add_argument("--drivers", type=int, default=3, help="drivers per item")
    args = ap.parse_args()

    if not args.input.is_file():
        raise SystemExit(
            f"Missing {args.input}. Run: make demo-fixture\n"
            "(ExplainScorer needs results.json)"
        )

    data = load_results(args.input)
    items = sorted(data.get("items") or [], key=lambda x: int(x.get("rank") or 0))
    explained = [explain_item(it, DEFAULT_WEIGHTS, top_k=args.drivers) for it in items]

    payload = {
        "meta": {
            "tool": "ExplainScorer",
            "weights": DEFAULT_WEIGHTS,
            "weights_disclaimer": (
                "Illustrative teaching weights only — not production X weights."
            ),
            "source_results": str(args.input),
            "run_mode": (data.get("run_meta") or {}).get("mode"),
        },
        "items": explained,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("ExplainScorer (teaching weights — not production X)")
    print("=" * 56)
    for ex in explained[: args.top_k_items]:
        print(format_human(ex))
        print()
    print(f"✔ wrote {args.output}")
    print("Note: reconstructed finals may differ from reported finals; both are demo-scale.")


if __name__ == "__main__":
    main()
