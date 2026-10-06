#!/usr/bin/env python3
"""Generate the animated, theme-aware SVG artwork used by the profile README.

Edit the CONTENT section below, then run:

    python3 scripts/generate.py

Every graphic is written twice into ./assets: `<name>-dark.svg` and
`<name>-light.svg`. The README picks the right one with <picture>.
Only the standard library is used, so nothing needs to be installed.
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# --------------------------------------------------------------------------
# CONTENT
# --------------------------------------------------------------------------

FIRST_NAME = "Abdullah"
LAST_NAME = "Khiariy"
TAGLINE = "CS @ Arizona State University  ·  AI products  ·  Full-stack"
STATUS = "building ReviewMyAgent"
TYPING = [
    "building AI-powered products",
    "designing clean interfaces",
    "shipping full-stack systems",
    "turning complexity into clarity",
]

PROJECTS = [
    {
        "slug": "reviewmyagent",
        "kicker": "01 — LIVE PRODUCT",
        "live": True,
        "title": "ReviewMyAgent",
        "subtitle": "PSC AI",
        "lines": [
            "A platform for discovering and reviewing AI agents.",
            "Structured feedback, real-world comparisons, and",
            "signals that help developers ship better agents.",
        ],
        "chips": ["Next.js", "React", "Supabase", "Turborepo", "Railway"],
        "cta": "reviewmyagent.today",
        "art": "stars",
    },
    {
        "slug": "smartcity",
        "kicker": "02 — CASE STUDY",
        "live": False,
        "title": "SmartCity Hub",
        "subtitle": "Urban services platform",
        "lines": [
            "Making city services easier to access and",
            "understand. A full technical case study is",
            "being prepared for publication.",
        ],
        "chips": ["Smart city", "Public services", "In progress"],
        "cta": "case study coming soon",
        "art": "city",
    },
]

STACK = [
    "JavaScript", "React", "Next.js", "Supabase",
    "Turborepo", "Railway", "Java", "XML/XSD", "Git",
]

BUTTONS = [
    ("linkedin", "LinkedIn", "in"),
    ("email", "Email", "@"),
    ("website", "ReviewMyAgent", "↗"),
]

SECTIONS = [
    ("about", "01", "about"),
    ("work", "02", "selected work"),
    ("stack", "03", "toolkit"),
    ("activity", "04", "activity"),
]

FOOTER = "Build carefully. Explain clearly. Keep improving."

# --------------------------------------------------------------------------
# THEME
# --------------------------------------------------------------------------

THEMES = {
    "dark": {
        "bg": "#0A0D14",
        "panel": "#0F1420",
        "border": "#1E2533",
        "text": "#E8ECF4",
        "muted": "#8B94A7",
        "a1": "#7C5CFF",
        "a2": "#22D3EE",
        "a3": "#F472B6",
        "ok": "#34D399",
        "glow": 0.42,
    },
    "light": {
        "bg": "#F7F8FC",
        "panel": "#FFFFFF",
        "border": "#E2E6EF",
        "text": "#0B1020",
        "muted": "#5A6377",
        "a1": "#6D4AFF",
        "a2": "#0891B2",
        "a3": "#DB2777",
        "ok": "#059669",
        "glow": 0.22,
    },
}

SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(width, height, body, style="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}" fill="none">\n'
        f"<style>{style}{REDUCED_MOTION}</style>\n{body}\n</svg>\n"
    )


def accent_gradient(t, gid, animate=True):
    anim = (
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>'
        if animate
        else ""
    )
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">'
        f'<stop offset="0" stop-color="{t["a1"]}"/>'
        f'<stop offset="0.5" stop-color="{t["a2"]}"/>'
        f'<stop offset="1" stop-color="{t["a3"]}"/>{anim}</linearGradient>'
    )


# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------

def typing_block(t, x, y, fs, phrases, slot=4.0):
    """Typewriter effect built with discrete SMIL animations.

    Each phrase is clipped by a rect whose width steps one character at a
    time; textLength pins every glyph to the grid so clip and cursor line up
    regardless of which monospace font the viewer has.
    """
    cw = fs * 0.6
    total = slot * len(phrases)
    parts, defs = [], []
    cursor_pts = [(0.0, 0.0)]

    for i, phrase in enumerate(phrases):
        n = len(phrase)
        s = i * slot
        pts = [(0.0, 0.0), (s, 0.0)]
        for k in range(1, n + 1):
            pts.append((s + 0.2 + k * 0.055, k * cw))
        hold_end = s + slot - 0.9
        for k in range(1, n + 1):
            pts.append((hold_end + k * (0.6 / n), (n - k) * cw))
        cursor_pts += pts[1:]
        times = ";".join(f"{p[0] / total:.4f}" for p in pts) + ";1"
        values = ";".join(f"{p[1]:.1f}" for p in pts) + ";0"
        cid = f"type{i}"
        defs.append(
            f'<clipPath id="{cid}"><rect x="{x}" y="{y - fs}" width="0" height="{fs * 1.5}">'
            f'<animate attributeName="width" calcMode="discrete" dur="{total}s" '
            f'repeatCount="indefinite" keyTimes="{times}" values="{values}"/></rect></clipPath>'
        )
        parts.append(
            f'<text x="{x}" y="{y}" clip-path="url(#{cid})" font-family="{MONO}" font-size="{fs}" '
            f'fill="{t["text"]}" textLength="{n * cw:.1f}" lengthAdjust="spacing">{escape(phrase)}</text>'
        )

    cursor_pts.sort(key=lambda p: p[0])
    times = ";".join(f"{p[0] / total:.4f}" for p in cursor_pts) + ";1"
    values = ";".join(f"{x + p[1]:.1f}" for p in cursor_pts) + f";{x}"
    parts.append(
        f'<rect class="caret" x="{x}" y="{y - fs * 0.8}" width="{fs * 0.5}" height="{fs}" rx="1.5" fill="{t["a2"]}">'
        f'<animate attributeName="x" calcMode="discrete" dur="{total}s" repeatCount="indefinite" '
        f'keyTimes="{times}" values="{values}"/></rect>'
    )
    return "".join(defs), "\n".join(parts)


def header(t):
    W, H = 1000, 340
    type_defs, type_body = typing_block(t, 92, 206, 22, TYPING)
    pill_w = len(STATUS) * 7.4 + 44
    pill_x = W - 36 - pill_w
    cx, cy = 838, 214

    orbits = []
    for r, dur, dots, color in ((58, 18, 1, t["a2"]), (88, 28, 2, t["a1"]), (116, 44, 3, t["a3"])):
        dot_svg = "".join(
            f'<circle cx="{cx + r}" cy="{cy}" r="4" fill="{color}" transform="rotate({j * 360 / dots} {cx} {cy})"/>'
            for j in range(dots)
        )
        orbits.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{t["muted"]}" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="2 6"/>'
            f'<g>{dot_svg}<animateTransform attributeName="transform" type="rotate" '
            f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>'
        )

    style = (
        f".blob{{animation:drift 16s ease-in-out infinite alternate}}"
        f".b2{{animation-duration:20s;animation-delay:-6s}}.b3{{animation-duration:24s;animation-delay:-12s}}"
        f"@keyframes drift{{0%{{transform:translate(0,0)}}50%{{transform:translate(60px,-30px)}}100%{{transform:translate(-40px,25px)}}}}"
        f".caret{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}"
        f".pulse{{animation:pulse 2s ease-out infinite;transform-origin:{pill_x + 20}px 40px}}"
        f"@keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(3);opacity:0}}}}"
        f".rise{{animation:rise 1s cubic-bezier(.2,.7,.2,1) both}}.d1{{animation-delay:.15s}}.d2{{animation-delay:.3s}}.d3{{animation-delay:.45s}}"
        f"@keyframes rise{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}"
        f".core{{animation:breathe 4s ease-in-out infinite;transform-origin:{cx}px {cy}px}}"
        f"@keyframes breathe{{50%{{transform:scale(1.15)}}}}"
    )

    body = f"""<defs>
{accent_gradient(t, "acc")}
<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="{t["border"]}" stroke-width="1"/></pattern>
<radialGradient id="fade" cx="0.35" cy="0.4" r="0.75"><stop offset="0" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<radialGradient id="coreg"><stop offset="0" stop-color="{t["a2"]}"/><stop offset="0.6" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>
{type_defs}
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<g filter="url(#blur)" opacity="{t["glow"]}">
<circle class="blob" cx="160" cy="60" r="150" fill="{t["a1"]}"/>
<circle class="blob b2" cx="820" cy="300" r="170" fill="{t["a2"]}"/>
<circle class="blob b3" cx="560" cy="20" r="120" fill="{t["a3"]}"/>
</g>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)" opacity="0.7"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="21.5" stroke="{t["border"]}"/>

<g class="rise">
<text x="56" y="84" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{t["muted"]}">HELLO, WORLD — I'M</text>
</g>
<g class="rise d1">
<text x="52" y="152" font-family="{SANS}" font-size="64" font-weight="800" letter-spacing="-2" fill="{t["text"]}">{FIRST_NAME} <tspan fill="url(#acc)">{LAST_NAME}</tspan></text>
</g>
<g class="rise d2">
<text x="56" y="206" font-family="{MONO}" font-size="22" font-weight="700" fill="{t["a2"]}">~$</text>
{type_body}
</g>
<g class="rise d3">
<text x="56" y="262" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{escape(TAGLINE)}</text>
<rect x="56" y="284" width="64" height="3" rx="1.5" fill="url(#acc)"/>
</g>

<g>
<rect x="{pill_x}" y="24" width="{pill_w}" height="32" rx="16" fill="{t["panel"]}" stroke="{t["border"]}"/>
<circle class="pulse" cx="{pill_x + 20}" cy="40" r="4" fill="{t["ok"]}"/>
<circle cx="{pill_x + 20}" cy="40" r="4" fill="{t["ok"]}"/>
<text x="{pill_x + 32}" y="44.5" font-family="{MONO}" font-size="12" fill="{t["text"]}">{escape(STATUS)}</text>
</g>

<g>
{"".join(orbits)}
<circle class="core" cx="{cx}" cy="{cy}" r="26" fill="url(#coreg)" opacity="0.9"/>
<circle cx="{cx}" cy="{cy}" r="9" fill="{t["bg"]}" stroke="{t["a2"]}" stroke-width="2"/>
</g>"""
    return svg(W, H, body, style, f"{FIRST_NAME} {LAST_NAME} — {TAGLINE}")


# --------------------------------------------------------------------------
# PROJECT CARDS
# --------------------------------------------------------------------------

def chips_row(t, x, y, labels, fs=11):
    out, cx = [], x
    for label in labels:
        w = len(label) * fs * 0.6 + 20
        out.append(
            f'<rect x="{cx}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'<text x="{cx + 10}" y="{y + 16}" font-family="{MONO}" font-size="{fs}" fill="{t["muted"]}" '
            f'textLength="{len(label) * fs * 0.6:.1f}" lengthAdjust="spacing">{escape(label)}</text>'
        )
        cx += w + 8
    return "".join(out)


def art_stars(t, x, y):
    out = []
    star = "M0,-9 L2.6,-3.2 9,-2.8 4.1,1.5 5.6,7.8 0,4.4 -5.6,7.8 -4.1,1.5 -9,-2.8 -2.6,-3.2Z"
    for i in range(5):
        out.append(
            f'<path d="{star}" transform="translate({x + i * 24} {y})" fill="{t["border"]}"/>'
            f'<path class="star s{i}" d="{star}" transform="translate({x + i * 24} {y})" fill="{t["a1"] if i % 2 == 0 else t["a2"]}"/>'
        )
    style = "".join(
        f".s{i}{{animation:star 5s {i * 0.25:.2f}s ease-in-out infinite}}" for i in range(5)
    ) + "@keyframes star{0%,8%{opacity:0}18%,80%{opacity:1}92%,100%{opacity:0}}"
    return "".join(out), style


def art_city(t, x, y):
    buildings = [(0, 34), (22, 54), (48, 26), (66, 64), (94, 40)]
    out, style, k = [], [], 0
    for bx, bh in buildings:
        w = 18 if bx != 66 else 22
        out.append(f'<rect x="{x + bx}" y="{y - bh}" width="{w}" height="{bh}" rx="2" fill="{t["bg"]}" stroke="{t["border"]}"/>')
        for row in range(int((bh - 8) // 10)):
            for col in range(2):
                k += 1
                color = t["a2"] if k % 3 else t["a3"]
                out.append(
                    f'<rect class="w w{k % 6}" x="{x + bx + 4 + col * (w - 12):.1f}" '
                    f'y="{y - bh + 6 + row * 10}" width="4" height="4" rx="1" fill="{color}"/>'
                )
    style = "".join(
        f".w{i}{{animation:win {2.4 + i * 0.7:.1f}s {i * 0.4:.1f}s steps(1) infinite}}" for i in range(6)
    ) + "@keyframes win{0%{opacity:.25}50%{opacity:1}}"
    out.append(f'<path d="M{x - 6} {y}H{x + 122}" stroke="{t["border"]}" stroke-width="1.5"/>')
    return "".join(out), style


def card(t, p):
    W, H = 480, 270
    art, art_style = (art_stars if p["art"] == "stars" else art_city)(t, *((352, 46) if p["art"] == "stars" else (334, 88)))
    status_color = t["ok"] if p["live"] else t["a3"]
    lines = "".join(
        f'<text x="32" y="{136 + i * 22}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{escape(l)}</text>'
        for i, l in enumerate(p["lines"])
    )
    style = (
        art_style
        + ".dot{animation:dot 2s ease-in-out infinite}@keyframes dot{50%{opacity:.25}}"
        + ".arrow{animation:nudge 2.4s ease-in-out infinite}@keyframes nudge{50%{transform:translate(4px,-4px)}}"
    )
    body = f"""<defs>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1" gradientUnits="objectBoundingBox">
<stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.35" stop-color="{t["border"]}"/><stop offset="0.65" stop-color="{t["border"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="8s" repeatCount="indefinite"/>
</linearGradient>
{accent_gradient(t, "acc", animate=False)}
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{t["panel"]}" stroke="url(#ring)" stroke-width="1.5"/>
<circle class="dot" cx="38" cy="40" r="4" fill="{status_color}"/>
<text x="50" y="44" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{t["muted"]}">{escape(p["kicker"])}</text>
<text x="32" y="90" font-family="{SANS}" font-size="30" font-weight="800" letter-spacing="-1" fill="{t["text"]}">{escape(p["title"])}</text>
<text x="32" y="112" font-family="{MONO}" font-size="12" fill="{t["a2"]}">{escape(p["subtitle"])}</text>
{art}
{lines}
{chips_row(t, 32, 200, p["chips"])}
<path d="M32 242H{W - 32}" stroke="{t["border"]}"/>
<text x="{W - 52}" y="258" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["text"]}">{escape(p["cta"])}</text>
<g class="arrow"><path d="M{W - 44} 256l8-8m-6 0h6v6" stroke="url(#acc)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>"""
    return svg(W, H, body, style, f'{p["title"]} — {" ".join(p["lines"])}')


# --------------------------------------------------------------------------
# SMALL PIECES
# --------------------------------------------------------------------------

def section(t, num, label):
    W, H = 1000, 48
    tx = 56 + len(label) * 9.6 + 22
    body = f"""<defs>{accent_gradient(t, "acc", animate=False)}
<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.4" stop-color="{t["border"]}"/><stop offset="1" stop-color="{t["border"]}" stop-opacity="0"/></linearGradient></defs>
<text x="0" y="30" font-family="{MONO}" font-size="14" font-weight="700" fill="url(#acc)">{num}</text>
<text x="30" y="30" font-family="{MONO}" font-size="14" fill="{t["muted"]}">/</text>
<text x="48" y="30" font-family="{MONO}" font-size="16" font-weight="700" letter-spacing="1" fill="{t["text"]}">{escape(label.upper())}</text>
<path class="grow" d="M{tx} 25H{W}" stroke="url(#line)" stroke-width="1.5"/>"""
    style = f".grow{{stroke-dasharray:{W};animation:grow 1.6s ease-out both}}@keyframes grow{{from{{stroke-dashoffset:{W}}}to{{stroke-dashoffset:0}}}}"
    return svg(W, H, body, style, f"{num} {label}")


def stack(t):
    W, H = 1000, 76
    fs = 13
    items, x = [], 0
    for _ in range(2):
        for name in STACK:
            w = len(name) * fs * 0.6 + 44
            items.append(
                f'<rect x="{x:.1f}" y="18" width="{w:.1f}" height="40" rx="20" fill="{t["panel"]}" stroke="{t["border"]}"/>'
                f'<circle cx="{x + 20:.1f}" cy="38" r="4" fill="url(#acc)"/>'
                f'<text x="{x + 32:.1f}" y="42.5" font-family="{MONO}" font-size="{fs}" fill="{t["text"]}" '
                f'textLength="{len(name) * fs * 0.6:.1f}" lengthAdjust="spacing">{escape(name)}</text>'
            )
            x += w + 12
    loop = x / 2
    style = f".track{{animation:scroll {len(STACK) * 2.6:.0f}s linear infinite}}@keyframes scroll{{to{{transform:translateX(-{loop:.1f}px)}}}}"
    body = f"""<defs>{accent_gradient(t, "acc", animate=False)}
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.08" stop-color="#fff"/><stop offset="0.92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask></defs>
<g mask="url(#m)"><g class="track">{"".join(items)}</g></g>"""
    return svg(W, H, body, style, "Toolkit: " + ", ".join(STACK))


def button(t, label, glyph):
    fs = 14
    W = int(len(label) * fs * 0.62 + 84)
    H = 48
    body = f"""<defs>{accent_gradient(t, "acc")}</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="{t["panel"]}" stroke="{t["border"]}"/>
<circle cx="25" cy="24" r="13" fill="url(#acc)"/>
<text x="25" y="28.5" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#fff">{escape(glyph)}</text>
<text x="48" y="29" font-family="{SANS}" font-size="{fs}" font-weight="600" fill="{t["text"]}">{escape(label)}</text>"""
    return svg(W, H, body, "", label)


def footer(t):
    W, H = 1000, 120
    body = f"""<defs>{accent_gradient(t, "acc")}</defs>
<path d="M0 30 Q 250 0 500 30 T 1000 30" stroke="{t["border"]}" stroke-width="1.5">
<animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0 30 Q 250 0 500 30 T 1000 30;M0 30 Q 250 60 500 30 T 1000 30;M0 30 Q 250 0 500 30 T 1000 30"/></path>
<text x="500" y="84" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="1" fill="url(#acc)">{escape(FOOTER)}</text>"""
    return svg(W, H, body, "", FOOTER)


# --------------------------------------------------------------------------

def main():
    OUT.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        files = {
            "header": header(t),
            "stack": stack(t),
            "footer": footer(t),
        }
        for p in PROJECTS:
            files[f"card-{p['slug']}"] = card(t, p)
        for slug, num, label in SECTIONS:
            files[f"section-{slug}"] = section(t, num, label)
        for slug, label, glyph in BUTTONS:
            files[f"btn-{slug}"] = button(t, label, glyph)
        for name, content in files.items():
            (OUT / f"{name}-{theme}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
