#!/usr/bin/env python3
"""Render plain-language AHA HTML report from results.json (English only).

Visual language inspired by X (dark UI, feed cards, blue accent) — not an
official X product skin.
"""

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
    # X-adjacent palette: sky blue, green, rose
    color = {
        "good": "#00ba7c",
        "bad": "#f4212e",
        "mid": "#1d9bf0",
    }.get(kind, "#1d9bf0")
    return (
        f'<div class="bar-wrap">'
        f'<div class="track"><i style="width:{pct:.0f}%;background:{color}"></i></div>'
        f'<span class="pct">{val:.2f}</span></div>'
    )


def pick_scores(item: dict[str, Any]) -> tuple[float, float, float]:
    s = item.get("scores") or {}
    fav = float(s.get("favorite", s.get("like", 0)) or 0)
    dwell = float(s.get("dwell", 0) or 0)
    block = float(s.get("block", 0) or 0)
    return fav, dwell, block


def avatar_letter(label: str) -> str:
    for ch in label or "U":
        if ch.isalnum():
            return ch.upper()
    return "U"


def render(data: dict[str, Any]) -> str:
    meta = data.get("run_meta") or {}
    user = data.get("user") or {}
    corpus = data.get("corpus") or {}
    pipe = data.get("pipeline") or {}
    items: list[dict[str, Any]] = data.get("items") or []

    user_label = user.get("label") or user.get("id") or "Demo user"
    user_id = user.get("id") or "demo_user"
    handle = f"@{user_id}" if not str(user_id).startswith("@") else str(user_id)

    title = "How For You ranks"
    subtitle = "2-minute brief · public Phoenix demo"

    one_liner = (
        "It recalls what you engaged with, retrieves similar candidates, predicts what you’ll do next, "
        "turns those predictions into a score, and sorts."
    )

    steps = [
        ("1", "Remembers you", "Past likes, dwells, video views…"),
        ("2", "Retrieves", "Pulls fit candidates from a large pool."),
        ("3", "Scores", "P(like), P(dwell), P(block)… multi-action."),
        ("4", "Ranks", "Positives lift · negatives bury."),
    ]

    top = items[0] if items else None
    low = None
    if len(items) >= 8:
        low = items[7]
    elif len(items) >= 2:
        low = items[-1]

    def post_card(it: dict[str, Any] | None, badge: str, tone: str) -> str:
        if not it:
            return '<div class="post-card empty"><p class="muted">No item</p></div>'
        fav, dwell, block = pick_scores(it)
        hint = it.get("hint") or "Candidate post"
        rank = it.get("rank")
        pid = it.get("post_id")
        aid = it.get("author_id")
        final = it.get("final")
        tone_class = "up" if tone == "up" else "down"
        letter = avatar_letter(str(aid or "A"))
        return f"""
        <article class="post-card {tone_class}">
          <div class="post-head">
            <div class="avatar sm">{esc(letter)}</div>
            <div class="post-meta">
              <div class="name-row">
                <span class="display">author_{esc(aid)}</span>
                <span class="badge {tone_class}">{esc(badge)}</span>
              </div>
              <div class="sub">rank #{esc(rank)} · final <strong>{esc(final)}</strong> · {esc(pid)}</div>
            </div>
          </div>
          <p class="post-body">{esc(hint)}</p>
          <div class="metrics">
            <div class="metric">
              <span class="m-label">Favorite</span>
              {bar(fav, "good")}
            </div>
            <div class="metric">
              <span class="m-label">Dwell</span>
              {bar(dwell, "good")}
            </div>
            <div class="metric">
              <span class="m-label">Block</span>
              {bar(block, "bad")}
            </div>
          </div>
        </article>
        """

    # Feed list rows
    feed_rows = []
    for it in items[:12]:
        fav, dwell, block = pick_scores(it)
        hint = it.get("hint") or "—"
        letter = avatar_letter(str(it.get("author_id") or "P"))
        feed_rows.append(
            f"""
            <article class="feed-item">
              <div class="rank-pill">#{esc(it.get('rank'))}</div>
              <div class="avatar sm">{esc(letter)}</div>
              <div class="feed-body">
                <div class="name-row">
                  <span class="display">author_{esc(it.get('author_id'))}</span>
                  <span class="muted mono"> · {esc(it.get('post_id'))}</span>
                </div>
                <p class="post-body tight">{esc(hint)}</p>
                <div class="stat-row">
                  <span class="stat good">♥ {fav:.2f}</span>
                  <span class="stat mid">◎ {dwell:.2f}</span>
                  <span class="stat bad">⊘ {block:.2f}</span>
                  <span class="stat final">score {esc(it.get('final'))}</span>
                </div>
              </div>
            </article>
            """
        )

    hist_html = ""
    for h in user.get("history") or []:
        acts = " · ".join(h.get("actions") or [])
        hist_html += f"""
        <div class="chip-row">
          <span class="tag">{esc(h.get('hint') or 'post')}</span>
          <span class="mono muted">{esc(h.get('post_id'))}</span>
          <span class="actions">{esc(acts)}</span>
        </div>
        """

    takeaways = [
        "The feed is not “most likes win” — it’s predicted for you from history.",
        "First retrieve candidates, then multi-action rank.",
        "Positive actions lift; negatives (block / mute) bury.",
        "“Going viral” isn’t magic here — high positive / low negative (demo-scale).",
    ]
    take_html = "".join(f"<li>{esc(t)}</li>" for t in takeaways)

    steps_html = "".join(
        f"""
        <div class="step">
          <div class="step-num">{esc(n)}</div>
          <div>
            <div class="step-title">{esc(t)}</div>
            <div class="step-desc">{esc(d)}</div>
          </div>
        </div>
        """
        for n, t, d in steps
    )

    mode = esc(meta.get("mode", "unknown"))
    letter = avatar_letter(str(user_label))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)} · x-algorithm-studio</title>
  <style>
    :root {{
      --bg: #000000;
      --bg-elev: #0a0a0a;
      --panel: #16181c;
      --panel-hover: #1e2026;
      --border: #2f3336;
      --border-soft: #1e2026;
      --text: #e7e9ea;
      --muted: #71767b;
      --blue: #1d9bf0;
      --blue-dim: rgba(29, 155, 240, 0.12);
      --green: #00ba7c;
      --red: #f4212e;
      --amber: #ffd400;
      --radius: 16px;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}

    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .shell {{
      max-width: 600px;
      margin: 0 auto;
      min-height: 100vh;
      border-left: 1px solid var(--border);
      border-right: 1px solid var(--border);
      background: var(--bg);
    }}

    /* Top bar — X-like sticky header */
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 20;
      backdrop-filter: blur(12px);
      background: rgba(0,0,0,0.75);
      border-bottom: 1px solid var(--border);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 18px;
      letter-spacing: -0.02em;
    }}
    .brand-mark {{
      width: 32px;
      height: 32px;
      border-radius: 999px;
      background: radial-gradient(circle at 30% 30%, #8ecdf8, var(--blue) 55%, #0c4a6e);
      display: grid;
      place-items: center;
      font-size: 14px;
      font-weight: 900;
      color: #fff;
    }}
    .pill-meta {{
      font-size: 12px;
      color: var(--muted);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 6px 10px;
      white-space: nowrap;
    }}
    .pill-meta b {{ color: var(--text); font-weight: 600; }}

    .hero {{
      padding: 20px 16px 8px;
      border-bottom: 1px solid var(--border);
    }}
    .eyebrow {{
      color: var(--blue);
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 28px;
      line-height: 1.15;
      letter-spacing: -0.03em;
      font-weight: 800;
    }}
    .lede {{
      margin: 0;
      color: var(--muted);
      font-size: 15px;
    }}

    .section {{
      padding: 16px;
      border-bottom: 1px solid var(--border);
    }}
    .section-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin: 0 0 12px;
    }}

    /* Profile card */
    .profile {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }}
    .avatar {{
      width: 52px;
      height: 52px;
      border-radius: 999px;
      background: linear-gradient(145deg, #1d9bf0, #7856ff);
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: 20px;
      flex-shrink: 0;
      color: #fff;
    }}
    .avatar.sm {{
      width: 40px;
      height: 40px;
      font-size: 15px;
    }}
    .profile h2 {{
      margin: 0;
      font-size: 17px;
      font-weight: 800;
    }}
    .handle {{ color: var(--muted); font-size: 14px; margin-top: 2px; }}
    .bio {{ margin: 10px 0 0; color: var(--text); font-size: 15px; }}

    .chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid var(--border-soft);
      font-size: 13px;
    }}
    .chip-row:last-child {{ border-bottom: 0; }}
    .tag {{
      background: var(--blue-dim);
      color: var(--blue);
      font-weight: 700;
      font-size: 12px;
      padding: 3px 10px;
      border-radius: 999px;
    }}
    .actions {{ color: var(--green); font-size: 12px; }}
    .mono {{ font-family: var(--mono); font-size: 12px; }}
    .muted {{ color: var(--muted); }}

    /* One-liner callout */
    .callout {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px;
      font-size: 16px;
      font-weight: 600;
      letter-spacing: -0.01em;
      line-height: 1.4;
    }}

    /* Pipeline steps */
    .steps {{
      display: grid;
      gap: 10px;
    }}
    .step {{
      display: grid;
      grid-template-columns: 36px 1fr;
      gap: 12px;
      align-items: start;
      padding: 12px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: var(--bg-elev);
    }}
    .step-num {{
      width: 36px;
      height: 36px;
      border-radius: 999px;
      background: var(--blue-dim);
      color: var(--blue);
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: 14px;
    }}
    .step-title {{ font-weight: 700; font-size: 15px; }}
    .step-desc {{ color: var(--muted); font-size: 13px; margin-top: 2px; }}

    /* Formula */
    .formula {{
      font-family: var(--mono);
      font-size: 13px;
      background: #0a0a0a;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px 16px;
      line-height: 1.6;
      overflow-x: auto;
    }}
    .pos {{ color: var(--green); }}
    .neg {{ color: #ff7a82; }}
    .hint {{
      margin: 10px 0 0;
      font-size: 13px;
      color: var(--muted);
    }}

    /* Post cards */
    .post-card {{
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px;
      background: var(--panel);
      margin-bottom: 12px;
    }}
    .post-card.up {{ box-shadow: inset 3px 0 0 var(--green); }}
    .post-card.down {{ box-shadow: inset 3px 0 0 var(--red); }}
    .post-head {{ display: flex; gap: 10px; }}
    .post-meta {{ flex: 1; min-width: 0; }}
    .name-row {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
    .display {{ font-weight: 700; font-size: 15px; }}
    .badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
    }}
    .badge.up {{ background: rgba(0,186,124,.15); color: var(--green); }}
    .badge.down {{ background: rgba(244,33,46,.15); color: #ff7a82; }}
    .sub {{ color: var(--muted); font-size: 12px; margin-top: 2px; word-break: break-all; }}
    .post-body {{
      margin: 10px 0 0;
      font-size: 15px;
      line-height: 1.45;
    }}
    .post-body.tight {{ margin-top: 4px; font-size: 14px; color: var(--text); }}

    .metrics {{ margin-top: 12px; display: grid; gap: 8px; }}
    .metric {{
      display: grid;
      grid-template-columns: 72px 1fr;
      gap: 8px;
      align-items: center;
      font-size: 12px;
    }}
    .m-label {{ color: var(--muted); font-weight: 600; }}
    .bar-wrap {{ display: flex; gap: 8px; align-items: center; }}
    .track {{
      flex: 1;
      height: 6px;
      border-radius: 99px;
      background: #2f3336;
      overflow: hidden;
    }}
    .track i {{ display: block; height: 100%; border-radius: 99px; }}
    .pct {{
      width: 40px;
      text-align: right;
      font-variant-numeric: tabular-nums;
      color: var(--text);
      font-size: 12px;
      font-weight: 600;
    }}

    /* Feed list */
    .feed-item {{
      display: grid;
      grid-template-columns: 36px 40px 1fr;
      gap: 10px;
      padding: 14px 0;
      border-bottom: 1px solid var(--border);
    }}
    .feed-item:last-child {{ border-bottom: 0; }}
    .feed-item:hover {{ background: rgba(255,255,255,0.02); margin: 0 -16px; padding-left: 16px; padding-right: 16px; }}
    .rank-pill {{
      width: 36px;
      height: 28px;
      border-radius: 999px;
      background: var(--panel);
      border: 1px solid var(--border);
      display: grid;
      place-items: center;
      font-size: 11px;
      font-weight: 800;
      color: var(--muted);
      margin-top: 6px;
    }}
    .stat-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 8px;
      font-size: 12px;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
    }}
    .stat.good {{ color: var(--green); }}
    .stat.mid {{ color: var(--blue); }}
    .stat.bad {{ color: #ff7a82; }}
    .stat.final {{ color: var(--text); margin-left: auto; }}

    /* Takeaways */
    .takeaways {{
      background: linear-gradient(180deg, rgba(29,155,240,0.08), transparent);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px 14px 12px;
    }}
    .takeaways ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--text);
      font-size: 14px;
    }}
    .takeaways li {{ margin: 8px 0; }}

    .disclaimer {{
      font-size: 13px;
      color: var(--muted);
      margin: 12px 0 0;
      line-height: 1.45;
    }}

    details.tech {{
      margin-top: 4px;
    }}
    details.tech summary {{
      cursor: pointer;
      color: var(--blue);
      font-weight: 700;
      font-size: 14px;
      padding: 8px 0;
      list-style: none;
    }}
    details.tech summary::-webkit-details-marker {{ display: none; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 8px;
    }}
    th {{
      text-align: left;
      color: var(--muted);
      font-weight: 600;
      padding: 8px 6px;
      border-bottom: 1px solid var(--border);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.04em;
    }}
    td {{
      padding: 10px 6px;
      border-bottom: 1px solid var(--border-soft);
      vertical-align: middle;
      font-variant-numeric: tabular-nums;
    }}

    footer {{
      padding: 20px 16px 40px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    footer .dot {{ margin: 0 6px; opacity: 0.5; }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-top: 14px;
    }}
    .stat-box {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 10px;
      text-align: center;
    }}
    .stat-box .k {{ color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
    .stat-box .v {{ font-size: 16px; font-weight: 800; margin-top: 4px; letter-spacing: -0.02em; }}

    @media (max-width: 640px) {{
      .shell {{ border: 0; }}
      h1 {{ font-size: 24px; }}
      .stats-grid {{ grid-template-columns: 1fr 1fr 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark">𝕏</div>
        <span>For You lab</span>
      </div>
      <div class="pill-meta">mode <b>{mode}</b></div>
    </header>

    <div class="hero">
      <div class="eyebrow">x-algorithm-studio</div>
      <h1>{esc(title)}</h1>
      <p class="lede">{esc(subtitle)}</p>
      <div class="stats-grid">
        <div class="stat-box">
          <div class="k">Corpus</div>
          <div class="v">~{esc(corpus.get('size') or '—')}</div>
        </div>
        <div class="stat-box">
          <div class="k">Retrieved</div>
          <div class="v">{esc(pipe.get('retrieved_k') or '—')}</div>
        </div>
        <div class="stat-box">
          <div class="k">Shown</div>
          <div class="v">{esc(pipe.get('ranked_k') or len(items))}</div>
        </div>
      </div>
    </div>

    <section class="section">
      <h3 class="section-title">Demo viewer</h3>
      <div class="profile">
        <div class="avatar">{esc(letter)}</div>
        <div>
          <h2>{esc(user_label)}</h2>
          <div class="handle">{esc(handle)}</div>
          <p class="bio">Sample engagement history used for this ranking run.</p>
        </div>
      </div>
      <div style="margin-top:12px">{hist_html or '<p class="muted">No history</p>'}</div>
    </section>

    <section class="section">
      <h3 class="section-title">One sentence</h3>
      <div class="callout">{esc(one_liner)}</div>
    </section>

    <section class="section">
      <h3 class="section-title">How it works</h3>
      <div class="steps">{steps_html}</div>
    </section>

    <section class="section">
      <h3 class="section-title">Scoring</h3>
      <div class="formula">
        Final ≈ <span class="pos">+ w·P(like) + w·P(dwell) + …</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="neg">− w·P(block) − w·P(mute) − …</span>
      </div>
      <p class="hint">Aha: likes alone aren’t enough — negatives can bury a post.</p>
    </section>

    <section class="section">
      <h3 class="section-title">Why this order?</h3>
      {post_card(top, "On top", "up")}
      {post_card(low, "Lower", "down")}
    </section>

    <section class="section">
      <h3 class="section-title">Ranked feed</h3>
      {''.join(feed_rows) if feed_rows else '<p class="muted">No items</p>'}
    </section>

    <section class="section">
      <h3 class="section-title">Takeaways</h3>
      <div class="takeaways">
        <ul>{take_html}</ul>
      </div>
      <p class="disclaimer">
        Honest note: this is the <strong style="color:var(--text)">public demo mechanism</strong>,
        not your live X timeline or production weights. It still teaches the right mental model
        for why posts surface.
      </p>
      <div style="margin-top:14px;font-size:12px;color:var(--muted)">
        upstream <b style="color:var(--text)">{esc(meta.get('upstream_commit'))}</b>
        · studio <b style="color:var(--text)">{esc(meta.get('studio_version'))}</b>
        · {esc(meta.get('duration_s'))}s
      </div>
    </section>

    <section class="section">
      <details class="tech">
        <summary>Technical table</summary>
        <table>
          <thead>
            <tr>
              <th>#</th><th>post / author</th><th>src</th>
              <th>fav</th><th>dwell</th><th>block</th><th>final</th>
            </tr>
          </thead>
          <tbody>
            {''.join(
              f'''<tr>
                <td>{esc(it.get("rank"))}</td>
                <td class="mono">{esc(it.get("post_id"))}<br/><span class="muted">{esc(it.get("author_id"))}</span></td>
                <td>{esc(it.get("source", "retrieval"))}</td>
                <td>{pick_scores(it)[0]:.2f}</td>
                <td>{pick_scores(it)[1]:.2f}</td>
                <td>{pick_scores(it)[2]:.2f}</td>
                <td><strong>{esc(it.get("final"))}</strong></td>
              </tr>'''
              for it in items[:20]
            ) if items else '<tr><td colspan="7">No items</td></tr>'}
          </tbody>
        </table>
      </details>
    </section>

    <footer>
      x-algorithm-studio
      <span class="dot">·</span>
      built on public xai-org/x-algorithm
      <span class="dot">·</span>
      not affiliated with X/xAI
      <span class="dot">·</span>
      not a live timeline
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
