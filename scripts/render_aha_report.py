#!/usr/bin/env python3
"""Render plain-language AHA HTML report from results.json (English only)."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def esc(s: Any) -> str:
    return html.escape("" if s is None else str(s))


def bar(val: float, kind: str = "mid") -> str:
    pct = max(0.0, min(1.0, float(val))) * 100
    color = {"good": "#15803d", "bad": "#b91c1c", "mid": "#1d4ed8"}.get(kind, "#1d4ed8")
    return (
        f'<div class="bar-wrap"><div class="track"><i style="width:{pct:.0f}%;background:{color}"></i></div>'
        f'<span class="pct">{val:.2f}</span></div>'
    )


def pick_scores(item: dict[str, Any]) -> tuple[float, float, float]:
    s = item.get("scores") or {}
    fav = float(s.get("favorite", s.get("like", 0)) or 0)
    dwell = float(s.get("dwell", 0) or 0)
    block = float(s.get("block", 0) or 0)
    return fav, dwell, block


def render(data: dict[str, Any]) -> str:
    meta = data.get("run_meta") or {}
    user = data.get("user") or {}
    corpus = data.get("corpus") or {}
    pipe = data.get("pipeline") or {}
    items: list[dict[str, Any]] = data.get("items") or []

    title = "How For You ranks — 2-minute brief"
    lead = (
        "This report is produced after running the public Phoenix demo from x-algorithm. "
        "Goal: understand <strong>why some posts surface</strong> — not memorize formulas."
    )
    one_liner = (
        "It recalls what you engaged with, retrieves similar candidates, predicts what you’ll do next, "
        "turns those predictions into a score, and sorts."
    )

    steps = [
        ("Remembers you", "Your past likes, dwells, video views, …"),
        ("Retrieves candidates", "Pulls nearby items from a large pool (demo: sports corpus)."),
        ("Scores", "Will you like? Dwell? Block? …"),
        ("Ranks", "Positives push up; negatives push down."),
    ]

    top = items[0] if items else None
    low = None
    if len(items) >= 8:
        low = items[7]
    elif len(items) >= 2:
        low = items[-1]

    def item_card(it: dict[str, Any] | None, heading: str, good: bool) -> str:
        if not it:
            return f'<div class="tweet"><div class="who">{esc(heading)}</div><p>—</p></div>'
        fav, dwell, block = pick_scores(it)
        hint = it.get("hint") or ""
        border = "#1d4ed8" if good else "#b91c1c"
        bg = "#eef2ff" if good else "#fef2f2"
        return f"""
        <div class="tweet" style="border-left-color:{border};background:{bg}">
          <div class="who">{esc(heading)}</div>
          <div class="meta">rank {esc(it.get('rank'))} · post {esc(it.get('post_id'))} · final {esc(it.get('final'))}
          {f' · {esc(hint)}' if hint else ''}</div>
          <div class="bars">
            <div class="row"><span>Favorite</span>{bar(fav, "good")}</div>
            <div class="row"><span>Dwell</span>{bar(dwell, "good")}</div>
            <div class="row"><span>Block</span>{bar(block, "bad")}</div>
          </div>
        </div>
        """

    rows = []
    for it in items[:15]:
        fav, dwell, block = pick_scores(it)
        rows.append(
            f"""<tr>
            <td class="rank">{esc(it.get('rank'))}</td>
            <td><div class="mono">{esc(it.get('post_id'))}</div>
                <div class="muted mono">{esc(it.get('author_id'))}</div></td>
            <td>{esc(it.get('source', 'retrieval'))}</td>
            <td>{bar(fav)}</td>
            <td>{bar(dwell, 'good')}</td>
            <td>{bar(block, 'bad')}</td>
            <td class="final">{esc(it.get('final'))}</td>
            </tr>"""
        )

    hist_html = ""
    for h in user.get("history") or []:
        acts = ", ".join(h.get("actions") or [])
        hist_html += f"""<div class="hist">
          <span class="tag">{esc(h.get('hint') or 'post')}</span>
          <span class="mono">{esc(h.get('post_id'))}</span>
          <span class="chip">{esc(acts)}</span>
        </div>"""

    takeaways = [
        "The feed is not “most likes win”; it’s predicted for you from history.",
        "First retrieve candidates, then multi-action rank.",
        "Positive actions lift; negatives (block/mute) bury.",
        "“Going viral” isn’t magic here — high positive / low negative predictions (demo-scale reading).",
    ]

    disc = (
        "Honest note: this is the <strong>public demo mechanism</strong>. Not your live X timeline or production weights. "
        "It still teaches the right mental model for why posts surface."
    )

    steps_html = "".join(
        f'<div class="step"><div class="n">{i}</div><div><b>{esc(t)}</b><span>{esc(d)}</span></div></div>'
        for i, (t, d) in enumerate(steps, 1)
    )
    take_html = "".join(f"<li>{esc(t)}</li>" for t in takeaways)

    mode = esc(meta.get("mode", "unknown"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>
    :root {{ --bg:#f6f4ef; --ink:#1a1a1a; --muted:#5c5c5c; --line:#e6e2d8; --card:#fff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: Georgia, "Iowan Old Style", serif; background:var(--bg); color:var(--ink); line-height:1.55; }}
    .wrap {{ max-width:820px; margin:0 auto; padding:32px 20px 72px; }}
    h1 {{ font-size:28px; line-height:1.2; margin:0 0 8px; }}
    .lead {{ color:var(--muted); font-size:17px; margin:0 0 22px; }}
    h2 {{ font-family: system-ui,sans-serif; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin:28px 0 12px; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 18px; margin-bottom:12px; }}
    .big {{ font-size:20px; font-weight:700; margin:0 0 8px; }}
    .meta-pills {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 20px; font-family:system-ui,sans-serif; font-size:12px; }}
    .pill {{ background:#fff; border:1px solid var(--line); border-radius:999px; padding:5px 10px; color:var(--muted); }}
    .pill b {{ color:var(--ink); }}
    .steps {{ display:grid; gap:10px; font-family:system-ui,sans-serif; }}
    .step {{ display:grid; grid-template-columns:36px 1fr; gap:12px; padding:12px; border:1px solid var(--line); border-radius:12px; background:#fafaf8; }}
    .n {{ width:36px; height:36px; border-radius:50%; background:#111; color:#fff; display:grid; place-items:center; font-weight:800; }}
    .step b {{ display:block; }}
    .step span {{ color:var(--muted); font-size:14px; }}
    .formula {{ font-family: ui-monospace, Menlo, monospace; background:#111; color:#e7e7e7; padding:14px; border-radius:12px; font-size:13px; }}
    .pos {{ color:#86efac; }} .neg {{ color:#fca5a5; }}
    .tweet {{ border-left:4px solid #1d4ed8; padding:12px 14px; border-radius:0 12px 12px 0; margin:10px 0; font-family:system-ui,sans-serif; }}
    .who {{ font-weight:700; }} .meta {{ color:var(--muted); font-size:12px; margin:4px 0 8px; }}
    .bars {{ display:grid; gap:8px; }}
    .row {{ display:grid; grid-template-columns:100px 1fr; gap:10px; align-items:center; font-size:13px; }}
    .bar-wrap {{ display:flex; gap:8px; align-items:center; }}
    .track {{ flex:1; height:10px; background:#e5e7eb; border-radius:99px; overflow:hidden; }}
    .track i {{ display:block; height:100%; }}
    .pct {{ width:42px; text-align:right; font-variant-numeric: tabular-nums; }}
    .takeaway {{ background:#ecfdf5; border:1px solid #86efac; border-radius:14px; padding:16px; font-family:system-ui,sans-serif; }}
    .takeaway ul {{ margin:8px 0 0; padding-left:18px; color:#14532d; }}
    .hist {{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; padding:8px 0; border-bottom:1px solid var(--line); font-family:system-ui,sans-serif; font-size:13px; }}
    .tag {{ background:#eef2ff; color:#1d4ed8; border-radius:6px; padding:2px 8px; font-weight:700; font-size:11px; }}
    .chip {{ background:#ecfdf5; color:#15803d; border-radius:999px; padding:2px 8px; font-size:11px; }}
    .mono {{ font-family: ui-monospace, Menlo, monospace; font-size:12px; }}
    .muted {{ color:var(--muted); }}
    table {{ width:100%; border-collapse:collapse; font-family:system-ui,sans-serif; font-size:13px; }}
    th {{ text-align:left; color:var(--muted); font-size:11px; text-transform:uppercase; padding:8px; border-bottom:1px solid var(--line); }}
    td {{ padding:10px 8px; border-bottom:1px solid #eee; vertical-align:middle; }}
    .rank {{ font-weight:800; color:var(--muted); }}
    .final {{ font-weight:700; }}
    details {{ margin-top:12px; font-family:system-ui,sans-serif; }}
    summary {{ cursor:pointer; font-weight:600; }}
    footer {{ margin-top:28px; font-family:system-ui,sans-serif; font-size:12px; color:var(--muted); }}
    .disc {{ font-family:system-ui,sans-serif; font-size:13px; color:var(--muted); margin-top:10px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{esc(title)}</h1>
    <p class="lead">{lead}</p>
    <div class="meta-pills">
      <div class="pill">mode: <b>{mode}</b></div>
      <div class="pill">upstream: <b>{esc(meta.get('upstream_commit'))}</b></div>
      <div class="pill">duration: <b>{esc(meta.get('duration_s'))}s</b></div>
      <div class="pill">studio: <b>{esc(meta.get('studio_version'))}</b></div>
    </div>

    <h2>1 · One sentence</h2>
    <div class="card"><p class="big">{esc(one_liner)}</p></div>

    <h2>2 · Demo user</h2>
    <div class="card">
      <p><strong>{esc(user.get('label') or user.get('id'))}</strong></p>
      {hist_html or '<p class="muted">—</p>'}
      <p class="muted" style="margin-top:10px;font-family:system-ui,sans-serif;font-size:13px;">
        corpus: {esc(corpus.get('name'))} · size≈{esc(corpus.get('size'))} ·
        retrieved {esc(pipe.get('retrieved_k'))} → shown {esc(pipe.get('ranked_k') or len(items))}
      </p>
    </div>

    <h2>3 · 4 steps</h2>
    <div class="steps">{steps_html}</div>

    <h2>4 · Scoring</h2>
    <div class="card">
      <div class="formula">Final ≈ <span class="pos">+ w·P(like) + w·P(dwell) + …</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="neg">− w·P(block) − w·P(mute) − …</span></div>
      <p class="disc">Aha: likes alone aren’t enough; negatives can bury a post.</p>
    </div>

    <h2>5 · Concrete example</h2>
    <div class="card">
      {item_card(top, "#1 — why on top?", True)}
      {item_card(low, "Lower rank — why behind?", False)}
    </div>

    <h2>6 · Takeaways</h2>
    <div class="takeaway">
      <ul>{take_html}</ul>
    </div>
    <p class="disc">{disc}</p>

    <details>
      <summary>Technical table (details)</summary>
      <div class="card" style="margin-top:12px;overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>#</th><th>post / author</th><th>src</th>
              <th>fav</th><th>dwell</th><th>block</th><th>final</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows) if rows else '<tr><td colspan="7">No items</td></tr>'}
          </tbody>
        </table>
      </div>
    </details>

    <footer>
      x-algorithm-studio · built on public xai-org/x-algorithm · not affiliated with X/xAI · not a live timeline
    </footer>
  </div>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    html_out = render(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_out, encoding="utf-8")
    print(f"✔ wrote {args.output}")


if __name__ == "__main__":
    main()
