"""Builds `01-homepage-desktop.svg` — the CorporateLounge homepage at 1440px.

Run:  python3 design/build_homepage.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokens import C, GRID, DISPLAY, BODY
from svgkit import Doc, measure
from components import (logo, button, text_link, chip_row, icon, card,
                        eyebrow, compass)
import content as CP

W = GRID["desktop_width"]
M = GRID["margin"]
CW = GRID["content"]
R = M + CW  # right content edge, 1320


def section(d, name, y, draw, background=None, watermark=None):
    """Run `draw(d, y) -> bottom_y`, then paint a background behind it.

    Section height depends on wrapped text, so the content is buffered and
    re-emitted above a background sized to the measured result.
    """
    start = d.mark()
    bottom = draw(d, y)
    content = d.cut(start)
    with d.group(f"Section / {name}"):
        if background:
            d.rect(0, y, W, bottom - y, fill=background, name="Background")
        if watermark:
            # Clipped to the band so decorative art never bleeds into the
            # neighbouring section.
            clip = d.clip_rect(0, y, W, bottom - y)
            with d.group("Decoration", clip=clip):
                watermark(d, y, bottom - y)
        d.paste(content)
    return bottom


def section_head(d, y, eyebrow_text, heading, sub=None, centered=True,
                 on_dark=False, heading_width=820, sub_width=700):
    """Eyebrow + H2 + optional sub-paragraph. Returns the bottom y."""
    fg = C["white"] if on_dark else C["ink"]
    sub_fg = C["on_dark_soft"] if on_dark else C["slate_600"]
    accent = C["gold"] if on_dark else C["red_600"]
    x = W / 2 if centered else M
    anchor = "middle" if centered else "start"
    with d.group(f"Section header / {heading[:32]}"):
        eyebrow(d, x, y, eyebrow_text, color=accent, rule=not centered,
                anchor=anchor)
        y = d.para(x, y + 18, heading, heading_width, style="h2", fill=fg,
                   anchor=anchor, name="Heading")
        if sub:
            y = d.para(x, y + 16, sub, sub_width, style="body_lg", fill=sub_fg,
                       anchor=anchor, name="Subheading")
    return y


# ------------------------------------------------------------ utility bar ---
def utility_bar(d, y):
    h = 44
    d.rect(0, y, W, h, fill=C["navy_900"], name="Background")
    d.text(M, y + h / 2 + 4, CP.UTILITY_LEFT, family=BODY, size=13, weight=600,
           fill=C["on_dark_soft"], name="Locale")
    d.text(R, y + h / 2 + 4, CP.UTILITY_RIGHT, family=BODY, size=13, weight=600,
           tracking=0.3, fill=C["on_dark_mute"], anchor="end",
           name="Credentials")
    return y + h


# ----------------------------------------------------------------- header ---
def header(d, y):
    h = 88
    d.rect(0, y, W, h, fill=C["white"], name="Background")
    d.line(0, y + h, W, y + h, stroke=C["line"], sw=1, name="Bottom rule")
    logo(d, M, y + 25, scale=0.80)

    with d.group("Primary navigation"):
        nx = 452
        for label in CP.NAV:
            tw = measure(label, BODY, 600, 15, 0.1)
            d.text(nx, y + h / 2 + 5, label, style="nav", fill=C["ink"],
                   name=f"Nav / {label}")
            if label == CP.NAV[0]:
                cx = nx + tw + 9
                d.path(f"M{cx:g} {y + h / 2 - 1:g} L{cx + 4.5:g} "
                       f"{y + h / 2 + 3.5:g} L{cx + 9:g} {y + h / 2 - 1:g}",
                       stroke=C["slate_400"], sw=1.6, name="Chevron")
                tw += 14
            nx += tw + 36

    with d.group("Header actions"):
        bw = 190
        button(d, R - bw, y + 18, "Schedule a Call", "primary", h=52, width=bw)
        lw = measure("Contact Us", BODY, 700, 15, 0.3) + 23
        text_link(d, R - bw - 34 - lw, y + h / 2 + 5, "Contact Us",
                  color=C["navy"])
    return y + h


# ------------------------------------------------------------------- hero ---
def hero_visual(d, x, y, w, h):
    """Floating 'process drift' telemetry card — the hero's brand illustration."""
    with d.group("Drift telemetry card"):
        d.rect(x + 12, y + 16, w, h, fill=C["navy_900"], r=GRID["radius_lg"],
               opacity=0.30, name="Shadow")
        d.rect(x, y, w, h, fill=C["white"], r=GRID["radius_lg"], name="Surface")

        pad = 28
        eyebrow(d, x + pad, y + 44, "Process telemetry", color=C["red_600"])
        d.text(x + pad, y + 82, "Intake → Approval", family=DISPLAY, size=24,
               weight=700, tracking=-0.2, fill=C["ink"], name="Card title")
        d.text(x + w - pad, y + 80, "Last 90 days", family=BODY, size=13,
               weight=600, fill=C["slate_400"], anchor="end", name="Range")
        d.line(x + pad, y + 104, x + w - pad, y + 104, stroke=C["line"], sw=1,
               name="Divider")

        tx = x + pad + 92
        tw = w - pad * 2 - 92 - 56
        lanes = [("Intake", 0.18, "+2d"), ("Review", 0.52, "+5d"),
                 ("Approval", 1.0, "+7d")]
        for i, (label, drift, delta) in enumerate(lanes):
            ly = y + 148 + i * 64
            with d.group(f"Lane / {label}"):
                d.text(x + pad, ly + 5, label, family=BODY, size=14, weight=600,
                       fill=C["slate_700"], name="Label")
                d.line(tx, ly, tx + tw, ly, stroke=C["line"], sw=2, dash="5 5",
                       cap="round", name="Standard path")
                dy = 22 * drift
                d.path(f"M{tx:g} {ly:g} C{tx + tw * 0.40:g} {ly:g} "
                       f"{tx + tw * 0.55:g} {ly + dy:g} {tx + tw:g} {ly + dy:g}",
                       stroke=C["red_600"], sw=2.6, name="Actual path")
                d.circle(tx, ly, 3.6, fill=C["white"], stroke=C["navy"], sw=2,
                         name="Start node")
                d.circle(tx + tw, ly + dy, 4.6, fill=C["red_600"],
                         name="End node")
                d.text(x + w - pad, ly + dy + 5, delta, family=BODY, size=13,
                       weight=700, fill=C["red_600"], anchor="end",
                       name="Delta")

        fy = y + h - 78
        d.line(x + pad, fy, x + w - pad, fy, stroke=C["line"], sw=1,
               name="Footer divider")
        d.rect(x + pad, fy + 20, 142, 32, fill=C["red_100"],
               r=GRID["radius_pill"], name="Alert pill")
        d.circle(x + pad + 19, fy + 36, 4, fill=C["red_600"], name="Alert dot")
        d.text(x + pad + 32, fy + 41, "DRIFT DETECTED", family=BODY, size=11,
               weight=700, tracking=0.8, fill=C["red_700"], name="Alert label")
        d.text(x + w - pad, fy + 41, "14 days lost per cycle", family=BODY,
               size=13, weight=600, fill=C["slate_600"], anchor="end",
               name="Alert value")


def hero(d, y):
    with d.group("Hero copy"):
        cy = y + 122
        eyebrow(d, M, cy, CP.HERO_EYEBROW, color=C["gold"])
        cy = d.para(M, cy + 24, CP.HERO_H1, 700, style="display",
                    fill=C["white"], name="Hero headline")
        cy = d.para(M, cy + 24, CP.HERO_SUB, 570, style="body_lg",
                    fill=C["on_dark_soft"], name="Hero subheadline")
        by = cy + 40
        bw = button(d, M, by, CP.HERO_CTA_1, "primary", h=58, arrow=True)
        button(d, M + bw + 16, by, CP.HERO_CTA_2, "ghost-dark", h=58)
        d.line(M, by + 102, M + 630, by + 102, stroke=C["navy_line"], sw=1,
               name="Divider")
        d.text(M, by + 134, CP.HERO_TRUST, family=BODY, size=14, weight=600,
               tracking=0.2, fill=C["on_dark_mute"], name="Trust line")

    hero_visual(d, 852, y + 136, 468, 412)
    return y + 676


def hero_watermark(d, y, h):
    with d.group("Background compass watermark", opacity=0.10):
        compass(d, 1190, y + 300, 300, ring=C["white"], arc=C["gold"],
                needle=C["red"], sw=26)


# --------------------------------------------------------- certifications ---
def certifications(d, y):
    d.text(W / 2, y + 54, CP.CERT_LABEL.upper(), family=BODY, size=13,
           weight=700, tracking=1.6, fill=C["slate_400"], anchor="middle",
           name="Label")
    bottom = chip_row(d, W / 2, y + 78, CP.CERTS, max_width=CW)
    return bottom + 54


# ------------------------------------------------------------- industries ---
def industries(d, y):
    cy = section_head(d, y + 96, "Who we steer", CP.IND_H2, CP.IND_SUB) + 56
    cw = (CW - 3 * 24) / 4
    tw = cw - 56
    # One shared height, driven by the longest card so the row stays even.
    title_top, gap, link_gap, pad_bottom = 108, 12, 44, 26
    ch = max(title_top + d.para_height(t, tw, "h4") + gap
             + d.para_height(b, tw, "small") + link_gap + pad_bottom
             for _, t, b in CP.INDUSTRIES)

    with d.group("Industry cards"):
        for i, (kind, title, body) in enumerate(CP.INDUSTRIES):
            x = M + i * (cw + 24)
            with d.group(f"Card / {title}"):
                card(d, x, cy, cw, ch, name="Surface")
                d.rect(x + 28, cy + 32, 56, 56, fill=C["surface_2"],
                       r=GRID["radius_sm"], name="Icon tile")
                icon(d, kind, x + 42, cy + 46, size=28, color=C["navy"])
                ty = d.para(x + 28, cy + title_top, title, tw, style="h4",
                            fill=C["ink"], name="Title")
                d.para(x + 28, ty + gap, body, tw, style="small",
                       fill=C["slate_600"], name="Body")
                text_link(d, x + 28, cy + ch - pad_bottom, "Explore",
                          color=C["red_600"])
    return cy + ch + 96


# ------------------------------------------------------------------ about ---
def about(d, y):
    with d.group("Story visual"):
        vx, vy, vw, vh = M, y + 96, 552, 432
        d.rect(vx, vy, vw, vh, fill=C["navy_800"], r=GRID["radius_lg"],
               name="Panel")
        with d.group("Compass rings", opacity=0.22):
            for rr, col in ((178, C["white"]), (130, C["white"]),
                            (82, C["gold"])):
                d.circle(vx + vw / 2, vy + vh / 2 - 16, rr, stroke=col, sw=1.25,
                         name="Ring")
        compass(d, vx + vw / 2, vy + vh / 2 - 16, 62, ring=C["white"], sw=13)
        d.rect(vx + 32, vy + vh - 108, 248, 76, fill=C["white"],
               r=GRID["radius_md"], name="Stat card")
        d.text(vx + 54, vy + vh - 64, "Houston, TX", family=DISPLAY, size=22,
               weight=700, fill=C["ink"], name="Stat value")
        d.text(vx + 54, vy + vh - 44, "Serving clients nationwide", family=BODY,
               size=13, weight=400, fill=C["slate_600"], name="Stat label")

    with d.group("Story copy"):
        tx, tw = 736, 584
        ty = y + 124
        eyebrow(d, tx, ty, "Our story", color=C["red_600"])
        ty = d.para(tx, ty + 20, CP.ABOUT_H2, tw, style="h2", fill=C["ink"],
                    name="Heading")
        ty = d.para(tx, ty + 18, CP.ABOUT_P1, tw, style="body_lg",
                    fill=C["slate_600"], name="Paragraph 1")
        ty = d.para(tx, ty + 14, CP.ABOUT_P2, tw, style="body",
                    fill=C["slate_600"], name="Paragraph 2")
        sy = ty + 36
        d.line(tx, sy, tx + tw, sy, stroke=C["line"], sw=1, name="Divider")
        with d.group("Story stats"):
            for i, (val, lab) in enumerate(CP.ABOUT_STATS):
                sx = tx + i * (tw / 3)
                d.text(sx, sy + 62, val, style="stat", fill=C["navy"],
                       name="Value")
                d.para(sx, sy + 74, lab, tw / 3 - 24, style="small",
                       fill=C["slate_600"], name="Label")
    return y + 96 + 432 + 92


# ---------------------------------------------------------------- compass ---
def compass_method(d, y):
    cy = section_head(d, y + 104, "Why COMPASS", CP.COMPASS_H2, CP.COMPASS_SUB,
                      on_dark=True) + 60
    cw = (CW - 3 * 24) / 4
    ch = max(154 + d.para_height(t, cw - 56, "h4") + 12
             + d.para_height(b, cw - 56, "small") + 36
             for _, t, b in CP.COMPASS_PRINCIPLES)
    with d.group("COMPASS principle cards"):
        for i, (kind, title, body) in enumerate(CP.COMPASS_PRINCIPLES):
            x = M + i * (cw + 24)
            with d.group(f"Card / {title}"):
                card(d, x, cy, cw, ch, fill=C["navy_700"],
                     stroke=C["navy_line"], name="Surface")
                d.text(x + 28, cy + 52, f"0{i + 1}", style="index",
                       fill=C["gold"], name="Index")
                d.line(x + 28, cy + 70, x + 60, cy + 70, stroke=C["gold"], sw=2,
                       name="Index rule")
                icon(d, kind, x + 28, cy + 100, size=30, color=C["white"])
                ty = d.para(x + 28, cy + 154, title, cw - 56, style="h4",
                            fill=C["white"], name="Title")
                d.para(x + 28, ty + 12, body, cw - 56, style="small",
                       fill=C["on_dark_soft"], name="Body")
    return cy + ch + 104


def compass_watermark(d, y, h):
    with d.group("Watermark", opacity=0.07):
        compass(d, 130, y + h - 40, 230, ring=C["white"], arc=C["gold"],
                needle=C["white"], sw=20)


# --------------------------------------------------------------- outcomes ---
def outcomes(d, y):
    cy = section_head(d, y + 96, "What changes", CP.OUT_H2, CP.OUT_SUB) + 56
    cw = (CW - 2 * 24) / 3
    ch = max(80 + d.para_height(t, cw - 64, "h4") + 10
             + d.para_height(b, cw - 64, "small") + 34
             for t, b in CP.OUTCOMES)
    with d.group("Outcome cards"):
        for i, (title, body) in enumerate(CP.OUTCOMES):
            if i < 3:
                x, ry = M + i * (cw + 24), cy
            else:
                x = M + (CW - (cw * 2 + 24)) / 2 + (i - 3) * (cw + 24)
                ry = cy + ch + 24
            with d.group(f"Card / {title[:34]}"):
                card(d, x, ry, cw, ch, fill=C["surface"], stroke=C["line"],
                     name="Surface")
                icon(d, "check", x + 32, ry + 32, size=30, color=C["navy"])
                ty = d.para(x + 32, ry + 80, title, cw - 64, style="h4",
                            fill=C["ink"], name="Title")
                d.para(x + 32, ty + 10, body, cw - 64, style="small",
                       fill=C["slate_600"], name="Body")
    return cy + ch * 2 + 24 + 96


# -------------------------------------------------------------- expertise ---
def expertise(d, y):
    cy = section_head(d, y + 96, "Our expertise", CP.EXP_H2, CP.EXP_SUB) + 56
    cw = (CW - 24) / 2
    tw = cw - 152
    title_top, gap, link_gap, pad_bottom = 62, 10, 40, 30
    ch = max(title_top + d.para_height(t, tw, "h3") + gap
             + d.para_height(b, tw, "small") + link_gap + pad_bottom
             for _, t, b in CP.SERVICES)
    with d.group("Service cards"):
        for i, (kind, title, body) in enumerate(CP.SERVICES):
            x = M + (i % 2) * (cw + 24)
            ry = cy + (i // 2) * (ch + 24)
            with d.group(f"Card / {title}"):
                card(d, x, ry, cw, ch, name="Surface")
                d.rect(x + 32, ry + 44, 60, 60, fill=C["surface_2"],
                       r=GRID["radius_sm"], name="Icon tile")
                icon(d, kind, x + 47, ry + 59, size=30, color=C["navy"])
                d.text(x + 120, ry + 56, f"0{i + 1}", style="index",
                       fill=C["slate_400"], name="Index")
                ty = d.para(x + 120, ry + title_top, title, tw, style="h3",
                            fill=C["ink"], name="Title")
                d.para(x + 120, ty + gap, body, tw, style="small",
                       fill=C["slate_600"], name="Body")
                text_link(d, x + 120, ry + ch - pad_bottom, "View solution",
                          color=C["red_600"])
    fy = cy + ch * 2 + 24 + 40
    d.text(W / 2, fy, CP.EXP_FOOT, family=BODY, size=15, weight=600,
           fill=C["slate_600"], anchor="middle", name="Closing note")
    return fy + 76


# ---------------------------------------------------------------- toolkit ---
def toolkit(d, y):
    cy, ch = y + 64, 284
    d.rect(M, cy, CW, ch, fill=C["navy_800"], r=GRID["radius_lg"],
           name="Card surface")
    d.rect(M, cy, 6, ch, fill=C["gold"], r=3, name="Accent bar")
    card_clip = d.clip_rect(M, cy, CW, ch, r=GRID["radius_lg"])
    with d.group("Watermark", opacity=0.09, clip=card_clip):
        compass(d, M + CW - 130, cy + ch / 2, 150, ring=C["white"],
                arc=C["gold"], needle=C["white"], sw=15)

    tx = M + 56
    eyebrow(d, tx, cy + 64, "Free resource", color=C["gold"])
    ty = d.para(tx, cy + 80, CP.TOOLKIT_H2, 520, style="h2", fill=C["white"],
                name="Heading")
    d.para(tx, ty + 14, CP.TOOLKIT_SUB, 500, style="body",
           fill=C["on_dark_soft"], name="Body")

    with d.group("Email capture"):
        fx, fw, fy = M + 640, 504, cy + 74
        d.rect(fx, fy, fw, 58, fill=C["white"], r=GRID["radius_sm"],
               name="Input field")
        d.text(fx + 20, fy + 36, "Enter your work email", family=BODY, size=15,
               weight=400, fill=C["slate_400"], name="Placeholder")
        button(d, fx, fy + 72, "Unlock", "gold", h=54, width=fw)
        d.text(fx, fy + 156, CP.TOOLKIT_NOTE, family=BODY, size=12, weight=400,
               fill=C["on_dark_mute"], name="Consent note")
    return cy + ch + 64


# -------------------------------------------------------------- final CTA ---
def final_cta(d, y):
    ty = d.para(W / 2, y + 78, CP.CTA_H2, 760, style="h2", fill=C["white"],
                anchor="middle", name="Heading")
    ty = d.para(W / 2, ty + 14, CP.CTA_SUB, 640, style="body_lg",
                fill=C["on_dark_soft"], anchor="middle", name="Subheading")
    w1 = measure(CP.CTA_1.upper(), BODY, 700, 15, 0.8) + 22 + 56
    w2 = measure(CP.CTA_2.upper(), BODY, 700, 15, 0.8) + 56
    bx = W / 2 - (w1 + 16 + w2) / 2
    button(d, bx, ty + 36, CP.CTA_1, "primary", h=58, arrow=True, width=w1)
    button(d, bx + w1 + 16, ty + 36, CP.CTA_2, "ghost-dark", h=58, width=w2)
    return ty + 36 + 58 + 78


def cta_watermark(d, y, h):
    with d.group("Watermark", opacity=0.07):
        for cx in (130, 1310):
            for rr in (200, 148, 96):
                d.circle(cx, y + h / 2, rr, stroke=C["white"], sw=1.5,
                         name="Ring")


# ----------------------------------------------------------------- footer ---
def footer(d, y):
    h = 472
    with d.group("Footer brand"):
        logo(d, M, y + 74, scale=0.78, on_dark=True)
        d.para(M, y + 140, CP.FOOTER_TAGLINE, 320, style="small",
               fill=C["on_dark_mute"], name="Tagline")
        d.text(M, y + 224, "Houston, Texas", family=BODY, size=14, weight=600,
               fill=C["on_dark_soft"], name="Location")
        d.text(M, y + 250, CP.FOOTER_EMAIL, family=BODY, size=14,
               weight=400, fill=C["on_dark_mute"], name="Email")

    with d.group("Footer navigation"):
        colx = 620
        colw = (R - colx) / 4
        for i, (title, links) in enumerate(CP.FOOTER_COLUMNS):
            x = colx + i * colw
            with d.group(f"Column / {title}"):
                d.text(x, y + 80, title.upper(), family=BODY, size=12,
                       weight=700, tracking=1.4, fill=C["white"],
                       name="Heading")
                ly = y + 108
                for link in links:
                    ly = d.para(x, ly, link, colw - 28, style="small",
                                fill=C["on_dark_mute"], name=f"Link / {link}")
                    ly += 10

    with d.group("Footer certifications"):
        fy = y + h - 136
        d.line(M, fy, R, fy, stroke=C["navy_line"], sw=1, name="Divider")
        d.text(M, fy + 36, CP.FOOTER_CERTS, family=BODY, size=12, weight=600,
               tracking=0.4, fill=C["on_dark_mute"], name="Certifications")

    with d.group("Footer bottom bar"):
        by = y + h - 76
        d.line(M, by, R, by, stroke=C["navy_line"], sw=1, name="Divider")
        d.text(M, by + 44, CP.FOOTER_COPYRIGHT, family=BODY, size=13,
               weight=400, fill=C["on_dark_mute"], name="Copyright")
        sx = R - 88
        for i, tag in enumerate(("in", "X", "f")):
            d.circle(sx + i * 40, by + 39, 16, stroke=C["navy_line"], sw=1.25,
                     name="Social ring")
            d.text(sx + i * 40, by + 44, tag, family=BODY, size=12, weight=700,
                   fill=C["on_dark_soft"], anchor="middle", name=f"Social / {tag}")
    return y + h


# ------------------------------------------------------------------ build ---
def build(out_dir=None):
    d = Doc(W, 10, "Frame / Homepage — Desktop 1440", background=C["white"])
    d.define(
        '<linearGradient id="heroGradient" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{C["navy_800"]}"/>'
        f'<stop offset="1" stop-color="{C["navy_900"]}"/></linearGradient>')

    y = 0
    y = section(d, "Utility bar", y, utility_bar)
    y = section(d, "Header", y, header)
    y = section(d, "Hero", y, hero, "url(#heroGradient)", hero_watermark)
    y = section(d, "Contracts and certifications", y, certifications, C["white"])
    y = section(d, "Industries", y, industries, C["surface"])
    y = section(d, "We Are CorporateLounge", y, about, C["white"])
    y = section(d, "COMPASS method", y, compass_method, C["navy_800"],
                compass_watermark)
    y = section(d, "What changes when we step in", y, outcomes, C["white"])
    y = section(d, "Our expertise", y, expertise, C["surface"])
    y = section(d, "Free toolkit", y, toolkit, C["white"])
    y = section(d, "Final CTA", y, final_cta, C["navy_700"], cta_watermark)
    y = section(d, "Footer", y, footer, C["navy_900"])

    d.h = int(y)
    out_dir = out_dir or os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, "01-homepage-desktop.svg")
    d.save(out)
    print(f"{out}  {W}x{d.h}")
    return out


if __name__ == "__main__":
    build()
