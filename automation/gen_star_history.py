#!/usr/bin/env python3
"""重绘 README 里的 star 增长曲线：拉取本仓库最新 stargazer 时间戳，生成累计增长曲线 SVG。

用法：python3 automation/gen_star_history.py <输出路径>
本地跑依赖已登录的 gh CLI；CI 里依赖 GH_TOKEN。取数走 GraphQL 的 starredAt——
REST 的 stargazers 端点对 Actions 自带 GITHUB_TOKEN 一律 403（连本仓库都拒），GraphQL 放行。
产物由 .github/workflows/star-history.yml 每日生成并提交到 star-data 分支，不进 main。
"""
import json
import math
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO = "MrGeDiao/shuorenhua"
OPEN_DATE = date(2026, 3, 22)  # 开源日
EVENTS = [  # 曲线上的发版标注，日期以 GitHub releases 为准
    (date(2026, 6, 18), "v1.9 · Eval Harness"),
    (date(2026, 7, 15), "v2.0 · Plugin 一键安装"),
    (date(2026, 9, 13), "v2.5 · 编辑规则重构"),
]

PANEL, BORDER = "#F7F8F5", "#D7DCE2"
INK, MUTED = "#101318", "#66707C"
GRID, BASELINE = "#E6E9ED", "#929AA5"
ACCENT, AREA = "#246BFD", "#246BFD"

X0, X1, Y0, PLOT_H = 88, 1150, 340, 210  # 绘图区
SANS = "-apple-system, 'SF Pro Text', 'PingFang SC', 'Segoe UI', 'Microsoft YaHei', sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', monospace"


def fetch_star_dates():
    owner, name = REPO.split("/")
    dates, cursor = [], None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = (
            'query { repository(owner: "%s", name: "%s") { '
            "stargazers(first: 100, orderBy: {field: STARRED_AT, direction: ASC}%s) "
            "{ edges { starredAt } pageInfo { hasNextPage endCursor } } } }"
            % (owner, name, after)
        )
        out = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            stdout=subprocess.PIPE, text=True, check=True).stdout
        sg = json.loads(out)["data"]["repository"]["stargazers"]
        dates += [date.fromisoformat(e["starredAt"][:10]) for e in sg["edges"]]
        if not sg["pageInfo"]["hasNextPage"]:
            return dates
        cursor = sg["pageInfo"]["endCursor"]


def main():
    out = Path(sys.argv[1])
    star_dates = fetch_star_dates()
    today = date.today()
    span = (today - OPEN_DATE).days
    per_day = Counter(star_dates)

    def xs(d): return X0 + (d - OPEN_DATE).days / span * (X1 - X0)

    total = len(star_dates)
    ymax = math.ceil(total * 1.06 / 20) * 20

    def ys(v): return Y0 - v * PLOT_H / ymax

    cum, pts, cum_at = 0, [(xs(OPEN_DATE), ys(0))], {}
    for d in sorted(per_day):
        cum += per_day[d]
        pts.append((xs(d), ys(cum)))
        cum_at[d] = cum
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = line + f" L{X1},{Y0} L{X0},{Y0} Z"
    end_x, end_y = pts[-1]

    gridlines, ylabels = [], []
    for v in range(200, ymax, 200):
        y = ys(v)
        gridlines.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}"/>')
        ylabels.append(f'<text x="{X0-10}" y="{y+4:.1f}">{v}</text>')

    xticks = [f'<text x="{X0}" y="365" text-anchor="start">{OPEN_DATE.month}月{OPEN_DATE.day}日</text>']
    m = OPEN_DATE.month % 12 + 1
    year = OPEN_DATE.year + (OPEN_DATE.month == 12)
    while date(year, m, 1) <= today:
        if xs(date(year, m, 1)) - X0 < 60:  # 离开源日太近会和起点标签重叠
            year, m = (year + 1, 1) if m == 12 else (year, m + 1)
            continue
        xticks.append(f'<text x="{xs(date(year, m, 1)):.1f}" y="365">{m}月</text>')
        year, m = (year + 1, 1) if m == 12 else (year, m + 1)

    events_svg = []
    for ev_date, label in EVENTS:
        cum_v = max((c for d, c in cum_at.items() if d <= ev_date), default=0)
        ex, ey = xs(ev_date), ys(cum_v)
        events_svg.append(
            f'<line x1="{ex:.1f}" y1="{ey+6:.1f}" x2="{ex:.1f}" y2="{Y0}" stroke="{BASELINE}" stroke-width="1" stroke-dasharray="2 5"/>\n'
            f'  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{ACCENT}" stroke="{PANEL}" stroke-width="2"/>\n'
            f'  <text x="{ex-10:.1f}" y="{ey-15:.1f}" font-family="{SANS}" font-size="12" fill="{MUTED}" text-anchor="end">{label}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390" role="img" aria-label="说人话 star 增长曲线：开源 {span} 天，0 到 {total} stars，数据截至 {today}">
  <rect x="1" y="1" width="1198" height="388" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="0" y="0" width="1200" height="4" fill="{ACCENT}"/>

  <text x="40" y="37" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{ACCENT}">STAR 记录 / 每日更新</text>
  <text x="40" y="73" font-family="{SANS}" font-size="25" font-weight="700" fill="{INK}">开源以来</text>
  <text x="40" y="98" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{span} 天 · 数据截至 {today}</text>
  <text x="1150" y="75" font-family="{MONO}" font-size="43" font-weight="700" fill="{ACCENT}" text-anchor="end">{total}</text>
  <text x="1150" y="98" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">STARS</text>
  <line x1="40" y1="112" x2="1160" y2="112" stroke="{BORDER}" stroke-width="1"/>

  <g stroke="{GRID}" stroke-width="1">
    {''.join(gridlines)}
    <line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{BASELINE}" stroke-width="1.5"/>
  </g>
  <g font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="end">
    {''.join(ylabels)}
  </g>
  <g font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="middle">
    {''.join(xticks)}
  </g>

  <path d="{area}" fill="{AREA}" fill-opacity="0.07"/>
  <path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  {''.join(events_svg)}

  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="4.5" fill="{ACCENT}" stroke="{PANEL}" stroke-width="2"/>
  <text x="{end_x-12:.1f}" y="{end_y-10:.1f}" font-family="{SANS}" font-size="14" font-weight="700" fill="{ACCENT}" text-anchor="end">最新</text>
</svg>
'''
    out.write_text(svg, encoding="utf-8")
    print(f"written {out} — {total} stars, {span} days, ymax {ymax}")


if __name__ == "__main__":
    main()
