# Fonts

Static instances of **Varta** and **Open Sans**, both from Google Fonts and
both licensed under the [SIL Open Font License 1.1](https://openfontlicense.org/).

They are vendored here for one reason: the build scripts measure real glyph
advances with Pillow so that line wrapping in the generated SVGs matches what
Figma and the browser will do. They are not embedded in the SVG output — the
frames reference the families by name, so install them locally before opening
the files in Figma.
