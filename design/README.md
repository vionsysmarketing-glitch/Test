# CorporateLounge, LLC — Homepage Design

A homepage design for [thecorporatelounge.com](https://www.thecorporatelounge.com/),
delivered as layered SVG frames that import into Figma as editable layers.

| File | Frame | Size |
|---|---|---|
| `01-homepage-desktop.svg` | Homepage — Desktop | 1440 × 6062 |
| `02-homepage-mobile.svg` | Homepage — Mobile | 390 × 7304 |
| `03-design-system.svg` | Design system | 1440 × 4314 |

PNG previews of all three are in `preview/`.

## Importing into Figma

1. Install the two fonts first, so text lands with the right metrics —
   **[Varta](https://fonts.google.com/specimen/Varta)** and
   **[Open Sans](https://fonts.google.com/specimen/Open+Sans)**, both free from
   Google Fonts. (Use the Figma desktop app; the browser version only sees
   fonts exposed by the Font Helper.)
2. In Figma: **File → Import**, or drag the `.svg` files onto the canvas.
3. Each file arrives as one named frame containing named section groups
   (`Section / Hero`, `Section / Footer`, …), so the layer panel matches the
   page structure.

Everything imports as native vector: text stays editable text, shapes stay
shapes, nothing is flattened or rasterised. Colours land as literal fills —
to turn them into a library, select a swatch in `03-design-system.svg` and
create a style from it.

### What Figma does on import

- `<text>` → editable text layers, with font family, size, weight, and
  letter-spacing preserved.
- `<g id="…">` → groups named from the `id`.
- `clipPath` → clipped groups (used to keep the decorative compass artwork
  inside its section band).
- Gradients → real gradient fills.

Figma has no concept of an SVG "auto-layout", so groups import as absolute
positioned layers. Adding auto-layout to the card rows is a quick manual pass
if you want them to reflow.

## Design decisions

**Colour** is sampled directly from the official CL logo artwork rather than
from the current site CSS: navy `#163969`, red `#C62C28`, gold `#F7B537`. The
live site's stylesheet is mostly Divi defaults (`#2ea3f2` and friends) that
don't reflect the brand mark. The navy ramp and neutrals are built around
those three.

**Type** keeps the pairing already loaded on the live site — Varta for display
and Open Sans for body — so the design doesn't introduce a new typeface
dependency.

**Copy** is verbatim from the live homepage wherever the site has it: the hero
headline and subheadline, the four COMPASS principles, the five "what changes"
outcomes, the section headings, and the CTA labels. Supporting body copy was
written to match the site's voice in the places where the live page uses
imagery or long-form blocks that don't map onto a design comp. Every value in
`content.py` is tagged `[site]` or `[authored]` so the two are never confused.

Two `[authored]` values are placeholders standing in for information the live
site doesn't publish, and should be replaced before this design is used
publicly: the footer email address (`FOOTER_EMAIL`) and the three figures in
the "Our story" stat row (`ABOUT_STATS`).

**The hero illustration** is a "process drift" telemetry card — three workflow
lanes diverging from their standard path, with a drift alert. It gives the
hero a concrete visual for the headline's claim instead of stock imagery, and
it's built from the same primitives as the rest of the design.

**Accessibility**: every foreground/background pair used across the frames
clears WCAG AA (4.5:1) for normal text; most clear AAA. The ratios are
computed from the tokens and listed in block 07 of the design system frame.

## Regenerating

The frames are generated, so edits to copy or tokens propagate to every frame
rather than needing to be repeated by hand.

```bash
cd design
python3 build_homepage.py     # 01-homepage-desktop.svg
python3 build_mobile.py       # 02-homepage-mobile.svg
python3 build_styleguide.py   # 03-design-system.svg
```

Requires Python 3 and Pillow (used only to measure text for line wrapping,
against the TTFs in `fonts/`).

| Module | Purpose |
|---|---|
| `tokens.py` | Colour, type scale, grid and radius tokens |
| `content.py` | All homepage copy |
| `svgkit.py` | SVG document builder with Figma-friendly output |
| `components.py` | Logo, compass mark, buttons, chips, cards, icons |
| `build_*.py` | One script per frame |
