#!/usr/bin/env python3
"""
Generate the social preview image (images/og-image.png, 1200x630).

This is what LinkedIn, Slack, Teams, WhatsApp and email clients show when
someone shares a link to the site. Re-run after changing the palette, the role
line, or the profile photo.

    python3 tools/make-og-image.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630

# Light palette, from theme-light.scss
PAPER = (253, 252, 250)
SAND = (244, 241, 236)
INK = (27, 36, 50)
MUTED = (110, 119, 132)
EMBER = (180, 85, 43)
NIGHT = (47, 90, 105)

SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS = "/System/Library/Fonts/SFNS.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            line = trial
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Ember rule down the left edge, the site's one recurring gesture
    d.rectangle([0, 0, 14, H], fill=EMBER)

    # Photo, circular, on the right
    photo_path = ROOT / "images" / "profile.jpg"
    if photo_path.exists():
        size = 340
        p = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")
        p = ImageOps.fit(p, (size, size), Image.LANCZOS, centering=(0.5, 0.32))
        mask = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size * 4, size * 4], fill=255)
        mask = mask.resize((size, size), Image.LANCZOS)
        px, py = W - size - 90, (H - size) // 2
        ring = Image.new("L", (size + 16, size + 16), 0)
        ImageDraw.Draw(ring).ellipse([0, 0, size + 15, size + 15], fill=255)
        img.paste(SAND, (px - 8, py - 8), ring)
        img.paste(p, (px, py), mask)
        text_w = W - size - 90 - 90 - 60
    else:
        text_w = W - 200

    x = 90
    y = 150

    f_eyebrow = font(SANS, 22)
    f_name = font(SERIF_BOLD, 76)
    f_role = font(SANS, 27)
    f_url = font(SANS, 23)

    d.text((x, y), "ENVIRONMENTAL PHYSIOLOGY  ·  HEAT, SLEEP, HEALTH",
           font=f_eyebrow, fill=EMBER)
    y += 58

    d.text((x, y), "Michèle Renard", font=f_name, fill=INK)
    y += 100

    role = "Research Fellow, Yong Loo Lin School of Medicine, National University of Singapore"
    for line in wrap(d, role, f_role, text_w):
        d.text((x, y), line, font=f_role, fill=MUTED)
        y += 38

    y += 26
    d.rectangle([x, y, x + 66, y + 4], fill=NIGHT)
    y += 34
    d.text((x, y), "michelerenard.github.io", font=f_url, fill=NIGHT)

    out = ROOT / "images" / "og-image.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.relative_to(ROOT)}  ({W}x{H}, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
