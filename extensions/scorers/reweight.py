#!/usr/bin/env python3
"""Re-rank results.json with a teaching weight pack (English-only).

Does not call the neural model — applies post-hoc linear combination on
existing action probabilities for experiments / agent tasks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def score_item(scores: dict[str, float], weights: dict[str, float]) -> float:
    total = 0.0
    keys = {k.lower(): float(v) for k, v in scores.items()}
    # prefer favorite over like if both
    if "favorite" in keys and "like" in keys:
        keys.pop("like", None)
    for action, p in keys.items():
        total += weights.get(action, 0.0) * p
    return round(total, 4)


def main() -> None:
    root = project_root()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--input",
        type=Path,
        default=root / "out" / "latest" / "results.json",
    )
    ap.add_argument(
        "--weights",
        type=Path,
        required=True,
        help="JSON map of action → weight, e.g. presets/weights/anti_negative.json",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=root / "out" / "latest" / "results_reweighted.json",
    )
    args = ap.parse_args()

    data = load_json(args.input)
    weights = load_json(args.weights)
    if not isinstance(weights, dict):
        raise SystemExit("weights file must be a JSON object of action → number")

    items = list(data.get("items") or [])
    for it in items:
        scores = {k: float(v) for k, v in (it.get("scores") or {}).items()}
        it["final_before"] = it.get("final")
        it["final"] = score_item(scores, {k.lower(): float(v) for k, v in weights.items()})

    items_sorted = sorted(items, key=lambda x: float(x.get("final") or 0), reverse=True)
    for i, it in enumerate(items_sorted, 1):
        it["rank_before"] = it.get("rank")
        it["rank"] = i

    data["items"] = items_sorted
    data.setdefault("run_meta", {})
    data["run_meta"]["mode"] = "reweighted"
    data["run_meta"]["weights_file"] = str(args.weights)
    data["weights_note"] = (
        "Post-hoc teaching reweight — not neural re-inference; not production X."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print("Reweight result (top 5)")
    print("=" * 48)
    for it in items_sorted[:5]:
        print(
            f"#{it['rank']}  final={it['final']}  "
            f"(was rank {it.get('rank_before')} final {it.get('final_before')})  "
            f"post={it.get('post_id')}"
            + (f"  {it.get('hint')}" if it.get("hint") else "")
        )
    print(f"✔ wrote {args.output}")
    print("Tip: python3 scripts/render_aha_report.py --input", args.output, "--output out/latest/report_reweighted.html")


if __name__ == "__main__":
    main()
