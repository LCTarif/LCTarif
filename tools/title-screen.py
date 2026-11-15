"""Draws assets/title-screen.svg, the animated title card at the top of the profile README.

It is painted flat in বেপরোয়া's rickshaw-art colours: no gradients and no glow.
A rainy night street with a Dhaka-like skyline, load-shedding windows, and a
police car chasing a red car on the left side of the road.
Fonts are embedded from বেপরোয়া's bundled woff2 files, so the card looks the same everywhere.

Run from the repo root:  python tools/title-screen.py
"""
import base64
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT.parent / 'beporowa' / 'public' / 'fonts'
OUT = ROOT / 'assets' / 'title-screen.svg'

W, H = 1280, 420
SOOT, TIN, TOMATO, MARIGOLD, TEAL, INDIGO = '#1b1410', '#efe3c8', '#d8402b', '#f2a20c', '#0f7f7a', '#1d2a5b'
FAR, NEAR, DARK_WINDOW, KERB = '#2a3566', '#15111d', '#2b2333', '#3a2e2a'
STREET = 318
rng = random.Random(7)


def font(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode('ascii')


def star(x, y, s):
    k = s * 0.3
    return (f'M{x} {y - s}L{x + k} {y - k}L{x + s} {y}L{x + k} {y + k}'
            f'L{x} {y + s}L{x - k} {y + k}L{x - s} {y}L{x - k} {y - k}Z')


def car(body, band, glass, extra=''):
    """A small car facing left, drawn at 0,0; about 132 wide and 45 tall."""
    return f'''
      <polygon points="2,18 -96,6 -96,36" fill="{MARIGOLD}" opacity=".16"/>
      <path d="M4 30V20Q6 14 16 12L34 10L50-2Q54-6 62-6H100Q108-6 112 0L122 12L128 14Q132 16 132 22V30Z"
            fill="{body}" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M53 9L61 0H82V9ZM87 9V0H100L107 9Z" fill="{glass}" stroke="#000" stroke-width="2"/>
      <rect x="8" y="17" width="120" height="5" fill="{band}" stroke="#000" stroke-width="1.5"/>
      <rect x="1" y="15" width="6" height="6" fill="{MARIGOLD}" stroke="#000" stroke-width="1.5"/>
      <rect x="127" y="15" width="5" height="7" fill="{TOMATO}" stroke="#000" stroke-width="1.5"/>
      <circle cx="30" cy="30" r="9" fill="#000"/><circle cx="30" cy="30" r="3" fill="{TIN}"/>
      <circle cx="104" cy="30" r="9" fill="#000"/><circle cx="104" cy="30" r="3" fill="{TIN}"/>{extra}'''


s = []
add = s.append

add(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">LC Tarif, player one</title>
<desc id="d">An arcade title screen painted in rickshaw-art colours. A rainy night street in a Dhaka-like city, with a minaret, a বেপরোয়া signboard and windows that go dark in load-shedding. A police car chases a red car along the road. The title reads তারিফুল হক, LC Tarif, game developer, Dhaka, press start.</desc>
<defs>
<style>
@font-face{{font-family:Galada;src:url(data:font/woff2;base64,{font('galada-bengali-400-normal.woff2')}) format('woff2')}}
@font-face{{font-family:Anek;font-weight:800;src:url(data:font/woff2;base64,{font('anek-bangla-latin-800-normal.woff2')}) format('woff2')}}
.bn{{font-family:Galada,serif}}
.lat{{font-family:Anek,'Arial Black',sans-serif;font-weight:800}}
.rain{{animation:rain .8s linear infinite}}
.drive{{animation:drive 9s linear infinite both}}
.cop{{animation-delay:1.1s}}
.shed{{animation:shed 7s linear infinite}}
.tw{{animation:tw 2.4s ease-in-out infinite alternate}}
.sh{{animation:sh 1.6s ease-in-out infinite alternate}}
.blink{{animation:blink 1.2s linear infinite}}
.sa{{animation:sa .5s linear infinite}}
.sb{{animation:sa .5s linear infinite reverse}}
@keyframes rain{{from{{transform:translateY(0)}}to{{transform:translateY({H}px)}}}}
@keyframes drive{{0%{{transform:translateX(1330px)}}75%,100%{{transform:translateX(-430px)}}}}
@keyframes shed{{0%,68%{{opacity:1}}70%,84%{{opacity:.08}}86%,100%{{opacity:1}}}}
@keyframes tw{{from{{opacity:.35}}to{{opacity:1}}}}
@keyframes sh{{from{{opacity:.2}}to{{opacity:.6}}}}
@keyframes blink{{0%,55%{{opacity:1}}58%,100%{{opacity:0}}}}
@keyframes sa{{0%,49%{{fill:{TOMATO}}}50%,100%{{fill:#3d6cd8}}}}
@media (prefers-reduced-motion:reduce){{
  .rain,.drive,.shed,.tw,.sh,.blink,.sa,.sb{{animation:none!important}}
  .drive{{transform:translateX(700px)}}
  .cop{{transform:translateX(900px)}}
}}
</style>
<clipPath id="scene"><rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="12"/></clipPath>
<mask id="moon"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="1166" cy="104" r="28" fill="#000"/></mask>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="#000"/>
<g clip-path="url(#scene)">
<rect width="{W}" height="{H}" fill="{INDIGO}"/>''')

# Stars and the moon.
for i, (x, y, r) in enumerate([(560, 92, 6), (700, 150, 4), (730, 82, 5), (812, 120, 4), (1040, 74, 6), (1236, 160, 5), (520, 160, 4)]):
    add(f'<path class="tw" style="animation-delay:{i * 0.37:.2f}s" d="{star(x, y, r)}" fill="{TIN}"/>')
add(f'<circle cx="1150" cy="118" r="32" fill="{MARIGOLD}" stroke="#000" stroke-width="3" mask="url(#moon)"/>')

# Far skyline, with a minaret.
d = [f'M8 {STREET}']
x = 8
while x < W:
    w = rng.randint(40, 90)
    # Keep the far skyline low behind the title on the left.
    top = rng.randint(278, 296) if x < 520 else rng.randint(226, 274)
    d.append(f'V{top}H{min(x + w, W)}')
    x += w
d.append(f'V{STREET}Z')
add(f'<path d="{"".join(d)}" fill="{FAR}" stroke="#000" stroke-width="2"/>')
add(f'''<path d="M628 {STREET}V196H622V188H652V196H646V{STREET}Z M626 188L637 162L648 188Z M637 162V150" fill="{FAR}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>
<circle cx="637" cy="148" r="3" fill="{MARIGOLD}" stroke="#000" stroke-width="1.5"/>''')

# Near buildings with windows; some lose power now and then.
buildings = [(12, 70, 292), (82, 56, 300), (138, 84, 286), (222, 60, 296), (282, 90, 288), (372, 64, 272),
             (436, 80, 252), (516, 70, 228), (586, 96, 240), (682, 64, 208), (746, 110, 224),
             (856, 150, 178), (1006, 80, 214), (1086, 104, 194), (1190, 82, 232)]
shed = {3: 0.0, 7: 2.3, 10: 4.6, 13: 1.2}
lit_windows = []
for i, (bx, bw, top) in enumerate(buildings):
    add(f'<rect x="{bx}" y="{top}" width="{bw}" height="{STREET - top + 2}" fill="{NEAR}" stroke="#000" stroke-width="2"/>')
    cols, rows = (bw - 10) // 18, (STREET - top - 14) // 22
    cls = f' class="shed" style="animation-delay:{shed[i]}s"' if i in shed else ''
    add(f'<g{cls}>')
    for r in range(rows):
        for c in range(cols):
            wx, wy = bx + 9 + c * 18, top + 10 + r * 22
            roll = rng.random()
            colour = MARIGOLD if roll < 0.45 else TIN if roll < 0.58 else DARK_WINDOW
            add(f'<rect x="{wx}" y="{wy}" width="8" height="11" fill="{colour}"/>')
            if colour != DARK_WINDOW and r >= rows - 2:
                lit_windows.append(wx)
    add('</g>')

# A hand-painted tin signboard on the tallest roof.
add(f'''<path d="M876 160V178M986 160V178" stroke="#000" stroke-width="4"/>
<rect x="846" y="112" width="170" height="50" fill="{TIN}" stroke="#000" stroke-width="3"/>
<rect x="852" y="118" width="158" height="38" fill="none" stroke="{TOMATO}" stroke-width="2"/>
<text x="931" y="148" text-anchor="middle" class="bn" font-size="31" fill="{TOMATO}">বেপরোয়া</text>''')

# The street: kerb, wet road, lane marks and window light in the puddles.
add(f'<rect x="0" y="{STREET}" width="{W}" height="9" fill="{KERB}" stroke="#000" stroke-width="2"/>')
add(f'<rect x="0" y="{STREET + 9}" width="{W}" height="{H - STREET - 9}" fill="{SOOT}"/>')
for x in range(26, W, 84):
    add(f'<rect x="{x}" y="362" width="42" height="4" fill="{TIN}" opacity=".5"/>')
for i, wx in enumerate(sorted(set(lit_windows))[::3]):
    add(f'<rect class="sh" style="animation-delay:{(i % 5) * 0.31:.2f}s" x="{wx - 3}" y="{334 + (i * 7) % 20}" width="{rng.randint(12, 24)}" height="2" fill="{MARIGOLD}"/>')

# A red car with the police on its tail, driving on the left.
add(f'<g class="drive"><g transform="translate(0 362)">{car(TOMATO, MARIGOLD, TEAL)}</g></g>')
add(f'''<g class="drive cop"><g transform="translate(0 362)">{car(TIN, INDIGO, '#9fb7c9', f"""
      <rect class="sa" x="64" y="-12" width="12" height="6" fill="{TOMATO}" stroke="#000" stroke-width="1.5"/>
      <rect class="sb" x="78" y="-12" width="12" height="6" fill="#3d6cd8" stroke="#000" stroke-width="1.5"/>""")}</g></g>''')

# Rain, two stacked copies so the fall loops without a seam.
drops = []
for _ in range(80):
    x, y, ln = rng.randint(0, W), rng.randint(0, H), rng.randint(16, 30)
    drops.append(f'<path d="M{x} {y}l-5 {ln}"/>')
add(f'<g class="rain" stroke="{TIN}" stroke-width="1.5" stroke-linecap="round" opacity=".24"><g id="drops">{"".join(drops)}</g><use href="#drops" y="-{H}"/></g>')

# Title block.
add(f'''<text x="60" y="98" class="lat" font-size="15" letter-spacing="5" fill="{TIN}">PLAYER 1 · READY</text>
<text x="61" y="195" class="bn" font-size="92" fill="{TOMATO}" stroke="#000" stroke-width="3" paint-order="stroke">তারিফুল হক</text>
<text x="56" y="190" class="bn" font-size="92" fill="{MARIGOLD}" stroke="#000" stroke-width="3" paint-order="stroke">তারিফুল হক</text>
<text x="62" y="244" class="lat" font-size="38" letter-spacing="10" fill="{TIN}" stroke="#000" stroke-width="2" paint-order="stroke">LC TARIF</text>
<text x="64" y="274" class="lat" font-size="15" letter-spacing="4" fill="{MARIGOLD}" stroke="#000" stroke-width="2" paint-order="stroke">GAME DEVELOPER · DHAKA</text>
<rect x="56" y="328" width="244" height="36" rx="3" fill="#000" stroke="{TOMATO}" stroke-width="3"/>
<g class="blink"><path d="M74 337L89 346L74 355Z" fill="{MARIGOLD}"/>
<text x="100" y="354" class="lat" font-size="19" letter-spacing="4" fill="{MARIGOLD}">PRESS START</text></g>''')

# Arcade score strip along the top.
add(f'''<rect x="0" y="0" width="{W}" height="54" fill="#000"/>
<text x="40" y="41" class="lat" font-size="17" letter-spacing="3"><tspan fill="{TOMATO}">1UP</tspan><tspan fill="{TIN}" dx="12">LC TARIF</tspan></text>
<text x="{W // 2}" y="41" text-anchor="middle" class="lat" font-size="17" letter-spacing="3"><tspan fill="{TIN}">STAGE</tspan><tspan fill="{MARIGOLD}" dx="10">7/7</tspan><tspan fill="{TIN}" dx="10">CLEARED</tspan></text>
<text x="{W - 40}" y="41" text-anchor="end" class="lat" font-size="17" letter-spacing="3"><tspan fill="{TIN}">NEXT</tspan><tspan fill="{MARIGOLD}" dx="10">GO LIVE</tspan></text>
</g>
<rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="9" fill="none" stroke="{TOMATO}" stroke-width="3"/>
</svg>
''')

OUT.write_text('\n'.join(s), encoding='utf-8')
print(OUT, OUT.stat().st_size // 1024, 'KB')
