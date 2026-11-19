#!/usr/bin/env python3
"""Regenerates every SVG in ../assets (except stats.svg, which scripts/gen_stats.py builds from the GitHub API).
Usage: python generators/build_all.py
Edit PROJECTS below to fill in the featured-project cards (None fields render as clear placeholders)."""
import math
from lib import *

REPOS = 'https://github.com/Gothi2213?tab=repositories'
# ----- fill these in when you have real projects. Leave a field as None to keep the placeholder text. -----
PROJECTS = [
    dict(title=None, desc=None, stack=None, url=None),
    dict(title=None, desc=None, stack=None, url=None),
    dict(title=None, desc=None, stack=None, url=None),
]
TX, MU = '#EAF2FF', '#9FB3D9'


# ============================================================ HERO
def hero():
    W, H = 900, 440
    d, o, c = slab(W, H, 30, uid='hs')
    pts = [(610, 318), (668, 222), (738, 262), (792, 160), (852, 112), (748, 356), (836, 300)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 2)]
    con = ''
    for i, (a, b) in enumerate(edges):
        con += (f'<path d="M{pts[a][0]},{pts[a][1]}L{pts[b][0]},{pts[b][1]}" pathLength="1" stroke="#93C5FD" stroke-opacity=".5" stroke-width="1.2" fill="none" '
                f'stroke-dasharray="1" style="animation:draw 1.6s cubic-bezier(.4,0,.2,1) {1.0 + i * .22:.2f}s both"/>')
    for i, (x, y) in enumerate(pts):
        big = i in (0, 2, 4)
        con += (f'<g style="animation:fade .8s ease {1.2 + i * .2:.1f}s both"><circle cx="{x}" cy="{y}" r="{16 if big else 10}" fill="url(#aC)"/>'
                f'<circle cx="{x}" cy="{y}" r="{3.6 if big else 2.4}" fill="#E0F2FE" class="tw" style="animation-delay:-{i * 1.1:.1f}s;animation-duration:{4 + i * .7:.1f}s"/></g>')
    css = '''
.d1{animation:d1 70s ease-in-out infinite alternate}.d2{animation:d2 46s ease-in-out infinite alternate}
@keyframes d1{to{transform:translateX(-34px)}}@keyframes d2{to{transform:translateX(-70px)}}
.a1{animation:a1 26s ease-in-out infinite alternate}.a2{animation:a2 34s ease-in-out infinite alternate}.a3{animation:a3 41s ease-in-out infinite alternate}
@keyframes a1{to{transform:translate(60px,26px)}}@keyframes a2{to{transform:translate(-70px,-20px)}}@keyframes a3{to{transform:translate(40px,-30px)}}
.bm{transform-origin:470px -10px;animation:sw 16s cubic-bezier(.45,0,.55,1) infinite alternate}@keyframes sw{from{transform:rotate(-2.5deg)}to{transform:rotate(3deg)}}
'''
    defs = f'''{d}
<linearGradient id="bmH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#67E8F9" stop-opacity="0"/><stop offset=".5" stop-color="#67E8F9" stop-opacity=".22"/><stop offset="1" stop-color="#67E8F9" stop-opacity="0"/></linearGradient>
<linearGradient id="bmV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".85" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="bmM"><rect width="{W}" height="{H}" fill="url(#bmV)"/></mask>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#BFDBFE"/><stop offset="1" stop-color="#67E8F9"/></linearGradient>
<mask id="nmask"><text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="#fff">SARCO</text></mask>'''
    b = f'''{o}
<g class="a1"><ellipse cx="170" cy="400" rx="330" ry="170" fill="url(#aB)"/></g>
<g class="a2"><ellipse cx="760" cy="150" rx="300" ry="190" fill="url(#aC)" opacity=".8"/></g>
<g class="a3"><ellipse cx="520" cy="470" rx="320" ry="120" fill="url(#aV)" opacity=".8"/></g>
<g mask="url(#bmM)"><g class="bm"><polygon points="440,-10 500,-10 700,{H} 380,{H}" fill="url(#bmH)"/></g><g class="bm" style="animation-duration:23s;animation-direction:alternate-reverse"><polygon points="520,-10 560,-10 860,{H} 640,{H}" fill="url(#bmH)" opacity=".7"/></g></g>
<g fill="#BFDBFE" opacity=".45" class="d1">{stars(46, 3, W, H, .5, 1.1)}</g>
<g fill="#DBEAFE" opacity=".65" class="d2">{stars(22, 8, W, H, .9, 1.6)}</g>
<ellipse cx="730" cy="228" rx="205" ry="82" transform="rotate(-18 730 228)" fill="none" stroke="#60A5FA" stroke-opacity=".35" stroke-dasharray="2 9" stroke-linecap="round"/>
<ellipse cx="730" cy="228" rx="150" ry="52" transform="rotate(-18 730 228)" fill="none" stroke="#93C5FD" stroke-opacity=".18"/>
<g class="mo"><circle r="4" fill="#fff"><animateMotion dur="38s" repeatCount="indefinite" path="M525,228a205,82 0 1,0 410,0a205,82 0 1,0 -410,0" rotate="auto"/></circle></g>
{con}
{c}
<g class="in" style="animation-delay:.1s"><rect x="60" y="54" width="248" height="34" rx="17" fill="url(#gl)" stroke="#93C5FD" stroke-opacity=".3"/>
<circle cx="80" cy="71" r="4" fill="#4ADE80"/><circle cx="80" cy="71" r="4" fill="#4ADE80" class="pu"/>
<text class="m" x="95" y="76" font-size="12.5" fill="#CFE3FF" textLength="198" lengthAdjust="spacing">OPEN TO OPPORTUNITIES</text></g>
<g class="in" style="animation-delay:.3s"><text x="60" y="214" font-size="104" font-weight="300" textLength="470" lengthAdjust="spacing" fill="#EAF2FF">THIAGO</text></g>
<g class="in" style="animation-delay:.5s"><text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="#3B82F6" filter="url(#blur14)" opacity=".6">SARCO</text>
<text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="url(#nm)">SARCO</text>
<g mask="url(#nmask)" class="mo"><rect y="200" width="120" height="130" fill="url(#sw)" transform="skewX(-16)"><animateTransform attributeName="transform" type="translate" values="-260 0;760 0;760 0" keyTimes="0;.32;1" dur="9s" begin="2.2s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1"/></rect></g></g>
<g class="in" style="animation-delay:.8s"><rect x="60" y="346" width="64" height="3" rx="1.5" fill="url(#acc)"/>
<text class="m" x="60" y="382" font-size="15" fill="#93C5FD" textLength="470" lengthAdjust="spacing">SOFTWARE DEVELOPER IN TRAINING</text>
<text x="60" y="414" font-size="19" fill="{MU}">Learning by building &#183; Argentina</text></g>'''
    return svg(W, H, 'Thiago Sarco, software developer in training from Argentina, open to opportunities', b, defs, css)


# ============================================================ STATUS strip
def status():
    W, H = 900, 128
    cols = [('STATUS', 'Open to work', '#4ADE80'), ('LOOKING FOR', 'First experience', '#22D3EE'), ('BASED IN', 'Argentina &#183; UTC&#8722;3', '#60A5FA'), ('FOCUS', 'Java &#183; Web &#183; SQL', '#A78BFA')]
    d, o, c = slab(W, H, 22, uid='st', extra='<ellipse cx="450" cy="150" rx="520" ry="90" fill="url(#aB)" opacity=".7"/>')
    b = o + c
    for i, (lab, val, col) in enumerate(cols):
        x = 34 + i * 218
        if i:
            b += f'<path d="M{x - 22},28V100" stroke="#93C5FD" stroke-opacity=".18"/>'
        dot = (f'<circle cx="{x + 5}" cy="{50 - 4}" r="4.5" fill="{col}"/><circle cx="{x + 5}" cy="46" r="4.5" fill="{col}" class="pu" style="animation-delay:-{i * .7}s"/>' if i == 0
               else f'<circle cx="{x + 5}" cy="46" r="4" fill="{col}" opacity=".9"/>')
        b += (f'<g class="in" style="animation-delay:{.15 + i * .12:.2f}s">{dot}<text class="m" x="{x + 18}" y="51" font-size="12.5" fill="{MU}" textLength="{len(lab) * 9.2:.0f}" lengthAdjust="spacing">{lab}</text>'
              f'<text x="{x}" y="88" font-size="22" font-weight="700" fill="{TX}">{val}</text></g>')
    return svg(W, H, 'Status: open to work, looking for a first professional experience, based in Argentina (UTC-3), focus on Java, web and SQL', b, d)


# ============================================================ ABOUT (chamfered slab + tilted terminal)
def about():
    W, H = 900, 400
    d, o, c = slab(W, H, 26, cut=90, uid='ab', extra='<ellipse cx="120" cy="400" rx="380" ry="190" fill="url(#aB)" opacity=".8"/><ellipse cx="800" cy="60" rx="260" ry="150" fill="url(#aV)" opacity=".7"/>')
    lines = [('$ whoami', '#67E8F9'), ('thiago_sarco  &#183;  dev in training', '#DBEAFE'), ('$ cat focus.txt', '#67E8F9'), ('&gt; Java &#183; OOP', '#9FB3D9'), ('&gt; HTML &#183; CSS &#183; JavaScript', '#9FB3D9'),
             ('&gt; SQL &#183; data modeling', '#9FB3D9'), ('$ git status', '#67E8F9'), ('&gt; open to opportunities', '#4ADE80')]
    term = ''
    for i, (t, col) in enumerate(lines):
        term += (f'<text class="m" x="22" y="{70 + i * 25}" font-size="14.5" fill="{col}" style="animation:fade .01s steps(1) {.6 + i * .55:.2f}s both">{t}</text>')
    css = '@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1.1s steps(1) infinite}.ul{stroke-dasharray:1;animation:draw 1.4s cubic-bezier(.5,0,.2,1) 1.1s both}'
    b = f'''{o}<g fill="#BFDBFE" opacity=".5">{stars(30, 11, W, H, .5, 1.1, 0, 0)}</g>{c}
<g class="in"><text class="m" x="56" y="74" font-size="13" fill="#22D3EE" textLength="150" lengthAdjust="spacing">01 &#8212; ABOUT ME</text>
<text x="54" y="150" font-size="62" font-weight="300" fill="{TX}">I learn</text>
<text x="54" y="222" font-size="68" font-weight="900" fill="url(#txt)" textLength="410" lengthAdjust="spacing">by building.</text>
<path class="ul" pathLength="1" d="M56,240C140,250 300,232 460,242" stroke="url(#acc)" stroke-width="4" stroke-linecap="round" fill="none"/>
<text x="56" y="292" font-size="16.5" fill="{MU}">Software Development student combining academic</text>
<text x="56" y="318" font-size="16.5" fill="{MU}">learning with continuous practice. Into software and</text>
<text x="56" y="344" font-size="16.5" fill="{MU}">web development, databases and problem solving.</text></g>
<g transform="translate(528,76) rotate(2)" filter="url(#sh)"><g class="in" style="animation-delay:.3s">
<rect width="336" height="268" rx="16" fill="#070C1A" fill-opacity=".82" stroke="#93C5FD" stroke-opacity=".3"/>
<rect width="336" height="34" rx="16" fill="#fff" fill-opacity=".06"/><path d="M16,.8H320" stroke="#fff" stroke-opacity=".45"/>
<circle cx="20" cy="17" r="5" fill="#F87171"/><circle cx="38" cy="17" r="5" fill="#FBBF24"/><circle cx="56" cy="17" r="5" fill="#4ADE80"/>
<text class="m" x="168" y="21" font-size="11.5" fill="#6B7C99" text-anchor="middle">thiago@argentina: ~</text>
{term}<rect class="cur" x="22" y="{70 + 8 * 25 - 12}" width="9" height="16" fill="#67E8F9" style="animation-delay:5s"/></g></g>'''
    return svg(W, H, 'About me: Thiago Sarco learns by building. Software Development student combining academic learning and continuous practice, interested in software development, web development, databases and problem solving', b, d, css)


# ============================================================ MARQUEE (transparent, big display type, mid-tone colours that read on light and dark)
def marquee():
    W, H = 900, 150
    items = 'JAVA &#183; JAVASCRIPT &#183; HTML &#183; CSS &#183; SQL &#183; MYSQL &#183; GIT &#183; GITHUB &#183; C++ &#183; '
    L = 1900

    def row(y, size, cls, dur, rev, fill):
        t = lambda x: f'<text x="{x}" y="{y}" font-size="{size}" font-weight="900" textLength="{L}" lengthAdjust="spacing" {fill}>{items}</text>'
        return f'<g class="{cls}" style="animation-duration:{dur}s;animation-direction:{"reverse" if rev else "normal"}">{t(0)}{t(L)}</g>'
    css = f'@keyframes mq{{to{{transform:translateX(-{L}px)}}}}.r1,.r2{{animation:mq linear infinite}}'
    defs = ('<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="mk"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>')
    b = (f'<g mask="url(#mk)">{row(60, 54, "r1", 95, False, "fill=\"#3B82F6\" fill-opacity=\".92\"")}'
         f'{row(128, 54, "r2", 120, True, "fill=\"none\" stroke=\"#3B82F6\" stroke-width=\"1.6\" stroke-opacity=\".8\"")}</g>')
    return svg(W, H, 'Technologies: Java, JavaScript, HTML, CSS, SQL, MySQL, Git, GitHub, C++', b, defs, css)


# ============================================================ SECTION HEADERS (no box; alternating alignment)
SECTIONS = ['About me', 'Skill map', 'Featured projects', 'Mindset', 'Journey', 'Objective', 'Languages', 'GitHub stats', "Let's connect"]
SLUGS = ['about', 'skills', 'projects', 'mindset', 'journey', 'objective', 'languages', 'stats', 'connect']


def section(i, title):
    W, H = 900, 96
    right = i % 2 == 1
    n = f'{i + 1:02d}'
    x = W - 4 if right else 4
    anc = 'end' if right else 'start'
    defs = ('<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="#0891B2"/></linearGradient>'
            f'<linearGradient id="lg" x1="{1 if right else 0}" y1="0" x2="{0 if right else 1}" y2="0"><stop offset="0" stop-color="#3B82F6" stop-opacity=".9"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></linearGradient>')
    sx0, sx1 = (880, 20) if right else (20, 880)
    b = f'''<g class="in" style="animation-delay:{i * .05:.2f}s">
<text x="{6 if right else W - 6}" y="78" font-size="104" font-weight="900" text-anchor="{"start" if right else "end"}" fill="none" stroke="#3B82F6" stroke-opacity=".3" stroke-width="1.4">{n}</text>
<text class="m" x="{x}" y="30" font-size="12.5" text-anchor="{anc}" fill="#3B82F6" letter-spacing="3.2">SECTION {n}</text>
<text x="{x}" y="66" font-size="38" font-weight="800" text-anchor="{anc}" fill="url(#tg)" letter-spacing="-.5">{esc(title)}</text></g>
<rect x="4" y="86" width="892" height="1.6" rx=".8" fill="url(#lg)"/>
<circle r="3" cy="86.8" fill="#22D3EE" class="mo"><animate attributeName="cx" values="{sx0};{sx1};{sx1}" keyTimes="0;.55;1" dur="{9 + i % 4 * 2}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .2 1;0 0 1 1"/>
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.5;.58;1" dur="{9 + i % 4 * 2}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite"/></circle>'''
    return svg(W, H, f'Section {n}: {title}', b, defs)


# ============================================================ SKILL MAP (orbits)
def chipw(t):
    return len(t) * 9.9 + 42


def chip(t, col, strong):
    w = chipw(t)
    return (f'<g transform="translate({-w / 2:.1f},-18)"><rect width="{w:.1f}" height="36" rx="18" fill="{"url(#gl)" if strong else "#0A1330"}" fill-opacity="{1 if strong else .72}" stroke="{col}" stroke-opacity="{.75 if strong else .45}"/>'
            f'<circle cx="19" cy="18" r="4" fill="{col}"/><text x="31" y="24" font-size="18" font-weight="600" fill="{TX}">{t}</text></g>')


def skills():
    W, H = 900, 500
    cx, cy, ratio = 450, 244, .48
    d, o, c = slab(W, H, 30, uid='sk', extra='<ellipse cx="450" cy="244" rx="460" ry="230" fill="url(#aB)" opacity=".55"/><ellipse cx="450" cy="244" rx="150" ry="70" fill="url(#aC)"/>')
    rings = [(112, ['Java', 'JavaScript', 'SQL'], 80, 1, '#22D3EE', True, 20),
             (214, ['HTML', 'CSS', 'MySQL', 'Git', 'GitHub', 'C++'], 130, -1, '#60A5FA', False, 0),
             (352, ['OOP', 'Data Structures', 'Database Design', 'Responsive Design', 'Problem Solving', 'Git Workflows'], 190, 1, '#A78BFA', False, 45)]
    b = o + f'<g fill="#DBEAFE" opacity=".55" class="d1" style="animation:none">{stars(60, 5, W, H, .5, 1.2, 0, 0)}</g>'
    b += f'<g transform="translate({cx},{cy}) scale(1,{ratio})">'
    for R, items, per, dr, col, strong, off in rings:
        b += f'<ellipse rx="{R}" ry="{R}" fill="none" stroke="{col}" stroke-opacity=".6" stroke-dasharray="3 9" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        n = len(items)
        for i, t in enumerate(items):
            a = off + 360 * i / n
            fwd, rev = ('normal', 'reverse') if dr == 1 else ('reverse', 'normal')
            b += (f'<g transform="rotate({a:.1f})"><g class="rot" style="animation-duration:{per}s;animation-direction:{fwd}"><g transform="translate({R},0)">'
                  f'<g class="rot" style="animation-duration:{per}s;animation-direction:{rev}"><g transform="rotate({-a:.1f})"><g transform="scale(1,{1 / ratio:.4f})">{chip(t, col, strong)}</g></g></g></g></g></g>')
    b += '</g>'
    # core
    b += f'''<g transform="translate({cx},{cy})"><circle r="46" fill="url(#aC)"/><circle r="34" fill="#0A1330" stroke="url(#acc)" stroke-width="1.6"/><circle r="34" fill="none" stroke="#67E8F9" class="pu" style="animation-duration:4s"/>
<text y="7" font-size="20" font-weight="800" text-anchor="middle" fill="#E0F2FE" class="m">&lt;/&gt;</text></g>'''
    leg = [('#22D3EE', 'CORE', 'what I focus on'), ('#60A5FA', 'TOOLS', 'what I build with'), ('#A78BFA', 'CONCEPTS', 'what I am learning')]
    b += f'<text class="m" x="40" y="58" font-size="13" fill="#22D3EE" letter-spacing="3">02 &#8212; SKILL MAP</text>'
    for i, (col, a, t) in enumerate(leg):
        y = 428 + i * 22
        b += f'<circle cx="46" cy="{y - 5}" r="4.5" fill="{col}"/><text class="m" x="60" y="{y}" font-size="12.5" fill="{TX}" letter-spacing="2">{a}</text><text x="150" y="{y}" font-size="14" fill="{MU}">{t}</text>'
    b += c
    return svg(W, H, 'Skill map: core Java, JavaScript, SQL; tools HTML, CSS, MySQL, Git, GitHub, C++; concepts OOP, data structures, database design, responsive design, problem solving, Git workflows', b, d)


# ============================================================ PROJECTS (3 asymmetric cards, placeholders until filled)
def project(i, big):
    p = PROJECTS[i]
    W, H = (560, 392) if big else (340, 186)
    col = ['#60A5FA', '#22D3EE', '#A78BFA'][i]
    glow = ['aB', 'aC', 'aV'][i]
    ph = p['title'] is None
    d, o, c = slab(W, H, 26 if big else 22, uid=f'p{i}', extra=f'<ellipse cx="{W * (.8 if i % 2 == 0 else .2)}" cy="{H * .2}" rx="{W * .6}" ry="{H * .5}" fill="url(#{glow})" opacity=".9"/>')
    title = esc(p['title'] or 'Your project name')
    desc = esc(p['desc'] or 'One sentence: what problem it solves.')
    stack = (p['stack'] or ['Tech 1', 'Tech 2', 'Tech 3'])[: 4 if big else 3]
    tag = 'PLACEHOLDER' if ph else 'FEATURED'
    x = 32 if big else 26
    b = o + c
    b += f'<g class="in" style="animation-delay:{i * .15:.2f}s">'
    b += f'<text class="m" x="{x}" y="{46 if big else 38}" font-size="{13 if big else 12}" fill="{col}" letter-spacing="3">PROJECT 0{i + 1}</text>'
    tw_ = 112
    b += f'<rect x="{W - x - tw_}" y="{28 if big else 22}" width="{tw_}" height="24" rx="12" fill="none" stroke="{col}" stroke-opacity=".6" {"stroke-dasharray=\"4 3\"" if ph else ""}/><text class="m" x="{W - x - tw_ / 2}" y="{44 if big else 38}" font-size="11" fill="{col}" text-anchor="middle" letter-spacing="1.5">{tag}</text>'
    if big:
        # skeleton "window" preview
        b += f'<g transform="translate(32,70)"><rect width="496" height="130" rx="12" fill="#050914" stroke="#93C5FD" stroke-opacity=".22"/><rect width="496" height="22" rx="12" fill="#fff" fill-opacity=".05"/>'
        b += '<circle cx="14" cy="11" r="3.5" fill="#F87171"/><circle cx="28" cy="11" r="3.5" fill="#FBBF24"/><circle cx="42" cy="11" r="3.5" fill="#4ADE80"/>'
        for k, (xx, yy, ww, hh) in enumerate([(18, 38, 150, 14), (18, 62, 230, 8), (18, 78, 190, 8), (18, 98, 90, 18), (280, 38, 198, 78)]):
            b += (f'<rect x="{xx}" y="{yy}" width="{ww}" height="{hh}" rx="4" fill="{col}" fill-opacity=".16"><animate attributeName="fill-opacity" values=".1;.26;.1" dur="{3.2 + k * .5:.1f}s" begin="-{k * .6:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/></rect>')
        b += '</g>'
        ty, dy, cy_ = 252, 286, 328
    else:
        ty, dy, cy_ = 88, 116, 152
    b += f'<text x="{x}" y="{ty}" font-size="{34 if big else 24}" font-weight="800" fill="{TX if not ph else "#C7D7F5"}">{title}</text>'
    b += f'<text x="{x}" y="{dy}" font-size="{17 if big else 15}" fill="{MU}">{desc}</text>'
    cxp = x
    for t in stack:
        w = len(t) * 8.4 + 26
        b += f'<rect x="{cxp:.0f}" y="{cy_ - 17}" width="{w:.0f}" height="26" rx="13" fill="#fff" fill-opacity=".06" stroke="{col}" stroke-opacity=".45" {"stroke-dasharray=\"4 3\"" if ph else ""}/><text class="m" x="{cxp + w / 2:.0f}" y="{cy_}" font-size="12.5" fill="{TX}" text-anchor="middle">{esc(t)}</text>'
        cxp += w + 8
    if big:
        b += f'<text class="m" x="{x}" y="372" font-size="13" fill="{col}" letter-spacing="1.5">{"VIEW REPOSITORY  &#8594;" if not ph else "&#8594;  ADD YOUR FIRST PROJECT"}</text>'
    b += '</g>'
    lab = (f'Featured project {i + 1}: {p["title"]}. {p["desc"] or ""}' if not ph else f'Featured project {i + 1}: placeholder, to be filled with a real project')
    return svg(W, H, lab, b, d)


# ============================================================ MINDSET (ascending steps)
def mindset():
    W, H = 900, 370
    data = [('01', 'Understand', 'Analyze the problem', 'before writing|the solution', '#60A5FA', 200), ('02', 'Build', 'Turn ideas into', 'functional software', '#22D3EE', 250),
            ('03', 'Improve', 'Learn from mistakes and', 'refine the solution', '#A78BFA', 300), ('04', 'Grow', 'Keep learning and take', 'on new challenges', '#4ADE80', 352)]
    defs, b = '', ''
    for i, (n, t, l1, l2, col, h) in enumerate(data):
        x, w = 8 + i * 222, 206
        y = H - h - 8
        d, o, c = slab(w, h, 20, uid=f'm{i}', extra=f'<ellipse cx="{w / 2}" cy="0" rx="{w * .8}" ry="{h * .5}" fill="{col}" opacity=".16"/>')
        defs += d
        b += (f'<g transform="translate({x},{y})" class="in" style="animation-delay:{i * .14:.2f}s"><g>{o}{c}'
              f'<text x="{w - 12}" y="{h - 14}" font-size="86" font-weight="900" text-anchor="end" fill="none" stroke="{col}" stroke-opacity=".28" stroke-width="1.4">{n}</text>'
              f'<rect x="20" y="26" width="26" height="3" rx="1.5" fill="{col}"/>'
              f'<text x="20" y="66" font-size="29" font-weight="800" fill="{TX}">{t}</text>'
              +''.join(f'<text x="20" y="{96 + k * 21}" font-size="15" fill="{MU}">{ln}</text>' for k, ln in enumerate([l1] + l2.split('|'))) + '</g></g>')
    return svg(W, H, 'Development mindset: Understand, Build, Improve, Grow', b, defs)


# ============================================================ JOURNEY (flight path)
def journey():
    W, H = 900, 380
    nodes = [(120, 205, '01', 'Learn', 'Academic learning and', 'continuous practice', 'ONGOING', '#4ADE80', 'low'),
             (340, 140, '02', 'Build', 'Turn ideas into', 'functional software', 'ONGOING', '#4ADE80', 'up'),
             (570, 205, '03', 'Collaborate', 'Join a team of', 'developers', 'NEXT', '#60A5FA', 'low'),
             (790, 140, '04', 'First experience', 'Professional experience', 'in software development', 'GOAL', '#A78BFA', 'up')]
    path = 'M120,205C230,205 230,140 340,140C455,140 455,205 570,205C680,205 680,140 790,140'
    seg1 = 'M120,205C230,205 230,140 340,140'
    d, o, c = slab(W, H, 30, uid='jo', extra='<ellipse cx="160" cy="330" rx="340" ry="170" fill="url(#aB)" opacity=".7"/><ellipse cx="780" cy="40" rx="300" ry="160" fill="url(#aV)" opacity=".7"/>')
    b = o + f'<g fill="#BFDBFE" opacity=".5">{stars(40, 21, W, H, .5, 1.1, 0, 0)}</g>' + c
    b += f'<path d="{path}" fill="none" stroke="#93C5FD" stroke-opacity=".35" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/>'
    b += f'<path d="{seg1}" pathLength="1" fill="none" stroke="url(#acc)" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1" style="animation:draw 2.2s cubic-bezier(.5,0,.2,1) .4s both"/>'
    b += f'<g class="mo"><circle r="9" fill="#67E8F9" opacity=".35"/><circle r="3.6" fill="#fff"/><animateMotion dur="7s" repeatCount="indefinite" path="{seg1}" keyPoints="0;1;1" keyTimes="0;.55;1" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></g>'
    for i, (x, y, n, t, l1, l2, st, col, pos) in enumerate(nodes):
        up = pos == 'up'
        done = st == 'ONGOING'
        ty = y - 78 if up else y + 62
        cyc = ty - 56 if up else ty + 64   # chip y
        sy = 0
        b += f'<g class="in" style="animation-delay:{.3 + i * .18:.2f}s">'
        b += f'<circle cx="{x}" cy="{y}" r="30" fill="url(#aC)" opacity="{.9 if done else .4}"/>'
        b += f'<circle cx="{x}" cy="{y}" r="24" fill="#0A1330" stroke="{col}" stroke-width="{2 if done else 1.5}" {"" if done else "stroke-dasharray=\"4 4\""}/>'
        if done:
            b += f'<circle cx="{x}" cy="{y}" r="24" fill="none" stroke="{col}" class="pu" style="animation-delay:-{i * 1.2}s"/>'
        b += f'<text class="m" x="{x}" y="{y + 5}" font-size="14" font-weight="700" text-anchor="middle" fill="{TX}">{n}</text>'
        cy0 = (y - 78 - 40) if up else (y + 62 + 40 + 6)
        cy0 = y - 124 if up else y + 58
        b += f'<rect x="{x - 40}" y="{cy0}" width="80" height="22" rx="11" fill="none" stroke="{col}" stroke-opacity=".6"/><text class="m" x="{x}" y="{cy0 + 15}" font-size="11" text-anchor="middle" fill="{col}" letter-spacing="1.8">{st}</text>'
        ty = (cy0 + 46) if up else (cy0 + 46)
        b += f'<text x="{x}" y="{ty}" font-size="22" font-weight="800" text-anchor="middle" fill="{TX}">{t}</text>'
        b += f'<text x="{x}" y="{ty + 22}" font-size="14.5" text-anchor="middle" fill="{MU}">{l1}</text><text x="{x}" y="{ty + 41}" font-size="14.5" text-anchor="middle" fill="{MU}">{l2}</text></g>'
    return svg(W, H, 'Journey: Learn (ongoing), Build (ongoing), Collaborate (next), First experience (goal)', b, d)


# ============================================================ OBJECTIVE
def objective():
    W, H = 900, 330
    d, o, c = slab(W, H, 30, uid='ob', extra='<ellipse cx="780" cy="90" rx="380" ry="200" fill="url(#aC)" opacity=".8"/><ellipse cx="80" cy="330" rx="360" ry="170" fill="url(#aB)"/>')
    items = [('Learn', 'From experienced', 'developers', '#60A5FA'), ('Collaborate', 'As part of', 'a team', '#22D3EE'), ('Contribute', 'Applying my', 'technical knowledge', '#A78BFA'), ('Grow', 'Continue', 'improving', '#4ADE80')]
    b = o + c
    b += f'''<g class="in"><text class="m" x="56" y="62" font-size="13" fill="#22D3EE" letter-spacing="3">06 &#8212; PROFESSIONAL OBJECTIVE</text>
<text x="54" y="122" font-size="44" font-weight="300" fill="{TX}" textLength="560" lengthAdjust="spacing">Looking for my first</text>
<text x="54" y="176" font-size="52" font-weight="900" fill="url(#txt)" textLength="700" lengthAdjust="spacing">professional experience</text>
<text x="56" y="208" font-size="18" fill="{MU}">in software development, joining a team where I can:</text></g>'''
    for i, (t, l1, l2, col) in enumerate(items):
        x = 56 + i * 208
        if i:
            b += f'<path d="M{x - 24},238V300" stroke="#93C5FD" stroke-opacity=".2"/>'
        b += (f'<g class="in" style="animation-delay:{.4 + i * .12:.2f}s"><rect x="{x}" y="240" width="26" height="3" rx="1.5" fill="{col}"/>'
              f'<text x="{x}" y="270" font-size="21" font-weight="800" fill="{TX}">{t}</text><text x="{x}" y="291" font-size="14.5" fill="{MU}">{l1}</text><text x="{x}" y="309" font-size="14.5" fill="{MU}">{l2}</text></g>')
    return svg(W, H, 'Professional objective: first professional experience in software development, to learn, collaborate, contribute and grow', b, d)


# ============================================================ LANGUAGES
def languages():
    W, H = 900, 150
    d, o, c = slab(W, H, 24, uid='lg', extra='<ellipse cx="450" cy="170" rx="500" ry="90" fill="url(#aB)" opacity=".7"/>')
    css = '@keyframes shm{from{transform:translateX(-160px)}to{transform:translateX(620px)}}.shm{animation:shm 3.6s cubic-bezier(.45,0,.35,1) infinite}'
    ticks = ''.join(f'<rect x="{i * 22}" y="0" width="14" height="10" rx="3" fill="#60A5FA" fill-opacity=".28"/>' for i in range(28))
    b = o + c + f'''<g class="in"><text class="m" x="40" y="52" font-size="13" fill="#22D3EE" letter-spacing="2.5">ES</text><text x="82" y="54" font-size="22" font-weight="800" fill="{TX}">Spanish</text>
<text class="m" x="860" y="52" font-size="12.5" text-anchor="end" fill="#4ADE80" letter-spacing="2.5">NATIVE</text><rect x="40" y="68" width="820" height="10" rx="5" fill="url(#acc)"/></g>
<g class="in" style="animation-delay:.2s"><text class="m" x="40" y="108" font-size="13" fill="#60A5FA" letter-spacing="2.5">EN</text><text x="82" y="110" font-size="22" font-weight="800" fill="{TX}">English</text>
<text class="m" x="860" y="108" font-size="12.5" text-anchor="end" fill="#60A5FA" letter-spacing="2.5">IMPROVING</text>
<clipPath id="ec"><rect x="40" y="124" width="620" height="10"/></clipPath><g transform="translate(40,124)">{ticks}</g>
<g clip-path="url(#ec)" class="mo"><rect x="0" y="124" width="120" height="10" fill="url(#sw2)" class="shm"/></g></g>'''
    d += '<linearGradient id="sw2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#67E8F9" stop-opacity="0"/><stop offset=".5" stop-color="#67E8F9" stop-opacity=".9"/><stop offset="1" stop-color="#67E8F9" stop-opacity="0"/></linearGradient>'
    return svg(W, H, 'Languages: Spanish native, English improving', b, d, css)


# ============================================================ CONNECT
def connect_mail():
    W, H = 900, 112
    d, o, c = slab(W, H, 26, uid='cm', fill='url(#cmg)')
    d += '<linearGradient id="cmg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1D4ED8"/><stop offset="1" stop-color="#0E7490"/></linearGradient><linearGradient id="sh3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    b = o + '<g class="mo"><rect y="0" width="140" height="112" fill="url(#sh3)" transform="skewX(-18)"><animateTransform attributeName="transform" type="translate" values="-260 0;1100 0;1100 0" keyTimes="0;.4;1" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></rect></g>' + c
    b += (f'<text class="m" x="44" y="42" font-size="13" fill="#CFE8FF" letter-spacing="3">SAY HELLO &#8212; EMAIL</text><text x="42" y="82" font-size="34" font-weight="800" fill="#fff">thiagosarco13@gmail.com</text>'
          '<g transform="translate(820,56)"><circle r="26" fill="#fff" fill-opacity=".16"/><path d="M-9,0H9M2,-8L10,0L2,8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return svg(W, H, 'Email Thiago: thiagosarco13@gmail.com', b, d)


def connect_small(kind):
    W, H = 440, 92
    label, val, col, alt = (('GITHUB', 'github.com/Gothi2213', '#60A5FA', 'GitHub: Gothi2213') if kind == 'gh' else ('LOCATION', 'Argentina &#183; UTC&#8722;3', '#22D3EE', 'Location: Argentina'))
    d, o, c = slab(W, H, 22, uid='cs', extra=f'<ellipse cx="{W * .9}" cy="0" rx="200" ry="90" fill="url(#{"aB" if kind == "gh" else "aC"})"/>')
    b = o + c + f'<g class="in"><circle cx="40" cy="46" r="5" fill="{col}"/><circle cx="40" cy="46" r="5" fill="{col}" class="pu"/><text class="m" x="62" y="38" font-size="12.5" fill="{col}" letter-spacing="3">{label}</text><text x="62" y="68" font-size="22" font-weight="800" fill="{TX}">{val}</text></g>'
    return svg(W, H, alt, b, d)


# ============================================================ FOOTER
def footer():
    W, H = 900, 170
    d, o, c = slab(W, H, 30, uid='ft', extra='<ellipse cx="450" cy="190" rx="520" ry="120" fill="url(#aB)"/>')
    css = '.w1{animation:wv 11s ease-in-out infinite alternate}.w2{animation:wv 15s ease-in-out infinite alternate-reverse}@keyframes wv{to{transform:translateX(-90px)}}'
    wave = lambda y, a, ph: 'M-120,%d ' % y + ' '.join(f'Q{-120 + k * 120 + 60},{y + (a if k % 2 == 0 else -a)} {-120 + (k + 1) * 120},{y}' for k in range(10))
    b = o + f'<g fill="#BFDBFE" opacity=".5">{stars(36, 33, W, H, .5, 1.1, 0, 0)}</g>'
    b += f'<path class="w1" d="{wave(132, 14, 0)}" fill="none" stroke="#60A5FA" stroke-opacity=".5"/><path class="w2" d="{wave(142, 12, 0)}" fill="none" stroke="#22D3EE" stroke-opacity=".4"/>' + c
    b += f'<text x="450" y="76" font-size="40" font-weight="300" text-anchor="middle" fill="{TX}" textLength="430" lengthAdjust="spacing">THIAGO <tspan font-weight="900">SARCO</tspan></text>'
    b += f'<text class="m" x="450" y="106" font-size="13" text-anchor="middle" fill="#93C5FD" letter-spacing="4">LEARNING BY BUILDING &#183; ARGENTINA</text>'
    return svg(W, H, 'Thiago Sarco. Learning by building. Argentina', b, d, css)


if __name__ == '__main__':
    out = {'hero.svg': hero(), 'status.svg': status(), 'about.svg': about(), 'marquee.svg': marquee(), 'skills.svg': skills(),
           'project-1.svg': project(0, True), 'project-2.svg': project(1, False), 'project-3.svg': project(2, False),
           'mindset.svg': mindset(), 'journey.svg': journey(), 'objective.svg': objective(), 'languages.svg': languages(),
           'connect-mail.svg': connect_mail(), 'connect-github.svg': connect_small('gh'), 'connect-location.svg': connect_small('loc'), 'footer.svg': footer()}
    for i, t in enumerate(SECTIONS):
        out[f'sec-{SLUGS[i]}.svg'] = section(i, t)
    for k, v in out.items():
        print(k, write(k, v))
