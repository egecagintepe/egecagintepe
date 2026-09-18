#!/usr/bin/env python3
import collections
import datetime as dt
import html
import json
import os
import urllib.request
from pathlib import Path

USER = "egecagintepe"
API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_json(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "egecagintepe-profile-renderer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def safe(value):
    return html.escape(str(value), quote=True)

repos = get_json(f"{API}/users/{USER}/repos?per_page=100&type=owner&sort=pushed")
events = get_json(f"{API}/users/{USER}/events/public?per_page=100")

repos = [r for r in repos if not r.get("fork")]
repo_count = len(repos)
stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
forks = sum(int(r.get("forks_count") or 0) for r in repos)
languages = collections.Counter(r.get("language") for r in repos if r.get("language"))
recent_events = len(events)
latest = max(repos, key=lambda r: r.get("pushed_at") or "", default={})
latest_name = latest.get("name", "—")
latest_push = (latest.get("pushed_at") or "")[:10] or "—"
top_langs = languages.most_common(5)
max_lang = max((count for _, count in top_langs), default=1)
now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

bars = []
for i, (lang, count) in enumerate(top_langs):
    y = 177 + i * 25
    width = max(18, int(250 * count / max_lang))
    bars.append(
        f'<text x="755" y="{y}" class="m mut" font-size="11">{safe(lang)}</text>'
        f'<rect x="846" y="{y-10}" width="250" height="7" rx="3.5" fill="#13212d"/>'
        f'<rect x="846" y="{y-10}" width="{width}" height="7" rx="3.5" fill="url(#accent)" opacity=".82"/>'
        f'<text x="1110" y="{y}" class="m w" font-size="10">{count}</text>'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
<title id="title">Live GitHub telemetry</title>
<desc id="desc">Automatically generated public GitHub activity telemetry for {safe(USER)}.</desc>
<defs>
  <linearGradient id="bg" x1="0" x2="1"><stop stop-color="#081018"/><stop offset="1" stop-color="#0d1721"/></linearGradient>
  <linearGradient id="accent" x1="0" x2="1"><stop stop-color="#68e4ff"/><stop offset=".55" stop-color="#9beeff"/><stop offset="1" stop-color="#718cff"/></linearGradient>
  <style>
    .m{{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace}} .s{{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
    .w{{fill:#edf7ff}} .mut{{fill:#718698}} .a{{fill:#9beeff}}
    .flow{{stroke-dasharray:7 14;animation:f 4s linear infinite}} .pulse{{animation:p 2.5s ease-in-out infinite}}
    @keyframes f{{to{{stroke-dashoffset:-84}}}} @keyframes p{{0%,100%{{opacity:.32}}50%{{opacity:1}}}}
  </style>
</defs>
<rect x="1" y="1" width="1198" height="328" rx="22" fill="url(#bg)" stroke="#b8eaff" stroke-opacity=".13"/>
<text x="38" y="42" class="m mut" font-size="13" letter-spacing="1.6">LIVE TELEMETRY // AUTO-RENDERED FROM PUBLIC GITHUB DATA</text>
<circle class="pulse" cx="1130" cy="37" r="5" fill="#72efae"/><text x="1143" y="42" class="m" fill="#72efae" font-size="11">SYNC</text>
<text x="38" y="83" class="s w" font-size="27" font-weight="720">Public engineering activity, rendered as a system panel.</text>
<text x="38" y="108" class="s mut" font-size="14">No third-party stats service. Generated inside this repository by GitHub Actions.</text>

<g transform="translate(38 145)">
  <rect width="155" height="108" rx="14" fill="#0b151e" stroke="#9beeff" stroke-opacity=".11"/>
  <text x="16" y="26" class="m mut" font-size="10">PUBLIC REPOS</text><text x="16" y="66" class="s w" font-size="32" font-weight="750">{repo_count:02d}</text><text x="16" y="91" class="m a" font-size="10">OWNER / NON-FORK</text>
</g>
<g transform="translate(211 145)">
  <rect width="155" height="108" rx="14" fill="#0b151e" stroke="#9beeff" stroke-opacity=".11"/>
  <text x="16" y="26" class="m mut" font-size="10">PUBLIC STARS</text><text x="16" y="66" class="s w" font-size="32" font-weight="750">{stars:02d}</text><text x="16" y="91" class="m a" font-size="10">ACROSS REPOS</text>
</g>
<g transform="translate(384 145)">
  <rect width="155" height="108" rx="14" fill="#0b151e" stroke="#9beeff" stroke-opacity=".11"/>
  <text x="16" y="26" class="m mut" font-size="10">RECENT EVENTS</text><text x="16" y="66" class="s w" font-size="32" font-weight="750">{recent_events:02d}</text><text x="16" y="91" class="m a" font-size="10">PUBLIC FEED</text>
</g>
<g transform="translate(557 145)">
  <rect width="155" height="108" rx="14" fill="#0b151e" stroke="#9beeff" stroke-opacity=".11"/>
  <text x="16" y="26" class="m mut" font-size="10">LATEST PUSH</text><text x="16" y="57" class="s w" font-size="17" font-weight="680">{safe(latest_name[:16])}</text><text x="16" y="86" class="m a" font-size="10">{safe(latest_push)}</text>
</g>

<text x="755" y="146" class="m a" font-size="11" letter-spacing="1.2">PRIMARY LANGUAGE FOOTPRINT</text>
{"".join(bars)}

<path d="M38 280H1162" stroke="#9beeff" stroke-opacity=".1"/>
<path class="flow" d="M38 280H1162" stroke="url(#accent)" stroke-width="1.5" opacity=".42"/>
<text x="38" y="307" class="m mut" font-size="10">LAST RENDER: {safe(now)}</text>
<text x="945" y="307" class="m mut" font-size="10">FORKS: {forks:02d} / SOURCE: GITHUB API</text>
</svg>"""

Path("assets").mkdir(parents=True, exist_ok=True)
Path("assets/live-telemetry.svg").write_text(svg, encoding="utf-8")
print(f"rendered assets/live-telemetry.svg for {repo_count} public repositories")
