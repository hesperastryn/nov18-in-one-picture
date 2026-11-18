#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261118:
the world news of Wednesday 18 November 2026 in one picture.

A newspaper-style front page: a big date header, six illustrated story
panels with bold captions, and an "also today" ticker along the bottom.

The day's stories (as reported on 18 Nov 2026 by Anadolu, Reuters via
Just Security's Early Edition, Outlook India, Times of India and the
Daily Mirror):
  1. Trump, Xi and Putin gather in Shenzhen for the APEC summit;
     Putin and Xi met, Trump arrived, three-way talks set for Nov 19.
  2. Iran launched drones at US forces in Kuwait (Ali Al Salem base);
     Bahrain intercepted attacks; a tanker was hit near Hormuz.
  3. Israel began a new "concentrated operation" in central Gaza.
  4. Severe Cyclone Akvan approached Odisha; people moved to shelters.
  5. Grand Theft Auto VI launched at midnight after a 13-year wait.
  6. Gold slid to its lowest in over a year on a firm dollar.
Ticker: Quad leaders met in Manila for the first time in over two
years; the US lost its measles-free status; a magnitude 6 earthquake
struck Papua New Guinea.

Run locally:  python3 generate.py   (writes entry.png beside this file)
The grading program is main.py, which copies the committed entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (10, 22, 40)
GOLD = (232, 184, 75)
WHITE = (245, 247, 250)
CAPTION_BG = (7, 14, 26)
SUB = (178, 198, 222)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    """Largest font at or below size that fits text in max_w pixels."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def draw_tracked(draw, xy, text, f, fill, tracking=6):
    """Draw text with extra letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def vgrad(img, box, top, bottom):
    """Vertical gradient inside box."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- panels
PW, PH = 480, 240          # panel size
CAP_H = 64                 # caption bar height
ART_H = PH - CAP_H         # illustration height


def panel_base(top, bottom):
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    vgrad(img, (0, 0, PW, ART_H), top, bottom)
    return img


def caption(img, head, sub):
    d = ImageDraw.Draw(img)
    d.rectangle([0, ART_H, PW, PH], fill=CAPTION_BG)
    d.line([(0, ART_H), (PW, ART_H)], fill=GOLD, width=3)
    hf = fit_font(d, head, FONT_BOLD, 31, PW - 28)
    d.text((14, ART_H + 5), head, font=hf, fill=WHITE)
    sf = fit_font(d, sub, FONT_REG, 21, PW - 28)
    d.text((14, ART_H + 39), sub, font=sf, fill=SUB)


def flag_us(d, x, y, w, h):
    for i in range(7):
        yy = y + i * h / 7
        d.rectangle([x, yy, x + w, yy + h / 7 + 1],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.44, y + h * 4 / 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            cx = x + 8 + c * (w * 0.44 - 14) / 4
            cy = y + 6 + r * (h * 4 / 7 - 10) / 3
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon([(x + 16, y + 10), (x + 20, y + 22), (x + 33, y + 22),
               (x + 22, y + 29), (x + 26, y + 42), (x + 16, y + 34),
               (x + 6, y + 42), (x + 10, y + 29), (x - 1, y + 22),
               (x + 13, y + 22)], fill=(255, 222, 0))
    for dx, dy in [(44, 8), (50, 22), (50, 36), (44, 48)]:
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3],
                  fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))


def p_summit():
    img = panel_base((38, 92, 122), (240, 178, 110))
    d = ImageDraw.Draw(img)
    # Shenzhen skyline silhouette
    towers = [(0, 118, 40), (34, 96, 30), (60, 128, 46), (100, 84, 26),
              (122, 110, 38), (300, 100, 34), (330, 124, 48), (372, 90, 28),
              (396, 116, 40), (432, 104, 48)]
    for x, top, w in towers:
        d.rectangle([x, top, x + w, ART_H], fill=(16, 30, 48))
        for wy in range(top + 10, ART_H - 8, 16):
            for wx in range(x + 6, x + w - 6, 12):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 120))
    # flag poles and flags
    for px, draw_flag in [(86, flag_us), (216, flag_cn), (346, flag_ru)]:
        d.line([(px, 26), (px, ART_H)], fill=(30, 30, 30), width=5)
        draw_flag(d, px + 4, 28, 96, 62)
    caption(img, "TRUMP · XI · PUTIN SUMMIT", "LEADERS GATHER FOR APEC — SHENZHEN")
    return img


def p_iran():
    img = panel_base((10, 18, 38), (24, 52, 84))
    d = ImageDraw.Draw(img)
    # sea
    d.rectangle([0, 118, PW, ART_H], fill=(13, 42, 66))
    for i in range(9):
        x = (i * 67) % PW
        d.line([(x, 132 + (i % 3) * 14), (x + 34, 132 + (i % 3) * 14)],
               fill=(70, 130, 170), width=3)
    # tanker silhouette
    d.polygon([(36, 118), (52, 100), (250, 100), (268, 118)], fill=(8, 10, 14))
    d.rectangle([196, 84, 226, 100], fill=(8, 10, 14))
    for i in range(5):
        d.rectangle([66 + i * 24, 90, 86 + i * 24, 100], fill=(20, 24, 30))
    d.line([(36, 118), (268, 118)], fill=(200, 80, 50), width=3)
    # explosion burst on the right shore
    cx, cy = 408, 108
    for ang in range(0, 360, 30):
        r = 34 if ang % 60 == 0 else 20
        d.line([(cx, cy), (cx + r * math.cos(math.radians(ang)),
                           cy + r * math.sin(math.radians(ang)))],
               fill=(255, 150, 40), width=5)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 196, 64))
    d.rectangle([368, 118, PW, ART_H], fill=(8, 10, 14))
    # drones with dotted paths
    for (dx, dy, ph) in [(120, 34, 0), (196, 20, 2), (292, 44, 4)]:
        for t in range(9):
            px = dx - 66 + t * 8
            py = dy + 30 - t * 3 + ph
            d.ellipse([px, py, px + 3, py + 3], fill=(150, 190, 220))
        d.rectangle([dx - 9, dy - 4, dx + 9, dy + 4], fill=(200, 210, 220))
        for ox, oy in [(-13, -8), (13, -8), (-13, 8), (13, 8)]:
            d.ellipse([dx + ox - 5, dy + oy - 2, dx + ox + 5, dy + oy + 2],
                      outline=(200, 210, 220), width=2)
    caption(img, "IRAN STRIKES GULF BASES", "DRONES HIT KUWAIT — BAHRAIN INTERCEPTS")
    return img


def p_gaza():
    img = panel_base((172, 158, 138), (120, 110, 100))
    d = ImageDraw.Draw(img)
    d.ellipse([24, 14, 76, 66], fill=(232, 212, 168))
    # back row of blocks (paler), then front row (darker)
    back = [(0, 92, 58), (52, 78, 46), (150, 88, 60), (262, 80, 52),
            (356, 90, 64), (436, 82, 44)]
    for x, top, w in back:
        d.rectangle([x, top, x + w, ART_H], fill=(110, 102, 94))
    front = [(16, 112, 66), (96, 100, 56), (196, 116, 74), (300, 104, 58),
             (392, 110, 66)]
    for x, top, w in front:
        d.rectangle([x, top, x + w, ART_H], fill=(56, 52, 48))
        d.rectangle([x + 8, top - 10, x + 22, top], fill=(56, 52, 48))
    d.polygon([(196, 116), (232, 100), (270, 116)], fill=(56, 52, 48))
    # window grids on the front blocks
    for x, top, w in front:
        for wy in range(top + 12, ART_H - 10, 18):
            for wx in range(x + 8, x + w - 10, 16):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 7, wy + 9], fill=(150, 140, 124))
    # smoke columns: tapered stacks of puffs rising and drifting right
    for bx, by, s in [(124, 100, 1.0), (330, 104, 1.2), (424, 110, 0.8)]:
        for i in range(7):
            r = (6 + i * 3.2) * s
            x = bx + i * 7 - r
            y = by - i * 12 - r
            shade = 88 - i * 4
            d.ellipse([x, y, x + 2 * r, y + 2 * r],
                      fill=(shade + 22, shade + 18, shade + 14))
    d.rectangle([0, ART_H - 10, PW, ART_H], fill=(40, 37, 34))
    caption(img, "NEW GAZA OPERATION", "ISRAEL MOVES INTO CENTRAL GAZA")
    return img


def p_cyclone():
    img = panel_base((26, 52, 84), (44, 88, 116))
    d = ImageDraw.Draw(img)
    # storm spiral
    cx, cy = 330, 92
    for i, r in enumerate(range(16, 96, 13)):
        start = i * 55
        d.arc([cx - r, cy - r * 0.78, cx + r, cy + r * 0.78],
              start=start, end=start + 215, fill=(214, 234, 244), width=9)
    d.ellipse([cx - 13, cy - 10, cx + 13, cy + 10], fill=(16, 34, 56))
    # coast landmass
    d.polygon([(0, 118), (150, 104), (238, 128), (260, ART_H), (0, ART_H)],
              fill=(196, 168, 110))
    d.polygon([(0, 132), (140, 118), (226, 138), (240, ART_H), (0, ART_H)],
              fill=(172, 144, 92))
    # bending palms
    for bx, lean in [(52, 26), (118, 34), (176, 20)]:
        top_x = bx + lean
        d.line([(bx, ART_H), (bx + lean // 2, 128), (top_x, 104)],
               fill=(60, 44, 26), width=6)
        for a in range(-160, 30, 32):
            ex = top_x + 30 * math.cos(math.radians(a + lean))
            ey = 104 + 15 * math.sin(math.radians(a + lean)) + 8
            d.line([(top_x, 104), (ex, ey)], fill=(46, 110, 60), width=5)
    # rain
    for i in range(26):
        x = (i * 41) % PW
        y = (i * 29) % ART_H
        d.line([(x, y), (x - 7, y + 15)], fill=(160, 200, 225), width=3)
    caption(img, "CYCLONE AKVAN", "SEVERE STORM — ODISHA EVACUATES")
    return img


def p_gta():
    img = panel_base((88, 30, 110), (250, 120, 70))
    d = ImageDraw.Draw(img)
    d.ellipse([196, 58, 284, 146], fill=(255, 176, 84))
    d.rectangle([0, 138, PW, ART_H], fill=(30, 22, 44))
    # road perspective
    d.polygon([(196, ART_H), (284, ART_H), (258, 140), (222, 140)],
              fill=(52, 46, 66))
    d.line([(240, 172), (240, ART_H)], fill=(255, 214, 90), width=4)
    # car silhouette, rear view
    d.rounded_rectangle([198, 122, 282, 150], 9, fill=(12, 12, 18))
    d.rectangle([186, 146, 294, 162], fill=(12, 12, 18))
    d.rectangle([204, 150, 224, 157], fill=(255, 70, 70))
    d.rectangle([256, 150, 276, 157], fill=(255, 70, 70))
    # palms: curved segmented trunks, long arcing fronds
    for bx, flip in [(58, 1), (424, -1)]:
        pts = []
        for i in range(7):
            t = i / 6
            pts.append((bx + flip * 16 * t * t, ART_H - t * (ART_H - 78)))
        d.line(pts, fill=(16, 12, 22), width=8, joint="curve")
        tx, ty = pts[-1]
        for a in range(-175, 0, 25):
            ex = tx + 52 * math.cos(math.radians(a)) * flip
            ey = ty + 26 * math.sin(math.radians(a)) + 16
            mx = tx + 30 * math.cos(math.radians(a)) * flip
            my = ty + 20 * math.sin(math.radians(a)) - 7
            d.line([(tx, ty), (mx, my), (ex, ey)], fill=(16, 12, 22),
                   width=5, joint="curve")
    # VI badge
    d.rounded_rectangle([316, 22, 452, 100], 14, outline=(64, 224, 255), width=4)
    vf = fit_font(d, "VI", FONT_BOLD, 62, 120)
    d.text((384 - d.textlength("VI", font=vf) / 2 + 3, 34), "VI", font=vf,
           fill=(255, 64, 190))
    d.text((384 - d.textlength("VI", font=vf) / 2, 31), "VI", font=vf,
           fill=(255, 240, 250))
    caption(img, "GTA VI LAUNCHES", "OUT AT MIDNIGHT — AFTER A 13-YEAR WAIT")
    return img


def p_gold():
    img = panel_base((8, 26, 20), (10, 34, 26))
    d = ImageDraw.Draw(img)
    for gx in range(30, PW, 56):
        d.line([(gx, 8), (gx, ART_H - 8)], fill=(24, 54, 44), width=1)
    for gy in range(12, ART_H, 28):
        d.line([(8, gy), (PW - 8, gy)], fill=(24, 54, 44), width=1)
    # falling chart line with arrow
    pts = [(36, 36), (130, 30), (214, 62), (300, 56), (384, 96), (438, 128)]
    d.line(pts, fill=(255, 84, 84), width=7, joint="curve")
    d.polygon([(438, 146), (424, 118), (452, 120)], fill=(255, 84, 84))
    # gold bars
    def bar(x, y, w=86):
        d.polygon([(x + 12, y), (x + w - 12, y), (x + w, y + 22), (x, y + 22)],
                  fill=(240, 196, 84))
        d.polygon([(x + 12, y), (x + w - 12, y), (x + w - 4, y + 10),
                   (x + 4, y + 10)], fill=(255, 226, 130))
    bar(40, 128)
    bar(140, 128)
    bar(90, 104)
    caption(img, "GOLD SLIDES", "LOWEST IN OVER A YEAR — DOLLAR FIRMS")
    return img


# ---------------------------------------------------------------- page
def build():
    page = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(page)

    # header
    kf = font(FONT_REG, 27)
    draw_tracked(d, (26, 24), "WEDNESDAY · THE WORLD IN ONE PICTURE", kf,
                 (150, 178, 208), tracking=5)
    df = fit_font(d, "18 NOVEMBER 2026", FONT_BOLD, 96, W - 52)
    d.text((24, 56), "18 NOVEMBER 2026", font=df, fill=WHITE)
    d.rectangle([24, 158, W - 24, 164], fill=GOLD)

    panels = [p_summit(), p_iran(), p_gaza(), p_cyclone(), p_gta(), p_gold()]
    xs = [24, 520]
    ys = [182, 438, 694]
    for i, p in enumerate(panels):
        x, y = xs[i % 2], ys[i // 2]
        page.paste(p, (x, y))
        d.rectangle([x - 2, y - 2, x + PW + 2, y + PH + 2],
                    outline=(52, 74, 104), width=2)

    # ticker
    d.rectangle([0, 950, W, H], fill=(122, 24, 32))
    tick = ("ALSO TODAY: QUAD LEADERS MEET IN MANILA · US LOSES "
            "MEASLES-FREE STATUS · M6 QUAKE IN PAPUA NEW GUINEA")
    tf = fit_font(d, tick, FONT_BOLD, 25, W - 40)
    tw = d.textlength(tick, font=tf)
    d.text(((W - tw) / 2, 972), tick, font=tf, fill=(255, 238, 220))
    return page


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
