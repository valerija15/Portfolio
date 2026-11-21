#!/usr/bin/env python3
"""
Generates the fictional placeholder media used by the site (images, posters,
looping videos, OG image, CV PDF). Everything it writes is meant to be
REPLACED with real assets — see README › "Replacing images and videos".

Run:  npm run media:placeholders   (requires Python 3 + Pillow, and ffmpeg for videos)
"""
import math, os, random, shutil, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "src", "assets", "images")
PUB = os.path.join(ROOT, "public")
os.makedirs(IMG, exist_ok=True)
for d in ("video", "cv", "og"):
    os.makedirs(os.path.join(PUB, d), exist_ok=True)

PALETTES = {
    "sand":  [(226, 218, 203), (196, 182, 160), (120, 104, 86), (46, 42, 38)],
    "clay":  [(214, 196, 180), (178, 120, 92), (122, 74, 54), (36, 30, 28)],
    "olive": [(206, 205, 188), (128, 128, 96), (78, 80, 58), (30, 31, 26)],
    "stone": [(220, 220, 214), (168, 168, 160), (96, 98, 98), (28, 29, 30)],
    "ink":   [(62, 64, 68), (38, 40, 44), (150, 140, 124), (16, 16, 18)],
    "rose":  [(228, 214, 206), (196, 160, 148), (120, 86, 78), (40, 32, 32)],
}

def grain(img, amount=14, seed=0):
    rnd = random.Random(seed)
    noise = Image.effect_noise(img.size, 64).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) * amount // 64)
    base = img.convert("RGB")
    overlay = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(base, Image.composite(base, overlay, Image.new("L", img.size, 200)), 0.18)

def vignette(img, strength=0.35):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.18))
    dark = Image.new("RGB", (w, h), (12, 12, 12))
    return Image.composite(img, Image.blend(img, dark, strength), mask)

def soft_shadow(layer_draw_fn, size, blur, offset=(0, 0), opacity=90):
    sh = Image.new("L", size, 0)
    layer_draw_fn(ImageDraw.Draw(sh), offset)
    return sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * opacity // 255)

def light_falloff(img, pal, seed):
    """Window-light wash: a large blurred bright shape from one side."""
    w, h = img.size
    rnd = random.Random(seed)
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    x = rnd.choice([-0.3, 0.55])
    d.polygon([(w * x, 0), (w * (x + 0.75), 0), (w * (x + 0.45), h), (w * (x - 0.3), h)], fill=110)
    m = m.filter(ImageFilter.GaussianBlur(w * 0.08))
    return Image.composite(Image.new("RGB", (w, h), tuple(min(255, c + 22) for c in pal[0])), img, m)

# ---------- scenes ---------------------------------------------------------

def scene_portrait(w, h, pal, seed):
    img = Image.new("RGB", (w, h), pal[1])
    img = light_falloff(img, pal, seed)
    cx = w * 0.52
    def body(d, o=(0, 0)):
        ox, oy = o
        d.ellipse([cx - w * 0.15 + ox, h * 0.2 + oy, cx + w * 0.15 + ox, h * 0.2 + w * 0.38 + oy], fill=255)
        d.rounded_rectangle([cx - w * 0.07 + ox, h * 0.2 + w * 0.3 + oy, cx + w * 0.07 + ox, h * 0.2 + w * 0.48 + oy], 20, fill=255)
        d.ellipse([cx - w * 0.42 + ox, h * 0.2 + w * 0.46 + oy, cx + w * 0.42 + ox, h * 1.4 + oy], fill=255)
    sh = soft_shadow(body, (w, h), w * 0.03, (w * 0.04, w * 0.02), 120)
    img = Image.composite(Image.new("RGB", (w, h), pal[3]), img, sh)
    m = Image.new("L", (w, h), 0); body(ImageDraw.Draw(m)); m = m.filter(ImageFilter.GaussianBlur(w * 0.004))
    fig = Image.new("RGB", (w, h), pal[3])
    # rim light on figure
    rim = Image.new("L", (w, h), 0); body(ImageDraw.Draw(rim), (-w * 0.012, 0))
    rim = Image.eval(Image.composite(Image.new("L", (w, h), 0), rim, m), lambda v: v)
    fig = Image.composite(fig, Image.new("RGB", (w, h), pal[2]), Image.eval(m, lambda v: v))
    img = Image.composite(fig, img, m)
    hair = Image.new("L", (w, h), 0)
    ImageDraw.Draw(hair).ellipse([cx - w * 0.17, h * 0.18, cx + w * 0.16, h * 0.2 + w * 0.22], fill=255)
    img = Image.composite(Image.new("RGB", (w, h), tuple(max(0, c - 10) for c in pal[3])), img, hair.filter(ImageFilter.GaussianBlur(w * 0.01)))
    return img

def scene_audience(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), pal[3])
    d = ImageDraw.Draw(img)
    # stage glow
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).rectangle([w * 0.2, h * 0.12, w * 0.8, h * 0.5], fill=255)
    img = Image.composite(Image.new("RGB", (w, h), pal[1]), img, glow.filter(ImageFilter.GaussianBlur(w * 0.06)))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.3, h * 0.18, w * 0.7, h * 0.42], fill=pal[0])
    d.rectangle([w * 0.47, h * 0.3, w * 0.53, h * 0.55], fill=pal[3])
    d.ellipse([w * 0.475, h * 0.255, w * 0.525, h * 0.315], fill=pal[3])
    for row in range(6):
        y = h * (0.62 + row * 0.08)
        r = w * (0.022 + row * 0.006)
        n = int(w / (r * 2.6))
        for i in range(n + 2):
            x = i * r * 2.6 + rnd.uniform(-r, r) - r
            col = tuple(max(0, c - 8 - row * 2) for c in pal[3])
            d.ellipse([x - r, y - r * 1.2, x + r, y + r * 1.2], fill=col)
            d.rounded_rectangle([x - r * 1.9, y + r * 0.9, x + r * 1.9, y + r * 5], int(r), fill=col)
    return img.filter(ImageFilter.GaussianBlur(1.2))

def scene_press(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), pal[1])
    img = light_falloff(img, pal, seed)
    for k in range(3):
        ang = rnd.uniform(-14, 14)
        pw, ph = int(w * 0.46), int(w * 0.6)
        paper = Image.new("RGBA", (pw, ph), pal[0] + (255,))
        pd = ImageDraw.Draw(paper)
        pd.rectangle([pw * 0.08, ph * 0.07, pw * 0.92, ph * 0.16], fill=pal[3])
        pd.rectangle([pw * 0.08, ph * 0.2, pw * 0.55, ph * 0.46], fill=pal[2])
        for i in range(16):
            y = ph * (0.5 + i * 0.028)
            x2 = pw * (0.92 if i % 5 else 0.6)
            pd.rectangle([pw * 0.08, y, x2, y + ph * 0.008], fill=tuple(c - 60 for c in pal[0]))
        for i in range(10):
            y = ph * (0.2 + i * 0.026)
            pd.rectangle([pw * 0.6, y, pw * 0.92, y + ph * 0.008], fill=tuple(c - 60 for c in pal[0]))
        paper = paper.rotate(ang, expand=True, resample=Image.BICUBIC)
        x, y = int(w * (0.1 + k * 0.2) + rnd.uniform(-30, 30)), int(h * (0.1 + k * 0.07))
        shadow = Image.new("L", paper.size, 0); shadow.paste(paper.split()[3])
        shadow = shadow.filter(ImageFilter.GaussianBlur(w * 0.015)).point(lambda v: v * 90 // 255)
        img.paste(Image.new("RGB", paper.size, (10, 10, 10)), (x + int(w * 0.015), y + int(w * 0.02)), shadow)
        img.paste(paper, (x, y), paper)
    return img

def scene_still(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), pal[0])
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.64, w, h], fill=pal[1])
    img = light_falloff(img, pal, seed)
    shapes = []
    x = w * rnd.uniform(0.12, 0.22)
    for i in range(3):
        kind = rnd.choice(["arch", "circle", "block"])
        sw = w * rnd.uniform(0.16, 0.26)
        sh = h * rnd.uniform(0.22, 0.42)
        shapes.append((kind, x, h * 0.64 - sh + h * 0.02, sw, sh, pal[2 + (i % 2)] if i != 1 else tuple(min(255, c + 30) for c in pal[2])))
        x += sw * rnd.uniform(0.7, 1.05)
    for kind, x, y, sw, sh, col in shapes:
        def draw(dd, o=(0, 0), kind=kind, x=x, y=y, sw=sw, sh=sh):
            ox, oy = o
            if kind == "arch":
                dd.rectangle([x + ox, y + sw / 2 + oy, x + sw + ox, y + sh + oy], fill=255)
                dd.ellipse([x + ox, y + oy, x + sw + ox, y + sw + oy], fill=255)
            elif kind == "circle":
                dd.ellipse([x + ox, y + sh - sw + oy, x + sw + ox, y + sh + oy], fill=255)
            else:
                dd.rectangle([x + ox, y + oy, x + sw + ox, y + sh + oy], fill=255)
        s = soft_shadow(draw, (w, h), w * 0.02, (w * 0.05, h * 0.01), 110)
        img = Image.composite(Image.new("RGB", (w, h), (20, 18, 16)), img, s)
        m = Image.new("L", (w, h), 0); draw(ImageDraw.Draw(m))
        img = Image.composite(Image.new("RGB", (w, h), col), img, m)
    return img

def scene_studio(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), pal[2])
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.7, w, h], fill=pal[3])
    # desk microphone + table
    d.rectangle([w * 0.1, h * 0.66, w * 0.9, h * 0.72], fill=pal[1])
    for cx in (w * 0.33, w * 0.67):
        d.rectangle([cx - w * 0.006, h * 0.45, cx + w * 0.006, h * 0.66], fill=pal[3])
        d.rounded_rectangle([cx - w * 0.03, h * 0.33, cx + w * 0.03, h * 0.47], int(w * 0.03), fill=pal[3])
    lamp = Image.new("L", (w, h), 0)
    ImageDraw.Draw(lamp).ellipse([w * 0.35, -h * 0.4, w * 0.65, h * 0.3], fill=200)
    img = Image.composite(Image.new("RGB", (w, h), pal[0]), img, lamp.filter(ImageFilter.GaussianBlur(w * 0.08)))
    return img

def scene_abstract(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), pal[0])
    d = ImageDraw.Draw(img)
    cols = [pal[1], pal[2], pal[3]]
    x = 0
    while x < w:
        bw = w * rnd.uniform(0.08, 0.3)
        d.rectangle([x, h * rnd.uniform(0.0, 0.5), x + bw, h], fill=rnd.choice(cols))
        x += bw + w * rnd.uniform(0.0, 0.06)
    d.ellipse([w * 0.55, h * 0.12, w * 0.55 + h * 0.3, h * 0.42], fill=pal[0])
    return img.filter(ImageFilter.GaussianBlur(0.8))

SCENES = dict(portrait=scene_portrait, audience=scene_audience, press=scene_press,
              still=scene_still, studio=scene_studio, abstract=scene_abstract)

def make(name, w, h, scene, palette, seed):
    pal = PALETTES[palette]
    img = SCENES[scene](w, h, pal, seed)
    img = vignette(img, 0.28)
    img = grain(img, seed=seed)
    path = os.path.join(IMG, name + ".jpg")
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return path

# ---------- manifest -------------------------------------------------------
L, T, W, S = (2400, 1600), (1600, 2000), (2400, 1350), (2000, 1500)
manifest = [
    ("portrait-hero", T, "portrait", "sand"),
    ("portrait-about", (1500, 2000), "portrait", "clay"),
    ("portrait-teaser", (1600, 1600), "portrait", "olive"),
]
projects = [
    ("nordlys", "audience", "clay", L), ("baltic-forum", "audience", "ink", T),
    ("riga-light", "studio", "ink", W), ("vilks", "still", "sand", S),
    ("green-harbour", "abstract", "olive", T), ("kultura", "press", "stone", L),
    ("tilts", "still", "rose", S), ("aqua", "press", "olive", W),
]
for i, (slug, scene, pal, size) in enumerate(projects):
    manifest.append((f"projects/{slug}-cover", size, scene, pal))
    alt_scenes = ["still", "press", "audience", "studio", "abstract", "portrait"]
    for g in range(4):
        gsize = [L, T, S, W][(g + i) % 4]
        manifest.append((f"projects/{slug}-{g + 1}", gsize, alt_scenes[(g + i) % 6], pal))
for slug, pal in [("interview-1", "ink"), ("interview-2", "clay")]:
    manifest.append((f"media/{slug}", (1600, 900), "studio", pal))
manifest.append(("og-default", (1200, 630), "still", "sand"))

os.makedirs(os.path.join(IMG, "projects"), exist_ok=True)
os.makedirs(os.path.join(IMG, "media"), exist_ok=True)
for n, (name, size, scene, pal) in enumerate(manifest):
    make(name, size[0], size[1], scene, pal, seed=n * 7 + 3)
print("images:", len(manifest))

# ---------- OG default (with type) ----------------------------------------
from fontTools.ttLib import TTFont as _TT
FONTDIR = os.path.join(ROOT, "scripts", "fonts")
def font_pair(fam, size):
    """Fontsource ships latin and latin-ext as separate files; pick per glyph."""
    out = []
    for sub in ("latin", "latin-ext"):
        path = os.path.join(FONTDIR, f"{fam}-{sub}.ttf")
        out.append((ImageFont.truetype(path, size), set(_TT(path).getBestCmap())))
    return out
def draw_text(d, xy, text, pair, fill):
    x, y = xy
    for ch in text:
        f = next((f for f, cmap in pair if ord(ch) in cmap), pair[0][0])
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch)
serif, sans = font_pair("Newsreader", 76), font_pair("HankenGrotesk", 22)
og = Image.open(os.path.join(IMG, "og-default.jpg")).convert("RGB")
d = ImageDraw.Draw(og)
d.rectangle([0, 0, 540, 630], fill=(245, 243, 238))
draw_text(d, (56, 360), "Anna", serif, (22, 22, 22))
draw_text(d, (56, 440), "Bērziņa", serif, (22, 22, 22))
draw_text(d, (58, 556), "PUBLIC RELATIONS SPECIALIST", sans, (140, 76, 52))
og.save(os.path.join(PUB, "og", "og-default.jpg"), quality=86)

# ---------- videos (slow push-in loops, muted, no audio track) -------------
def video(src_name, out, w=1280, h=720, seconds=8):
    if not shutil.which("ffmpeg"):
        print("ffmpeg missing – skipping", out); return
    src = os.path.join(IMG, src_name + ".jpg")
    frames = seconds * 25
    vf = (f"scale={w*2}:-2,crop={w*2}:{h*2},"
          f"zoompan=z='1+0.06*sin(PI*on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps=25,"
          f"format=yuv420p")
    for ext, codec in (("mp4", ["-c:v", "libx264", "-crf", "30", "-preset", "slow", "-movflags", "+faststart"]),
                       ("webm", ["-c:v", "libvpx-vp9", "-crf", "42", "-b:v", "0"])):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-vf", vf,
                        "-t", str(seconds), "-an", *codec, os.path.join(PUB, "video", f"{out}.{ext}")], check=True)
video("portrait-hero", "hero-loop", 1080, 1350)
video("projects/riga-light-cover", "riga-light-loop")
video("projects/green-harbour-2", "green-harbour-loop")
video("projects/baltic-forum-2", "baltic-forum-recap")
print("videos done")

# ---------- placeholder CV PDF --------------------------------------------
pdf = Image.new("RGB", (1240, 1754), (255, 255, 255))
d = ImageDraw.Draw(pdf)
draw_text(d, (120, 140), "Anna Bērziņa — CV (placeholder)", font_pair("Newsreader", 52), (20, 20, 20))
draw_text(d, (120, 240), "Replace public/cv/anna-berzina-cv.pdf with the real CV.", sans, (80, 80, 80))
pdf.save(os.path.join(PUB, "cv", "anna-berzina-cv.pdf"), "PDF", resolution=150)
print("cv done")
