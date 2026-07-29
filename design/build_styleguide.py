"""Builds `03-design-system.svg` — tokens and components behind the homepage.

Run:  python3 design/build_styleguide.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokens import C, GRID, TYPE, DISPLAY, BODY
from svgkit import Doc, measure
from components import (logo, logo_size, button, text_link, chip, icon,
                        card, eyebrow, compass)

W = GRID["desktop_width"]
M = GRID["margin"]
CW = GRID["content"]
R = M + CW


# ------------------------------------------------------------- contrast ----
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------- helpers ----
def block_head(d, y, index, title, note=None):
    with d.group(f"Block header / {title}"):
        d.text(M, y, index, family=BODY, size=13, weight=700, tracking=1.6,
               fill=C["red_600"], name="Index")
        d.text(M + 46, y, title, family=DISPLAY, size=30, weight=700,
               tracking=-0.2, fill=C["ink"], name="Title")
        if note:
            d.text(R, y, note, family=BODY, size=14, weight=400,
                   fill=C["slate_400"], anchor="end", name="Note")
        d.line(M, y + 20, R, y + 20, stroke=C["line"], sw=1, name="Rule")
    return y + 20


def swatch(d, x, y, w, h, hexcolor, name, usage, on_dark=False, border=False):
    with d.group(f"Swatch / {name}"):
        d.rect(x, y, w, h, fill=hexcolor, r=GRID["radius_sm"],
               stroke=C["line"] if border else None, sw=1, name="Chip")
        d.text(x, y + h + 24, name, family=BODY, size=14, weight=700,
               fill=C["ink"], name="Name")
        d.text(x, y + h + 44, hexcolor.upper(), family=BODY, size=13,
               weight=400, fill=C["slate_600"], name="Hex")
        d.para(x, y + h + 54, usage, w, style="micro", fill=C["slate_400"],
               name="Usage")


# ----------------------------------------------------------------- title ----
def title_block(d, y):
    d.rect(0, y, W, 236, fill=C["navy_800"], name="Background")
    clip = d.clip_rect(0, y, W, 236)
    with d.group("Decoration", opacity=0.09, clip=clip):
        compass(d, 1290, y + 118, 190, ring=C["white"], arc=C["gold"],
                needle=C["red"], sw=18)
    logo(d, M, y + 52, scale=0.9, on_dark=True)
    d.text(M, y + 152, "Homepage Design System", family=DISPLAY, size=34,
           weight=700, tracking=-0.3, fill=C["white"], name="Title")
    d.text(M, y + 184, "Tokens, components, and layout rules used across the "
           "desktop and mobile homepage frames.", family=BODY, size=15,
           weight=400, fill=C["on_dark_soft"], name="Subtitle")
    return y + 236


# ------------------------------------------------------------------ logo ----
def logo_block(d, y):
    y = block_head(d, y + 88, "01", "Logo & mark",
                   "Compass replaces the O — never substitute a plain letter")
    ry = y + 48
    h = 176
    cols = [
        ("Primary lockup", C["white"], False, True),
        ("Reversed lockup", C["navy_800"], True, False),
        ("Mark only", C["surface"], False, True),
    ]
    cw = (CW - 2 * 24) / 3
    for i, (label, bg, on_dark, border) in enumerate(cols):
        x = M + i * (cw + 24)
        with d.group(f"Logo / {label}"):
            d.rect(x, ry, cw, h, fill=bg, r=GRID["radius_md"],
                   stroke=C["line"] if border else None, sw=1, name="Stage")
            if label == "Mark only":
                compass(d, x + cw / 2, ry + h / 2, 44, sw=13)
            else:
                lw, lh = logo_size(0.78)
                logo(d, x + (cw - lw) / 2, ry + h / 2 - lh / 2, scale=0.78,
                     on_dark=on_dark)
            d.text(x + cw / 2, ry + h + 26, label, family=BODY, size=13,
                   weight=600, fill=C["slate_600"], anchor="middle",
                   name="Label")

    ny = ry + h + 60
    notes = [
        ("Clear space", "Minimum padding on all sides equals the height of "
                        "the compass mark."),
        ("Minimum size", "120px wide on screen. Below that, use the compass "
                         "mark on its own."),
        ("Colour", "Navy wordmark with a red LOUNGE. Reversed lockup keeps "
                   "LOUNGE red on navy."),
    ]
    for i, (t, b) in enumerate(notes):
        x = M + i * (cw + 24)
        d.text(x, ny, t, family=BODY, size=14, weight=700, fill=C["ink"],
               name=f"Note / {t}")
        d.para(x, ny + 10, b, cw - 16, style="small", fill=C["slate_600"],
               name="Body")
    return ny + 78


# ---------------------------------------------------------------- colour ----
def colour_block(d, y):
    y = block_head(d, y + 24, "02", "Colour",
                   "Brand values sampled from the CL logo artwork")
    ry = y + 46
    d.text(M, ry, "BRAND", family=BODY, size=12, weight=700, tracking=1.4,
           fill=C["slate_400"], name="Group label")
    brand = [
        (C["navy"], "Navy", "Primary. Wordmark, headings, dark surfaces."),
        (C["red"], "Red", "Accent. Primary CTAs, links, alert states."),
        (C["gold"], "Gold", "Highlight. Eyebrows on dark, lead-magnet CTA."),
    ]
    sw, sh = 200, 104
    for i, (hexc, name, usage) in enumerate(brand):
        swatch(d, M + i * (sw + 24), ry + 18, sw, sh, hexc, name, usage)

    ry2 = ry + 18 + sh + 118
    d.text(M, ry2, "NAVY RAMP", family=BODY, size=12, weight=700, tracking=1.4,
           fill=C["slate_400"], name="Group label")
    ramp = [
        (C["navy_900"], "Navy 900", "Footer, deepest surface."),
        (C["navy_800"], "Navy 800", "Hero, COMPASS band, feature cards."),
        (C["navy_700"], "Navy 700", "Brand navy. CTA band, card fills."),
        (C["navy_600"], "Navy 600", "Hover state on navy surfaces."),
        (C["navy_line"], "Navy line", "Hairlines and borders on dark."),
    ]
    sw2 = (CW - 4 * 24) / 5
    for i, (hexc, name, usage) in enumerate(ramp):
        swatch(d, M + i * (sw2 + 24), ry2 + 18, sw2, 84, hexc, name, usage)

    ry3 = ry2 + 18 + 84 + 118
    d.text(M, ry3, "NEUTRALS & ACCENT RAMP", family=BODY, size=12, weight=700,
           tracking=1.4, fill=C["slate_400"], name="Group label")
    neutral = [
        (C["ink"], "Ink", "Headings and high-emphasis body."),
        (C["slate_600"], "Slate 600", "Body copy on light surfaces."),
        (C["slate_400"], "Slate 400", "Meta, placeholders, muted labels."),
        (C["line"], "Line", "Card borders, dividers."),
        (C["surface"], "Surface", "Alternating section background."),
        (C["white"], "White", "Base surface and reversed type."),
        (C["red_700"], "Red 700", "CTA hover / pressed."),
        (C["red_100"], "Red 100", "Alert pill background."),
    ]
    sw3 = (CW - 7 * 16) / 8
    for i, (hexc, name, usage) in enumerate(neutral):
        swatch(d, M + i * (sw3 + 16), ry3 + 18, sw3, 72, hexc, name, usage,
               border=hexc in (C["white"], C["surface"]))
    return ry3 + 18 + 72 + 118


# ------------------------------------------------------------ typography ----
def type_block(d, y):
    y = block_head(d, y, "03", "Typography",
                   "Varta for display · Open Sans for body — both live on the site")
    ry = y + 52
    specimens = [
        ("display", "Display", "Hero headline"),
        ("h2", "H2", "Section headings"),
        ("h3", "H3", "Service card titles"),
        ("h4", "H4", "Feature card titles"),
        ("body_lg", "Body L", "Hero and section intros"),
        ("body", "Body", "Long-form paragraphs"),
        ("small", "Small", "Card body, footer links"),
        ("eyebrow", "Eyebrow", "Section kickers, all caps"),
        ("button", "Button", "All CTA labels, all caps"),
        ("micro", "Micro", "Legal, consent, captions"),
    ]
    for name, label, usage in specimens:
        fam, size, lh, weight, tr = TYPE[name]
        row_h = max(lh + 18, 46)
        with d.group(f"Type / {label}"):
            d.text(M, ry + row_h / 2 + 4, label, family=BODY, size=13,
                   weight=700, fill=C["ink"], name="Name")
            d.text(M + 96, ry + row_h / 2 + 4,
                   f"{fam} {weight} · {size}/{lh} · {tr:+g} tracking",
                   family=BODY, size=12, weight=400, fill=C["slate_400"],
                   name="Spec")
            # Longest sample that clears the usage column on the right.
            avail = R - 210 - (M + 372)
            for candidate in ("Guiding Ambition. Charting Success.",
                              "Charting Success.", "Aa Bb Cc"):
                sample = candidate.upper() if name in ("eyebrow", "button") \
                    else candidate
                if measure(sample, fam, weight, size, tr) <= avail:
                    break
            d.text(M + 372, ry + row_h / 2 + size * 0.36, sample, family=fam,
                   size=size, weight=weight, tracking=tr, fill=C["ink"],
                   name="Sample")
            d.text(R, ry + row_h / 2 + 4, usage, family=BODY, size=12,
                   weight=400, fill=C["slate_400"], anchor="end", name="Usage")
            d.line(M, ry + row_h, R, ry + row_h, stroke=C["line"], sw=1,
                   name="Rule")
        ry += row_h
    return ry + 78


# ------------------------------------------------------------------ grid ----
def grid_block(d, y):
    y = block_head(d, y, "04", "Layout grid",
                   "1440 desktop · 390 mobile")
    ry = y + 48
    h = 244
    d.rect(M, ry, CW, h, fill=C["surface"], r=GRID["radius_md"], name="Stage")

    with d.group("Desktop grid"):
        # Scaled 1440 frame preview inside the stage.
        scale = 0.6
        fx = M + (CW - W * scale) / 2
        fy = ry + 36
        d.rect(fx, fy, W * scale, 150, fill=C["white"], stroke=C["line"], sw=1,
               name="Frame 1440")
        colw = GRID["column_width"] * scale
        gut = GRID["gutter"] * scale
        gx = fx + M * scale
        for i in range(GRID["columns"]):
            d.rect(gx + i * (colw + gut), fy + 14, colw, 122, fill=C["red_600"],
                   opacity=0.14, name="Column")
        d.line(fx + M * scale, fy - 12, fx + M * scale, fy + 150,
               stroke=C["navy"], sw=1, dash="4 4", name="Margin guide")
        d.line(fx + (W - M) * scale, fy - 12, fx + (W - M) * scale, fy + 150,
               stroke=C["navy"], sw=1, dash="4 4", name="Margin guide")
        d.text(fx + M * scale / 2, fy + 176, "120", family=BODY, size=11,
               weight=600, fill=C["slate_600"], anchor="middle",
               name="Margin label")
        d.text(fx + W * scale - M * scale / 2, fy + 176, "120", family=BODY,
               size=11, weight=600, fill=C["slate_600"], anchor="middle",
               name="Margin label")
        d.text(fx + W * scale / 2, fy + 176,
               "12 columns · 76px column · 24px gutter · 1200px content",
               family=BODY, size=12, weight=600, fill=C["slate_600"],
               anchor="middle", name="Spec")

    ny = ry + h + 44
    specs = [
        ("Desktop 1440", "120px margin · 12 cols · 24px gutter"),
        ("Mobile 390", "20px margin · 4 cols · 16px gutter"),
        ("Radius", "6 buttons/inputs · 10 cards · 16 panels · pill chips"),
        ("Spacing", "8pt base. Section padding 96–104px desktop, 56px mobile."),
    ]
    cw = (CW - 3 * 24) / 4
    for i, (t, b) in enumerate(specs):
        x = M + i * (cw + 24)
        d.text(x, ny, t, family=BODY, size=14, weight=700, fill=C["ink"],
               name=f"Spec / {t}")
        d.para(x, ny + 10, b, cw - 16, style="small", fill=C["slate_600"],
               name="Body")
    return ny + 96


# ------------------------------------------------------------ components ----
def component_block(d, y):
    y = block_head(d, y, "05", "Components", "Interactive states listed below each")
    ry = y + 48

    with d.group("Buttons"):
        d.text(M, ry, "BUTTONS", family=BODY, size=12, weight=700, tracking=1.4,
               fill=C["slate_400"], name="Group label")
        by = ry + 20
        d.rect(M, by, 592, 132, fill=C["white"], r=GRID["radius_md"],
               stroke=C["line"], sw=1, name="Light stage")
        bx = M + 28
        bx += button(d, bx, by + 28, "Primary", "primary", h=52) + 16
        bx += button(d, bx, by + 28, "Secondary", "ghost-light", h=52) + 16
        button(d, bx, by + 28, "Unlock", "gold", h=52)
        text_link(d, M + 28, by + 108, "Text link", color=C["red_600"])
        d.text(M + 168, by + 108, "Hover: Red 700 · Focus: 2px navy ring",
               family=BODY, size=12, weight=400, fill=C["slate_400"],
               name="States")

        d.rect(M + 616, by, 584, 132, fill=C["navy_800"], r=GRID["radius_md"],
               name="Dark stage")
        bx = M + 644
        bx += button(d, bx, by + 28, "Primary", "primary", h=52) + 16
        bx += button(d, bx, by + 28, "Secondary", "ghost-dark", h=52) + 16
        button(d, bx, by + 28, "On white", "white", h=52)
        d.text(M + 644, by + 108, "Reversed set for navy sections",
               family=BODY, size=12, weight=400, fill=C["on_dark_mute"],
               name="States")

    fy = by + 132 + 52
    with d.group("Form field & chips"):
        d.text(M, fy, "INPUT & CHIPS", family=BODY, size=12, weight=700,
               tracking=1.4, fill=C["slate_400"], name="Group label")
        d.rect(M, fy + 20, 380, 56, fill=C["white"], r=GRID["radius_sm"],
               stroke=C["line"], sw=1.25, name="Input / default")
        d.text(M + 18, fy + 54, "Enter your work email", family=BODY, size=15,
               weight=400, fill=C["slate_400"], name="Placeholder")
        d.rect(M + 404, fy + 20, 380, 56, fill=C["white"], r=GRID["radius_sm"],
               stroke=C["navy"], sw=2, name="Input / focus")
        d.text(M + 422, fy + 54, "ops@agency.gov", family=BODY, size=15,
               weight=400, fill=C["ink"], name="Value")
        cx = M + 808
        for label in ("HUB", "DIR-Approved", "NMSDC"):
            cx += chip(d, cx, fy + 30, label) + 12

    cy = fy + 76 + 52
    with d.group("Cards"):
        d.text(M, cy, "CARDS", family=BODY, size=12, weight=700, tracking=1.4,
               fill=C["slate_400"], name="Group label")
        cy += 20
        cw, ch = (CW - 2 * 24) / 3, 224
        # Light feature card
        card(d, M, cy, cw, ch, name="Card / Feature (light)")
        d.rect(M + 28, cy + 28, 52, 52, fill=C["surface_2"],
               r=GRID["radius_sm"], name="Icon tile")
        icon(d, "government", M + 40, cy + 40, size=28, color=C["navy"])
        d.text(M + 28, cy + 116, "Feature card", family=DISPLAY, size=20,
               weight=700, fill=C["ink"], name="Title")
        d.para(M + 28, cy + 126, "Icon tile, title, two lines of body, and an "
               "arrow link pinned to the base.", cw - 56, style="small",
               fill=C["slate_600"], name="Body")
        text_link(d, M + 28, cy + ch - 26, "Explore", color=C["red_600"])

        # Dark principle card
        x2 = M + cw + 24
        card(d, x2, cy, cw, ch, fill=C["navy_700"], stroke=C["navy_line"],
             name="Card / Principle (dark)")
        d.text(x2 + 28, cy + 48, "01", family=DISPLAY, size=15, weight=700,
               tracking=1.2, fill=C["gold"], name="Index")
        d.line(x2 + 28, cy + 66, x2 + 60, cy + 66, stroke=C["gold"], sw=2,
               name="Index rule")
        d.text(x2 + 28, cy + 112, "Principle card", family=DISPLAY, size=20,
               weight=700, fill=C["white"], name="Title")
        d.para(x2 + 28, cy + 122, "Numbered index, gold rule, icon, title and "
               "body on Navy 700.", cw - 56, style="small",
               fill=C["on_dark_soft"], name="Body")

        # Outcome card
        x3 = M + (cw + 24) * 2
        card(d, x3, cy, cw, ch, fill=C["surface"], stroke=C["line"],
             name="Card / Outcome")
        icon(d, "check", x3 + 30, cy + 30, size=30, color=C["navy"])
        d.text(x3 + 30, cy + 106, "Outcome card", family=DISPLAY, size=20,
               weight=700, fill=C["ink"], name="Title")
        d.para(x3 + 30, cy + 116, "Filled check disc, title, and supporting "
               "line. No link.", cw - 60, style="small", fill=C["slate_600"],
               name="Body")
    return cy + ch + 88


# ----------------------------------------------------------------- icons ----
def icon_block(d, y):
    y = block_head(d, y, "06", "Icon set",
                   "1.9px stroke · round caps · 24px grid")
    ry = y + 48
    kinds = [
        ("government", "Government"), ("education", "Education"),
        ("energy", "Energy"), ("corporate", "Corporate"),
        ("standardize", "Standardize"), ("control", "Control"),
        ("delay", "Find delays"), ("ownership", "Ownership"),
        ("check", "Outcome"), ("process", "Process"),
        ("program", "Programme"), ("tech", "Technology"),
        ("managed", "Managed IT"),
    ]
    cols = 7
    cw = (CW - (cols - 1) * 16) / cols
    for i, (kind, label) in enumerate(kinds):
        x = M + (i % cols) * (cw + 16)
        ty = ry + (i // cols) * 128
        with d.group(f"Icon tile / {label}"):
            d.rect(x, ty, cw, 88, fill=C["surface"], r=GRID["radius_md"],
                   name="Stage")
            icon(d, kind, x + cw / 2 - 16, ty + 28, size=32, color=C["navy"])
            d.text(x + cw / 2, ty + 108, label, family=BODY, size=12,
                   weight=600, fill=C["slate_600"], anchor="middle",
                   name="Label")
    rows = (len(kinds) + cols - 1) // cols
    return ry + rows * 128 + 60


# --------------------------------------------------------- accessibility ----
def a11y_block(d, y):
    y = block_head(d, y, "07", "Contrast", "WCAG 2.1 · computed from the tokens")
    ry = y + 48
    pairs = [
        (C["ink"], C["white"], "Ink on White", "Body & headings"),
        (C["slate_600"], C["white"], "Slate 600 on White", "Body copy"),
        (C["slate_600"], C["surface"], "Slate 600 on Surface", "Card body"),
        (C["white"], C["navy_800"], "White on Navy 800", "Hero & dark bands"),
        (C["on_dark_soft"], C["navy_800"], "On-dark soft on Navy 800", "Dark body"),
        (C["white"], C["red_600"], "White on Red 600", "Primary button"),
        (C["navy_900"], C["gold"], "Navy 900 on Gold", "Gold button"),
        (C["gold"], C["navy_800"], "Gold on Navy 800", "Eyebrow on dark"),
    ]
    rh = 52
    for i, (fg, bg, label, usage) in enumerate(pairs):
        ty = ry + i * rh
        ratio = contrast(fg, bg)
        # 14px+ bold and 18px+ regular are "large text" (AA needs 3.0).
        grade = "AAA" if ratio >= 7 else ("AA" if ratio >= 4.5
                                          else ("AA Large" if ratio >= 3
                                                else "Fail"))
        gcol = C["slate_600"] if grade != "Fail" else C["red_600"]
        with d.group(f"Contrast / {label}"):
            d.rect(M, ty + 8, 96, 36, fill=bg, r=GRID["radius_sm"],
                   stroke=C["line"] if bg == C["white"] else None, sw=1,
                   name="Sample")
            d.text(M + 48, ty + 32, "Aa", family=BODY, size=16, weight=700,
                   fill=fg, anchor="middle", name="Sample text")
            d.text(M + 120, ty + 32, label, family=BODY, size=14, weight=600,
                   fill=C["ink"], name="Pair")
            d.text(M + 460, ty + 32, usage, family=BODY, size=13, weight=400,
                   fill=C["slate_400"], name="Usage")
            d.text(M + 780, ty + 32, f"{ratio:.2f}:1", family=BODY, size=14,
                   weight=700, fill=C["ink"], name="Ratio")
            d.text(R, ty + 32, grade, family=BODY, size=13, weight=700,
                   tracking=0.6, fill=gcol, anchor="end", name="Grade")
            d.line(M, ty + rh, R, ty + rh, stroke=C["line"], sw=1, name="Rule")
    ny = ry + len(pairs) * rh + 32
    d.para(M, ny, "Every pair used across these frames clears WCAG AA (4.5:1) "
           "for normal text, and most clear AAA. Gold is reserved for bold, "
           "tracked caps on navy — it is never used for body copy, and never "
           "on a light surface.", CW, style="small", fill=C["slate_600"],
           name="Note")
    return ny + 92


# ------------------------------------------------------------------ build ---
def build(out_dir=None):
    d = Doc(W, 10, "Frame / Design system", background=C["white"])
    y = 0
    y = title_block(d, y)
    y = logo_block(d, y)
    y = colour_block(d, y)
    y = type_block(d, y)
    y = grid_block(d, y)
    y = component_block(d, y)
    y = icon_block(d, y)
    y = a11y_block(d, y)

    d.h = int(y)
    out_dir = out_dir or os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, "03-design-system.svg")
    d.save(out)
    print(f"{out}  {W}x{d.h}")
    return out


if __name__ == "__main__":
    build()
