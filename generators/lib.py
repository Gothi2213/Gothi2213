"""Shared helpers for the Gothi2213 profile generators (viewBox width 900 everywhere)."""
import html, random, os

FONT = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ASSETS = os.path.join(ROOT, 'assets')
esc = lambda s: html.escape(str(s), quote=True)

BASE_CSS = f"""
text{{font-family:{FONT}}} .m{{font-family:{MONO}}}
@keyframes in{{from{{opacity:0;transform:translateY(16px)}}}}
@keyframes fade{{from{{opacity:0}}}}
@keyframes rot{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.7}}70%,100%{{transform:scale(3.2);opacity:0}}}}
@keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.in{{animation:in 1s cubic-bezier(.2,.8,.2,1) both}}
.rot{{animation:rot linear infinite;transform-origin:0 0}}
.pu{{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s cubic-bezier(.2,.6,.3,1) infinite}}
.tw{{animation:tw 5s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}} .mo{{display:none}}}}
"""

# shared gradients / filters. ids are prefixed so several can coexist.
DEFS = """
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07050A"/><stop offset=".6" stop-color="#16070E"/><stop offset="1" stop-color="#2E0A16"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FDA4AF" stop-opacity=".55"/><stop offset=".45" stop-color="#FB7185" stop-opacity=".06"/><stop offset="1" stop-color="#F97316" stop-opacity=".35"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF1F2"/><stop offset=".55" stop-color="#FDA4AF"/><stop offset="1" stop-color="#FDBA74"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#DC2626"/><stop offset="1" stop-color="#F97316"/></linearGradient>
<radialGradient id="aB"><stop offset="0" stop-color="#DC2626" stop-opacity=".55"/><stop offset="1" stop-color="#DC2626" stop-opacity="0"/></radialGradient>
<radialGradient id="aC"><stop offset="0" stop-color="#F97316" stop-opacity=".38"/><stop offset="1" stop-color="#F97316" stop-opacity="0"/></radialGradient>
<radialGradient id="aV"><stop offset="0" stop-color="#F472B6" stop-opacity=".4"/><stop offset="1" stop-color="#F472B6" stop-opacity="0"/></radialGradient>
<filter id="fn" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 -.18"/></filter>
<pattern id="gr" width="160" height="160" patternUnits="userSpaceOnUse"><rect width="160" height="160" filter="url(#fn)" opacity=".5"/></pattern>
<filter id="blur6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="blur14" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".55"/></filter>
"""


def svg(w, h, label, body, defs='', css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><defs>{DEFS}{defs}</defs><style>{BASE_CSS}{css}</style>{body}</svg>')


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    p = os.path.join(ASSETS, name)
    open(p, 'w', encoding='utf-8').write(content)
    return len(content.encode())


def slab_path(w, h, r=26, cut=0):
    """rounded slab; cut>0 chamfers the top-right corner (breaks the 'same rounded card' look)."""
    if not cut:
        return f'M{r},0H{w - r}Q{w},0 {w},{r}V{h - r}Q{w},{h} {w - r},{h}H{r}Q0,{h} 0,{h - r}V{r}Q0,0 {r},0Z'
    return f'M{r},0H{w - cut}L{w},{cut}V{h - r}Q{w},{h} {w - r},{h}H{r}Q0,{h} 0,{h - r}V{r}Q0,0 {r},0Z'


def slab(w, h, r=26, cut=0, uid='s', fill='url(#bg)', extra=''):
    """returns (defs, open_group, close_group): content between is clipped to the slab; grain + rim light on top."""
    d = slab_path(w, h, r, cut)
    defs = f'<clipPath id="{uid}"><path d="{d}"/></clipPath>'
    o = f'<g clip-path="url(#{uid})"><rect width="{w}" height="{h}" fill="{fill}"/>{extra}'
    c = (f'<rect width="{w}" height="{h}" fill="url(#gr)" opacity=".35" style="mix-blend-mode:soft-light"/></g>'
         f'<path d="{d}" fill="none" stroke="url(#hl)" stroke-width="1.5"/>')
    return defs, o, c


def stars(n, seed, w, h, rmin, rmax, x0=-60, x1=60):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.uniform(x0, w + x1):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(rmin, rmax):.1f}"/>' for _ in range(n))


def glass(x, y, w, h, r=14, op=1):
    return (f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#gl)" stroke="#FDA4AF" stroke-opacity=".25"/>'
            f'<path d="M{x + r},{y + .8}H{x + w - r}" stroke="#fff" stroke-opacity=".5" stroke-linecap="round"/></g>')


BASE_CSS += """
@keyframes rise{0%{transform:translate(0,0) scale(1);opacity:0}12%{opacity:.95}100%{transform:translate(var(--dx,20px),var(--dy,-260px)) scale(.3);opacity:0}}
@keyframes shoot{0%,84%{transform:translate(0,0);opacity:0}86%{opacity:1}100%{transform:translate(-360px,180px);opacity:0}}
@keyframes flt{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes flow{to{stroke-dashoffset:-120}}
@keyframes breathe{0%,100%{transform:scale(1);opacity:.85}50%{transform:scale(1.08);opacity:1}}
@keyframes dr{to{transform:translate(60px,24px)}}
@keyframes dd{from{stroke-dasharray:0 700}to{stroke-dasharray:700 0}}
@keyframes ph{0%{opacity:0;transform:translateY(10px)}6%,30%{opacity:1;transform:none}36%,100%{opacity:0;transform:translateY(-10px)}}
.em{animation:rise linear infinite}.fl{animation:flt 6s cubic-bezier(.45,0,.55,1) infinite}.fw{animation:flow 9s linear infinite}
.br{transform-box:fill-box;transform-origin:center;animation:breathe 7s cubic-bezier(.45,0,.55,1) infinite}.dr{animation:dr 24s ease-in-out infinite alternate}
@media (prefers-reduced-motion:reduce){.em,.sh,.p2,.p3{display:none}}
"""


def embers(n, seed, w, h, cols=('#FB923C', '#FDBA74', '#F87171', '#FDA4AF')):
    r = random.Random(seed)
    out = ''
    for _ in range(n):
        dur = r.uniform(7, 15)
        out += (f'<circle class="em" cx="{r.uniform(0, w):.0f}" cy="{h + 8}" r="{r.uniform(.8, 2.3):.1f}" fill="{r.choice(cols)}" '
                f'style="--dx:{r.uniform(-60, 60):.0f}px;--dy:-{r.uniform(.45, .95) * h:.0f}px;animation-duration:{dur:.1f}s;animation-delay:-{r.uniform(0, dur):.1f}s"/>')
    return out


import math


def _smooth(pts):
    n = len(pts)
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f'C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + 'Z'


def blob(cx, cy, r, seed, n=7):
    rnd = random.Random(seed)
    return _smooth([(cx + r * rnd.uniform(.7, 1.25) * math.cos(2 * math.pi * k / n), cy + r * rnd.uniform(.7, 1.25) * math.sin(2 * math.pi * k / n)) for k in range(n)])


def blob_anim(cx, cy, r, seed, dur, fill, op=.5):
    """morphing liquid blob (SMIL path morph, same command structure so it interpolates)."""
    ds = [blob(cx, cy, r, seed + k * 7) for k in range(3)]
    vals = ';'.join(ds + [ds[0]])
    return (f'<path d="{ds[0]}" fill="{fill}" opacity="{op}" class="mo"><animate attributeName="d" values="{vals}" dur="{dur}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></path>')
