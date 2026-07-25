#!/usr/bin/env python3
"""Normalize Phoenix demo output into studio results.json schema."""

from __future__ import annotations

import argparse
import json
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STUDIO_VERSION = "0.1.0"


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def base_meta(
    duration: int,
    artifacts_dir: str | None,
    vendor: str | None,
    note: str | None = None,
) -> dict[str, Any]:
    upstream = "unknown"
    if vendor:
        head = Path(vendor) / ".git"
        # try rev-parse via reading HEAD if plain
        try:
            import subprocess

            upstream = (
                subprocess.check_output(
                    ["git", "-C", vendor, "rev-parse", "--short", "HEAD"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()
                or "unknown"
            )
        except Exception:
            upstream = "unknown"

    art_sha = None
    if artifacts_dir:
        marker = Path(artifacts_dir) / ".studio_ready"
        art_sha = sha256_file(marker) if marker.exists() else None

    meta: dict[str, Any] = {
        "studio_version": STUDIO_VERSION,
        "upstream_commit": upstream,
        "artifact_sha": art_sha or "n/a",
        "duration_s": duration,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "live",
    }
    if note:
        meta["note"] = note
    return meta


def default_user() -> dict[str, Any]:
    return {
        "id": "sample_sports_fan",
        "label": "Sample sports fan (upstream example sequence)",
        "history": [
            {
                "hint": "NFL",
                "post_id": "example_nfl",
                "actions": ["favorite", "dwell"],
            },
            {
                "hint": "NBA",
                "post_id": "example_nba",
                "actions": ["favorite"],
            },
            {
                "hint": "NHL",
                "post_id": "example_nhl",
                "actions": ["dwell", "video_view"],
            },
        ],
    }


def parse_log(log_text: str) -> list[dict[str, Any]]:
    """
    Best-effort parse of run_pipeline stdout.
    Upstream format may vary; we accept several loose patterns.
    """
    items: list[dict[str, Any]] = []
    # Patterns like: rank 1 post_id=123 scores favorite=0.12 ...
    line_re = re.compile(
        r"(?:^|\s)(?:#|rank[=:\s]+)?(\d{1,3})[)\].:\s]+"
        r".*?(?:post[_ ]?id[=:\s]+)?(\d{6,})",
        re.I,
    )
    prob_re = re.compile(
        r"(favorite|like|reply|repost|dwell|block|mute|click|video[_\s]?view)"
        r"\s*[=:]\s*([0-9]*\.?[0-9]+)",
        re.I,
    )
    final_re = re.compile(r"(?:final|score)\s*[=:]\s*([0-9]*\.?[0-9]+)", re.I)

    for line in log_text.splitlines():
        m = line_re.search(line)
        if not m:
            continue
        rank = int(m.group(1))
        post_id = m.group(2)
        scores: dict[str, float] = {}
        for pm in prob_re.finditer(line):
            key = pm.group(1).lower().replace(" ", "_").replace("like", "favorite")
            scores[key] = float(pm.group(2))
        final = None
        fm = final_re.search(line)
        if fm:
            final = float(fm.group(1))
        elif scores:
            # crude weighted demo fallback
            pos = scores.get("favorite", 0) * 2.0 + scores.get("dwell", 0) * 1.5
            neg = scores.get("block", 0) * 3.0
            final = round(pos - neg, 4)
        items.append(
            {
                "rank": rank,
                "post_id": str(post_id),
                "author_id": "unknown",
                "source": "retrieval",
                "scores": scores,
                "final": final if final is not None else 0.0,
                "hint": None,
            }
        )

    # de-dupe by rank
    by_rank: dict[int, dict[str, Any]] = {}
    for it in items:
        by_rank[it["rank"]] = it
    return [by_rank[k] for k in sorted(by_rank)]


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=["parse-log", "fixture"], required=True)
    p.add_argument("--log", type=Path, default=None)
    p.add_argument("--fixture", type=Path, default=None)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--duration", type=int, default=0)
    p.add_argument("--artifacts-dir", default=None)
    p.add_argument("--vendor", default=None)
    p.add_argument("--note", default=None)
    args = p.parse_args()

    if args.mode == "fixture":
        assert args.fixture, "--fixture required"
        data = load_fixture(args.fixture)
        data.setdefault("run_meta", {})
        data["run_meta"].update(
            base_meta(args.duration, args.artifacts_dir, args.vendor, args.note)
        )
        data["run_meta"]["mode"] = "fixture"
    else:
        assert args.log, "--log required"
        log_text = args.log.read_text(encoding="utf-8", errors="replace")
        items = parse_log(log_text)
        if not items:
            # keep structure so renderer still works if user substitutes fixture
            raise SystemExit(
                "Could not parse ranked items from pipeline log. "
                "Use make demo-fixture or improve parse_log for your upstream version."
            )
        data = {
            "run_meta": base_meta(
                args.duration, args.artifacts_dir, args.vendor, args.note
            ),
            "user": default_user(),
            "corpus": {
                "name": "sports_corpus (upstream demo)",
                "size": 537000,
                "note": "Public mini Phoenix sports demo corpus",
            },
            "pipeline": {
                "retrieved_k": 200,
                "ranked_k": len(items),
                "stages": [
                    "history",
                    "retrieval",
                    "ranking",
                    "report",
                ],
            },
            "items": items,
            "weights_note": "Final scores as reported/parsed from demo run; weights are illustrative when recomputed.",
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"✔ wrote {args.output}")


if __name__ == "__main__":
    main()
