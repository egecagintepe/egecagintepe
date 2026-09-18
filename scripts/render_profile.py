import json
import os
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USERNAME = "egecagintepe"
TOKEN = os.getenv("GITHUB_TOKEN", "")
API = "https://api.github.com"

def get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "egecagintepe-profile-telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

repos = get(f"{API}/users/{USERNAME}/repos?per_page=100&type=owner&sort=updated")
repos = [r for r in repos if not r.get("fork")]

stars = sum(r.get("stargazers_count", 0) for r in repos)
forks = sum(r.get("forks_count", 0) for r in repos)
latest = max(repos, key=lambda r: r.get("pushed_at") or "") if repos else None

langs = Counter()
for repo in repos:
    try:
        data = get(repo["languages_url"])
        langs.update(data)
    except Exception:
        pass

top = langs.most_common(5)
total = sum(v for _, v in top) or 1
updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
latest_name = latest["name"] if latest else "—"

palette = ["#6DE7FF", "#8AB8FF", "#A8F0FF", "#70F0AE", "#C0A6FF"]
bars = []
y = 224
for i, (name, value) in enumerate(top):
    pct = value / total
    width = max(8, round(410 * pct))
    bars.append(
        f'<text x="690" y="{y}" class="m muted" font-size="11">{escape(name)}</text>'
        f'<rect x="790" y="{y-10}" width="410" height="8" rx="4" fill="#13212E"/>'
        f'<rect x="790" y="{y-10}" width="{width}" height="8" rx="4" fill="{palette[i % len(palette)]}" opacity=".86"/>'
    )
    y += 29

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390" role="img" aria-labelledby="t d">
<title id="t">Public GitHub Telemetry</title><desc id="d">Automatically generated public repository telemetry for {USERNAME}.</desc>
<defs>
<linearGradient id="bg" x1="0" x2="1"><stop stop-color="#091018"/><stop offset="1" stop-color="#0E1722"/></linearGradient>
<style>.m{{font-family:"SFMono-Regular",Consolas,monospace}}.s{{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.muted{{fill:#70869A}}.w{{fill:#EDF7FF}}.a{{fill:#9FEAFF}}.blink{{animation:b 2.5s ease-in-out infinite}}@keyframes b{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}</style>
</defs>
<rect x="1" y="1" width="1198" height="388" rx="22" fill="url(#bg)" stroke="#B8E9FF" stroke-opacity=".13"/>
<text x="38" y="43" class="m muted" font-size="13" letter-spacing="1.6">PUBLIC GITHUB TELEMETRY // GENERATED</text>
<circle class="blink" cx="1139" cy="38" r="5" fill="#70F0AE"/>

<text x="38" y="96" class="s w" font-size="28" font-weight="720">Repository signal</text>
<text x="38" y="122" class="s muted" font-size="14">Self-generated from public GitHub data. No third-party stats service.</text>

<g class="m">
<text x="40" y="184" class="muted" font-size="11">PUBLIC REPOS</text><text x="40" y="230" class="w" font-size="34">{len(repos):02d}</text>
<text x="208" y="184" class="muted" font-size="11">TOTAL STARS</text><text x="208" y="230" class="w" font-size="34">{stars:02d}</text>
<text x="374" y="184" class="muted" font-size="11">FORKS</text><text x="374" y="230" class="w" font-size="34">{forks:02d}</text>
<text x="515" y="184" class="muted" font-size="11">LATEST PUSH</text><text x="515" y="213" class="a" font-size="13">{escape(latest_name[:22])}</text>
</g>

<path d="M38 264H635" stroke="#A4ECFF" stroke-opacity=".1"/>
<path d="M665 154V342" stroke="#A4ECFF" stroke-opacity=".1"/>

<text x="690" y="180" class="m muted" font-size="11" letter-spacing="1.1">PUBLIC LANGUAGE SIGNAL</text>
{''.join(bars)}

<text x="38" y="332" class="m muted" font-size="11">LAST REFRESH</text>
<text x="38" y="356" class="m w" font-size="12">{updated}</text>
<text x="945" y="356" class="m muted" font-size="10">PROFILE / AUTO REFRESH</text>
</svg>"""

Path("assets").mkdir(exist_ok=True)
Path("assets/telemetry.svg").write_text(svg, encoding="utf-8")
