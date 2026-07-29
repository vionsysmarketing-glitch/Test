"""Minimal SVG builder tuned for Figma import.

Figma import rules this module respects:
  * a `<g id="...">` becomes a named layer/group, so every element is grouped
    and named;
  * `<text>` becomes a real editable text layer, so no text is converted to
    paths;
  * presentation attributes are used instead of a `<style>` block, which Figma
    largely ignores;
  * explicit `y` baselines are used instead of `dominant-baseline`, which Figma
    resolves inconsistently.
"""

import os
from PIL import ImageFont

from tokens import TYPE

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_FILES = {
    ("Varta", 400): "varta-400.ttf",
    ("Varta", 500): "varta-500.ttf",
    ("Varta", 600): "varta-600.ttf",
    ("Varta", 700): "varta-700.ttf",
    ("Open Sans", 400): "opensans-400.ttf",
    ("Open Sans", 600): "opensans-600.ttf",
    ("Open Sans", 700): "opensans-700.ttf",
}
_cache = {}


def _font(family, weight, size):
    avail = sorted(w for (f, w) in _FILES if f == family)
    weight = min(avail, key=lambda w: abs(w - weight))
    key = (family, weight, round(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, _FILES[(family, weight)]), round(size))
    return _cache[key]


def measure(text, family, weight, size, tracking=0.0):
    """Advance width of `text` in px, including letter-spacing."""
    if not text:
        return 0.0
    return _font(family, weight, size).getlength(text) + tracking * len(text)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def wrap(text, max_width, family, weight, size, tracking=0.0):
    """Greedy word wrap. Honours explicit newlines as hard breaks."""
    out = []
    for para in str(text).split("\n"):
        words, line = para.split(), ""
        for w in words:
            trial = f"{line} {w}".strip()
            if line and measure(trial, family, weight, size, tracking) > max_width:
                out.append(line)
                line = w
            else:
                line = trial
        out.append(line)
    return out


class Doc:
    """Accumulates SVG markup for a single frame."""

    def __init__(self, width, height, name, background="#FFFFFF"):
        self.w, self.h, self.name, self.bg = width, height, name, background
        self.body = []
        self.defs = []
        self._ids = {}

    # -- infrastructure ----------------------------------------------------
    def uid(self, base):
        self._ids[base] = self._ids.get(base, 0) + 1
        n = self._ids[base]
        return base if n == 1 else f"{base}-{n}"

    def add(self, markup):
        self.body.append(markup)

    def define(self, markup):
        self.defs.append(markup)

    def open_group(self, name, transform=None, opacity=None, clip=None):
        a = f' id="{esc(name)}"'
        if transform:
            a += f' transform="{transform}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if clip:
            a += f' clip-path="url(#{clip})"'
        self.add(f"<g{a}>")

    def close_group(self):
        self.add("</g>")

    def group(self, name, transform=None, opacity=None, clip=None):
        return _Group(self, name, transform, opacity, clip)

    def clip_rect(self, x, y, w, h, r=0):
        """Register a rectangular clip path and return its id."""
        cid = self.uid("clip")
        rx = f' rx="{r:g}" ry="{r:g}"' if r else ""
        self.define(f'<clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" '
                    f'width="{w:g}" height="{h:g}"{rx}/></clipPath>')
        return cid

    # Sections are laid out top-down, so their height is only known after the
    # content is drawn — but the background has to paint *underneath* it.
    # mark/cut/paste let a section buffer its content, then re-emit it above a
    # background sized to fit.
    def mark(self):
        return len(self.body)

    def cut(self, index):
        chunk = self.body[index:]
        del self.body[index:]
        return chunk

    def paste(self, chunk):
        self.body.extend(chunk)

    def render(self):
        defs = ("\n<defs>\n" + "\n".join(self.defs) + "\n</defs>") if self.defs else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" fill="none">'
            f"{defs}\n"
            f'<g id="{esc(self.name)}">\n'
            f'<rect id="Canvas" x="0" y="0" width="{self.w}" height="{self.h}" fill="{self.bg}"/>\n'
            + "\n".join(self.body)
            + "\n</g>\n</svg>\n"
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.render())
        return path

    # -- primitives --------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, r=0, stroke=None, sw=1, name="Rect",
             opacity=None, ry=None):
        a = (f'<rect id="{esc(self.uid(name))}" x="{x:g}" y="{y:g}" '
             f'width="{w:g}" height="{h:g}"')
        if r:
            a += f' rx="{r:g}" ry="{(ry if ry is not None else r):g}"'
        a += f' fill="{fill}"' if fill else ' fill="none"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.add(a + "/>")
        return y + h

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1, name="Circle",
               opacity=None):
        a = f'<circle id="{esc(self.uid(name))}" cx="{cx:g}" cy="{cy:g}" r="{r:g}"'
        a += f' fill="{fill}"' if fill else ' fill="none"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.add(a + "/>")

    def path(self, d, fill=None, stroke=None, sw=1, name="Path", cap="round",
             join="round", opacity=None, dash=None):
        a = f'<path id="{esc(self.uid(name))}" d="{d}"'
        a += f' fill="{fill}"' if fill else ' fill="none"'
        if stroke:
            a += (f' stroke="{stroke}" stroke-width="{sw:g}" '
                  f'stroke-linecap="{cap}" stroke-linejoin="{join}"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.add(a + "/>")

    def line(self, x1, y1, x2, y2, stroke, sw=1, name="Line", dash=None,
             opacity=None, cap="butt"):
        a = (f'<line id="{esc(self.uid(name))}" x1="{x1:g}" y1="{y1:g}" '
             f'x2="{x2:g}" y2="{y2:g}" stroke="{stroke}" stroke-width="{sw:g}" '
             f'stroke-linecap="{cap}"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.add(a + "/>")

    # -- text --------------------------------------------------------------
    def text(self, x, y, content, style="body", fill="#10203A", anchor="start",
             name=None, family=None, size=None, weight=None, tracking=None,
             opacity=None, upper=False):
        """Draw one line of text. `y` is the baseline."""
        f, s, _lh, wt, tr = TYPE[style]
        family = family or f
        size = size or s
        weight = weight or wt
        tracking = tr if tracking is None else tracking
        if upper:
            content = str(content).upper()
        a = (f'<text id="{esc(self.uid(name or str(content)[:40] or "Text"))}" '
             f'x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size:g}" '
             f'font-weight="{weight}" fill="{fill}"')
        if tracking:
            a += f' letter-spacing="{tracking:g}"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.add(a + f">{esc(content)}</text>")
        return size

    def para(self, x, y, content, max_width, style="body", fill="#56657C",
             anchor="start", name=None, line_height=None, size=None,
             weight=None, family=None, tracking=None, upper=False, max_lines=None):
        """Wrapped paragraph. `y` is the TOP of the first line box.

        Returns the y coordinate directly below the block.
        """
        f, s, lh, wt, tr = TYPE[style]
        family = family or f
        size = size or s
        weight = weight or wt
        tracking = tr if tracking is None else tracking
        lh = line_height or (lh * (size / s) if size != s else lh)
        if upper:
            content = str(content).upper()
        lines = wrap(content, max_width, family, weight, size, tracking)
        if max_lines:
            lines = lines[:max_lines]
        gname = self.uid(name or (lines[0][:40] if lines else "Paragraph"))
        self.open_group(gname)
        # Baseline sits ~74% down the line box for these faces.
        for i, ln in enumerate(lines):
            self.text(x, y + lh * i + lh * 0.74, ln, style=style, fill=fill,
                      anchor=anchor, family=family, size=size, weight=weight,
                      tracking=tracking, name=f"line-{i + 1}")
        self.close_group()
        return y + lh * len(lines)

    def para_height(self, content, max_width, style="body", size=None,
                    line_height=None, weight=None, family=None, tracking=None):
        f, s, lh, wt, tr = TYPE[style]
        family = family or f
        size = size or s
        weight = weight or wt
        tracking = tr if tracking is None else tracking
        lh = line_height or (lh * (size / s) if size != s else lh)
        return lh * len(wrap(content, max_width, family, weight, size, tracking))


class _Group:
    def __init__(self, doc, name, transform, opacity, clip=None):
        self.doc, self.name = doc, doc.uid(name)
        self.transform, self.opacity, self.clip = transform, opacity, clip

    def __enter__(self):
        self.doc.open_group(self.name, self.transform, self.opacity, self.clip)
        return self.doc

    def __exit__(self, *exc):
        self.doc.close_group()
        return False
