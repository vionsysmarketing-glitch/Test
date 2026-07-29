"""Builds `preview/index.html` — a self-contained viewer for the three frames.

The page inlines the SVGs (so page @font-face applies to their text) and
inlines subset copies of Varta and Open Sans, because the Artifact CSP blocks
external font hosts.

Run:  python3 design/build_preview.py
"""

import base64
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "index.html")

FRAMES = [
    ("01-homepage-desktop.svg", "Homepage — Desktop", "1440 × 6062",
     "The full page at desktop width. Twelve sections, 120px margins on a "
     "1200px content column."),
    ("02-homepage-mobile.svg", "Homepage — Mobile", "390 × 7304",
     "The same content and design language reflowed to one column, on a "
     "reduced type scale."),
    ("03-design-system.svg", "Design system", "1440 × 4314",
     "Logo rules, colour, type scale, grid, components, the icon set, and "
     "computed contrast ratios."),
]

FONTS = [("varta-400.ttf", "Varta", 400), ("varta-500.ttf", "Varta", 500),
         ("varta-600.ttf", "Varta", 600), ("varta-700.ttf", "Varta", 700),
         ("opensans-400.ttf", "Open Sans", 400),
         ("opensans-600.ttf", "Open Sans", 600),
         ("opensans-700.ttf", "Open Sans", 700)]


def subset_font(path, text):
    """Cut a font down to the glyphs actually used, and return woff2 bytes."""
    font = TTFont(path)
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["kern", "liga", "calt"]
    opts.notdef_outline = True
    sub = Subsetter(options=opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return buf.getvalue()


def prepare_svg(markup, prefix):
    """Namespace only the ids that are referenced by url(#…).

    Layer-name ids (`Section / Hero`) are never referenced, so they stay
    pristine — Figma uses them as layer names, and a prefix would be visible
    to whoever imports the downloaded file.
    """
    refs = set(re.findall(r'url\(#([^)]+)\)', markup))
    for ref in refs:
        markup = markup.replace(f'id="{ref}"', f'id="{prefix}-{ref}"')
        markup = markup.replace(f'url(#{ref})', f'url(#{prefix}-{ref})')
    # Let CSS drive the size; keep viewBox so it scales.
    markup = re.sub(r'<svg([^>]*?)\swidth="\d+"\sheight="\d+"', r'<svg\1',
                    markup, count=1)
    return markup.strip()


def build():
    svgs, chars = [], set()
    for filename, title, dims, blurb in FRAMES:
        raw = open(os.path.join(HERE, filename), encoding="utf-8").read()
        chars |= set(re.sub(r'<[^>]+>', '', raw))
        w, h = re.search(r'width="(\d+)" height="(\d+)"', raw).groups()
        svgs.append((prepare_svg(raw, f"f{len(svgs) + 1}"), title, dims, blurb,
                     int(w), int(h)))

    # Page chrome copy needs coverage too.
    chars |= set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        " .,:;!?'\"()[]/&%$#@*+-=_×—–·→’“”")
    text = "".join(sorted(c for c in chars if c.isprintable()))

    faces = []
    for filename, family, weight in FONTS:
        data = subset_font(os.path.join(HERE, "fonts", filename), text)
        b64 = base64.b64encode(data).decode()
        faces.append(
            f"@font-face{{font-family:'{family}';font-style:normal;"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
        print(f"  {filename:18} {len(data) / 1024:6.1f} KB")

    tabs, panels = [], []
    for i, (svg, title, dims, blurb, w, h) in enumerate(svgs):
        sel = ' aria-selected="true"' if i == 0 else ' aria-selected="false"'
        tabs.append(
            f'<button class="tab" role="tab" id="tab-{i}"'
            f' aria-controls="panel-{i}"{sel} data-i="{i}">{title}</button>')
        panels.append(f"""<section class="panel{' is-active' if i == 0 else ''}"
   id="panel-{i}" role="tabpanel" aria-labelledby="tab-{i}"{'' if i == 0 else ' hidden'}>
  <div class="spec">
    <div class="spec-main">
      <h2>{title}</h2>
      <p>{blurb}</p>
    </div>
    <dl class="spec-data">
      <div><dt>Artboard</dt><dd>{dims}</dd></div>
      <div><dt>Format</dt><dd>Layered SVG</dd></div>
    </dl>
    <button class="dl" data-frame="{i}" data-name="{FRAMES[i][0]}">Download SVG</button>
  </div>
  <div class="stage">
    <div class="art" style="--nat-w:{w}px;--ratio:{h / w}">{svg}</div>
  </div>
</section>""")

    html = f"""<title>CorporateLounge — Homepage design</title>
<style>
{"".join(faces)}

:root {{
  --ground:#F7F8FA; --surface:#FFFFFF; --ink:#16181C; --muted:#666D78;
  --rule:#E2E5EA; --rule-strong:#CFD4DB; --shadow:16 24 40;
  --display:'Varta',system-ui,sans-serif; --body:'Open Sans',system-ui,sans-serif;
}}
@media (prefers-color-scheme:dark) {{
  :root {{
    --ground:#14161A; --surface:#1C1F24; --ink:#EDEFF2; --muted:#939AA5;
    --rule:#2A2E35; --rule-strong:#3A3F47; --shadow:0 0 0;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#14161A; --surface:#1C1F24; --ink:#EDEFF2; --muted:#939AA5;
  --rule:#2A2E35; --rule-strong:#3A3F47; --shadow:0 0 0;
}}
:root[data-theme="light"] {{
  --ground:#F7F8FA; --surface:#FFFFFF; --ink:#16181C; --muted:#666D78;
  --rule:#E2E5EA; --rule-strong:#CFD4DB; --shadow:16 24 40;
}}

*,*::before,*::after {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--body); font-size:15px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}}
:focus-visible {{ outline:2px solid var(--ink); outline-offset:2px; border-radius:2px; }}

.bar {{
  position:sticky; top:0; z-index:20; background:var(--surface);
  border-bottom:1px solid var(--rule);
  display:flex; flex-wrap:wrap; align-items:center; gap:20px 28px;
  padding:14px 28px;
}}
.brand {{ font-family:var(--display); font-weight:700; font-size:17px; letter-spacing:-.2px; }}
.brand span {{ color:var(--muted); font-weight:600; }}
.tabs {{ display:flex; gap:4px; margin-inline-end:auto; }}
.tab {{
  font:inherit; font-size:13.5px; font-weight:600; color:var(--muted);
  background:none; border:0; padding:7px 13px; border-radius:6px; cursor:pointer;
}}
.tab:hover {{ color:var(--ink); }}
.tab[aria-selected="true"] {{ background:var(--ink); color:var(--surface); }}
.zoom {{ display:flex; border:1px solid var(--rule-strong); border-radius:6px; overflow:hidden; }}
.zoom button {{
  font:inherit; font-size:12px; font-weight:700; letter-spacing:.06em;
  text-transform:uppercase; color:var(--muted); background:var(--surface);
  border:0; padding:7px 13px; cursor:pointer;
}}
.zoom button + button {{ border-inline-start:1px solid var(--rule-strong); }}
.zoom button[aria-pressed="true"] {{ background:var(--ink); color:var(--surface); }}

main {{ padding:0 28px 80px; }}
.panel {{ max-width:1180px; margin:0 auto; }}
.panel[hidden] {{ display:none; }}

.spec {{
  display:flex; flex-wrap:wrap; align-items:flex-end; gap:24px 40px;
  padding:40px 0 22px;
}}
.spec-main {{ flex:1 1 320px; max-width:60ch; }}
.spec h2 {{
  font-family:var(--display); font-size:27px; font-weight:700;
  letter-spacing:-.3px; margin:0 0 6px; text-wrap:balance;
}}
.spec p {{ margin:0; color:var(--muted); font-size:14.5px; }}
.spec-data {{ display:flex; gap:32px; margin:0; }}
.spec-data div {{ display:flex; flex-direction:column; gap:2px; }}
dt {{
  font-size:10.5px; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:var(--muted);
}}
dd {{ margin:0; font-size:14px; font-weight:600; font-variant-numeric:tabular-nums; }}
.dl {{
  font:inherit; font-size:13px; font-weight:700; color:var(--surface);
  background:var(--ink); border:0; padding:11px 18px; border-radius:6px;
  cursor:pointer; white-space:nowrap;
}}
.dl:hover {{ opacity:.86; }}

.stage {{
  background:var(--surface); border:1px solid var(--rule); border-radius:10px;
  padding:14px; overflow-x:auto;
  box-shadow:0 1px 2px rgb(var(--shadow)/.05), 0 12px 32px rgb(var(--shadow)/.06);
}}
.art {{ margin-inline:auto; }}
.art svg {{ display:block; width:100%; height:auto; border-radius:3px; }}
body.is-actual .art {{ width:var(--nat-w); }}
body.is-actual .art svg {{ width:var(--nat-w); }}
#panel-1 .art {{ max-width:430px; }}

.guide {{
  max-width:1180px; margin:0 auto; padding-top:64px;
  border-top:1px solid var(--rule); margin-top:64px;
  display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:40px;
}}
.guide h3 {{
  font-size:10.5px; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:var(--muted); margin:0 0 14px;
}}
.guide ol, .guide ul {{ margin:0; padding-inline-start:18px; }}
.guide li {{ margin-bottom:9px; color:var(--muted); font-size:14px; }}
.guide li strong {{ color:var(--ink); font-weight:600; }}
.guide p {{ margin:0 0 10px; color:var(--muted); font-size:14px; }}
.note {{ color:var(--ink); font-weight:600; }}

@media (max-width:720px) {{
  .bar {{ padding:12px 16px; gap:12px 16px; }}
  .tabs {{ order:3; width:100%; margin:0; overflow-x:auto; }}
  main {{ padding:0 16px 56px; }}
  .spec {{ padding-top:28px; }}
}}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<header class="bar">
  <div class="brand">CorporateLounge <span>/ Homepage design</span></div>
  <nav class="tabs" role="tablist" aria-label="Frames">{"".join(tabs)}</nav>
  <div class="zoom" role="group" aria-label="Zoom">
    <button id="z-fit" aria-pressed="true">Fit</button>
    <button id="z-act" aria-pressed="false">Actual</button>
  </div>
</header>

<main>
{"".join(panels)}

<section class="guide">
  <div>
    <h3>Open in Figma</h3>
    <ol>
      <li>Install <strong>Varta</strong> and <strong>Open Sans</strong> — both free from Google Fonts. Use the Figma desktop app.</li>
      <li>Download the SVG above.</li>
      <li>In Figma, <strong>File → Import</strong>, or drag the file onto the canvas.</li>
    </ol>
  </div>
  <div>
    <h3>What you get</h3>
    <ul>
      <li>Editable <strong>text layers</strong> — family, size, weight and tracking intact.</li>
      <li>Real vector shapes and gradients. Nothing flattened or rasterised.</li>
      <li>Named section groups matching the page, so the layer panel reads like the design.</li>
    </ul>
  </div>
  <div>
    <h3>Before this goes public</h3>
    <p class="note">Two values are placeholders.</p>
    <p>The footer email address and the three figures in the “Our story” stat row stand in for information the live site doesn’t publish. Replace both with real values.</p>
    <p>Brand colours are sampled from the CL logo artwork — navy #163969, red #C62C28, gold #F7B537.</p>
  </div>
</section>
</main>

<script>
(function () {{
  var tabs = [].slice.call(document.querySelectorAll('.tab'));
  var panels = [].slice.call(document.querySelectorAll('.panel'));

  function show(i) {{
    tabs.forEach(function (t, n) {{ t.setAttribute('aria-selected', n === i); }});
    panels.forEach(function (p, n) {{ p.hidden = n !== i; }});
    window.scrollTo({{ top: 0 }});
  }}
  tabs.forEach(function (t, i) {{
    t.addEventListener('click', function () {{ show(i); }});
    t.addEventListener('keydown', function (e) {{
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + tabs.length) % tabs.length;
      tabs[n].focus(); show(n);
    }});
  }});

  var fit = document.getElementById('z-fit'), act = document.getElementById('z-act');
  function zoom(actual) {{
    document.body.classList.toggle('is-actual', actual);
    fit.setAttribute('aria-pressed', !actual);
    act.setAttribute('aria-pressed', actual);
  }}
  fit.addEventListener('click', function () {{ zoom(false); }});
  act.addEventListener('click', function () {{ zoom(true); }});

  document.querySelectorAll('.dl').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var svg = panels[+btn.dataset.frame].querySelector('svg');
      var out = new XMLSerializer().serializeToString(svg);
      var url = URL.createObjectURL(new Blob([out], {{ type: 'image/svg+xml' }}));
      var a = document.createElement('a');
      a.href = url; a.download = btn.dataset.name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () {{ URL.revokeObjectURL(url); }}, 1000);
      var label = btn.textContent;
      btn.textContent = 'Downloaded';
      setTimeout(function () {{ btn.textContent = label; }}, 1600);
    }});
  }});
}})();
</script>
"""

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"{OUT}  {len(html) / 1024:.0f} KB")
    return OUT


if __name__ == "__main__":
    build()
