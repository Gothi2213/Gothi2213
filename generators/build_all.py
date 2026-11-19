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
TX, MU = '#FFF1F2', '#D1A5AE'


# ============================================================ HERO
def hero():
    W, H = 900, 440
    d, o, c = slab(W, H, 30, uid='hs')
    pts = [(610, 318), (668, 222), (738, 262), (792, 160), (852, 112), (748, 356), (836, 300)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 2)]
    con = ''
    for i, (a, b) in enumerate(edges):
        con += (f'<path d="M{pts[a][0]},{pts[a][1]}L{pts[b][0]},{pts[b][1]}" pathLength="1" stroke="#FDA4AF" stroke-opacity=".5" stroke-width="1.2" fill="none" '
                f'stroke-dasharray="1" style="animation:draw 1.6s cubic-bezier(.4,0,.2,1) {1.0 + i * .22:.2f}s both"/>')
    for i, (x, y) in enumerate(pts):
        big = i in (0, 2, 4)
        con += (f'<g style="animation:fade .8s ease {1.2 + i * .2:.1f}s both"><circle cx="{x}" cy="{y}" r="{16 if big else 10}" fill="url(#aC)"/>'
                f'<circle cx="{x}" cy="{y}" r="{3.6 if big else 2.4}" fill="#FFF1F2" class="tw" style="animation-delay:-{i * 1.1:.1f}s;animation-duration:{4 + i * .7:.1f}s"/></g>')
    rays = ''.join(f'<path d="M{104 * math.cos(a):.1f},{104 * math.sin(a):.1f}L{(104 + L) * math.cos(a):.1f},{(104 + L) * math.sin(a):.1f}" stroke="#FDA4AF" stroke-opacity="{op}" stroke-width="{w_}" stroke-linecap="round"/>'
                   for a, L, op, w_ in [(k * math.pi / 18, 10 + (k * 37 % 5) * 9, .14 + (k % 3) * .09, 1 + (k % 2) * .6) for k in range(36)])
    css = '''
.p1,.p2,.p3{animation:ph 15s cubic-bezier(.2,.8,.2,1) infinite}.p2{animation-delay:5s}.p3{animation-delay:10s}
.d1{animation:d1 70s ease-in-out infinite alternate}.d2{animation:d2 46s ease-in-out infinite alternate}
@keyframes d1{to{transform:translateX(-34px)}}@keyframes d2{to{transform:translateX(-70px)}}
.a1{animation:a1 26s ease-in-out infinite alternate}.a2{animation:a2 34s ease-in-out infinite alternate}.a3{animation:a3 41s ease-in-out infinite alternate}
@keyframes a1{to{transform:translate(60px,26px)}}@keyframes a2{to{transform:translate(-70px,-20px)}}@keyframes a3{to{transform:translate(40px,-30px)}}
.bm{transform-origin:470px -10px;animation:sw 16s cubic-bezier(.45,0,.55,1) infinite alternate}@keyframes sw{from{transform:rotate(-2.5deg)}to{transform:rotate(3deg)}}
'''
    defs = f'''{d}
<radialGradient id="aE"><stop offset=".42" stop-color="#EF4444" stop-opacity=".55"/><stop offset=".6" stop-color="#F97316" stop-opacity=".22"/><stop offset="1" stop-color="#EF4444" stop-opacity="0"/></radialGradient><linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF1F2"/><stop offset=".4" stop-color="#FB7185"/><stop offset="1" stop-color="#F97316" stop-opacity=".2"/></linearGradient>
<linearGradient id="bmH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FDBA74" stop-opacity="0"/><stop offset=".5" stop-color="#FDBA74" stop-opacity=".22"/><stop offset="1" stop-color="#FDBA74" stop-opacity="0"/></linearGradient>
<linearGradient id="bmV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".85" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="bmM"><rect width="{W}" height="{H}" fill="url(#bmV)"/></mask>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#FECDD3"/><stop offset="1" stop-color="#FDBA74"/></linearGradient>
<filter id="lit" x="-4%" y="-12%" width="108%" height="130%"><feGaussianBlur in="SourceAlpha" stdDeviation="2.6" result="b"/>
<feSpecularLighting in="b" surfaceScale="7" specularConstant="1.2" specularExponent="22" lighting-color="#FFEBD9" result="sp"><feDistantLight azimuth="30" elevation="42"><animate attributeName="azimuth" values="25;155;25" dur="10s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></feDistantLight></feSpecularLighting>
<feComposite in="sp" in2="SourceAlpha" operator="in" result="s2"/><feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/></filter>
<filter id="plasma" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".02 .035" numOctaves="2" seed="4" result="n"><animate attributeName="baseFrequency" values=".02 .035;.035 .02;.02 .035" dur="16s" repeatCount="indefinite"/></feTurbulence><feDisplacementMap in="SourceGraphic" in2="n" scale="30" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="1.2"/></filter>
<mask id="nmask"><text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="#fff">SARCO</text></mask>'''
    b = f'''{o}
<g class="a1"><ellipse cx="170" cy="400" rx="330" ry="170" fill="url(#aB)"/></g>
<g class="a2"><ellipse cx="760" cy="150" rx="300" ry="190" fill="url(#aC)" opacity=".8"/></g>
<g class="a3"><ellipse cx="520" cy="470" rx="320" ry="120" fill="url(#aV)" opacity=".8"/></g>
{blob_anim(250, 400, 200, 3, 19, "url(#aB)", .9)}{blob_anim(700, 110, 170, 11, 23, "url(#aC)", .7)}
<g mask="url(#bmM)"><g class="bm"><polygon points="440,-10 500,-10 700,{H} 380,{H}" fill="url(#bmH)"/></g><g class="bm" style="animation-duration:23s;animation-direction:alternate-reverse"><polygon points="520,-10 560,-10 860,{H} 640,{H}" fill="url(#bmH)" opacity=".7"/></g></g>
<g fill="#FECDD3" opacity=".45" class="d1">{stars(46, 3, W, H, .5, 1.1)}</g>
<g fill="#FFE4E6" opacity=".65" class="d2">{stars(22, 8, W, H, .9, 1.6)}</g>
<g class="a1" style="animation-duration:19s"><circle class="br" cx="730" cy="228" r="215" fill="url(#aE)"/></g>
<g transform="translate(730,228)"><g class="rot" style="animation-duration:160s">{rays}</g></g>
<circle cx="730" cy="228" r="98" fill="#07050A"/><circle cx="730" cy="228" r="98" fill="none" stroke="url(#rim)" stroke-width="2.5"/><circle cx="730" cy="228" r="98" fill="none" stroke="#FB923C" stroke-opacity=".45" stroke-width="10" filter="url(#blur6)"/><g filter="url(#plasma)"><circle cx="730" cy="228" r="106" fill="none" stroke="#F97316" stroke-width="8" stroke-opacity=".9"/><circle cx="730" cy="228" r="113" fill="none" stroke="#EF4444" stroke-width="5" stroke-opacity=".7"/></g>
<ellipse cx="730" cy="228" rx="205" ry="82" transform="rotate(-18 730 228)" fill="none" stroke="#FB7185" stroke-opacity=".35" stroke-dasharray="2 9" stroke-linecap="round"/>
<ellipse cx="730" cy="228" rx="150" ry="52" transform="rotate(-18 730 228)" fill="none" stroke="#FDA4AF" stroke-opacity=".18"/>
<g class="mo"><circle r="4" fill="#fff"><animateMotion dur="38s" repeatCount="indefinite" path="M525,228a205,82 0 1,0 410,0a205,82 0 1,0 -410,0" rotate="auto"/></circle></g>
{embers(26, 4, W, H)}
<g class="sh"><g style="animation:shoot 14s cubic-bezier(.3,.6,.4,1) 3s infinite"><path d="M840,50l70,-35" stroke="#FFE4E6" stroke-width="1.8" stroke-linecap="round" opacity=".9"/></g><g style="animation:shoot 21s cubic-bezier(.3,.6,.4,1) 11s infinite"><path d="M600,18l60,-30" stroke="#FDBA74" stroke-width="1.5" stroke-linecap="round" opacity=".9"/></g></g>
{con}
{c}
<g class="in" style="animation-delay:.1s"><rect x="60" y="54" width="248" height="34" rx="17" fill="url(#gl)" stroke="#FDA4AF" stroke-opacity=".3"/>
<circle cx="80" cy="71" r="4" fill="#4ADE80"/><circle cx="80" cy="71" r="4" fill="#4ADE80" class="pu"/>
<text class="m" x="95" y="76" font-size="12.5" fill="#FFE0E4" textLength="198" lengthAdjust="spacing">OPEN TO OPPORTUNITIES</text></g>
<g class="in" style="animation-delay:.3s"><text x="60" y="214" font-size="104" font-weight="300" textLength="470" lengthAdjust="spacing" fill="#FFF1F2">THIAGO</text></g>
<g class="in" style="animation-delay:.5s"><text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="#EF4444" filter="url(#blur14)" opacity=".6">SARCO</text>
<text x="60" y="318" font-size="112" font-weight="900" textLength="470" lengthAdjust="spacing" fill="url(#nm)" filter="url(#lit)">SARCO</text>
<g mask="url(#nmask)" class="mo"><rect y="200" width="120" height="130" fill="url(#sw)" transform="skewX(-16)"><animateTransform attributeName="transform" type="translate" values="-260 0;760 0;760 0" keyTimes="0;.32;1" dur="9s" begin="2.2s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1"/></rect></g></g>
<g class="in" style="animation-delay:.8s"><rect x="60" y="346" width="64" height="3" rx="1.5" fill="url(#acc)"/>
<text class="m" x="60" y="382" font-size="15" fill="#FDA4AF" textLength="470" lengthAdjust="spacing">SOFTWARE DEVELOPER IN TRAINING</text>
<text class="p1" x="60" y="414" font-size="19" fill="{MU}">Learning by building &#183; Argentina</text><text class="p2" x="60" y="414" font-size="19" fill="{MU}" style="opacity:0">Java &#183; JavaScript &#183; SQL &#183; Web</text><text class="p3" x="60" y="414" font-size="19" fill="{MU}" style="opacity:0">Looking for my first professional experience</text></g>'''
    return svg(W, H, 'Thiago Sarco, software developer in training from Argentina, open to opportunities', b, defs, css)


# ============================================================ STATUS strip
def status():
    W, H = 900, 128
    cols = [('STATUS', 'Open to work', '#4ADE80'), ('LOOKING FOR', 'First experience', '#F97316'), ('BASED IN', 'Argentina &#183; UTC&#8722;3', '#FB7185'), ('FOCUS', 'Java &#183; Web &#183; SQL', '#F472B6')]
    d, o, c = slab(W, H, 22, uid='st', extra='<ellipse cx="450" cy="150" rx="520" ry="90" fill="url(#aB)" opacity=".7"/>')
    b = o + '<g class="mo"><polygon points="0,0 90,0 50,128 -40,128" fill="#fff" fill-opacity=".06"><animateTransform attributeName="transform" type="translate" values="-160 0;1000 0;1000 0" keyTimes="0;.35;1" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></polygon></g>' + c
    for i, (lab, val, col) in enumerate(cols):
        x = 34 + i * 218
        if i:
            b += f'<path d="M{x - 22},28V100" stroke="#FDA4AF" stroke-opacity=".18"/>'
        dot = (f'<circle cx="{x + 5}" cy="{50 - 4}" r="4.5" fill="{col}"/><circle cx="{x + 5}" cy="46" r="4.5" fill="{col}" class="pu" style="animation-delay:-{i * .7}s"/>' if i == 0
               else f'<circle cx="{x + 5}" cy="46" r="4" fill="{col}" opacity=".9"/>')
        b += (f'<g class="in" style="animation-delay:{.15 + i * .12:.2f}s">{dot}<text class="m" x="{x + 18}" y="51" font-size="12.5" fill="{MU}" textLength="{len(lab) * 9.2:.0f}" lengthAdjust="spacing">{lab}</text>'
              f'<text x="{x}" y="88" font-size="22" font-weight="700" fill="{TX}">{val}</text></g>')
    b += '<path d="M24,112 h40' + ''' l14,0 l5,-4 l5,4 l8,0 l4,-22 l8,34 l6,-16 l5,4 l16,0 h60 l14,0 l5,-4 l5,4 l8,0 l4,-22 l8,34 l6,-16 l5,4 l16,0 h60 l14,0 l5,-4 l5,4 l8,0 l4,-22 l8,34 l6,-16 l5,4 l16,0 h60 l14,0 l5,-4 l5,4 l8,0 l4,-22 l8,34 l6,-16 l5,4 l16,0 h60 l14,0 l5,-4 l5,4 l8,0 l4,-22 l8,34 l6,-16 l5,4 l16,0 h60''' + '" pathLength="1000" fill="none" stroke="#4ADE80" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="120 880" class="ecg"/>'
    css = '@keyframes ec{from{stroke-dashoffset:120}to{stroke-dashoffset:-1000}}.ecg{animation:ec 5.5s cubic-bezier(.4,0,.3,1) infinite}'
    return svg(W, H, 'Status: open to work, looking for a first professional experience, based in Argentina (UTC-3), focus on Java, web and SQL', b, d, css)


# ============================================================ ABOUT (chamfered slab + tilted terminal)
def about():
    W, H = 900, 400
    d, o, c = slab(W, H, 26, cut=90, uid='ab', extra='<ellipse cx="120" cy="400" rx="380" ry="190" fill="url(#aB)" opacity=".8"/><ellipse cx="800" cy="60" rx="260" ry="150" fill="url(#aV)" opacity=".7"/>')
    lines = [('$ whoami', '#FDBA74'), ('thiago_sarco  &#183;  dev in training', '#FFE4E6'), ('$ cat focus.txt', '#FDBA74'), ('&gt; Java &#183; OOP', '#D1A5AE'), ('&gt; HTML &#183; CSS &#183; JavaScript', '#D1A5AE'),
             ('&gt; SQL &#183; data modeling', '#D1A5AE'), ('$ git status', '#FDBA74'), ('&gt; open to opportunities', '#4ADE80')]
    term = ''
    for i, (t, col) in enumerate(lines):
        term += (f'<text class="m" x="22" y="{70 + i * 25}" font-size="14.5" fill="{col}" style="animation:L{i} 24s linear infinite">{t}</text>')
    css = ''.join(f'@keyframes L{i}{{0%,{(.6 + i * .55) / .24:.2f}%{{opacity:0}}{(.6 + i * .55) / .24 + .01:.2f}%,93%{{opacity:1}}97%,100%{{opacity:0}}}}' for i in range(8))
    css += '@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1.1s steps(1) infinite}.ul{stroke-dasharray:1;animation:draw 1.4s cubic-bezier(.5,0,.2,1) 1.1s both}'
    b = f'''{o}<g fill="#FECDD3" opacity=".5">{stars(30, 11, W, H, .5, 1.1, 0, 0)}</g>{c}
<g class="in"><text class="m" x="56" y="74" font-size="13" fill="#F97316" textLength="150" lengthAdjust="spacing">01 &#8212; ABOUT ME</text>
<text x="54" y="150" font-size="62" font-weight="300" fill="{TX}">I learn</text>
<text x="54" y="222" font-size="68" font-weight="900" fill="url(#txt)" textLength="410" lengthAdjust="spacing">by building.</text>
<path class="ul" pathLength="1" d="M56,240C140,250 300,232 460,242" stroke="url(#acc)" stroke-width="4" stroke-linecap="round" fill="none"/>
<text x="56" y="292" font-size="16.5" fill="{MU}">Software Development student combining academic</text>
<text x="56" y="318" font-size="16.5" fill="{MU}">learning with continuous practice. Into software and</text>
<text x="56" y="344" font-size="16.5" fill="{MU}">web development, databases and problem solving.</text></g>
<g transform="translate(528,76) rotate(2)" filter="url(#sh)"><g class="in" style="animation-delay:.3s">
<rect width="336" height="268" rx="16" fill="#0B0508" fill-opacity=".82" stroke="#FDA4AF" stroke-opacity=".3"/>
<rect width="336" height="34" rx="16" fill="#fff" fill-opacity=".06"/><path d="M16,.8H320" stroke="#fff" stroke-opacity=".45"/>
<circle cx="20" cy="17" r="5" fill="#F87171"/><circle cx="38" cy="17" r="5" fill="#FBBF24"/><circle cx="56" cy="17" r="5" fill="#4ADE80"/>
<text class="m" x="168" y="21" font-size="11.5" fill="#A07C84" text-anchor="middle">thiago@argentina: ~</text>
{term}<g style="animation:L7 24s linear infinite"><rect class="cur" x="22" y="{70 + 8 * 25 - 12}" width="9" height="16" fill="#FDBA74" style="animation-delay:5s"/></g></g></g>'''
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
    b = (f'<g mask="url(#mk)">{row(60, 54, "r1", 95, False, "fill=\"#EF4444\" fill-opacity=\".92\"")}'
         f'{row(128, 54, "r2", 120, True, "fill=\"none\" stroke=\"#EF4444\" stroke-width=\"1.6\" stroke-opacity=\".8\"")}</g>')
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
    defs = ('<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#DC2626"/><stop offset="1" stop-color="#EA580C"/></linearGradient>'
            f'<linearGradient id="lg" x1="{1 if right else 0}" y1="0" x2="{0 if right else 1}" y2="0"><stop offset="0" stop-color="#EF4444" stop-opacity=".9"/><stop offset="1" stop-color="#EF4444" stop-opacity="0"/></linearGradient>')
    sx0, sx1 = (880, 20) if right else (20, 880)
    b = f'''<g class="in" style="animation-delay:{i * .05:.2f}s">
<text x="{6 if right else W - 6}" y="78" font-size="104" font-weight="900" text-anchor="{"start" if right else "end"}" fill="none" stroke="#EF4444" stroke-opacity=".3" stroke-width="1.4" style="animation:dd 2.6s cubic-bezier(.4,0,.2,1) both">{n}</text>
<text class="m" x="{x}" y="30" font-size="12.5" text-anchor="{anc}" fill="#EF4444" letter-spacing="3.2">SECTION {n}</text>
<text x="{x}" y="66" font-size="38" font-weight="800" text-anchor="{anc}" fill="url(#tg)" letter-spacing="-.5">{esc(title)}</text></g>
<rect x="4" y="86" width="892" height="1.6" rx=".8" fill="url(#lg)"/>
<circle r="3" cy="86.8" fill="#F97316" class="mo"><animate attributeName="cx" values="{sx0};{sx1};{sx1}" keyTimes="0;.55;1" dur="{9 + i % 4 * 2}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .2 1;0 0 1 1"/>
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.5;.58;1" dur="{9 + i % 4 * 2}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite"/></circle>'''
    return svg(W, H, f'Section {n}: {title}', b, defs)


# ============================================================ SKILL MAP (orbits)
def chipw(t):
    return len(t) * 9.9 + 42


def chip(t, col, strong):
    w = chipw(t)
    return (f'<g transform="translate({-w / 2:.1f},-18)"><rect width="{w:.1f}" height="36" rx="18" fill="{"url(#gl)" if strong else "#16070E"}" fill-opacity="{1 if strong else .72}" stroke="{col}" stroke-opacity="{.75 if strong else .45}"/>'
            f'<circle cx="19" cy="18" r="4" fill="{col}"/><text x="31" y="24" font-size="18" font-weight="600" fill="{TX}">{t}</text></g>')


DEPTH = '@keyframes dp{0%{transform:scale(.88);opacity:.74}12.5%{transform:scale(.98);opacity:.95}25%{transform:scale(1.02);opacity:1}37.5%{transform:scale(.98);opacity:.95}50%{transform:scale(.88);opacity:.74}62.5%{transform:scale(.78);opacity:.58}75%{transform:scale(.74);opacity:.5}87.5%{transform:scale(.78);opacity:.58}100%{transform:scale(.88);opacity:.74}}.dp{animation:dp linear infinite}'


def skills():
    W, H = 900, 500
    cx, cy, ratio = 450, 244, .48
    d, o, c = slab(W, H, 30, uid='sk', extra='<ellipse cx="450" cy="244" rx="460" ry="230" fill="url(#aB)" opacity=".55"/><ellipse cx="450" cy="244" rx="150" ry="70" fill="url(#aC)"/>')
    rings = [(112, ['Java', 'JavaScript', 'SQL'], 80, 1, '#F97316', True, 20),
             (214, ['HTML', 'CSS', 'MySQL', 'Git', 'GitHub', 'C++'], 130, -1, '#FB7185', False, 0),
             (352, ['OOP', 'Data Structures', 'Database Design', 'Responsive Design', 'Problem Solving', 'Git Workflows'], 190, 1, '#F472B6', False, 45)]
    b = o + f'<g fill="#FFE4E6" opacity=".55" class="d1" style="animation:none">{stars(60, 5, W, H, .5, 1.2, 0, 0)}</g>'
    b += f'<g transform="translate({cx},{cy}) scale(1,{ratio})">'
    for R, items, per, dr, col, strong, off in rings:
        b += f'<ellipse class="fw" style="animation-duration:{per // 5}s;animation-direction:{"normal" if dr == 1 else "reverse"}" rx="{R}" ry="{R}" fill="none" stroke="{col}" stroke-opacity=".6" stroke-dasharray="3 9" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        n = len(items)
        for i, t in enumerate(items):
            a = off + 360 * i / n
            fwd, rev = ('normal', 'reverse') if dr == 1 else ('reverse', 'normal')
            b += (f'<g transform="rotate({a:.1f})"><g class="rot" style="animation-duration:{per}s;animation-direction:{fwd}"><g transform="translate({R},0)">'
                  f'<g class="rot" style="animation-duration:{per}s;animation-direction:{rev}"><g transform="rotate({-a:.1f})"><g transform="scale(1,{1 / ratio:.4f})"><g class="dp" style="animation-duration:{per}s;animation-direction:{'normal' if dr == 1 else 'reverse'};animation-delay:{(-per * a / 360) if dr == 1 else (-per * (1 - a / 360)):.2f}s">{chip(t, col, strong)}</g></g></g></g></g></g></g>')
    b += '</g>'
    # core
    b += f'''<g transform="translate({cx},{cy})"><circle r="46" fill="url(#aC)"/><circle r="34" fill="#16070E" stroke="url(#acc)" stroke-width="1.6"/><circle r="34" fill="none" stroke="#FDBA74" class="pu" style="animation-duration:4s"/><circle r="34" fill="none" stroke="#F97316" class="pu" style="animation-duration:4s;animation-delay:-2s"/>
<text y="7" font-size="20" font-weight="800" text-anchor="middle" fill="#FFF1F2" class="m">&lt;/&gt;</text></g>'''
    leg = [('#F97316', 'CORE', 'what I focus on'), ('#FB7185', 'TOOLS', 'what I build with'), ('#F472B6', 'CONCEPTS', 'what I am learning')]
    b += f'<text class="m" x="40" y="58" font-size="13" fill="#F97316" letter-spacing="3">02 &#8212; SKILL MAP</text>'
    for i, (col, a, t) in enumerate(leg):
        y = 428 + i * 22
        b += f'<circle cx="46" cy="{y - 5}" r="4.5" fill="{col}"/><text class="m" x="60" y="{y}" font-size="12.5" fill="{TX}" letter-spacing="2">{a}</text><text x="150" y="{y}" font-size="14" fill="{MU}">{t}</text>'
    b += embers(18, 9, W, H) + c
    return svg(W, H, 'Skill map: core Java, JavaScript, SQL; tools HTML, CSS, MySQL, Git, GitHub, C++; concepts OOP, data structures, database design, responsive design, problem solving, Git workflows', b, d, DEPTH)


# ============================================================ PROJECTS (3 asymmetric cards, placeholders until filled)
def project(i, big):
    p = PROJECTS[i]
    W, H = (560, 392) if big else (340, 186)
    col = ['#FB7185', '#F97316', '#F472B6'][i]
    glow = ['aB', 'aC', 'aV'][i]
    ph = p['title'] is None
    d, o, c = slab(W, H, 26 if big else 22, uid=f'p{i}', extra=f'<ellipse cx="{W * (.8 if i % 2 == 0 else .2)}" cy="{H * .2}" rx="{W * .6}" ry="{H * .5}" fill="url(#{glow})" opacity=".9"/>')
    title = esc(p['title'] or 'Your project name')
    desc = esc(p['desc'] or 'One sentence: what problem it solves.')
    stack = (p['stack'] or ['Tech 1', 'Tech 2', 'Tech 3'])[: 4 if big else 3]
    tag = 'PLACEHOLDER' if ph else 'FEATURED'
    x = 32 if big else 26
    d += '<radialGradient id="spot"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    b = o + f'<circle r="{H * .8:.0f}" fill="url(#spot)" class="mo"><animate attributeName="cx" values="{W * .1:.0f};{W * .9:.0f};{W * .1:.0f}" dur="{13 + i * 3}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/><animate attributeName="cy" values="{H * .1:.0f};{H * .9:.0f};{H * .1:.0f}" dur="{9 + i * 2}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>' + c
    b += f'<g class="in" style="animation-delay:{i * .15:.2f}s">'
    b += f'<text class="m" x="{x}" y="{46 if big else 38}" font-size="{13 if big else 12}" fill="{col}" letter-spacing="3">PROJECT 0{i + 1}</text>'
    tw_ = 112
    b += f'<rect x="{W - x - tw_}" y="{28 if big else 22}" width="{tw_}" height="24" rx="12" fill="none" stroke="{col}" stroke-opacity=".6" {"stroke-dasharray=\"4 3\"" if ph else ""}/><text class="m" x="{W - x - tw_ / 2}" y="{44 if big else 38}" font-size="11" fill="{col}" text-anchor="middle" letter-spacing="1.5">{tag}</text>'
    if big:
        # skeleton "window" preview
        b += f'<g transform="translate(32,70)"><rect width="496" height="130" rx="12" fill="#09040A" stroke="#FDA4AF" stroke-opacity=".22"/><rect width="496" height="22" rx="12" fill="#fff" fill-opacity=".05"/>'
        b += '<circle cx="14" cy="11" r="3.5" fill="#F87171"/><circle cx="28" cy="11" r="3.5" fill="#FBBF24"/><circle cx="42" cy="11" r="3.5" fill="#4ADE80"/>'
        rows = [(18, 36, [(70, 0), (120, 1)]), (36, 52, [(60, 2), (150, 0)]), (36, 68, [(110, 1), (80, 2)]), (36, 84, [(40, 0), (170, 1)]), (18, 100, [(90, 2)]), (18, 116 - 2, [(0, 0)])]
        for k, (rx, ry, segs) in enumerate(rows[:5]):
            cx_ = rx
            for sw_, ci in segs:
                b += f'<rect class="tp" x="{cx_}" y="{ry}" width="{sw_}" height="7" rx="3.5" fill="{[col, "#FDBA74", "#FFE4E6"][ci]}" fill-opacity="{[.55, .6, .35][ci]}" style="animation-delay:{.5 + k * .7:.1f}s"/>'
                cx_ += sw_ + 8
        b += f'<rect class="cur" x="{270}" y="108" width="7" height="12" fill="{col}"/>'
        b += '</g>'
        ty, dy, cy_ = 252, 286, 328
    else:
        ty, dy, cy_ = 88, 116, 152
    b += f'<text x="{x}" y="{ty}" font-size="{34 if big else 24}" font-weight="800" fill="{TX if not ph else "#F3CBD2"}">{title}</text>'
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
    return svg(W, H, lab, b, d, '@keyframes tp{0%{transform:scaleX(0)}14%,82%{transform:scaleX(1)}94%,100%{transform:scaleX(0)}}.tp{transform-box:fill-box;transform-origin:left center;animation:tp 11s cubic-bezier(.3,.7,.2,1) infinite}@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1s steps(1) infinite}')


# ============================================================ MINDSET (ascending steps)
def mindset():
    W, H = 900, 370
    data = [('01', 'Understand', 'Analyze the problem', 'before writing|the solution', '#FB7185', 200), ('02', 'Build', 'Turn ideas into', 'functional software', '#F97316', 250),
            ('03', 'Improve', 'Learn from mistakes and', 'refine the solution', '#F472B6', 300), ('04', 'Grow', 'Keep learning and take', 'on new challenges', '#4ADE80', 352)]
    defs, b = '', ''
    for i, (n, t, l1, l2, col, h) in enumerate(data):
        x, w = 8 + i * 222, 206
        y = H - h - 8
        d, o, c = slab(w, h, 20, uid=f'm{i}', extra=f'<ellipse cx="{w / 2}" cy="0" rx="{w * .8}" ry="{h * .5}" fill="{col}" opacity=".16"/>')
        defs += d
        b += (f'<g transform="translate({x},{y})" class="in" style="animation-delay:{i * .14:.2f}s"><g class="fl" style="animation-delay:-{i * 1.3:.1f}s;animation-duration:{5.5 + i * .8:.1f}s">{o}<polygon points="0,0 36,0 16,{h} -20,{h}" fill="#fff" fill-opacity=".07" class="mo"><animateTransform attributeName="transform" type="translate" values="-60 0;{w + 80} 0;{w + 80} 0" keyTimes="0;.3;1" dur="{9 + i * 1.5}s" begin="-{i * 2}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></polygon>{c}'
              f'<text x="{w - 12}" y="{h - 14}" font-size="86" font-weight="900" text-anchor="end" fill="none" stroke="{col}" stroke-opacity=".28" stroke-width="1.4">{n}</text>'
              f'<rect x="20" y="26" width="26" height="3" rx="1.5" fill="{col}"/>'
              f'<text x="20" y="66" font-size="29" font-weight="800" fill="{TX}">{t}</text>'
              +''.join(f'<text x="20" y="{96 + k * 21}" font-size="15" fill="{MU}">{ln}</text>' for k, ln in enumerate([l1] + l2.split('|'))) + '</g></g>')
    return svg(W, H, 'Development mindset: Understand, Build, Improve, Grow', b, defs)


# ============================================================ JOURNEY (flight path)
def journey():
    """git-graph timeline: main branch + feature branch, HEAD marker, commit pulses."""
    W, H = 900, 400
    main = 'M60,258H860'
    br = 'M210,258C262,258 272,166 340,166C408,166 418,258 470,258'
    d, o, c = slab(W, H, 30, uid='jo', extra='<ellipse cx="160" cy="360" rx="340" ry="170" fill="url(#aB)" opacity=".7"/><ellipse cx="780" cy="40" rx="300" ry="160" fill="url(#aV)" opacity=".7"/>')
    b = o + f'<g fill="#FECDD3" opacity=".45">{stars(36, 21, W, H, .5, 1.1, 0, 0)}</g>' + embers(10, 2, W, H) + c
    # dim future, bright past
    b += f'<path d="{main}" fill="none" stroke="#FDA4AF" stroke-opacity=".3" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/>'
    b += f'<path d="M60,258H210" pathLength="1" fill="none" stroke="#F97316" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1" style="animation:draw 1.2s cubic-bezier(.5,0,.2,1) .3s both"/><path d="M470,258H500" pathLength="1" fill="none" stroke="#DC2626" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1" style="animation:draw 1s ease 2.4s both"/>'
    b += f'<path d="{br}" pathLength="1" fill="none" stroke="#F97316" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1" style="animation:draw 2s cubic-bezier(.5,0,.2,1) .8s both"/>'
    b += f'<path d="M470,258H570" fill="none" stroke="#FDA4AF" stroke-opacity=".5" stroke-width="2.4" stroke-linecap="round"/>'
    # commit pulses travelling main -> branch -> main
    full = 'M60,258H210C262,258 272,166 340,166C408,166 418,258 470,258'
    for k, bg in enumerate((.5, .32, .16, 0)):
        b += (f'<g class="mo"><circle r="{9 + k}" fill="#F97316" opacity="{.08 * (k + 1)}"/><circle r="{1.8 + k * .5}" fill="#FFF1F2"/>'
              f'<animateMotion dur="9s" begin="-{bg}s" repeatCount="indefinite" path="{full}" keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></g>')
    nodes = [(120, 258, '01', 'Learn', 'Academic learning and', 'continuous practice', 'ONGOING', '#4ADE80', 'low', True),
             (340, 166, '02', 'Build', 'Turn ideas into', 'functional software', 'ONGOING', '#4ADE80', 'up', True),
             (570, 258, '03', 'Collaborate', 'Join a team of', 'developers', 'NEXT', '#FB7185', 'low', False),
             (790, 258, '04', 'First experience', 'Professional experience', 'in software development', 'GOAL', '#F472B6', 'low', False)]
    for i, (x, y, n, t, l1, l2, st, col, pos, done) in enumerate(nodes):
        up = pos == 'up'
        b += f'<g class="in" style="animation-delay:{.4 + i * .18:.2f}s">'
        b += f'<circle cx="{x}" cy="{y}" r="28" fill="url(#aC)" opacity="{.95 if done else .4}"/>'
        b += f'<circle cx="{x}" cy="{y}" r="17" fill="{"#16070E" if not done else "url(#acc)"}" stroke="{col}" stroke-width="2" {"" if done else "stroke-dasharray=\"4 4\""}/>'
        if done:
            b += f'<circle cx="{x}" cy="{y}" r="17" fill="none" stroke="{col}" class="pu" style="animation-delay:-{i * 1.2}s"/>'
        b += f'<text class="m" x="{x}" y="{y + 4.5}" font-size="12.5" font-weight="700" text-anchor="middle" fill="#fff">{n}</text>'
        cy0 = y - 140 if up else y + 34
        ty = cy0 + 46
        b += f'<rect x="{x - 40}" y="{cy0}" width="80" height="22" rx="11" fill="none" stroke="{col}" stroke-opacity=".6"/><text class="m" x="{x}" y="{cy0 + 15}" font-size="11" text-anchor="middle" fill="{col}" letter-spacing="1.8">{st}</text>'
        b += f'<text x="{x}" y="{ty}" font-size="22" font-weight="800" text-anchor="middle" fill="{TX}">{t}</text>'
        b += f'<text x="{x}" y="{ty + 22}" font-size="14.5" text-anchor="middle" fill="{MU}">{l1}</text><text x="{x}" y="{ty + 41}" font-size="14.5" text-anchor="middle" fill="{MU}">{l2}</text></g>'
    # branch tags + HEAD pointer
    b += f'<g class="in" style="animation-delay:1.2s"><rect x="24" y="226" width="58" height="22" rx="6" fill="#fff" fill-opacity=".08" stroke="#FDA4AF" stroke-opacity=".4"/><text class="m" x="53" y="241" font-size="12" text-anchor="middle" fill="{TX}">main</text></g>'
    b += f'<g class="in" style="animation-delay:1.4s"><rect x="262" y="140" width="92" height="22" rx="6" fill="#fff" fill-opacity=".08" stroke="#F97316" stroke-opacity=".6"/><text class="m" x="308" y="155" font-size="12" text-anchor="middle" fill="#FDBA74">feat/build</text></g>'
    b += f'<g class="fl" style="animation-delay:-1s"><g class="in" style="animation-delay:1.7s"><rect x="372" y="186" width="58" height="22" rx="11" fill="#4ADE80"/><text class="m" x="401" y="201" font-size="11.5" font-weight="700" text-anchor="middle" fill="#052E16">HEAD</text><path d="M372,197l-12,0" stroke="#4ADE80" stroke-width="2"/></g></g>'
    return svg(W, H, 'Journey as a git graph: Learn (ongoing), Build (ongoing, HEAD), Collaborate (next), First experience (goal)', b, d)



# ============================================================ OBJECTIVE
def objective():
    W, H = 900, 330
    d, o, c = slab(W, H, 30, uid='ob', extra='<ellipse class="dr" cx="780" cy="90" rx="380" ry="200" fill="url(#aC)" opacity=".8"/><ellipse cx="80" cy="330" rx="360" ry="170" fill="url(#aB)"/>')
    items = [('Learn', 'From experienced', 'developers', '#FB7185'), ('Collaborate', 'As part of', 'a team', '#F97316'), ('Contribute', 'Applying my', 'technical knowledge', '#F472B6'), ('Grow', 'Continue', 'improving', '#4ADE80')]
    b = o + blob_anim(700, 120, 190, 5, 20, 'url(#aC)', .8) + blob_anim(120, 300, 170, 9, 25, 'url(#aB)', .8) + embers(14, 12, W, H) + c
    b += f'''<g class="in"><text class="m" x="56" y="62" font-size="13" fill="#F97316" letter-spacing="3">06 &#8212; PROFESSIONAL OBJECTIVE</text>
<text x="54" y="122" font-size="44" font-weight="300" fill="{TX}" textLength="560" lengthAdjust="spacing">Looking for my first</text>
<text x="54" y="176" font-size="52" font-weight="900" fill="url(#txt)" textLength="700" lengthAdjust="spacing">professional experience</text>
<text x="56" y="208" font-size="18" fill="{MU}">in software development, joining a team where I can:</text></g>'''
    for i, (t, l1, l2, col) in enumerate(items):
        x = 56 + i * 208
        if i:
            b += f'<path d="M{x - 24},238V300" stroke="#FDA4AF" stroke-opacity=".2"/>'
        b += (f'<g class="in" style="animation-delay:{.4 + i * .12:.2f}s"><rect x="{x}" y="240" width="26" height="3" rx="1.5" fill="{col}"/>'
              f'<text x="{x}" y="270" font-size="21" font-weight="800" fill="{TX}">{t}</text><text x="{x}" y="291" font-size="14.5" fill="{MU}">{l1}</text><text x="{x}" y="309" font-size="14.5" fill="{MU}">{l2}</text></g>')
    return svg(W, H, 'Professional objective: first professional experience in software development, to learn, collaborate, contribute and grow', b, d)


# ============================================================ LANGUAGES
def languages():
    W, H = 900, 150
    d, o, c = slab(W, H, 24, uid='lg', extra='<ellipse cx="450" cy="170" rx="500" ry="90" fill="url(#aB)" opacity=".7"/>')
    css = '@keyframes shm{from{transform:translateX(-160px)}to{transform:translateX(620px)}}.shm{animation:shm 3.6s cubic-bezier(.45,0,.35,1) infinite}'
    ticks = ''.join(f'<rect x="{i * 22}" y="0" width="14" height="10" rx="3" fill="#FB7185" fill-opacity=".28"/>' for i in range(28))
    b = o + c + f'''<g class="in"><text class="m" x="40" y="52" font-size="13" fill="#F97316" letter-spacing="2.5">ES</text><text x="82" y="54" font-size="22" font-weight="800" fill="{TX}">Spanish</text>
<text class="m" x="860" y="52" font-size="12.5" text-anchor="end" fill="#4ADE80" letter-spacing="2.5">NATIVE</text><rect x="40" y="68" width="820" height="10" rx="5" fill="url(#acc)"/></g>
<g class="in" style="animation-delay:.2s"><text class="m" x="40" y="108" font-size="13" fill="#FB7185" letter-spacing="2.5">EN</text><text x="82" y="110" font-size="22" font-weight="800" fill="{TX}">English</text>
<text class="m" x="860" y="108" font-size="12.5" text-anchor="end" fill="#FB7185" letter-spacing="2.5">IMPROVING</text>
<clipPath id="ec"><rect x="40" y="124" width="620" height="10"/></clipPath><g transform="translate(40,124)">{ticks}</g>
<g clip-path="url(#ec)" class="mo"><rect x="0" y="124" width="120" height="10" fill="url(#sw2)" class="shm"/></g></g>'''
    d += '<linearGradient id="sw2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FDBA74" stop-opacity="0"/><stop offset=".5" stop-color="#FDBA74" stop-opacity=".9"/><stop offset="1" stop-color="#FDBA74" stop-opacity="0"/></linearGradient>'
    return svg(W, H, 'Languages: Spanish native, English improving', b, d, css)


# ============================================================ CONNECT
def connect_mail():
    W, H = 900, 112
    d, o, c = slab(W, H, 26, uid='cm', fill='url(#cmg)')
    d += '<linearGradient id="cmg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B91C1C"/><stop offset="1" stop-color="#C2410C"/></linearGradient><linearGradient id="sh3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    b = o + '<g class="mo"><rect y="0" width="140" height="112" fill="url(#sh3)" transform="skewX(-18)"><animateTransform attributeName="transform" type="translate" values="-260 0;1100 0;1100 0" keyTimes="0;.4;1" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/></rect></g>' + c
    b += (f'<text class="m" x="44" y="42" font-size="13" fill="#FFE4D6" letter-spacing="3">SAY HELLO &#8212; EMAIL</text><text x="42" y="82" font-size="34" font-weight="800" fill="#fff">thiagosarco13@gmail.com</text>'
          '<g transform="translate(820,56)"><circle r="26" fill="#fff" fill-opacity=".16"/><path d="M-9,0H9M2,-8L10,0L2,8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return svg(W, H, 'Email Thiago: thiagosarco13@gmail.com', b, d)


def connect_small(kind):
    W, H = 440, 92
    label, val, col, alt = (('GITHUB', 'github.com/Gothi2213', '#FB7185', 'GitHub: Gothi2213') if kind == 'gh' else ('LOCATION', 'Argentina &#183; UTC&#8722;3', '#F97316', 'Location: Argentina'))
    d, o, c = slab(W, H, 22, uid='cs', extra=f'<ellipse cx="{W * .9}" cy="0" rx="200" ry="90" fill="url(#{"aB" if kind == "gh" else "aC"})"/>')
    b = o + c + f'<g class="in"><circle cx="40" cy="46" r="5" fill="{col}"/><circle cx="40" cy="46" r="5" fill="{col}" class="pu"/><text class="m" x="62" y="38" font-size="12.5" fill="{col}" letter-spacing="3">{label}</text><text x="62" y="68" font-size="22" font-weight="800" fill="{TX}">{val}</text></g>'
    return svg(W, H, alt, b, d)


# ============================================================ FOOTER
def footer():
    W, H = 900, 210
    d, o, c = slab(W, H, 30, uid='ft')
    R, cx, cy = 340, 450, 470
    rnd = random.Random(8)
    lights = ''.join(f'<circle cx="{cx + R * .96 * math.sin(a):.0f}" cy="{cy - R * .96 * math.cos(a):.0f}" r="{rnd.uniform(.7, 1.6):.1f}" fill="#FDBA74" class="tw" style="animation-delay:-{rnd.uniform(0, 5):.1f}s;animation-duration:{rnd.uniform(3, 7):.1f}s"/>'
                     for a in [rnd.uniform(-.55, .55) for _ in range(46)] if (cy - R * .96 * math.cos(a)) < H)
    defs = (d + '<radialGradient id="pl" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#3A0F1C"/><stop offset=".25" stop-color="#14070D"/><stop offset="1" stop-color="#07050A"/></radialGradient>'
            '<radialGradient id="atm" cx=".5" cy=".5" r=".5"><stop offset=".9" stop-color="#F97316" stop-opacity=".0"/><stop offset=".965" stop-color="#FB923C" stop-opacity=".55"/><stop offset="1" stop-color="#EF4444" stop-opacity="0"/></radialGradient>')
    b = o + f'<g fill="#FECDD3" opacity=".6">{stars(60, 33, W, H, .4, 1.2, 0, 0)}</g>'
    b += f'<g class="a2"><ellipse cx="450" cy="{H}" rx="520" ry="110" fill="url(#aB)"/></g><circle cx="{cx}" cy="{cy}" r="{R + 46}" fill="url(#atm)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#pl)" stroke="#FDBA74" stroke-opacity=".55" stroke-width="1.6"/>' + lights
    b += '<g class="mo"><g><circle r="2.6" fill="#fff"/><path d="M0,0l-22,5" stroke="#fff" stroke-opacity=".5"/><animateMotion dur="26s" repeatCount="indefinite" path="M-30,110C220,20 640,20 930,120" calcMode="spline" keyTimes="0;1" keySplines=".35 0 .65 1"/></g></g>'
    b += embers(14, 14, W, H) + c
    b += f'<text x="450" y="84" font-size="42" font-weight="300" text-anchor="middle" fill="{TX}" textLength="450" lengthAdjust="spacing">THIAGO <tspan font-weight="900">SARCO</tspan></text>'
    b += f'<text class="m" x="450" y="116" font-size="13" text-anchor="middle" fill="#FDA4AF" letter-spacing="4">LEARNING BY BUILDING &#183; ARGENTINA</text>'
    return svg(W, H, 'Thiago Sarco. Learning by building. Argentina', b, defs, '.a2{animation:dr 20s ease-in-out infinite alternate}')


if __name__ == '__main__':
    out = {'hero.svg': hero(), 'status.svg': status(), 'about.svg': about(), 'marquee.svg': marquee(), 'skills.svg': skills(),
           'project-1.svg': project(0, True), 'project-2.svg': project(1, False), 'project-3.svg': project(2, False),
           'mindset.svg': mindset(), 'journey.svg': journey(), 'objective.svg': objective(), 'languages.svg': languages(),
           'connect-mail.svg': connect_mail(), 'connect-github.svg': connect_small('gh'), 'connect-location.svg': connect_small('loc'), 'footer.svg': footer()}
    for i, t in enumerate(SECTIONS):
        out[f'sec-{SLUGS[i]}.svg'] = section(i, t)
    for k, v in out.items():
        print(k, write(k, v))
