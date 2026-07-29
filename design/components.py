"""Reusable CorporateLounge UI components, drawn as Figma-friendly SVG."""

import math

from tokens import C, GRID, DISPLAY, BODY
from svgkit import measure


# ------------------------------------------------------------------ logo ----
def compass(d, cx, cy, r, ring=None, needle=None, arc=None, sw=None):
    """The CL compass mark: navy ring, gold arc, red needle."""
    ring = ring or C["navy"]
    needle = needle or C["red"]
    arc = arc or C["gold"]
    sw = sw or r * 0.30

    with d.group("Compass mark"):
        d.circle(cx, cy, r - sw / 2, stroke=ring, sw=sw, name="Ring")
        # Gold arc across the north-east quadrant of the ring.
        a0, a1 = math.radians(-72), math.radians(18)
        rr = r - sw / 2
        x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
        x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
        d.path(f"M{x0:g} {y0:g} A{rr:g} {rr:g} 0 0 1 {x1:g} {y1:g}",
               stroke=arc, sw=sw, cap="butt", name="Arc")
        # Needle: an elongated diamond on the NE–SW axis.
        L, W = r * 1.34, r * 0.30
        ux, uy = math.cos(math.radians(-58)), math.sin(math.radians(-58))
        px, py = -uy, ux
        pts = [(cx + ux * L, cy + uy * L), (cx + px * W, cy + py * W),
               (cx - ux * L, cy - uy * L), (cx - px * W, cy - py * W)]
        d.path("M" + " L".join(f"{x:g} {y:g}" for x, y in pts) + " Z",
               fill=needle, name="Needle")
        d.circle(cx, cy, r * 0.075, fill=C["white"], name="Pivot")


def logo_size(scale=1.0):
    """(width, height) of the lockup at `scale`, without drawing it."""
    size = 30 * scale
    tr = 1.2 * scale
    w = (measure("CORP", DISPLAY, 700, size, tr)
         + measure("RATE", DISPLAY, 700, size, tr)
         + size * 0.12 + size)
    return w, size * 1.30


def logo(d, x, y, scale=1.0, on_dark=False):
    """CL lockup. (x, y) is the top-left; returns (width, height)."""
    word = C["white"] if on_dark else C["navy"]
    ring = C["white"] if on_dark else C["navy"]
    size = 30 * scale
    tr = 1.2 * scale
    pre, post, sub = "CORP", "RATE", "LOUNGE"
    w_pre = measure(pre, DISPLAY, 700, size, tr)
    w_post = measure(post, DISPLAY, 700, size, tr)
    r = size * 0.50
    gap = size * 0.06
    base = y + size * 0.80
    total = w_pre + gap + r * 2 + gap + w_post

    with d.group("Logo / CorporateLounge"):
        d.text(x, base, pre, family=DISPLAY, size=size, weight=700,
               tracking=tr, fill=word, name="CORP")
        cx = x + w_pre + gap + r
        compass(d, cx, base - size * 0.335, r, ring=ring, sw=size * 0.145)
        d.text(cx + r + gap, base, post, family=DISPLAY, size=size, weight=700,
               tracking=tr, fill=word, name="RATE")
        sub_size = size * 0.60
        sub_tr = size * 0.145
        w_sub = measure(sub, DISPLAY, 700, sub_size, sub_tr)
        d.text(x + total - w_sub, base + size * 0.72, sub, family=DISPLAY,
               size=sub_size, weight=700, tracking=sub_tr, fill=C["red"],
               name="LOUNGE")
    return total, size * 1.30


# --------------------------------------------------------------- buttons ----
def button(d, x, y, label, kind="primary", h=52, pad=28, width=None,
           name=None, arrow=False):
    """Draw a button; returns its width. (x, y) is the top-left."""
    fills = {
        "primary": (C["red_600"], None, C["white"]),
        "navy": (C["navy"], None, C["white"]),
        "gold": (C["gold"], None, C["navy_900"]),
        "ghost-dark": (None, "#6F86A6", C["white"]),
        "ghost-light": (None, C["navy"], C["navy"]),
        "white": (C["white"], None, C["navy"]),
    }
    fill, stroke, fg = fills[kind]
    text = label.upper()
    size, aw = 15, (22 if arrow else 0)
    tw = measure(text, BODY, 700, size, 0.8)
    w = width or (tw + aw + pad * 2)
    # A fixed-width button (full-bleed on mobile) must not let a long label
    # spill past its edges — step the label down until it fits.
    while size > 11 and tw + aw + 32 > w:
        size -= 0.5
        tw = measure(text, BODY, 700, size, 0.8)

    with d.group(name or f"Button / {label}"):
        d.rect(x, y, w, h, fill=fill, r=GRID["radius_sm"], stroke=stroke,
               sw=1.5, name="Surface")
        tx = x + (w - tw - aw) / 2
        d.text(tx, y + h / 2 + size / 3, text, family=BODY, size=size,
               weight=700, tracking=0.8, fill=fg, name="Label")
        if arrow:
            ax, ay = tx + tw + 12, y + h / 2
            d.path(f"M{ax:g} {ay:g} H{ax + 12:g} M{ax + 7:g} {ay - 4.5:g} "
                   f"L{ax + 12:g} {ay:g} L{ax + 7:g} {ay + 4.5:g}",
                   stroke=fg, sw=1.8, name="Arrow")
    return w


def text_link(d, x, y, label, color=None, name=None):
    """Inline 'label →' link. `y` is the baseline. Returns width."""
    color = color or C["red_600"]
    w = measure(label, BODY, 700, 15, 0.3)
    with d.group(name or f"Link / {label}"):
        d.text(x, y, label, family=BODY, size=15, weight=700, tracking=0.3,
               fill=color, name="Label")
        ax = x + w + 10
        d.path(f"M{ax:g} {y - 5:g} H{ax + 13:g} M{ax + 8:g} {y - 9.5:g} "
               f"L{ax + 13:g} {y - 5:g} L{ax + 8:g} {y - 0.5:g}",
               stroke=color, sw=1.8, name="Arrow")
    return w + 23


def chip(d, x, y, label, h=38, on_dark=False, accent=False):
    """Pill chip used for certifications. Returns width."""
    tw = measure(label.upper(), BODY, 700, 12, 1.0)
    w = tw + 36
    border = C["navy_line"] if on_dark else C["line"]
    fg = C["on_dark_soft"] if on_dark else C["navy"]
    if accent:
        border, fg = C["gold"], C["gold"] if on_dark else C["gold_600"]
    with d.group(f"Chip / {label}"):
        d.rect(x, y, w, h, r=GRID["radius_pill"], stroke=border, sw=1.25,
               name="Surface")
        d.text(x + w / 2, y + h / 2 + 4, label.upper(), family=BODY, size=12,
               weight=700, tracking=1.0, fill=fg, anchor="middle", name="Label")
    return w


def chip_row(d, cx, y, labels, gap=12, h=38, on_dark=False, max_width=1200):
    """Centre-aligned, wrapping row of chips. Returns the bottom y."""
    widths = [measure(l.upper(), BODY, 700, 12, 1.0) + 36 for l in labels]
    rows, cur, cw = [], [], 0
    for lab, w in zip(labels, widths):
        add = w if not cur else w + gap
        if cur and cw + add > max_width:
            rows.append((cur, cw))
            cur, cw = [lab], w
        else:
            cur.append(lab)
            cw += add
    if cur:
        rows.append((cur, cw))

    with d.group("Certification chips"):
        for i, (row, rw) in enumerate(rows):
            rx = cx - rw / 2
            ry = y + i * (h + gap)
            for lab in row:
                rx += chip(d, rx, ry, lab, h=h, on_dark=on_dark) + gap
    return y + len(rows) * (h + gap) - gap


# ----------------------------------------------------------------- icons ----
def icon(d, kind, x, y, size=28, color=None, sw=1.9):
    """Geometric line icons, drawn inside a `size` box at (x, y)."""
    c = color or C["navy"]
    s = size
    u = s / 24.0  # unit scale against a 24px design grid

    def P(dd, **kw):
        d.path(dd, stroke=c, sw=sw, name=f"Icon / {kind}", **kw)

    with d.group(f"Icon / {kind}"):
        if kind == "government":
            P(f"M{x:g} {y + 21 * u:g} H{x + 24 * u:g}")
            P(f"M{x + 12 * u:g} {y + 2 * u:g} L{x + 22 * u:g} {y + 8 * u:g} "
              f"H{x + 2 * u:g} Z")
            for fx in (5, 11, 17):
                P(f"M{x + fx * u:g} {y + 10 * u:g} V{y + 19 * u:g}")
        elif kind == "education":
            P(f"M{x + 12 * u:g} {y + 3 * u:g} L{x + 23 * u:g} {y + 9 * u:g} "
              f"L{x + 12 * u:g} {y + 15 * u:g} L{x + 1 * u:g} {y + 9 * u:g} Z")
            P(f"M{x + 5 * u:g} {y + 11 * u:g} V{y + 17 * u:g} "
              f"C{x + 5 * u:g} {y + 20 * u:g} {x + 19 * u:g} {y + 20 * u:g} "
              f"{x + 19 * u:g} {y + 17 * u:g} V{y + 11 * u:g}")
        elif kind == "energy":
            P(f"M{x + 13 * u:g} {y + 2 * u:g} L{x + 4 * u:g} {y + 13.5 * u:g} "
              f"H{x + 11.5 * u:g} L{x + 10 * u:g} {y + 22 * u:g} "
              f"L{x + 20 * u:g} {y + 10 * u:g} H{x + 12 * u:g} Z")
        elif kind == "corporate":
            P(f"M{x + 2 * u:g} {y + 21 * u:g} H{x + 22 * u:g}")
            P(f"M{x + 3 * u:g} {y + 21 * u:g} V{y + 6 * u:g} "
              f"H{x + 13 * u:g} V{y + 21 * u:g}")
            P(f"M{x + 13 * u:g} {y + 21 * u:g} V{y + 11 * u:g} "
              f"H{x + 21 * u:g} V{y + 21 * u:g}")
            for gx, gy in ((6, 9), (10, 9), (6, 14), (10, 14), (16, 15)):
                P(f"M{x + gx * u:g} {y + gy * u:g} h{0.1 * u:g}", cap="round")
        elif kind == "standardize":
            # Three lanes snapped to one shared alignment guide.
            P(f"M{x + 4 * u:g} {y + 2.5 * u:g} V{y + 21.5 * u:g}")
            for gy in (6, 12, 18):
                d.rect(x + 8 * u, y + (gy - 2.5) * u, 13 * u, 5 * u, r=2.5 * u,
                       stroke=c, sw=sw, name="Lane")
        elif kind == "control":
            # A gate on the track: work only moves through a checkpoint.
            P(f"M{x + 2 * u:g} {y + 12 * u:g} H{x + 9 * u:g}")
            P(f"M{x + 15 * u:g} {y + 12 * u:g} H{x + 22 * u:g}")
            P(f"M{x + 18.5 * u:g} {y + 8.5 * u:g} L{x + 22 * u:g} "
              f"{y + 12 * u:g} L{x + 18.5 * u:g} {y + 15.5 * u:g}")
            d.rect(x + 9.5 * u, y + 6 * u, 5 * u, 12 * u, r=1.6 * u, fill=c,
                   name="Gate")
        elif kind == "delay":
            d.circle(x + 12 * u, y + 12 * u, 9.5 * u, stroke=c, sw=sw,
                     name="Dial")
            P(f"M{x + 12 * u:g} {y + 6.5 * u:g} V{y + 12 * u:g} "
              f"H{x + 16.5 * u:g}")
        elif kind == "ownership":
            P(f"M{x + 12 * u:g} {y + 2.5 * u:g} L{x + 21 * u:g} {y + 6.5 * u:g} "
              f"V{y + 13 * u:g} C{x + 21 * u:g} {y + 18 * u:g} "
              f"{x + 16 * u:g} {y + 20.5 * u:g} {x + 12 * u:g} {y + 21.5 * u:g} "
              f"C{x + 8 * u:g} {y + 20.5 * u:g} {x + 3 * u:g} {y + 18 * u:g} "
              f"{x + 3 * u:g} {y + 13 * u:g} V{y + 6.5 * u:g} Z")
            P(f"M{x + 8 * u:g} {y + 12 * u:g} L{x + 11 * u:g} {y + 15 * u:g} "
              f"L{x + 16.5 * u:g} {y + 9 * u:g}")
        elif kind == "check":
            d.circle(x + 12 * u, y + 12 * u, 11 * u, fill=c, name="Disc")
            d.path(f"M{x + 7 * u:g} {y + 12 * u:g} L{x + 10.5 * u:g} "
                   f"{y + 15.5 * u:g} L{x + 17 * u:g} {y + 8.5 * u:g}",
                   stroke=C["white"], sw=sw, name="Tick")
        elif kind == "process":
            for i in range(3):
                d.rect(x + 1 * u, y + (2 + i * 7.5) * u, 22 * u, 5 * u,
                       r=1.5 * u, stroke=c, sw=sw, name="Lane")
        elif kind == "program":
            P(f"M{x + 3 * u:g} {y + 20 * u:g} V{y + 4 * u:g}")
            P(f"M{x + 3 * u:g} {y + 20 * u:g} H{x + 21 * u:g}")
            for i, (bw, bh) in enumerate(((4, 6), (4, 11), (4, 15))):
                d.rect(x + (6 + i * 5) * u, y + (20 - bh) * u, bw * u, bh * u,
                       r=1 * u, stroke=c, sw=sw, name="Bar")
        elif kind == "tech":
            d.rect(x + 2 * u, y + 4 * u, 20 * u, 14 * u, r=2 * u, stroke=c,
                   sw=sw, name="Screen")
            P(f"M{x + 8 * u:g} {y + 21 * u:g} H{x + 16 * u:g}")
            P(f"M{x + 8.5 * u:g} {y + 9 * u:g} L{x + 6 * u:g} {y + 11.5 * u:g} "
              f"L{x + 8.5 * u:g} {y + 14 * u:g}")
            P(f"M{x + 15.5 * u:g} {y + 9 * u:g} L{x + 18 * u:g} "
              f"{y + 11.5 * u:g} L{x + 15.5 * u:g} {y + 14 * u:g}")
        elif kind == "managed":
            P(f"M{x + 12 * u:g} {y + 2.5 * u:g} L{x + 21 * u:g} "
              f"{y + 6.5 * u:g} V{y + 13 * u:g} C{x + 21 * u:g} {y + 18 * u:g} "
              f"{x + 16 * u:g} {y + 20.5 * u:g} {x + 12 * u:g} {y + 21.5 * u:g} "
              f"C{x + 8 * u:g} {y + 20.5 * u:g} {x + 3 * u:g} {y + 18 * u:g} "
              f"{x + 3 * u:g} {y + 13 * u:g} V{y + 6.5 * u:g} Z")
            d.circle(x + 12 * u, y + 11.5 * u, 2.6 * u, stroke=c, sw=sw,
                     name="Core")
            P(f"M{x + 12 * u:g} {y + 14.5 * u:g} V{y + 17.5 * u:g}")


# ----------------------------------------------------------------- cards ----
def card(d, x, y, w, h, fill=None, stroke=None, r=None, name="Card",
         top_rule=None):
    fill = C["white"] if fill is None else fill
    stroke = C["line"] if stroke is None else stroke
    r = GRID["radius_md"] if r is None else r
    d.rect(x, y, w, h, fill=fill, r=r, stroke=stroke, sw=1.25, name=name)
    if top_rule:
        d.rect(x + 1, y + 1, w - 2, 4, fill=top_rule, r=2, name="Accent rule")


def eyebrow(d, x, y, label, color=None, rule=True, anchor="start"):
    """Small caps eyebrow with an optional leading rule. `y` is the baseline."""
    color = color or C["red_600"]
    with d.group(f"Eyebrow / {label}"):
        if rule and anchor == "start":
            d.line(x, y - 5, x + 28, y - 5, stroke=color, sw=2, name="Rule")
            x += 40
        d.text(x, y, label.upper(), family=BODY, size=13, weight=700,
               tracking=1.6, fill=color, anchor=anchor, name="Label")
