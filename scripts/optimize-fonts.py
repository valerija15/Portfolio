#!/usr/bin/env python3
"""
Rebuilds the self-hosted fonts in src/assets/fonts from Fontsource packages:
  - limits Newsreader to wght 300–500 and opsz 24–72 (all the site uses)
  - subsets "latin" to Western Latin + typographic punctuation and
    "latin-ext" to Latin Extended-A (U+0100–017F: ā č ē ģ ī ķ ļ ņ š ū ž …)

Usage:
  npm i --no-save @fontsource-variable/newsreader @fontsource-variable/hanken-grotesk
  python3 scripts/optimize-fonts.py
Requires: pip install fonttools brotli
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NM = os.path.join(ROOT, "node_modules", "@fontsource-variable")
OUT = os.path.join(ROOT, "src", "assets", "fonts")
LATIN = "U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2013-2014,U+2018-201E,U+2022,U+2026,U+20AC,U+2122,U+2190-2193"
EXT = "U+0100-017F"

def codepoints(spec):
    out = []
    for part in spec.split(","):
        a = part[2:].split("-")
        out += range(int(a[0], 16), int(a[-1], 16) + 1)
    return out

JOBS = [
    ("newsreader", "newsreader-latin-opsz-normal", LATIN, {"wght": (300, 500), "opsz": (24, 72)}),
    ("newsreader", "newsreader-latin-opsz-italic", LATIN, {"wght": (300, 500), "opsz": (24, 72)}),
    ("newsreader", "newsreader-latin-ext-opsz-normal", EXT, {"wght": (300, 500), "opsz": (24, 72)}),
    ("newsreader", "newsreader-latin-ext-opsz-italic", EXT, {"wght": (300, 500), "opsz": (24, 72)}),
    ("hanken-grotesk", "hanken-grotesk-latin-wght-normal", LATIN, None),
    ("hanken-grotesk", "hanken-grotesk-latin-ext-wght-normal", EXT, None),
]

for pkg, name, uni, axes in JOBS:
    font = TTFont(os.path.join(NM, pkg, "files", name + ".woff2"))
    if axes:
        font = instancer.instantiateVariableFont(font, axes)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=codepoints(uni))
    sub.subset(font)
    font.flavor = "woff2"
    path = os.path.join(OUT, name + ".woff2")
    font.save(path)
    print(f"{name}: {os.path.getsize(path) // 1024} KB")
