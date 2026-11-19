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
def perim(w, h, r):
    return 2 * (w - 2 * r) + 2 * (h - 2 * r) + 2 * math.pi * r


def travel(x, y, w, h, r, dur, phase=0):
    P = perim(w, h, r)
    tail, head = P * .12, P * .02
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke-linecap="round"'
    an = lambda off: f'<animate attributeName="stroke-dashoffset" from="{-off:.1f}" to="{-off - P:.1f}" dur="{dur}s" begin="-{phase}s" repeatCount="indefinite"/></rect>'
    return (b + f' stroke="#22D3EE" stroke-width="6" stroke-opacity=".5" stroke-dasharray="{tail:.1f} {P - tail:.1f}" filter="url(#glow)">' + an(0) +
            b + f' stroke="url(#trail)" stroke-width="2" stroke-dasharray="{tail:.1f} {P - tail:.1f}">' + an(0) +
            b + f' stroke="#fff" stroke-width="2.6" stroke-dasharray="{head:.1f} {P - head:.1f}">' + an(tail - head))


def render(d):
    W, H = 1280, 470
    ph = d is None
    fmt = lambda v: '-' if ph else f'{v:,}'
    tiles = [('REPOSITORIES', 'repos'), ('TOTAL STARS', 'stars'), ('FOLLOWERS', 'followers'), ('CONTRIBUTIONS', 'total'),
             ('COMMITS / YEAR', 'commits'), ('PULL REQUESTS', 'prs'), ('ISSUES', 'issues'), ('CODE REVIEWS', 'reviews')]
    o = ''
    for i, (lab, key) in enumerate(tiles):
        cx, cy = 30 + (i % 2) * 190, 34 + (i // 2) * 96
        v = fmt(d[key]) if d else '-'
        col = PALETTE[i % 4]
        o += (f'<g><rect x="{cx}" y="{cy}" width="180" height="86" rx="14" fill="#0E1A3A" stroke="#1E3A8A"/>'
              f'<rect x="{cx}" y="{cy + 18}" width="3" height="50" rx="1.5" fill="{col}"><animate attributeName="opacity" values=".4;1;.4" dur="3s" begin="-{i * .4:.1f}s" repeatCount="indefinite"/></rect>'
              f'<text x="{cx + 18}" y="{cy + 28}" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{col}">{lab}</text>'
              f'<text x="{cx + 18}" y="{cy + 66}" font-family="{FONT}" font-size="34" font-weight="800" fill="#3B82F6" filter="url(#tb)" opacity=".5">{v}</text>'
              f'<text x="{cx + 18}" y="{cy + 66}" font-family="{FONT}" font-size="34" font-weight="800" fill="#FFFFFF">{v}</text>'
              f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{.1 + i * .06:.2f};1" dur="1.6s" fill="freeze"/></g>')
    # languages
    o += f'<text x="430" y="52" font-family="{MONO}" font-size="12" letter-spacing="2.4" fill="#22D3EE">TOP LANGUAGES</text>'
    o += '<rect x="430" y="66" width="820" height="18" rx="9" fill="#0E1A3A" stroke="#1E3A8A"/>'
    langs = []
    if d and d['langs']:
        tot = sum(d['langs'].values())
        items = sorted(d['langs'].items(), key=lambda kv: -kv[1])
        top = items[:6]
        rest = sum(v for _, v in items[6:])
        langs = [(k, v / tot) for k, v in top] + ([('Other', rest / tot)] if rest else [])
    if langs:
        x = 430
        clip = '<clipPath id="lc"><rect x="430" y="66" width="820" height="18" rx="9"/></clipPath><g clip-path="url(#lc)">'
        for i, (k, p) in enumerate(langs):
            wseg = 820 * p
            c = PALETTE[i % len(PALETTE)]
            clip += (f'<rect x="{x:.1f}" y="66" width="0" height="18" fill="{c}"><animate attributeName="width" values="0;0;{wseg:.1f}" keyTimes="0;{.15 + i * .08:.2f};1" dur="1.8s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1"/></rect>')
            x += wseg
        o += clip + '</g>'
        o += '<rect x="430" y="66" width="120" height="18" fill="url(#sheen)" clip-path="url(#lc)"><animate attributeName="x" values="380;1250;1250" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite"/></rect>'
        for i, (k, p) in enumerate(langs):
            lx, ly = 430 + (i % 4) * 205, 112 + (i // 4) * 28
            c = PALETTE[i % len(PALETTE)]
            o += (f'<circle cx="{lx + 6}" cy="{ly - 4}" r="5" fill="{c}"><animate attributeName="opacity" values="1;.4;1" dur="2.6s" begin="-{i * .3:.1f}s" repeatCount="indefinite"/></circle>'
                  f'<text x="{lx + 20}" y="{ly}" font-family="{FONT}" font-size="14" font-weight="600" fill="#DBEAFE">{esc(k)}</text>'
                  f'<text x="{lx + 186}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6B7C99">{p * 100:.1f}%</text>')
    else:
        o += f'<text x="430" y="112" font-family="{MONO}" font-size="13" fill="#6B7C99">// languages appear after the first sync with GitHub</text>'
    # heatmap
    o += f'<text x="430" y="212" font-family="{MONO}" font-size="12" letter-spacing="2.4" fill="#22D3EE">CONTRIBUTIONS / LAST 12 MONTHS</text>'
    weeks = d['weeks'][-53:] if d else [[0] * 7 for _ in range(53)]
    mx = max([max(w) for w in weeks] + [1])
    cols = ['#0E1A3A', '#1E3A8A', '#2563EB', '#60A5FA', '#67E8F9']
    lvl = lambda n: 0 if n == 0 else min(4, 1 + int(3.999 * n / mx))
    cells = ''
    for wi, wk in enumerate(weeks):
        for di, n in enumerate(wk):
            stk = ' stroke="#16294F"' if n == 0 else ''
            cells += f'<rect x="{430 + wi * 15}" y="{228 + di * 15}" width="12" height="12" rx="3" fill="{cols[lvl(n)]}"{stk}/>'
    o += (f'<clipPath id="hc"><rect x="430" y="224" width="0" height="116"><animate attributeName="width" values="0;800" dur="2.2s" fill="freeze" calcMode="spline" keySplines=".3 .6 .3 1" keyTimes="0;1"/></rect></clipPath>'
          f'<g clip-path="url(#hc)">{cells}</g>'
          '<clipPath id="hc2"><rect x="430" y="224" width="800" height="116"/></clipPath>'
          '<rect x="380" y="224" width="90" height="116" fill="url(#sheen)" clip-path="url(#hc2)" transform="skewX(-12)"><animate attributeName="x" values="380;1300;1300" keyTimes="0;.55;1" dur="6s" begin="2.2s" repeatCount="indefinite"/></rect>')
    # legend
    o += f'<text x="1070" y="368" text-anchor="end" font-family="{MONO}" font-size="11" fill="#6B7C99">less</text>'
    for i, c in enumerate(cols):
        o += f'<rect x="{1078 + i * 16}" y="358" width="12" height="12" rx="3" fill="{c}"/>'
    o += f'<text x="1166" y="368" font-family="{MONO}" font-size="11" fill="#6B7C99">more</text>'
    if ph:
        o += f'<text x="430" y="368" font-family="{MONO}" font-size="13" fill="#6B7C99">// waiting for the first sync (GitHub Action)</text>'
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    o += f'<text x="30" y="{H - 24}" font-family="{MONO}" font-size="11" fill="#5B6E92">{"awaiting first sync" if ph else "updated " + stamp + " UTC"}</text>'
    o += f'<text x="{W - 30}" y="{H - 24}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#5B6E92">data: GitHub API</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub stats: repositories, stars, followers, contributions, top languages and contribution heatmap">
<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E1833"/><stop offset="1" stop-color="#080D1B"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#60A5FA" stop-opacity=".95"/><stop offset=".5" stop-color="#1E3A8A" stop-opacity=".45"/><stop offset="1" stop-color="#22D3EE" stop-opacity=".7"/></linearGradient>
<linearGradient id="trail" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="#67E8F9"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#BFDBFE" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1E3A8A" stroke-opacity=".2"/></pattern>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>
<filter id="tb" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="7"/></filter>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="url(#panel)" stroke="url(#bd)" stroke-width="1.5"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="url(#grid)"/>
<path d="M410 30V{H - 40}" stroke="#1E3A8A" stroke-opacity=".6" stroke-dasharray="3 7"/>
{o}
{travel(1, 1, W - 2, H - 2, 22, 14)}
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
