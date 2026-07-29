"""Design tokens for the CorporateLounge, LLC homepage design.

Colours are sampled from the official CL logo mark; type is the pairing used on
thecorporatelounge.com (Varta for display, Open Sans for body copy).
"""

# ---------------------------------------------------------------- colour ----
C = {
    # Brand — sampled from CL_Logo.png
    "navy": "#163969",       # wordmark navy, primary brand colour
    "red": "#C62C28",        # "LOUNGE" + compass needle, accent / CTA
    "gold": "#F7B537",       # compass arc, highlight

    # Extended navy ramp
    "navy_900": "#0A1526",   # footer
    "navy_800": "#0E2647",   # dark sections
    "navy_700": "#163969",   # = brand navy
    "navy_600": "#1D4C86",
    "navy_500": "#2B5490",
    "navy_line": "#24405F",  # hairlines on dark

    # Accent ramp
    "red_700": "#A6231F",
    "red_600": "#C62C28",
    "red_100": "#F7E3E2",
    "gold_600": "#DE9C1D",
    "gold_100": "#FDF1D8",

    # Neutrals
    "ink": "#10203A",
    "slate_700": "#3C4A5F",
    "slate_600": "#56657C",
    "slate_400": "#8A97AA",
    "line": "#DEE5EE",
    "surface": "#F4F7FB",
    "surface_2": "#EAF0F7",
    "white": "#FFFFFF",

    # On-dark text
    "on_dark": "#FFFFFF",
    "on_dark_soft": "#B9C6D8",
    "on_dark_mute": "#8397B2",
}

# ------------------------------------------------------------------ type ----
DISPLAY = "Varta"
BODY = "Open Sans"

# name: (family, size, line-height, weight, letter-spacing)
TYPE = {
    "display":   (DISPLAY, 56, 64, 700, -0.5),
    "h1":        (DISPLAY, 48, 56, 700, -0.4),
    "h2":        (DISPLAY, 40, 48, 700, -0.3),
    "h3":        (DISPLAY, 26, 34, 700, -0.2),
    "h4":        (DISPLAY, 20, 28, 700, 0),
    "eyebrow":   (BODY, 13, 16, 700, 1.6),
    "body_lg":   (BODY, 18, 30, 400, 0),
    "body":      (BODY, 16, 27, 400, 0),
    "small":     (BODY, 14, 22, 400, 0),
    "micro":     (BODY, 12, 18, 400, 0.2),
    "button":    (BODY, 15, 20, 700, 0.3),
    "nav":       (BODY, 15, 20, 600, 0.1),
    "stat":      (DISPLAY, 44, 50, 700, -0.5),
    "index":     (DISPLAY, 15, 20, 700, 1.2),
}

# --------------------------------------------------------------- layout ----
GRID = {
    "desktop_width": 1440,
    "margin": 120,
    "content": 1200,
    "columns": 12,
    "gutter": 24,
    "column_width": 78,      # (1200 - 11*24) / 12
    "mobile_width": 390,
    "mobile_margin": 20,
    "mobile_content": 350,
    "base_unit": 8,
    "radius_sm": 6,
    "radius_md": 10,
    "radius_lg": 16,
    "radius_pill": 999,
}
