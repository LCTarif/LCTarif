"""Draws assets/title-screen-navy.svg, the animated title card at the top of the profile README.

A Dhaka street at night in dark navy and gold, the same palette as the LinkedIn card:
flat navy bands in the sky, a ringed gold sun with turning rays, navy building fronts
with lit windows, striped kerbs, and a police car chasing a red car on the left of the road.
Fonts are embedded from বেপরোয়া's bundled woff2 files, so the card looks the same everywhere.

Run from the repo root:  python tools/title-screen.py
"""
import base64
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT.parent / 'beporowa' / 'public' / 'fonts'
OUT = ROOT / 'assets' / 'title-screen-navy.svg'

W, H = 1280, 420
SOOT, TIN, TOMATO, MARIGOLD, TEAL, INDIGO = '#070d1d', '#f3efe6', '#d8402b', '#2a4180', '#2a4180', '#11204a'
SUN, CREAM, RANI = '#e9b44c', '#f3efe6', '#b8862f'
SKY = ['#060c1c', '#081127', '#0b1630', '#0e1b3a', '#112045', '#14264f', '#182c5a']
FAR = '#0e1838'
FRONTS = ['#1a2c5e', '#22386f', '#14224a', '#2a4180', '#1d3266', '#26407a']
CORNICE, DARK_NAVY, MUTED = '#3a5291', '#0b1630', '#9aabcb'
STREET = 318
SUN_X, SUN_Y = 1150, 150
rng = random.Random(11)


def font(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode('ascii')


def car(body, band, glass, extra=''):
    """A small car facing left, drawn at 0,0; about 132 wide and 45 tall."""
    return f'''
      <polygon points="2,18 -96,6 -96,36" fill="{SUN}" opacity=".22"/>
      <path d="M4 30V20Q6 14 16 12L34 10L50-2Q54-6 62-6H100Q108-6 112 0L122 12L128 14Q132 16 132 22V30Z"
            fill="{body}" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M53 9L61 0H82V9ZM87 9V0H100L107 9Z" fill="{glass}" stroke="#000" stroke-width="2"/>
      <rect x="8" y="17" width="120" height="5" fill="{band}" stroke="#000" stroke-width="1.5"/>
      <rect x="1" y="15" width="6" height="6" fill="{SUN}" stroke="#000" stroke-width="1.5"/>
      <rect x="127" y="15" width="5" height="7" fill="{TOMATO}" stroke="#000" stroke-width="1.5"/>
      <circle cx="30" cy="30" r="9" fill="#000"/><circle cx="30" cy="30" r="3" fill="{TIN}"/>
      <circle cx="104" cy="30" r="9" fill="#000"/><circle cx="104" cy="30" r="3" fill="{TIN}"/>{extra}'''


s = []
add = s.append

add(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Tariful Hoque, player one</title>
<desc id="d">An arcade title screen painted in rickshaw-art colours. A Dhaka-like street at night under bands of dark navy, with a ringed gold sun, birds, a minaret, a বেপরোয়া signboard and painted building fronts. A police car chases a red car along the road. The title reads Tariful Hoque, at LCTarif, game developer, Dhaka, press start, and the top strip says the game is at beporowa.netlify.app.</desc>
<defs>
<style>
@font-face{{font-family:Galada;src:url(data:font/woff2;base64,{font('galada-bengali-400-normal.woff2')}) format('woff2')}}
@font-face{{font-family:Anek;font-weight:800;src:url(data:font/woff2;base64,{font('anek-bangla-latin-800-normal.woff2')}) format('woff2')}}
.bn{{font-family:Galada,serif}}
.lat{{font-family:Anek,'Arial Black',sans-serif;font-weight:800}}
.rays{{transform-origin:{SUN_X}px {SUN_Y}px;animation:spin 80s linear infinite}}
.drive{{animation:drive 9s linear infinite both}}
.cop{{animation-delay:1.1s}}
.shed{{animation:shed 7s linear infinite}}
.bird{{animation:bob 2.6s ease-in-out infinite alternate}}
.sh{{animation:sh 1.6s ease-in-out infinite alternate}}
.blink{{animation:blink 1.2s linear infinite}}
.sa{{animation:sa .5s linear infinite}}
.sb{{animation:sa .5s linear infinite reverse}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes drive{{0%{{transform:translateX(1330px)}}75%,100%{{transform:translateX(-430px)}}}}
@keyframes shed{{0%,68%{{opacity:1}}70%,84%{{opacity:.1}}86%,100%{{opacity:1}}}}
@keyframes bob{{from{{transform:translateY(-5px)}}to{{transform:translateY(5px)}}}}
@keyframes sh{{from{{opacity:.3}}to{{opacity:.85}}}}
@keyframes blink{{0%,55%{{opacity:1}}58%,100%{{opacity:0}}}}
@keyframes sa{{0%,49%{{fill:{TOMATO}}}50%,100%{{fill:#3d6cd8}}}}
@media (prefers-reduced-motion:reduce){{
  .rays,.drive,.shed,.bird,.sh,.blink,.sa,.sb{{animation:none!important}}
  .drive{{transform:translateX(700px)}}
  .cop{{transform:translateX(900px)}}
}}
</style>
<clipPath id="scene"><rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="12"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="#000"/>
<g clip-path="url(#scene)">''')

# Sunset sky in flat painted bands, darkest at the top.
top, band_h = 54, (STREET - 54) / len(SKY)
for i, colour in enumerate(SKY):
    add(f'<rect x="0" y="{top + i * band_h:.1f}" width="{W}" height="{band_h + 1:.1f}" fill="{colour}"/>')

# The sun, low over the rooftops: turning rays, then painted rings.
rays = []
for k in range(20):
    a = math.radians(k * 18)
    da = math.radians(3.6)
    p1 = (SUN_X + 82 * math.cos(a - da), SUN_Y + 82 * math.sin(a - da))
    p2 = (SUN_X + 82 * math.cos(a + da), SUN_Y + 82 * math.sin(a + da))
    p3 = (SUN_X + 330 * math.cos(a), SUN_Y + 330 * math.sin(a))
    rays.append(f'{p1[0]:.1f},{p1[1]:.1f} {p3[0]:.1f},{p3[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}')
add(f'<g class="rays" fill="{SUN}" opacity=".13">' + ''.join(f'<polygon points="{r}"/>' for r in rays) + '</g>')
add(f'''<circle cx="{SUN_X}" cy="{SUN_Y}" r="70" fill="{SUN}" stroke="#000" stroke-width="3"/>
<circle cx="{SUN_X}" cy="{SUN_Y}" r="57" fill="none" stroke="{RANI}" stroke-width="6"/>
<circle cx="{SUN_X}" cy="{SUN_Y}" r="44" fill="none" stroke="{DARK_NAVY}" stroke-width="4"/>
<circle cx="{SUN_X}" cy="{SUN_Y}" r="31" fill="{CREAM}" stroke="#000" stroke-width="2"/>''')

# Birds, the way rickshaw painters draw them.
for i, (bx, by, sc) in enumerate([(700, 88, 1.0), (742, 112, .8), (1090, 82, 1.1), (1132, 104, .85), (1176, 90, .7)]):
    add(f'<g class="bird" style="animation-delay:{i * .45:.2f}s"><path transform="translate({bx} {by}) scale({sc})" '
        f'd="M0 0Q8-9 16 0Q24-9 32 0" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/></g>')

# Far skyline and a minaret, in deep plum.
d = [f'M8 {STREET}']
x = 8
while x < W:
    w = rng.randint(40, 90)
    t = rng.randint(278, 296) if x < 520 else rng.randint(226, 274)
    d.append(f'V{t}H{min(x + w, W)}')
    x += w
d.append(f'V{STREET}Z')
add(f'<path d="{"".join(d)}" fill="{FAR}" stroke="#000" stroke-width="2"/>')
add(f'''<path d="M791 {STREET}V196H785V188H815V196H809V{STREET}Z M789 188L800 162L811 188Z M800 162V150" fill="{FAR}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>
<circle cx="800" cy="148" r="3.5" fill="{SUN}" stroke="#000" stroke-width="1.5"/>''')

# Painted building fronts with cornices and windows; some lose power now and then.
buildings = [(12, 70, 292), (82, 56, 300), (138, 84, 286), (222, 60, 296), (282, 90, 288), (372, 64, 272),
             (436, 80, 264), (516, 70, 250), (586, 96, 240), (682, 64, 208), (746, 110, 224),
             (856, 150, 178), (1006, 80, 214), (1086, 104, 194), (1190, 82, 232)]
shed = {3: 0.0, 7: 2.3, 10: 4.6, 13: 1.2}
lit = []
for i, (bx, bw, top) in enumerate(buildings):
    front = INDIGO if i == 11 else FRONTS[(i * 4 + 1) % len(FRONTS)]
    add(f'<rect x="{bx}" y="{top}" width="{bw}" height="{STREET - top + 2}" fill="{front}" stroke="#000" stroke-width="2"/>')
    add(f'<rect x="{bx - 3}" y="{top - 3}" width="{bw + 6}" height="7" fill="{CORNICE}" stroke="#000" stroke-width="2"/>')
    cols, rows = (bw - 10) // 18, (STREET - top - 16) // 22
    cls = f' class="shed" style="animation-delay:{shed[i]}s"' if i in shed else ''
    add(f'<g{cls}>')
    for r in range(rows):
        for c in range(cols):
            wx, wy = bx + 9 + c * 18, top + 12 + r * 22
            roll = rng.random()
            colour = SUN if roll < 0.42 else CREAM if roll < 0.56 else SOOT
            add(f'<rect x="{wx}" y="{wy}" width="8" height="11" fill="{colour}" stroke="#000" stroke-width="1"/>')
            if colour != SOOT and r >= rows - 2:
                lit.append(wx)
    add('</g>')

# A hand-painted tin signboard on the tallest roof.
add(f'''<path d="M876 160V176M986 160V176" stroke="#000" stroke-width="4"/>
<rect x="846" y="112" width="170" height="50" fill="{TIN}" stroke="#000" stroke-width="3"/>
<rect x="852" y="118" width="158" height="38" fill="none" stroke="{SUN}" stroke-width="2"/>
<text x="931" y="148" text-anchor="middle" class="bn" font-size="31" fill="{INDIGO}">বেপরোয়া</text>''')

# The street: black-and-yellow kerb, road, lane marks and sunset in the puddles.
add(f'<rect x="0" y="{STREET}" width="{W}" height="9" fill="{MARIGOLD}" stroke="#000" stroke-width="2"/>')
for x in range(0, W, 48):
    add(f'<rect x="{x}" y="{STREET + 1}" width="24" height="7" fill="{DARK_NAVY}"/>')
add(f'<rect x="0" y="{STREET + 9}" width="{W}" height="{H - STREET - 9}" fill="{SOOT}"/>')
for x in range(26, W, 84):
    add(f'<rect x="{x}" y="362" width="42" height="4" fill="{TIN}" opacity=".35"/>')
puddle = [SUN, CREAM, MUTED, RANI]
for i, wx in enumerate(sorted(set(lit))[::3]):
    add(f'<rect class="sh" style="animation-delay:{(i % 5) * 0.31:.2f}s" x="{wx - 3}" y="{334 + (i * 7) % 20}" '
        f'width="{rng.randint(12, 26)}" height="2.5" fill="{puddle[i % len(puddle)]}"/>')

# A red car with the police on its tail, driving on the left.
add(f'<g class="drive"><g transform="translate(0 362)">{car(SUN, INDIGO, TEAL)}</g></g>')
add(f'''<g class="drive cop"><g transform="translate(0 362)">{car(TIN, INDIGO, '#9fb7c9', f"""
      <rect class="sa" x="64" y="-12" width="12" height="6" fill="{TOMATO}" stroke="#000" stroke-width="1.5"/>
      <rect class="sb" x="78" y="-12" width="12" height="6" fill="#3d6cd8" stroke="#000" stroke-width="1.5"/>""")}</g></g>''')

# Title block: the name in English with stacked, painted shadows.
name = 'TARIFUL HOQUE'
title = f'x="56" y="186" class="lat" font-size="78" letter-spacing="3"'
add(f'''<text x="60" y="98" class="lat" font-size="15" letter-spacing="5" fill="{MUTED}" stroke="#000" stroke-width="3" paint-order="stroke">PLAYER 1 · READY</text>
<text {title} transform="translate(9 9)" fill="{MARIGOLD}" stroke="#000" stroke-width="4" paint-order="stroke">{name}</text>
<text {title} transform="translate(5 5)" fill="{RANI}" stroke="#000" stroke-width="4" paint-order="stroke">{name}</text>
<text {title} fill="{CREAM}" stroke="#000" stroke-width="4" paint-order="stroke">{name}</text>
<text x="60" y="236" class="lat" font-size="19" letter-spacing="4" stroke="#000" stroke-width="5" paint-order="stroke"><tspan fill="{CREAM}">@LCTARIF</tspan><tspan fill="{SUN}" dx="14">· GAME DEVELOPER · DHAKA</tspan></text>
<rect x="56" y="328" width="244" height="36" rx="3" fill="{DARK_NAVY}" stroke="{SUN}" stroke-width="3"/>
<g class="blink"><path d="M74 337L89 346L74 355Z" fill="{SUN}"/>
<text x="100" y="354" class="lat" font-size="19" letter-spacing="4" fill="{SUN}">PRESS START</text></g>''')

# Arcade score strip along the top.
add(f'''<rect x="0" y="0" width="{W}" height="54" fill="#050a18"/>
<text x="40" y="41" class="lat" font-size="17" letter-spacing="3"><tspan fill="{SUN}">1UP</tspan><tspan fill="{TIN}" dx="12">TARIFUL HOQUE</tspan></text>
<text x="{W // 2}" y="41" text-anchor="middle" class="lat" font-size="17" letter-spacing="3"><tspan fill="{TIN}">STAGE</tspan><tspan fill="{SUN}" dx="10">7/7</tspan><tspan fill="{TIN}" dx="10">CLEARED</tspan></text>
<text x="{W - 40}" y="41" text-anchor="end" class="lat" font-size="17" letter-spacing="3"><tspan fill="{TIN}">PLAY</tspan><tspan fill="{SUN}" dx="10">BEPOROWA.NETLIFY.APP</tspan></text>
</g>
<rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="9" fill="none" stroke="{SUN}" stroke-width="3"/>
</svg>
''')

OUT.write_text('\n'.join(s), encoding='utf-8')
print(OUT, OUT.stat().st_size // 1024, 'KB')
