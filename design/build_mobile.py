"""Builds `02-homepage-mobile.svg` — the CorporateLounge homepage at 390px.

Same content and design language as the desktop frame, re-flowed to a single
column with a reduced type scale.

Run:  python3 design/build_mobile.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokens import C, GRID, DISPLAY, BODY
from svgkit import Doc, measure
from components import (logo, button, text_link, chip_row, icon, card,
                        eyebrow, compass)
import content as CP

W = GRID["mobile_width"]
M = GRID["mobile_margin"]
CW = GRID["mobile_content"]
R = M + CW

# Mobile type scale — sizes and line heights applied as overrides.
DISPLAY_S, DISPLAY_LH = 34, 41
H2_S, H2_LH = 27, 34
H3_S, H3_LH = 19, 26
BODY_S, BODY_LH = 15, 25
SMALL_S, SMALL_LH = 14, 22


def section(d, name, y, draw, background=None, watermark=None):
    start = d.mark()
    bottom = draw(d, y)
    content = d.cut(start)
    with d.group(f"Section / {name}"):
        if background:
            d.rect(0, y, W, bottom - y, fill=background, name="Background")
        if watermark:
            clip = d.clip_rect(0, y, W, bottom - y)
            with d.group("Decoration", clip=clip):
                watermark(d, y, bottom - y)
        d.paste(content)
    return bottom


def stacked_card_metrics(d, title, body, title_top, title_w, body_w,
                         icon_bottom, gap=6, pad_bottom=24):
    """Geometry for a stacked mobile card, so height matches what's drawn."""
    title_bottom = title_top + d.para_height(title, title_w, "h4", size=H3_S,
                                             line_height=H3_LH)
    body_top = max(title_bottom, icon_bottom) + gap
    body_bottom = body_top + d.para_height(body, body_w, "small", size=SMALL_S,
                                           line_height=SMALL_LH)
    return body_top, body_bottom + pad_bottom


def head(d, y, eyebrow_text, heading, sub=None, on_dark=False):
    fg = C["white"] if on_dark else C["ink"]
    sub_fg = C["on_dark_soft"] if on_dark else C["slate_600"]
    accent = C["gold"] if on_dark else C["red_600"]
    with d.group(f"Section header / {heading[:32]}"):
        eyebrow(d, M, y, eyebrow_text, color=accent)
        y = d.para(M, y + 16, heading, CW, style="h2", size=H2_S,
                   line_height=H2_LH, fill=fg, name="Heading")
        if sub:
            y = d.para(M, y + 12, sub, CW, style="body", size=BODY_S,
                       line_height=BODY_LH, fill=sub_fg, name="Subheading")
    return y


# ----------------------------------------------------------------- header ---
def header(d, y):
    h = 68
    d.rect(0, y, W, h, fill=C["white"], name="Background")
    d.line(0, y + h, W, y + h, stroke=C["line"], sw=1, name="Bottom rule")
    logo(d, M, y + 18, scale=0.66)
    with d.group("Menu button"):
        bx = R - 30
        for i in range(3):
            d.line(bx, y + 26 + i * 8, bx + 30, y + 26 + i * 8,
                   stroke=C["navy"], sw=2, cap="round", name="Bar")
    return y + h


# ------------------------------------------------------------------- hero ---
def hero_card(d, x, y, w):
    h = 302
    with d.group("Drift telemetry card"):
        d.rect(x, y, w, h, fill=C["white"], r=GRID["radius_md"], name="Surface")
        pad = 20
        eyebrow(d, x + pad, y + 34, "Process telemetry", color=C["red_600"],
                rule=False)
        d.text(x + pad, y + 66, "Intake → Approval", family=DISPLAY, size=19,
               weight=700, fill=C["ink"], name="Card title")
        d.line(x + pad, y + 84, x + w - pad, y + 84, stroke=C["line"], sw=1,
               name="Divider")

        tx = x + pad + 68
        tw = w - pad * 2 - 68 - 40
        for i, (label, drift, delta) in enumerate(
                [("Intake", 0.18, "+2d"), ("Review", 0.52, "+5d"),
                 ("Approval", 1.0, "+7d")]):
            ly = y + 116 + i * 46
            with d.group(f"Lane / {label}"):
                d.text(x + pad, ly + 4, label, family=BODY, size=12, weight=600,
                       fill=C["slate_700"], name="Label")
                d.line(tx, ly, tx + tw, ly, stroke=C["line"], sw=1.75,
                       dash="4 4", cap="round", name="Standard path")
                dy = 16 * drift
                d.path(f"M{tx:g} {ly:g} C{tx + tw * 0.40:g} {ly:g} "
                       f"{tx + tw * 0.55:g} {ly + dy:g} {tx + tw:g} {ly + dy:g}",
                       stroke=C["red_600"], sw=2.2, name="Actual path")
                d.circle(tx + tw, ly + dy, 3.6, fill=C["red_600"],
                         name="End node")
                d.text(x + w - pad, ly + dy + 4, delta, family=BODY, size=12,
                       weight=700, fill=C["red_600"], anchor="end",
                       name="Delta")

        fy = y + h - 58
        d.line(x + pad, fy, x + w - pad, fy, stroke=C["line"], sw=1,
               name="Footer divider")
        d.rect(x + pad, fy + 14, 128, 28, fill=C["red_100"],
               r=GRID["radius_pill"], name="Alert pill")
        d.circle(x + pad + 17, fy + 28, 3.5, fill=C["red_600"], name="Alert dot")
        d.text(x + pad + 28, fy + 32, "DRIFT DETECTED", family=BODY, size=10,
               weight=700, tracking=0.7, fill=C["red_700"], name="Alert label")
        d.text(x + w - pad, fy + 32, "14 days lost", family=BODY, size=12,
               weight=600, fill=C["slate_600"], anchor="end", name="Alert value")
    return y + h


def hero(d, y):
    cy = y + 56
    eyebrow(d, M, cy, CP.HERO_EYEBROW, color=C["gold"], rule=False)
    cy = d.para(M, cy + 16, CP.HERO_H1, CW, style="display", size=DISPLAY_S,
                line_height=DISPLAY_LH, fill=C["white"], name="Hero headline")
    cy = d.para(M, cy + 16, CP.HERO_SUB, CW, style="body", size=BODY_S,
                line_height=BODY_LH, fill=C["on_dark_soft"],
                name="Hero subheadline")
    cy += 28
    button(d, M, cy, CP.HERO_CTA_1, "primary", h=54, width=CW, arrow=True)
    button(d, M, cy + 66, CP.HERO_CTA_2, "ghost-dark", h=54, width=CW)
    cy = hero_card(d, M, cy + 66 + 54 + 32, CW)
    return cy + 56


def hero_watermark(d, y, h):
    with d.group("Background compass watermark", opacity=0.09):
        compass(d, 340, y + 120, 170, ring=C["white"], arc=C["gold"],
                needle=C["red"], sw=16)


# --------------------------------------------------------- certifications ---
def certifications(d, y):
    d.text(W / 2, y + 42, CP.CERT_LABEL.upper(), family=BODY, size=11,
           weight=700, tracking=1.4, fill=C["slate_400"], anchor="middle",
           name="Label")
    bottom = chip_row(d, W / 2, y + 62, CP.CERTS, h=32, gap=8, max_width=CW)
    return bottom + 44


# ------------------------------------------------------------- industries ---
def industries(d, y):
    cy = head(d, y + 56, "Who we steer", CP.IND_H2, CP.IND_SUB) + 32
    for kind, title, body in CP.INDUSTRIES:
        body_top, ch = stacked_card_metrics(d, title, body, 24, CW - 100,
                                            CW - 40, 70)
        with d.group(f"Card / {title}"):
            card(d, M, cy, CW, ch, name="Surface")
            d.rect(M + 20, cy + 22, 44, 44, fill=C["surface_2"],
                   r=GRID["radius_sm"], name="Icon tile")
            icon(d, kind, M + 31, cy + 33, size=22, color=C["navy"])
            d.para(M + 78, cy + 24, title, CW - 100, style="h4", size=H3_S,
                   line_height=H3_LH, fill=C["ink"], name="Title")
            d.para(M + 20, cy + body_top, body, CW - 40, style="small",
                   size=SMALL_S, line_height=SMALL_LH, fill=C["slate_600"],
                   name="Body")
        cy += ch + 16
    return cy + 40


# ------------------------------------------------------------------ about ---
def about(d, y):
    vy, vh = y + 56, 260
    d.rect(M, vy, CW, vh, fill=C["navy_800"], r=GRID["radius_lg"], name="Panel")
    pclip = d.clip_rect(M, vy, CW, vh, r=GRID["radius_lg"])
    with d.group("Compass rings", opacity=0.22, clip=pclip):
        for rr in (118, 86, 56):
            d.circle(W / 2, vy + vh / 2, rr, stroke=C["white"], sw=1.25,
                     name="Ring")
    compass(d, W / 2, vy + vh / 2, 44, ring=C["white"], sw=9)

    cy = vy + vh + 40
    eyebrow(d, M, cy, "Our story", color=C["red_600"])
    cy = d.para(M, cy + 16, CP.ABOUT_H2, CW, style="h2", size=H2_S,
                line_height=H2_LH, fill=C["ink"], name="Heading")
    cy = d.para(M, cy + 14, CP.ABOUT_P1, CW, style="body", size=BODY_S,
                line_height=BODY_LH, fill=C["slate_600"], name="Paragraph 1")
    cy = d.para(M, cy + 12, CP.ABOUT_P2, CW, style="small", size=SMALL_S,
                line_height=SMALL_LH, fill=C["slate_600"], name="Paragraph 2")

    cy += 28
    d.line(M, cy, R, cy, stroke=C["line"], sw=1, name="Divider")
    with d.group("Story stats"):
        for i, (val, lab) in enumerate(CP.ABOUT_STATS):
            sx = M + i * (CW / 3)
            d.text(sx, cy + 48, val, family=DISPLAY, size=30, weight=700,
                   fill=C["navy"], name="Value")
            d.para(sx, cy + 58, lab, CW / 3 - 12, style="micro",
                   fill=C["slate_600"], name="Label")
    return cy + 118


# ---------------------------------------------------------------- compass ---
def compass_method(d, y):
    cy = head(d, y + 60, "Why COMPASS", CP.COMPASS_H2, CP.COMPASS_SUB,
              on_dark=True) + 32
    for i, (kind, title, body) in enumerate(CP.COMPASS_PRINCIPLES):
        body_top, ch = stacked_card_metrics(d, title, body, 26, CW - 116,
                                            CW - 40, 66, pad_bottom=26)
        with d.group(f"Card / {title}"):
            card(d, M, cy, CW, ch, fill=C["navy_700"], stroke=C["navy_line"],
                 name="Surface")
            d.text(M + 20, cy + 40, f"0{i + 1}", style="index", fill=C["gold"],
                   name="Index")
            icon(d, kind, M + 58, cy + 24, size=24, color=C["white"])
            d.para(M + 94, cy + 26, title, CW - 116, style="h4", size=H3_S,
                   line_height=H3_LH, fill=C["white"], name="Title")
            d.para(M + 20, cy + body_top, body, CW - 40, style="small",
                   size=SMALL_S, line_height=SMALL_LH, fill=C["on_dark_soft"],
                   name="Body")
        cy += ch + 14
    return cy + 44


def compass_watermark(d, y, h):
    with d.group("Watermark", opacity=0.07):
        compass(d, 40, y + h - 40, 180, ring=C["white"], arc=C["gold"],
                needle=C["white"], sw=16)


# --------------------------------------------------------------- outcomes ---
def outcomes(d, y):
    cy = head(d, y + 56, "What changes", CP.OUT_H2, CP.OUT_SUB) + 28
    for i, (title, body) in enumerate(CP.OUTCOMES):
        with d.group(f"Outcome / {title[:34]}"):
            icon(d, "check", M, cy + 2, size=24, color=C["navy"])
            ty = d.para(M + 38, cy, title, CW - 38, style="h4", size=17,
                        line_height=24, fill=C["ink"], name="Title")
            ty = d.para(M + 38, ty + 6, body, CW - 38, style="small",
                        size=SMALL_S, line_height=SMALL_LH,
                        fill=C["slate_600"], name="Body")
        cy = ty + 22
        if i < len(CP.OUTCOMES) - 1:
            d.line(M, cy, R, cy, stroke=C["line"], sw=1, name="Divider")
            cy += 22
    return cy + 34


# -------------------------------------------------------------- expertise ---
def expertise(d, y):
    cy = head(d, y + 56, "Our expertise", CP.EXP_H2, CP.EXP_SUB) + 32
    for i, (kind, title, body) in enumerate(CP.SERVICES):
        body_top, ch = stacked_card_metrics(d, title, body, 38, CW - 100,
                                            CW - 40, 70)
        with d.group(f"Card / {title}"):
            card(d, M, cy, CW, ch, name="Surface")
            d.rect(M + 20, cy + 22, 44, 44, fill=C["surface_2"],
                   r=GRID["radius_sm"], name="Icon tile")
            icon(d, kind, M + 31, cy + 33, size=22, color=C["navy"])
            d.text(M + 78, cy + 34, f"0{i + 1}", family=DISPLAY, size=12,
                   weight=700, tracking=1.2, fill=C["slate_400"], name="Index")
            d.para(M + 78, cy + 38, title, CW - 100, style="h4", size=H3_S,
                   line_height=H3_LH, fill=C["ink"], name="Title")
            d.para(M + 20, cy + body_top, body, CW - 40, style="small",
                   size=SMALL_S, line_height=SMALL_LH, fill=C["slate_600"],
                   name="Body")
        cy += ch + 16
    ty = d.para(M, cy + 8, CP.EXP_FOOT, CW, style="small", size=SMALL_S,
                line_height=SMALL_LH, fill=C["slate_600"], anchor="start",
                name="Closing note")
    return ty + 48


# ---------------------------------------------------------------- toolkit ---
def toolkit(d, y):
    cy = y + 44
    tx = M + 24
    iw = CW - 48
    th = d.para_height(CP.TOOLKIT_H2, iw, "h2", size=H2_S, line_height=H2_LH)
    bh = d.para_height(CP.TOOLKIT_SUB, iw, "small", size=SMALL_S,
                       line_height=SMALL_LH)
    ch = 40 + 18 + th + 12 + bh + 26 + 52 + 12 + 52 + 30 + 24

    d.rect(M, cy, CW, ch, fill=C["navy_800"], r=GRID["radius_lg"],
           name="Card surface")
    d.rect(M, cy, 5, ch, fill=C["gold"], r=2.5, name="Accent bar")
    cclip = d.clip_rect(M, cy, CW, ch, r=GRID["radius_lg"])
    with d.group("Watermark", opacity=0.09, clip=cclip):
        compass(d, R - 40, cy + 70, 110, ring=C["white"], arc=C["gold"],
                needle=C["white"], sw=11)

    ty = cy + 40
    eyebrow(d, tx, ty, "Free resource", color=C["gold"], rule=False)
    ty = d.para(tx, ty + 12, CP.TOOLKIT_H2, iw, style="h2", size=H2_S,
                line_height=H2_LH, fill=C["white"], name="Heading")
    ty = d.para(tx, ty + 12, CP.TOOLKIT_SUB, iw, style="small", size=SMALL_S,
                line_height=SMALL_LH, fill=C["on_dark_soft"], name="Body")

    with d.group("Email capture"):
        fy = ty + 26
        d.rect(tx, fy, iw, 52, fill=C["white"], r=GRID["radius_sm"],
               name="Input field")
        d.text(tx + 16, fy + 33, "Enter your work email", family=BODY, size=14,
               weight=400, fill=C["slate_400"], name="Placeholder")
        button(d, tx, fy + 64, "Unlock", "gold", h=52, width=iw)
        d.text(tx, fy + 138, CP.TOOLKIT_NOTE, family=BODY, size=11, weight=400,
               fill=C["on_dark_mute"], name="Consent note")
    return cy + ch + 44


# -------------------------------------------------------------- final CTA ---
def final_cta(d, y):
    ty = d.para(M, y + 56, CP.CTA_H2, CW, style="h2", size=H2_S,
                line_height=H2_LH, fill=C["white"], name="Heading")
    ty = d.para(M, ty + 12, CP.CTA_SUB, CW, style="body", size=BODY_S,
                line_height=BODY_LH, fill=C["on_dark_soft"],
                name="Subheading")
    button(d, M, ty + 28, CP.CTA_1, "primary", h=54, width=CW, arrow=True)
    button(d, M, ty + 28 + 66, CP.CTA_2, "ghost-dark", h=54, width=CW)
    return ty + 28 + 66 + 54 + 56


def cta_watermark(d, y, h):
    with d.group("Watermark", opacity=0.07):
        for rr in (170, 124, 80):
            d.circle(W - 30, y + h / 2, rr, stroke=C["white"], sw=1.5,
                     name="Ring")


# ----------------------------------------------------------------- footer ---
def footer(d, y):
    logo(d, M, y + 48, scale=0.62, on_dark=True)
    cy = d.para(M, y + 96, CP.FOOTER_TAGLINE, CW, style="small",
                size=SMALL_S, line_height=SMALL_LH, fill=C["on_dark_mute"],
                name="Tagline")

    cy += 28
    colw = CW / 2
    with d.group("Footer navigation"):
        for i, (title, links) in enumerate(CP.FOOTER_COLUMNS):
            x = M + (i % 2) * colw
            ry = cy + (i // 2) * 172
            with d.group(f"Column / {title}"):
                d.text(x, ry, title.upper(), family=BODY, size=11, weight=700,
                       tracking=1.3, fill=C["white"], name="Heading")
                ly = ry + 14
                for link in links:
                    ly = d.para(x, ly, link, colw - 16, style="micro",
                                fill=C["on_dark_mute"], name=f"Link / {link}")
                    ly += 8
    cy += 172 * 2 - 24

    d.line(M, cy, R, cy, stroke=C["navy_line"], sw=1, name="Divider")
    d.text(M, cy + 30, "Houston, Texas", family=BODY, size=13, weight=600,
           fill=C["on_dark_soft"], name="Location")
    d.text(M, cy + 52, CP.FOOTER_EMAIL, family=BODY, size=13,
           weight=400, fill=C["on_dark_mute"], name="Email")

    with d.group("Social"):
        for i, tag in enumerate(("in", "X", "f")):
            d.circle(M + 15 + i * 38, cy + 92, 15, stroke=C["navy_line"],
                     sw=1.25, name="Social ring")
            d.text(M + 15 + i * 38, cy + 97, tag, family=BODY, size=11,
                   weight=700, fill=C["on_dark_soft"], anchor="middle",
                   name=f"Social / {tag}")

    cy += 128
    d.line(M, cy, R, cy, stroke=C["navy_line"], sw=1, name="Divider")
    d.text(M, cy + 32, CP.FOOTER_COPYRIGHT, family=BODY, size=12, weight=400,
           fill=C["on_dark_mute"], name="Copyright")
    return cy + 62


# ------------------------------------------------------------------ build ---
def build(out_dir=None):
    d = Doc(W, 10, "Frame / Homepage — Mobile 390", background=C["white"])
    d.define(
        '<linearGradient id="heroGradientM" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{C["navy_800"]}"/>'
        f'<stop offset="1" stop-color="{C["navy_900"]}"/></linearGradient>')

    y = 0
    y = section(d, "Header", y, header)
    y = section(d, "Hero", y, hero, "url(#heroGradientM)", hero_watermark)
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
    out = os.path.join(out_dir, "02-homepage-mobile.svg")
    d.save(out)
    print(f"{out}  {W}x{d.h}")
    return out


if __name__ == "__main__":
    build()
