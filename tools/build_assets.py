"""모여라 코드의 숲! — README 에셋 생성기

assets/ 아래의 SVG(헤더·푸터·주민·대화창·여권·간판·너굴폰 아이콘)와
GIF 프레임용 HTML을 생성한다. 한글 글꼴(Jua, OFL)은 사용된 글자만
서브셋해서 SVG 안에 base64로 넣기 때문에 어떤 환경에서도 같은 모양으로 보인다.

사용법:
  curl -L -o /tmp/Jua.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/jua/Jua-Regular.ttf
  pip install fonttools brotli pillow
  python tools/build_assets.py /tmp/Jua.ttf
  node tools/render_gif.js && python tools/build_gif.py
"""
import base64
import io
import os
import string
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
FONT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/Jua.ttf"
FACE_PATH = os.path.join(ROOT, "tools", "face.jpg")
CAT_PATH = os.path.join(ASSETS, "scatdule-cat.png")

# 동물의 숲 팔레트
CREAM = "#FFF9E5"
BROWN = "#6B4F3A"
WOOD = "#C98F5A"
WOOD_DARK = "#8B5A33"
MINT = "#8ED1B5"
LEAF = "#63B34B"
LEAF_DARK = "#3F8A33"
FUR = "#FBE3C8"
FUR_LINE = "#E2B48A"
HAIR = "#2B2321"
NAVY = "#2E3350"


def font_face(text):
    """text에 쓰인 글자만 담은 Jua woff2를 @font-face로 돌려준다."""
    chars = set(text) | set(string.printable)
    font = TTFont(FONT_PATH)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(chars))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return ("@font-face{font-family:'Jua';"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


FONT = "font-family:'Jua','Apple SD Gothic Neo','Malgun Gothic',sans-serif;"


def svg(w, h, body, css, text, extra_attr=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" {extra_attr}>'
            f"<style>{font_face(text) if text else ''} text{{{FONT}}} {css}</style>{body}</svg>")


def write(name, content):
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name:28s} {len(content.encode()) / 1024:6.1f} KB")


def b64file(path, mime):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


# ---------------------------------------------------------------- 공통 그림
LEAF_SYMBOL = f"""
<symbol id="leaf" viewBox="-40 -45 80 92">
  <mask id="bite"><rect x="-50" y="-50" width="100" height="100" fill="#fff"/>
    <circle cx="33" cy="12" r="11" fill="#000"/></mask>
  <g mask="url(#bite)">
    <path d="M0,-40 C25,-35 38,-10 32,15 C27,32 10,42 0,45 C-10,42 -27,32 -32,15 C-38,-10 -25,-35 0,-40 Z"
      fill="{LEAF}" stroke="{LEAF_DARK}" stroke-width="4"/>
    <path d="M0,-32 L0,40 M0,-10 L-16,-20 M0,-10 L16,-20 M0,10 L-18,0 M0,10 L14,2 M0,28 L-14,20"
      stroke="#A7DE8F" stroke-width="3.5" stroke-linecap="round" fill="none"/>
  </g>
</symbol>"""

BUTTERFLY_SYMBOL = """
<symbol id="butterfly" viewBox="-20 -16 40 32">
  <g class="flap-l"><path d="M0,0 C-6,-16 -20,-16 -18,-4 C-17,4 -8,4 0,0 Z" fill="#FFD36E" stroke="#E0A030" stroke-width="1.5"/>
    <path d="M0,0 C-8,4 -14,14 -6,14 C-2,13 0,6 0,0 Z" fill="#FFB5C2" stroke="#E08A9A" stroke-width="1.5"/></g>
  <g class="flap-r"><path d="M0,0 C6,-16 20,-16 18,-4 C17,4 8,4 0,0 Z" fill="#FFD36E" stroke="#E0A030" stroke-width="1.5"/>
    <path d="M0,0 C8,4 14,14 6,14 C2,13 0,6 0,0 Z" fill="#FFB5C2" stroke="#E08A9A" stroke-width="1.5"/></g>
  <rect x="-1.6" y="-8" width="3.2" height="18" rx="1.6" fill="#6B4F3A"/>
</symbol>"""

BUTTERFLY_CSS = """
.flap-l{animation:flapl .3s ease-in-out infinite;transform-origin:0 0}
.flap-r{animation:flapr .3s ease-in-out infinite;transform-origin:0 0}
@keyframes flapl{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.25)}}
@keyframes flapr{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.25)}}
"""

FLOWER_COLORS = [("#FF8A8A", "#FFE08A"), ("#FFE066", "#FFA94D"), ("#FFFFFF", "#FFD43B"),
                 ("#FFB3D1", "#FFF3BF"), ("#B197FC", "#FFE066"), ("#FFA94D", "#FFF3BF")]


def flower(x, y, i, r=7):
    petal, center = FLOWER_COLORS[i % len(FLOWER_COLORS)]
    petals = "".join(
        f'<circle cx="{x + r * dx:.1f}" cy="{y + r * dy:.1f}" r="{r * .75:.1f}" fill="{petal}" stroke="#00000018"/>'
        for dx, dy in [(0, -1), (.95, -.31), (.59, .81), (-.59, .81), (-.95, -.31)])
    return (f'<path d="M{x},{y} L{x},{y + r * 2.6}" stroke="#4E9A47" stroke-width="2.5"/>'
            f'{petals}<circle cx="{x}" cy="{y}" r="{r * .55:.1f}" fill="{center}"/>')


GRASS_PATTERN = """
<pattern id="grass" width="46" height="40" patternUnits="userSpaceOnUse">
  <rect width="46" height="40" fill="#7CC576"/>
  <path d="M6,14 l5,-8 l5,8 Z" fill="#8FD186"/><path d="M28,32 l5,-8 l5,8 Z" fill="#8FD186"/>
  <path d="M30,10 l4,-6 l4,6 Z" fill="#6DB866"/><path d="M8,34 l4,-6 l4,6 Z" fill="#6DB866"/>
</pattern>"""


def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#fff" opacity=".92">'
            '<ellipse cx="0" cy="0" rx="46" ry="22"/><ellipse cx="34" cy="-12" rx="32" ry="24"/>'
            '<ellipse cx="-30" cy="-6" rx="26" ry="18"/><ellipse cx="64" cy="4" rx="26" ry="16"/></g>')


def pine(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-9" y="-10" width="18" height="40" rx="5" fill="#9C6B43"/>'
            '<path d="M0,-150 L42,-80 L-42,-80 Z M0,-118 L56,-40 L-56,-40 Z M0,-80 L68,0 L-68,0 Z" '
            'fill="#4E8B55" stroke="#3B6E42" stroke-width="4" stroke-linejoin="round"/>'
            '<path d="M-20,-60 L-6,-74 M14,-30 L28,-44 M-30,-14 L-16,-28" stroke="#6FAE6C" stroke-width="5" stroke-linecap="round"/></g>')


def round_tree(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M-12,30 L-8,-40 L8,-40 L12,30 Z" fill="#A87448"/>'
            '<g fill="#6DBE5E" stroke="#4E9A47" stroke-width="4">'
            '<circle cx="-36" cy="-70" r="34"/><circle cx="36" cy="-70" r="34"/>'
            '<circle cx="0" cy="-104" r="38"/><circle cx="0" cy="-56" r="36"/></g>'
            '<path d="M-44,-80 q8,-10 16,0 M10,-118 q8,-10 16,0 M26,-62 q8,-10 16,0" stroke="#8ED37E" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


def note(x, y, s=1.0, color="#6B4F3A"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{color}">'
            '<ellipse cx="0" cy="0" rx="9" ry="7" transform="rotate(-20)"/>'
            '<rect x="6" y="-30" width="3.5" height="30"/>'
            '<path d="M9.5,-30 q14,6 10,20 q-2,-10 -10,-12 Z"/></g>')


# ---------------------------------------------------------------- 주민 캐릭터
def villager(waving=True):
    """코드의 숲 주민 '미르' — 긴 흑발·금색 링 귀걸이·네이비 세일러복의 고양이 주민.
    viewBox 기준 0 0 300 360."""
    right_arm = (
        f'<g class="wave"><path d="M200,262 Q228,240 238,206" stroke="{NAVY}" stroke-width="26" stroke-linecap="round" fill="none"/>'
        f'<circle cx="240" cy="200" r="15" fill="{FUR}" stroke="{FUR_LINE}" stroke-width="3"/>'
        f'<path d="M234,190 v-5 M241,189 v-5 M248,192 v-5" stroke="{FUR_LINE}" stroke-width="2.5" stroke-linecap="round"/></g>'
        if waving else
        f'<path d="M202,262 Q214,290 216,312" stroke="{NAVY}" stroke-width="26" stroke-linecap="round" fill="none"/>'
        f'<circle cx="217" cy="316" r="14" fill="{FUR}" stroke="{FUR_LINE}" stroke-width="3"/>')
    return f"""
<g class="tail"><path d="M196,318 C246,322 262,280 248,246 C244,236 250,226 258,232" stroke="{FUR_LINE}" stroke-width="24" stroke-linecap="round" fill="none"/>
<path d="M196,318 C246,322 262,280 248,246 C244,236 250,226 258,232" stroke="{FUR}" stroke-width="16" stroke-linecap="round" fill="none"/>
  <path d="M246,262 l9,-3 M250,290 l10,2" stroke="{FUR_LINE}" stroke-width="3.5" stroke-linecap="round"/></g>
<path d="M66,150 C52,214 56,268 82,292 L218,292 C244,268 248,214 234,150 Z" fill="{HAIR}"/>
<g fill="{FUR}" stroke="{FUR_LINE}" stroke-width="5" stroke-linejoin="round">
  <path d="M76,112 L86,38 L134,82 Z"/><path d="M224,112 L214,38 L166,82 Z"/></g>
<path d="M90,92 L94,56 L120,80 Z M210,92 L206,56 L180,80 Z" fill="#F6A6B5"/>
<circle cx="86" cy="76" r="7" fill="none" stroke="#E8B730" stroke-width="3.5"/>
<circle cx="214" cy="76" r="7" fill="none" stroke="#E8B730" stroke-width="3.5"/>
<rect x="120" y="328" width="18" height="14" fill="{FUR}"/><rect x="162" y="328" width="18" height="14" fill="{FUR}"/>
<ellipse cx="128" cy="344" rx="17" ry="9" fill="#7A4B2E"/><ellipse cx="172" cy="344" rx="17" ry="9" fill="#7A4B2E"/>
<path d="M96,250 Q150,236 204,250 L224,326 Q150,344 76,326 Z" fill="{NAVY}" stroke="#23273D" stroke-width="3" stroke-linejoin="round"/>
<path d="M98,262 Q86,290 84,312" stroke="{NAVY}" stroke-width="26" stroke-linecap="round" fill="none"/>
<circle cx="83" cy="316" r="14" fill="{FUR}" stroke="{FUR_LINE}" stroke-width="3"/>
<rect x="138" y="218" width="24" height="34" fill="{FUR}"/>
<path d="M100,248 L150,304 L200,248 L184,244 L150,282 L116,244 Z" fill="#3A4166"/>
<path d="M106,250 L150,298 L194,250 M113,248 L150,289 L187,248" stroke="#fff" stroke-width="3" fill="none"/>
<path d="M150,286 L136,300 L142,326 L150,308 L158,326 L164,300 Z" fill="#4A5583" stroke="#353E66" stroke-width="2" stroke-linejoin="round"/>
<circle cx="150" cy="292" r="8" fill="#4A5583" stroke="#353E66" stroke-width="2"/>
<ellipse cx="150" cy="150" rx="88" ry="78" fill="{FUR}" stroke="{FUR_LINE}" stroke-width="4"/>
<path d="M74,205 C68,160 66,120 84,96 C104,70 128,62 150,62 C172,62 196,70 216,96 C234,120 232,160 226,205 L212,205 C212,150 190,102 150,94 C110,102 88,150 88,205 Z"
  fill="{HAIR}"/>
<path d="M150,64 Q148,80 150,93" stroke="#4A3F3C" stroke-width="2.5" fill="none"/>
<path d="M120,74 Q132,68 142,70 M180,78 Q192,82 200,92" stroke="#5A4E4A" stroke-width="3" fill="none" stroke-linecap="round"/>
<g transform="translate(206,112) rotate(28)"><ellipse cx="0" cy="0" rx="16" ry="8" fill="#5B6573" stroke="#3F4753" stroke-width="2"/>
  <path d="M14,0 L26,-8 L24,8 Z" fill="#5B6573" stroke="#3F4753" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="-8" cy="-2" r="2" fill="#fff"/></g>
<path d="M104,121 Q118,111 132,118 M168,118 Q182,111 196,121" stroke="{HAIR}" stroke-width="6.5" stroke-linecap="round" fill="none"/>
<g class="blink"><ellipse cx="118" cy="152" rx="15" ry="19" fill="{HAIR}"/><circle cx="123" cy="145" r="5.5" fill="#fff"/>
  <circle cx="112" cy="160" r="2.2" fill="#fff"/></g>
<g class="blink"><ellipse cx="182" cy="152" rx="15" ry="19" fill="{HAIR}"/><circle cx="187" cy="145" r="5.5" fill="#fff"/>
  <circle cx="176" cy="160" r="2.2" fill="#fff"/></g>
<path d="M104,142 Q99,138 96,132 M196,142 Q201,138 204,132" stroke="{HAIR}" stroke-width="3" stroke-linecap="round" fill="none"/>
<ellipse cx="98" cy="183" rx="15" ry="9" fill="#F6A6A0" opacity=".75"/>
<ellipse cx="202" cy="183" rx="15" ry="9" fill="#F6A6A0" opacity=".75"/>
<path d="M143,170 Q150,165 157,170 Q154,178 150,179 Q146,178 143,170 Z" fill="#F07A5A"/>
<path d="M133,188 Q141,199 150,188 Q159,199 167,188" stroke="{HAIR}" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M144,193 Q150,200 156,193" fill="#E05A5A"/>
<path d="M84,176 L58,170 M84,186 L56,188 M216,176 L242,170 M216,186 L244,188"
  stroke="{FUR_LINE}" stroke-width="3" stroke-linecap="round"/>
{right_arm}"""


VILLAGER_CSS = """
.bob{animation:bob 1.2s ease-in-out infinite;transform-origin:150px 350px}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.blink{animation:blink 4.8s infinite;transform-box:fill-box;transform-origin:center}
@keyframes blink{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
.wave{animation:wave 1.2s ease-in-out infinite;transform-origin:202px 262px}
@keyframes wave{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(14deg)}}
.tail{animation:tail 2.4s ease-in-out infinite;transform-origin:200px 320px}
@keyframes tail{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(8deg)}}
"""


# ---------------------------------------------------------------- 헤더
def header():
    title = "모여라 코드의 숲!"
    sub = "lalala5772 섬에 오신 것을 환영해요"
    w, h = 1200, 340
    leaves = "".join(
        f'<g transform="translate({x},0)"><use href="#leaf" xlink:href="#leaf" class="fall" width="26" height="30" '
        f'x="-13" y="-15" style="animation-duration:{d}s;animation-delay:-{dl}s"/></g>'
        for x, d, dl in [(70, 11, 2), (260, 14, 9), (430, 12, 5), (780, 13, 1), (960, 10, 7), (1130, 15, 11)])
    clouds = "".join(
        f'<g class="drift" style="animation-duration:{d}s;animation-delay:-{dl}s">{cloud(0, y, s)}</g>'
        for y, s, d, dl in [(56, 1.0, 60, 5), (100, .7, 80, 40), (40, .8, 70, 30), (120, .55, 90, 70)])
    flowers = "".join(flower(x, y, i) for i, (x, y) in enumerate(
        [(240, 286), (300, 300), (360, 292), (840, 298), (900, 288), (960, 302), (520, 312), (690, 316)]))
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#C7B6EA"/><stop offset=".55" stop-color="#F8D3D3"/><stop offset="1" stop-color="#FFF0D4"/></linearGradient>
  <radialGradient id="sun" cx=".08" cy=".1" r=".5"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".95"/>
    <stop offset="1" stop-color="#FFF6D8" stop-opacity="0"/></radialGradient>
  {GRASS_PATTERN}{LEAF_SYMBOL}{BUTTERFLY_SYMBOL}
  <clipPath id="frame"><rect width="{w}" height="{h}" rx="28"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="url(#sky)"/><rect width="{w}" height="{h}" fill="url(#sun)"/>
{clouds}
<path d="M0,250 C160,200 330,230 480,215 C640,200 760,236 900,214 C1020,196 1120,214 1200,206 L1200,340 L0,340 Z" fill="#A8DC9B"/>
<rect x="0" y="236" width="{w}" height="22" fill="#E8A86E"/>
<path d="M0,236 L1200,236" stroke="#C9844E" stroke-width="3"/>
<path d="M0,262 C200,246 380,258 600,252 C820,246 1000,262 1200,250 L1200,340 L0,340 Z" fill="url(#grass)"/>
{pine(110, 292, 1.05)}{pine(195, 280, .62)}{round_tree(1085, 292, 1.0)}{round_tree(1000, 286, .6)}
{flowers}
{leaves}
<g transform="translate(330,190)"><use href="#butterfly" xlink:href="#butterfly" class="hover" width="30" height="24" x="-15" y="-12"/></g>
<g transform="translate(880,170)"><use href="#butterfly" xlink:href="#butterfly" class="hover" width="26" height="21" x="-13" y="-10" style="animation-delay:-.8s"/></g>
<g class="float">
  <text x="606" y="146" text-anchor="middle" font-size="80" fill="#3E6B2B" opacity=".25">{title}</text>
  <text x="600" y="140" text-anchor="middle" font-size="80" fill="#fff" stroke="#5B8C3E" stroke-width="12"
    stroke-linejoin="round" paint-order="stroke">{title}</text>
</g>
<g transform="translate(262,104)"><use href="#leaf" xlink:href="#leaf" class="wiggle" width="54" height="62" x="-27" y="-31"/></g>
<g transform="translate(600,198)">
  <rect x="-250" y="-26" width="500" height="50" rx="25" fill="{CREAM}" stroke="#E9D7AE" stroke-width="3"/>
  <text x="0" y="9" text-anchor="middle" font-size="25" fill="{BROWN}">{sub}</text>
</g>
</g>"""
    css = BUTTERFLY_CSS + """
.drift{animation:drift linear infinite}
@keyframes drift{from{transform:translateX(-200px)}to{transform:translateX(1400px)}}
.fall{animation:fall linear infinite}
@keyframes fall{0%{transform:translate(0,-30px) rotate(0)}25%{transform:translate(26px,70px) rotate(90deg)}
  50%{transform:translate(-18px,170px) rotate(180deg)}75%{transform:translate(22px,260px) rotate(270deg)}
  100%{transform:translate(0,370px) rotate(360deg)}}
.float{animation:float 3s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.wiggle{animation:wiggle 2.4s ease-in-out infinite;transform-origin:0 20px}
@keyframes wiggle{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(12deg)}}
.hover{animation:hover 2.4s ease-in-out infinite}
@keyframes hover{0%,100%{transform:translate(0,0)}25%{transform:translate(14px,-10px)}50%{transform:translate(26px,4px)}75%{transform:translate(10px,12px)}}
"""
    write("header.svg", svg(w, h, body, css, title + sub))


# ---------------------------------------------------------------- 푸터
def footer():
    t1 = "또 놀러 와요!"
    t2 = "오늘도 코드의 숲에 들러줘서 고마워요"
    t3 = "See you again!"
    w, h = 1200, 300
    flowers = "".join(flower(x, y, i, 8) for i, (x, y) in enumerate(
        [(60, 236), (130, 250), (330, 240), (420, 256), (780, 252), (860, 238), (1060, 248), (1140, 236)]))
    body = f"""
<defs>
  <linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFF0D4" stop-opacity="0"/><stop offset=".45" stop-color="#FFE9E0"/><stop offset="1" stop-color="#D9F2E4"/></linearGradient>
  {GRASS_PATTERN}{LEAF_SYMBOL}{BUTTERFLY_SYMBOL}
</defs>
<rect width="{w}" height="{h}" fill="url(#fsky)"/>
<g class="plane">
  <path d="M-170,64 L-30,64" stroke="#C9A06B" stroke-width="2" stroke-dasharray="4 4"/>
  <rect x="-200" y="46" width="170" height="36" rx="8" fill="#FFF9E5" stroke="#E0B97A" stroke-width="3"/>
  <text x="-115" y="71" text-anchor="middle" font-size="20" fill="#C46A3B">{t3}</text>
  <g transform="translate(20,62)">
    <path d="M-34,0 C-34,-14 30,-14 40,0 C30,12 -34,12 -34,0 Z" fill="#7CC0E8" stroke="#3E8CC0" stroke-width="3"/>
    <path d="M-6,-6 L10,-34 L22,-34 L14,-6 Z M-6,6 L6,26 L16,26 L12,6 Z" fill="#F7D05E" stroke="#C9A030" stroke-width="3" stroke-linejoin="round"/>
    <path d="M-34,0 L-46,-14 L-38,-14 Z" fill="#F7D05E" stroke="#C9A030" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="26" cy="-3" r="4" fill="#fff"/><circle cx="16" cy="-3" r="4" fill="#fff"/>
    <g class="prop"><rect x="40" y="-14" width="4" height="28" rx="2" fill="#6B4F3A"/></g>
  </g>
</g>
<path d="M0,212 C200,186 400,206 600,196 C800,186 1000,206 1200,194 L1200,300 L0,300 Z" fill="url(#grass)"/>
{flowers}
{pine(210, 252, .7)}{round_tree(990, 250, .72)}
<g transform="translate(600,0)">
  <rect x="-10" y="150" width="20" height="100" rx="5" fill="{WOOD_DARK}"/>
  <rect x="-260" y="70" width="520" height="104" rx="20" fill="{WOOD}" stroke="{WOOD_DARK}" stroke-width="5"/>
  <rect x="-248" y="80" width="496" height="18" rx="9" fill="#DDA772" opacity=".7"/>
  <path d="M-220,150 q40,-6 80,0 M60,152 q50,-6 120,0" stroke="#B07A48" stroke-width="3" fill="none" stroke-linecap="round"/>
  <text x="0" y="124" text-anchor="middle" font-size="40" fill="#FFF8E7" stroke="{WOOD_DARK}" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{t1}</text>
  <text x="0" y="158" text-anchor="middle" font-size="22" fill="#FFF3D6">{t2}</text>
  <g transform="translate(-226,82)"><use href="#leaf" xlink:href="#leaf" class="wiggle" width="34" height="40" x="-17" y="-20"/></g>
</g>
<g transform="translate(150,170)">
  <rect x="-5" y="20" width="10" height="56" fill="#8B6B4A"/>
  <path d="M-30,24 L-30,-4 Q-30,-22 0,-22 Q30,-22 30,-4 L30,24 Z" fill="#E86A5C" stroke="#B5473C" stroke-width="3"/>
  <rect x="-22" y="0" width="44" height="6" rx="3" fill="#B5473C"/>
  <g class="flag"><rect x="28" y="-20" width="5" height="26" fill="#6B4F3A"/><rect x="33" y="-20" width="16" height="11" fill="#FFD43B"/></g>
</g>
<g transform="translate(1010,120)"><use href="#butterfly" xlink:href="#butterfly" class="hover" width="28" height="22" x="-14" y="-11"/></g>
<g transform="translate(300,130)"><use href="#butterfly" xlink:href="#butterfly" class="hover" width="24" height="19" x="-12" y="-9" style="animation-delay:-1.2s"/></g>
"""
    css = BUTTERFLY_CSS + """
.plane{animation:plane 16s linear infinite}
@keyframes plane{0%{transform:translate(-120px,0)}50%{transform:translate(700px,-14px)}100%{transform:translate(1500px,0)}}
.prop{animation:prop .2s linear infinite;transform-box:fill-box;transform-origin:center}
@keyframes prop{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.2)}}
.wiggle{animation:wiggle 2.4s ease-in-out infinite;transform-origin:0 20px}
@keyframes wiggle{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(12deg)}}
.flag{animation:flag 2s ease-in-out infinite;transform-origin:30px 6px}
@keyframes flag{0%,60%,100%{transform:rotate(0)}75%{transform:rotate(-80deg)}}
.hover{animation:hover 2.4s ease-in-out infinite}
@keyframes hover{0%,100%{transform:translate(0,0)}25%{transform:translate(14px,-10px)}50%{transform:translate(26px,4px)}75%{transform:translate(10px,12px)}}
"""
    write("footer.svg", svg(w, h, body, css, t1 + t2 + t3))


# ---------------------------------------------------------------- 주민 단독 SVG
def villager_svg():
    body = f'<g class="bob">{villager()}</g>'
    write("villager.svg", svg(300, 360, body, VILLAGER_CSS, ""))


# ---------------------------------------------------------------- 대화창 (주민 소개)
DIALOG_LINES = [
    "안녕하세요! 코드의 숲에 사는 주민 미르예요.",
    "Java·Spring Boot로 튼튼한 백엔드 집을 짓고,",
    "Python으론 AI 도구를, Arduino론 텃밭을 키워요.",
    "원리부터 파고들어 끝까지 동작하는 걸 좋아해요~",
]


def intro():
    w, h = 940, 320
    name = "미르"
    lines = ""
    clips = ""
    for i, line in enumerate(DIALOG_LINES):
        y = 128 + i * 40
        clips += (f'<clipPath id="c{i}"><rect x="300" y="{y - 30}" width="0" height="40">'
                  f'<animate attributeName="width" from="0" to="600" begin="{0.4 + i * 1.3}s" dur="1.2s" fill="freeze"/>'
                  f'</rect></clipPath>')
        lines += f'<text x="318" y="{y}" font-size="23" fill="{BROWN}" clip-path="url(#c{i})">{line}</text>'
    body = f"""
<defs>{clips}
  <filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#9C7B4F" flood-opacity=".25"/></filter>
</defs>
<g transform="translate(6,8) scale(.86)"><g class="bob">{villager()}</g></g>
<path d="M282,60 C282,40 300,34 330,34 L880,30 C912,30 926,44 926,70 L930,250 C930,278 912,290 884,290 L332,294 C302,294 288,282 288,256 L286,190 L258,176 L286,160 Z"
  fill="{CREAM}" stroke="#EADBB4" stroke-width="3" filter="url(#sh)"/>
<g transform="translate(330,34) rotate(-5)">
  <rect x="0" y="-24" width="112" height="44" rx="22" fill="#F2A541" stroke="#D9852A" stroke-width="3"/>
  <text x="56" y="8" text-anchor="middle" font-size="26" fill="#fff">{name}</text>
</g>
{lines}
<path d="M884,262 L904,262 L894,276 Z" fill="#F2A541"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></path>
"""
    write("intro.svg", svg(w, h, body, VILLAGER_CSS, name + "".join(DIALOG_LINES)))


# ---------------------------------------------------------------- 여권 (주민 등록증)
PASSPORT = {
    "island": "코드의 숲",
    "name": "이미르",
    "en": "Lee Mir",
    "title": ["원리를 파고드는", "풀스택 주민"],
    "fields": [
        ("특기", "백엔드 · AI 연동 · IoT"),
        ("애용 도구", "Java · Spring Boot · Python · React"),
        ("사는 곳", "Seoul, Korea"),
        ("말버릇", "“왜지?”"),
    ],
    "comment": "기초 원리부터 파고들어, 끝까지 동작하는 걸 만들어요.",
}


def passport():
    w, h = 940, 460
    p = PASSPORT
    face = b64file(FACE_PATH, "image/jpeg")
    rows = ""
    for i, (k, v) in enumerate(p["fields"]):
        y = 236 + i * 42
        rows += (f'<rect x="330" y="{y - 24}" width="104" height="32" rx="16" fill="{MINT}"/>'
                 f'<text x="382" y="{y - 1}" text-anchor="middle" font-size="18" fill="#fff">{k}</text>'
                 f'<text x="452" y="{y}" font-size="22" fill="{BROWN}">{v}</text>'
                 f'<path d="M452,{y + 12} L890,{y + 12}" stroke="#EADFC3" stroke-width="2" stroke-dasharray="3 6"/>')
    tri = "".join(f'<path d="M{x},{y} l9,-14 l9,14 Z" fill="#ffffff" opacity=".22"/>'
                  for x in range(16, w, 58) for y in (30, 64))
    text = (p["island"] + p["name"] + p["en"] + "".join(p["title"]) + p["comment"]
            + "".join(k + v for k, v in p["fields"]) + "PASSPORT 주민 등록증 섬 @lalala5772 코드의 숲 주민 No.5772")
    body = f"""
<defs>
  <filter id="sh" x="-5%" y="-5%" width="110%" height="115%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#9C7B4F" flood-opacity=".25"/></filter>
  <clipPath id="photo"><rect x="44" y="110" width="236" height="236" rx="26"/></clipPath>
  <clipPath id="card"><rect x="10" y="10" width="{w - 20}" height="{h - 24}" rx="34"/></clipPath>
  {LEAF_SYMBOL}
</defs>
<rect x="10" y="10" width="{w - 20}" height="{h - 24}" rx="34" fill="#FFFBEA" filter="url(#sh)"/>
<g clip-path="url(#card)">
  <rect x="10" y="10" width="{w - 20}" height="72" fill="{MINT}"/>{tri}
  <path d="M10,82 Q{w / 2},96 {w - 10},82" fill="{MINT}"/>
</g>
<rect x="10" y="10" width="{w - 20}" height="{h - 24}" rx="34" fill="none" stroke="#E9DFC0" stroke-width="4"/>
<use href="#leaf" xlink:href="#leaf" x="38" y="22" width="38" height="44"/>
<text x="88" y="58" font-size="32" fill="#fff" letter-spacing="3">PASSPORT</text>
<text x="{w - 44}" y="56" text-anchor="end" font-size="26" fill="#fff">주민 등록증</text>
<rect x="38" y="104" width="248" height="248" rx="32" fill="#F6E3B4"/>
<image href="{face}" xlink:href="{face}" x="44" y="110" width="236" height="236" clip-path="url(#photo)" preserveAspectRatio="xMidYMid slice"/>
<rect x="64" y="370" width="196" height="38" rx="19" fill="#F2A541"/>
<text x="162" y="396" text-anchor="middle" font-size="21" fill="#fff">@lalala5772</text>
<g transform="translate(330,116)">
  <use href="#leaf" xlink:href="#leaf" x="0" y="-18" width="22" height="26"/>
  <text x="30" y="2" font-size="20" fill="#9C8B6E">섬</text>
  <text x="60" y="2" font-size="22" fill="{LEAF_DARK}">{p["island"]}</text>
  <text x="0" y="52" font-size="44" fill="{BROWN}">{p["name"]}</text>
  <text x="138" y="50" font-size="22" fill="#9C8B6E">{p["en"]}</text>
</g>
<g transform="translate(560,128)">
  <rect x="0" y="-26" width="330" height="70" rx="20" fill="#FFF3C9" stroke="#F0D98A" stroke-width="3"/>
  <text x="165" y="0" text-anchor="middle" font-size="21" fill="#C46A3B">{p["title"][0]}</text>
  <text x="165" y="30" text-anchor="middle" font-size="21" fill="#C46A3B">{p["title"][1]}</text>
</g>
{rows}
<rect x="330" y="392" width="560" height="34" rx="17" fill="#F3F9EE" stroke="#CFE8C4" stroke-width="2"/>
<text x="610" y="416" text-anchor="middle" font-size="19" fill="{LEAF_DARK}">{p["comment"]}</text>
<g transform="translate(852,224) rotate(-14)" opacity=".85" class="stamp">
  <circle r="46" fill="none" stroke="#E2725B" stroke-width="4"/>
  <circle r="38" fill="none" stroke="#E2725B" stroke-width="2" stroke-dasharray="4 4"/>
  <text y="-6" text-anchor="middle" font-size="16" fill="#E2725B">코드의 숲</text>
  <text y="18" text-anchor="middle" font-size="15" fill="#E2725B">주민 No.5772</text>
</g>
"""
    css = """.stamp{animation:stamp 4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes stamp{0%,100%{opacity:.85}50%{opacity:.6}}"""
    write("passport.svg", svg(w, h, body, css, text))


# ---------------------------------------------------------------- 섹션 간판
SIGNS = {
    "resident": ("주민 소개", "RESIDENT"),
    "inventory": ("주머니 속 기술 도구", "INVENTORY · TECH STACK"),
    "island": ("섬 시설 둘러보기", "ISLAND TOUR · PROJECTS"),
    "miles": ("너굴 마일 달성 기록", "NOOK MILES · LEARNINGS"),
    "kk": ("토요일 밤 K.K. 라이브", "NABI-BO-BET-TTA-U"),
    "news": ("섬 소식", "ISLAND NEWS · GITHUB STATS"),
}


def sign(key, title, caption):
    w, h = 660, 130
    body = f"""
<defs>{LEAF_SYMBOL}</defs>
<rect x="160" y="80" width="18" height="46" rx="5" fill="{WOOD_DARK}"/>
<rect x="482" y="80" width="18" height="46" rx="5" fill="{WOOD_DARK}"/>
<path d="M140,128 q10,-14 18,0 q8,-12 16,0 M470,128 q10,-14 18,0 q8,-12 16,0" fill="#7CC576"/>
<rect x="40" y="10" width="580" height="88" rx="22" fill="{WOOD}" stroke="{WOOD_DARK}" stroke-width="5"/>
<rect x="52" y="19" width="556" height="14" rx="7" fill="#DDA772" opacity=".7"/>
<path d="M70,84 q36,-5 74,0 M500,86 q40,-5 90,0" stroke="#B07A48" stroke-width="3" fill="none" stroke-linecap="round"/>
<text x="330" y="62" text-anchor="middle" font-size="34" fill="#FFF8E7" stroke="{WOOD_DARK}" stroke-width="6"
  stroke-linejoin="round" paint-order="stroke">{title}</text>
<text x="330" y="86" text-anchor="middle" font-size="14" fill="#FFE9C2" letter-spacing="3">{caption}</text>
<g transform="translate(60,22)"><use href="#leaf" xlink:href="#leaf" class="wiggle" width="34" height="40" x="-17" y="-20"/></g>
"""
    css = """.wiggle{animation:wiggle 2.4s ease-in-out infinite;transform-origin:0 18px}
@keyframes wiggle{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(12deg)}}"""
    write(f"sign-{key}.svg", svg(w, h, body, css, title + caption))


# ---------------------------------------------------------------- 너굴폰 앱 아이콘
APPS = [
    ("resident", "주민 소개", "#FFB5A7", "passport"),
    ("inventory", "기술 도구", "#FFD27F", "bag"),
    ("island", "섬 시설", "#8ED1B5", "map"),
    ("miles", "너굴 마일", "#A5C8FF", "miles"),
    ("news", "섬 소식", "#D7B5FF", "news"),
]


def app_glyph(kind):
    c = "#fff"
    s = BROWN
    if kind == "passport":
        return (f'<rect x="-22" y="-26" width="44" height="52" rx="8" fill="{c}" stroke="{s}" stroke-width="3"/>'
                f'<circle cx="0" cy="-6" r="10" fill="#F6C39A" stroke="{s}" stroke-width="2.5"/>'
                f'<path d="M-10,-10 Q0,-22 10,-10 L10,-2 L-10,-2 Z" fill="{HAIR}"/>'
                f'<path d="M-12,14 L12,14" stroke="{s}" stroke-width="3" stroke-linecap="round"/>')
    if kind == "bag":
        return (f'<path d="M-24,-6 Q-24,-24 0,-24 Q24,-24 24,-6 L24,22 Q24,28 18,28 L-18,28 Q-24,28 -24,22 Z" fill="#C98F5A" stroke="{s}" stroke-width="3"/>'
                f'<path d="M-24,-2 Q0,10 24,-2" fill="none" stroke="{s}" stroke-width="3"/>'
                f'<circle cx="0" cy="6" r="5" fill="#FFD43B" stroke="{s}" stroke-width="2"/>'
                f'<path d="M-8,-24 Q0,-34 8,-24" fill="none" stroke="{s}" stroke-width="3"/>')
    if kind == "map":
        return (f'<path d="M-26,-20 L-9,-26 L9,-20 L26,-26 L26,20 L9,26 L-9,20 L-26,26 Z" fill="{c}" stroke="{s}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M-9,-26 L-9,20 M9,-20 L9,26" stroke="{s}" stroke-width="2"/>'
                f'<ellipse cx="0" cy="0" rx="14" ry="10" fill="#8FD186"/><circle cx="4" cy="-2" r="4" fill="#E86A5C"/>')
    if kind == "miles":
        return (f'<circle r="26" fill="#FFD43B" stroke="{s}" stroke-width="3"/>'
                f'<circle r="18" fill="none" stroke="#E0A030" stroke-width="2.5"/>'
                f'<path d="M-9,10 L-9,-10 L0,2 L9,-10 L9,10" stroke="{s}" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    return (f'<rect x="-24" y="-24" width="48" height="48" rx="8" fill="{c}" stroke="{s}" stroke-width="3"/>'
            f'<rect x="-16" y="-16" width="16" height="14" rx="3" fill="#B197FC"/>'
            f'<path d="M6,-14 L16,-14 M6,-6 L16,-6 M-16,6 L16,6 M-16,14 L10,14" stroke="{s}" stroke-width="3" stroke-linecap="round"/>')


def app_icon(key, label, color, kind):
    w, h = 130, 150
    body = f"""
<rect x="15" y="10" width="100" height="100" rx="30" fill="{color}" stroke="#00000014" stroke-width="3"/>
<rect x="15" y="10" width="100" height="44" rx="22" fill="#ffffff" opacity=".18"/>
<g transform="translate(65,60)" class="pop">{app_glyph(kind)}</g>
<text x="65" y="138" text-anchor="middle" font-size="19" fill="{BROWN}">{label}</text>
"""
    css = """.pop{animation:pop 2.4s ease-in-out infinite}
@keyframes pop{0%,80%,100%{transform:translate(65px,60px) scale(1)}90%{transform:translate(65px,60px) scale(1.12)}}"""
    write(f"app-{key}.svg", svg(w, h, body, css, label))


# ---------------------------------------------------------------- GIF용 장면 HTML
def gif_scene():
    """나비보벳따우~ 장면. 모든 애니메이션 주기는 2.4초의 약수라 GIF가 끊김 없이 반복된다."""
    w, h = 600, 360
    word = "나비보벳따우~"
    chars = "".join(
        f'<text x="{398 + i * 26}" y="98" font-size="28" fill="{BROWN}" class="hop" '
        f'style="animation-delay:{-2.4 + i * .1:.2f}s">{ch}</text>' for i, ch in enumerate(word))
    notes = "".join(
        f'<g transform="translate({x},{y})"><g class="rise" style="animation-delay:-{d}s">{note(0, 0, s, c)}</g></g>'
        for x, y, s, d, c in [(250, 150, 1.0, 0, "#6B4F3A"), (300, 130, .8, .6, "#E2725B"),
                              (210, 120, .85, 1.2, "#3E8CC0"), (330, 170, .9, 1.8, "#4E9A47")])
    flowers = "".join(flower(x, y, i, 8) for i, (x, y) in enumerate(
        [(40, 300), (90, 318), (540, 296), (570, 322), (330, 330), (480, 334)]))
    cat = b64file(CAT_PATH, "image/png")
    body = f"""
<defs>
  <linearGradient id="gsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C7B6EA"/><stop offset=".6" stop-color="#FAD6D2"/><stop offset="1" stop-color="#FFF0D4"/></linearGradient>
  {GRASS_PATTERN}{BUTTERFLY_SYMBOL}{LEAF_SYMBOL}
</defs>
<rect width="{w}" height="{h}" fill="url(#gsky)"/>
{cloud(90, 50, .7)}{cloud(470, 36, .55)}
<path d="M0,262 C150,240 300,256 450,246 C520,242 570,248 600,244 L600,360 L0,360 Z" fill="url(#grass)"/>
{flowers}
<g transform="translate(60,66) scale(.78)"><g class="sway"><g class="bob">{villager(waving=False)}</g></g></g>
{notes}
<g transform="translate(470,250)"><g class="catbob"><image href="{cat}" x="-70" y="-90" width="140" height="140"/></g></g>
<g>
  <path d="M380,48 C380,36 390,30 404,30 L578,30 C590,30 596,38 596,50 L596,108 C596,120 588,126 576,126 L430,126 L404,148 L410,126 L402,126 C388,126 380,118 380,106 Z"
    fill="{CREAM}" stroke="#EADBB4" stroke-width="3"/>
  {chars}
</g>
<g transform="translate(150,60)"><use href="#butterfly" class="hover" width="30" height="24" x="-15" y="-12"/></g>
<g transform="translate(540,190)"><use href="#butterfly" class="hover" width="24" height="19" x="-12" y="-9" style="animation-delay:-1.2s"/></g>
"""
    css = VILLAGER_CSS + BUTTERFLY_CSS + """
.bob{animation:bob .6s ease-in-out infinite;transform-origin:150px 350px}
.sway{animation:sway 1.2s ease-in-out infinite;transform-origin:150px 350px}
@keyframes sway{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
.catbob{animation:catbob .6s ease-in-out infinite;transform-origin:0 50px}
@keyframes catbob{0%,100%{transform:translateY(0) rotate(5deg)}50%{transform:translateY(-10px) rotate(-5deg)}}
.rise{animation:rise 2.4s linear infinite}
@keyframes rise{0%{transform:translate(0,0);opacity:0}15%{opacity:1}80%{opacity:1}100%{transform:translate(30px,-110px);opacity:0}}
.hop{animation:hop 1.2s ease-in-out infinite}
@keyframes hop{0%,30%,100%{transform:translateY(0)}15%{transform:translateY(-10px)}}
.hover{animation:hover 2.4s ease-in-out infinite}
@keyframes hover{0%,100%{transform:translate(0,0)}25%{transform:translate(14px,-10px)}50%{transform:translate(26px,4px)}75%{transform:translate(10px,12px)}}
"""
    s = svg(w, h, body, css, word)
    out = os.path.join(ROOT, "tools", "gif_scene.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html><body style="margin:0;background:#fff">{s}</body></html>')
    print("  tools/gif_scene.html")


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    header()
    footer()
    villager_svg()
    intro()
    passport()
    for k, (t, c) in SIGNS.items():
        sign(k, t, c)
    for a in APPS:
        app_icon(*a)
    gif_scene()
