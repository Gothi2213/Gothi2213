#!/usr/bin/env python3
"""Generates assets/stats.svg (animated profile stats card) from the GitHub API.

Run in CI (see .github/workflows/stats.yml) with GH_TOKEN and GH_USER set.
Local preview without network: python scripts/gen_stats.py --placeholder
"""
import json, math, os, sys, html, datetime, urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'stats.svg')
FONT = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
PALETTE = ['#22D3EE', '#60A5FA', '#A78BFA', '#4ADE80', '#FBBF24', '#F472B6', '#94A3B8']
esc = lambda s: html.escape(str(s), quote=False)


# ------------------------------------------------------------------ data
def api(url, token, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'profile-stats')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch(user, token):
    q = '''query($u:String!){user(login:$u){followers{totalCount} following{totalCount}
      repositories(ownerAffiliation:OWNER,privacy:PUBLIC){totalCount}
      contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions totalPullRequestReviewContributions
        contributionCalendar{totalContributions weeks{contributionDays{contributionCount}}}}}}'''
    u = api('https://api.github.com/graphql', token, {'query': q, 'variables': {'u': user}})['data']['user']
    cc = u['contributionsCollection']
    repos, page = [], 1
    while True:
        chunk = api(f'https://api.github.com/users/{user}/repos?per_page=100&page={page}&type=owner', token)
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    stars = sum(r['stargazers_count'] for r in repos)
    langs = {}
    for r in repos:
        if r['fork']:
            continue
        for k, v in api(r['languages_url'], token).items():
            langs[k] = langs.get(k, 0) + v
    return {
        'repos': u['repositories']['totalCount'], 'stars': stars, 'followers': u['followers']['totalCount'],
        'following': u['following']['totalCount'], 'commits': cc['totalCommitContributions'],
        'prs': cc['totalPullRequestContributions'], 'issues': cc['totalIssueContributions'],
        'reviews': cc['totalPullRequestReviewContributions'], 'total': cc['contributionCalendar']['totalContributions'],
        'weeks': [[d['contributionCount'] for d in w['contributionDays']] for w in cc['contributionCalendar']['weeks']],
        'langs': langs,
    }


# ------------------------------------------------------------------ render
def render(d):
    W, H = 900, 500
    ph = d is None
    fmt = lambda v: '--' if ph else f'{v:,}'
    big = [('REPOSITORIES', 'repos', '#60A5FA'), ('STARS', 'stars', '#22D3EE'), ('FOLLOWERS', 'followers', '#A78BFA'), ('CONTRIBUTIONS', 'total', '#4ADE80')]
    small = [('commits / year', 'commits'), ('pull requests', 'prs'), ('issues', 'issues'), ('code reviews', 'reviews')]
    o = (f'<text class="m" x="40" y="46" font-size="13" fill="#22D3EE" letter-spacing="3">08 &#8212; LIVE FROM THE GITHUB API</text>')
    for i, (lab, key, col) in enumerate(big):
        x = 40 + i * 215
        if i:
            o += f'<path d="M{x - 22},72V150" stroke="#93C5FD" stroke-opacity=".18"/>'
        o += (f'<g class="in" style="animation-delay:{.1 + i * .12:.2f}s"><text class="m" x="{x}" y="86" font-size="12" letter-spacing="2.4" fill="{col}">{lab}</text>'
              f'<text x="{x}" y="140" font-size="58" font-weight="800" fill="{col}" filter="url(#b8)" opacity=".45">{fmt(d[key]) if d else "--"}</text>'
              f'<text x="{x}" y="140" font-size="58" font-weight="800" fill="#F1F6FF">{fmt(d[key]) if d else "--"}</text></g>')
    for i, (lab, key) in enumerate(small):
        x = 40 + i * 215
        o += (f'<g class="in" style="animation-delay:{.5 + i * .1:.2f}s"><text x="{x}" y="190" font-size="22" font-weight="700" fill="#DBEAFE">{fmt(d[key]) if d else "--"}</text>'
              f'<text class="m" x="{x + (len(fmt(d[key]) if d else "--") * 13 + 10)}" y="189" font-size="12.5" fill="#7F93BA">{lab}</text></g>')
    o += '<path d="M40,214H860" stroke="#93C5FD" stroke-opacity=".15"/>'
    # languages ribbon
    langs = []
    if d and d['langs']:
        tot = sum(d['langs'].values())
        items = sorted(d['langs'].items(), key=lambda kv: -kv[1])
        langs = [(k, v / tot) for k, v in items[:6]]
        rest = sum(v for _, v in items[6:])
        if rest:
            langs.append(('Other', rest / tot))
    o += '<text class="m" x="40" y="246" font-size="12" letter-spacing="2.4" fill="#22D3EE">TOP LANGUAGES</text>'
    o += '<clipPath id="lc"><rect x="40" y="258" width="820" height="14" rx="7"/></clipPath><rect x="40" y="258" width="820" height="14" rx="7" fill="#0A1330" stroke="#1E3A8A"/>'
    if langs:
        x, seg = 40, ''
        for i, (k, p) in enumerate(langs):
            w = 820 * p
            seg += f'<rect x="{x:.1f}" y="258" width="{max(w - 2, .5):.1f}" height="14" fill="{PALETTE[i % len(PALETTE)]}"/>'
            x += w
        o += f'<g clip-path="url(#lc)"><g class="grow">{seg}</g></g>'
        for i, (k, p) in enumerate(langs):
            lx, ly = 40 + (i % 4) * 205, 304 + (i // 4) * 26
            o += (f'<circle cx="{lx + 5}" cy="{ly - 5}" r="4.5" fill="{PALETTE[i % len(PALETTE)]}"/><text x="{lx + 17}" y="{ly}" font-size="15" font-weight="600" fill="#DBEAFE">{esc(k)}</text>'
                  f'<text x="{lx + 185}" y="{ly}" text-anchor="end" class="m" font-size="12.5" fill="#7F93BA">{p * 100:.1f}%</text>')
    else:
        o += '<text class="m" x="40" y="304" font-size="13" fill="#7F93BA">// languages appear after the first sync with GitHub</text>'
    # heatmap
    weeks = d['weeks'][-53:] if d else [[0] * 7 for _ in range(53)]
    mx = max([max(w) for w in weeks] + [1])
    cols = ['#0E1A3A', '#1E3A8A', '#2563EB', '#60A5FA', '#67E8F9']
    lvl = lambda n: 0 if n == 0 else min(4, 1 + int(3.999 * n / mx))
    o += '<text class="m" x="40" y="366" font-size="12" letter-spacing="2.4" fill="#22D3EE">CONTRIBUTIONS / LAST 12 MONTHS</text>'
    for wi, wk in enumerate(weeks):
        cells = ''.join(f'<rect x="{40 + wi * 15.5:.1f}" y="{380 + di * 15}" width="12" height="12" rx="3" fill="{cols[lvl(n)]}"{" stroke=\"#16294F\"" if n == 0 else ""}/>' for di, n in enumerate(wk))
        o += f'<g class="col" style="animation-delay:{.4 + wi * .022:.2f}s">{cells}</g>'
    if ph:
        o += '<text class="m" x="300" y="366" font-size="12" fill="#7F93BA">// waiting for the first sync (GitHub Action)</text>'
    for i, c in enumerate(cols):
        o += f'<rect x="{722 + i * 16}" y="356" width="12" height="12" rx="3" fill="{c}"/>'
    o += '<text class="m" x="714" y="366" text-anchor="end" font-size="11" fill="#7F93BA">less</text><text class="m" x="810" y="366" font-size="11" fill="#7F93BA">more</text>'
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    o += f'<text class="m" x="860" y="46" text-anchor="end" font-size="11.5" fill="#7F93BA">{"awaiting first sync" if ph else "updated " + stamp + " UTC"}</text>'
    css = (f"text{{font-family:{FONT}}}.m{{font-family:{MONO}}}"
           "@keyframes in{from{opacity:0;transform:translateY(12px)}}@keyframes gr{from{transform:scaleX(0)}}@keyframes cl{from{opacity:0}}"
           ".in{animation:in .9s cubic-bezier(.2,.8,.2,1) both}.grow{transform-box:fill-box;transform-origin:left center;animation:gr 1.6s cubic-bezier(.3,.7,.2,1) .5s both}"
           ".col{animation:cl .6s ease both}@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    label = 'GitHub stats: repositories, stars, followers, contributions, top languages and contribution heatmap'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}"><title>{label}</title>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060A13"/><stop offset=".6" stop-color="#0A1330"/><stop offset="1" stop-color="#0F1D45"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#93C5FD" stop-opacity=".55"/><stop offset=".45" stop-color="#60A5FA" stop-opacity=".06"/><stop offset="1" stop-color="#22D3EE" stop-opacity=".35"/></linearGradient>
<radialGradient id="aB"><stop offset="0" stop-color="#2563EB" stop-opacity=".5"/><stop offset="1" stop-color="#2563EB" stop-opacity="0"/></radialGradient>
<radialGradient id="aC"><stop offset="0" stop-color="#22D3EE" stop-opacity=".3"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
<filter id="b8" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
<clipPath id="sl"><rect width="{W}" height="{H}" rx="30"/></clipPath></defs>
<style>{css}</style>
<g clip-path="url(#sl)"><rect width="{W}" height="{H}" fill="url(#bg)"/><ellipse cx="820" cy="40" rx="360" ry="180" fill="url(#aC)"/><ellipse cx="60" cy="520" rx="400" ry="190" fill="url(#aB)"/>{o}</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="30" fill="none" stroke="url(#hl)" stroke-width="1.5"/>
</svg>'''


if __name__ == '__main__':
    if '--placeholder' in sys.argv:
        data = None
    elif '--sample' in sys.argv:  # preview only, fake numbers
        import random
        random.seed(3)
        data = {'repos': 12, 'stars': 7, 'followers': 5, 'following': 9, 'commits': 214, 'prs': 18, 'issues': 6, 'reviews': 3, 'total': 241,
                'weeks': [[random.choice([0, 0, 0, 1, 2, 4, 7]) for _ in range(7)] for _ in range(53)],
                'langs': {'Java': 52000, 'JavaScript': 31000, 'HTML': 18000, 'CSS': 9000, 'SQL': 5000}}
    else:
        data = fetch(os.environ['GH_USER'], os.environ['GH_TOKEN'])
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else OUT
    open(out, 'w', encoding='utf-8').write(render(data))
    print('wrote', os.path.abspath(out))
