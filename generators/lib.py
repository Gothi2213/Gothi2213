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
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060A13"/><stop offset=".6" stop-color="#0A1330"/><stop offset="1" stop-color="#0F1D45"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#93C5FD" stop-opacity=".55"/><stop offset=".45" stop-color="#60A5FA" stop-opacity=".06"/><stop offset="1" stop-color="#22D3EE" stop-opacity=".35"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#EAF2FF"/><stop offset=".55" stop-color="#93C5FD"/><stop offset="1" stop-color="#67E8F9"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="#22D3EE"/></linearGradient>
<radialGradient id="aB"><stop offset="0" stop-color="#2563EB" stop-opacity=".55"/><stop offset="1" stop-color="#2563EB" stop-opacity="0"/></radialGradient>
<radialGradient id="aC"><stop offset="0" stop-color="#22D3EE" stop-opacity=".38"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
<radialGradient id="aV"><stop offset="0" stop-color="#A78BFA" stop-opacity=".4"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/></radialGradient>
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
    return (f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#gl)" stroke="#93C5FD" stroke-opacity=".25"/>'
            f'<path d="M{x + r},{y + .8}H{x + w - r}" stroke="#fff" stroke-opacity=".5" stroke-linecap="round"/></g>')
