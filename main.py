#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Monday 23 November 2026.

Draws a one-page broadsheet front page summing up the world's news of
Monday 23 November 2026, as a 1024x1024 JPEG written to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR). Pure Pillow, fully deterministic: no clocks, no
randomness, no network. Two runs produce byte-identical output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (250, 246, 236)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (163, 22, 22)
NAVY = (15, 30, 61)
GREY = (90, 88, 80)
LIGHT_LINE = (120, 116, 104)

REGION_COLORS = {
    "EUROPE": (29, 78, 216),
    "MIDDLE EAST": (220, 38, 38),
    "AMERICAS": (21, 128, 61),
    "ASIA-PACIFIC": (234, 88, 12),
    "AFRICA": (13, 148, 136),
    "OCEANIA": (124, 58, 237),
    "WORLD": (71, 85, 105),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = "DejaVuSerif-Bold.ttf"
F_SERIF_R = "DejaVuSerif.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fname, size, width):
    """Greedy word wrap; returns list of lines fitting width pixels."""
    f = font(fname, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fname, size, fill=INK, leading=None):
    """Draw lines of text; returns y just below the last line."""
    f = font(fname, size)
    lh = leading if leading is not None else int(size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label, size=10):
    """Red tag with white bold text; returns width used."""
    f = font(F_SANS_B, size)
    w = int(draw.textlength(label, font=f)) + 10
    h = size + 7
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    draw.text((x + 5, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def centered(draw, cx, y, text, fname, size, fill=INK):
    f = font(fname, size)
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return w

# ---------------------------------------------------------------- illustrations
# Every picture is drawn from scratch with Pillow primitives: no photos, no
# copied pixels. Each function paints inside (x, y, w, h).


def ill_warship(d, x, y, w, h):
    """Night sea off Benghazi: a warship ablaze, drone boats closing in."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 22, 48))
    for i in range(5):
        d.ellipse([x + 18 + i * 64, y + h - 26, x + 30 + i * 64, y + h - 14],
                  fill=(24, 52, 96))
    # burning ship: hull + superstructure + mast
    d.polygon([(x + 96, y + 52), (x + 232, y + 52), (x + 216, y + 66),
               (x + 112, y + 66)], fill=(38, 38, 44))
    d.rectangle([x + 130, y + 34, x + 196, y + 52], fill=(52, 52, 58))
    d.rectangle([x + 158, y + 16, x + 164, y + 34], fill=(52, 52, 58))
    # fireball
    for r, c in ((30, (255, 120, 20)), (20, (255, 180, 40)),
                 (11, (255, 235, 120))):
        d.ellipse([x + 150 - r, y + 30 - r, x + 150 + r, y + 30 + r], fill=c)
    # smoke
    for cx, cy, r in ((132, 8, 12), (150, 2, 14), (170, 8, 11)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(70, 70, 78))
    # drone boats with wakes
    for bx in (28, 262):
        d.polygon([(x + bx, y + h - 16), (x + bx + 34, y + h - 16),
                   (x + bx + 26, y + h - 8), (x + bx + 8, y + h - 8)],
                  fill=(200, 200, 210))
        d.line([(x + bx - 14, y + h - 12), (x + bx, y + h - 12)],
               fill=(140, 170, 220), width=2)


def ill_cop(d, x, y, w, h):
    """Antalya coast at dusk: flags around a table, a red no-deal crack."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    d.rectangle([x, y, x + w, y + 34], fill=(245, 178, 80))
    d.ellipse([x + w - 58, y + 4, x + w - 18, y + 44], fill=(255, 214, 120))
    # sea
    d.rectangle([x, y + 44, x + w, y + 62], fill=(64, 130, 170))
    # flag poles
    for i, c in enumerate(((220, 38, 38), (29, 78, 216), (21, 128, 61),
                           (234, 88, 12), (124, 58, 237))):
        fx = x + 26 + i * 58
        d.line([(fx, y + 46), (fx, y + 78)], fill=(60, 60, 60), width=2)
        d.polygon([(fx, y + 46), (fx + 26, y + 52), (fx, y + 58)], fill=c)
    # crack through the table
    d.line([(x + 60, y + 78), (x + 120, y + 66), (x + 170, y + 80),
            (x + 230, y + 66), (x + 290, y + 78)], fill=(185, 28, 28), width=3)
    d.ellipse([x + 138, y + 62, x + 186, y + 84], fill=(185, 28, 28))
    d.text((x + 147, y + 68), "X", font=font(F_SANS_B, 14), fill=(255, 255, 255))


def ill_fire(d, x, y, w, h):
    """Cikande factory: flames at the base, black smoke over the roof."""
    d.rectangle([x, y, x + w, y + h], fill=(48, 44, 40))
    # smoke
    for cx, cy, r in ((70, 14, 16), (110, 6, 20), (160, 12, 18),
                      (210, 8, 16), (260, 16, 14)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(28, 28, 30))
    # factory block
    d.rectangle([x + 46, y + 40, x + w - 46, y + h - 22], fill=(120, 112, 100))
    d.rectangle([x + 46, y + 40, x + w - 46, y + 48], fill=(88, 82, 72))
    for wx in (66, 116, 166, 216, 266):
        d.rectangle([x + wx, y + 56, x + wx + 22, y + 72], fill=(255, 214, 120))
    # flames
    for fx, fh in ((60, 26), (100, 34), (150, 30), (200, 36), (250, 26)):
        d.polygon([(x + fx, y + h - 22), (x + fx + 12, y + h - 22 - fh),
                   (x + fx + 24, y + h - 22)], fill=(255, 120, 20))
        d.polygon([(x + fx + 6, y + h - 22), (x + fx + 12, y + h - 22 - fh + 12),
                   (x + fx + 18, y + h - 22)], fill=(255, 210, 60))


def ill_drones(d, x, y, w, h):
    """Night sky over Kyiv: drone dots, defence tracers, one burst."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    for i, (sx, sy) in enumerate(((30, 12), (80, 22), (130, 8), (180, 20),
                                  (230, 10), (280, 24), (55, 34), (160, 36),
                                  (250, 38))):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                  fill=(255, 220, 120))
    d.line([(x + 20, y + h - 4), (x + 120, y + 14)], fill=(255, 180, 60), width=2)
    d.line([(x + 300, y + h - 4), (x + 210, y + 16)], fill=(255, 180, 60), width=2)
    for r, c in ((12, (255, 140, 30)), (7, (255, 210, 90))):
        d.ellipse([x + 160 - r, y + 18 - r, x + 160 + r, y + 18 + r], fill=c)


def ill_chip(d, x, y, w, h):
    """Nvidia: a green chip and a rising market line."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 60, 32))
    d.rectangle([x + 108, y + 8, x + 208, y + 38], fill=(24, 120, 60))
    for px in (118, 138, 158, 178, 198):
        d.line([(x + px, y + 2), (x + px, y + 8)], fill=(140, 230, 170), width=2)
        d.line([(x + px, y + 38), (x + px, y + 44)], fill=(140, 230, 170), width=2)
    d.text((x + 138, y + 16), "AI", font=font(F_SANS_B, 16), fill=(255, 255, 255))
    d.line([(x + 8, y + 40), (x + 90, y + 32), (x + 170, y + 34),
            (x + 240, y + 14), (x + 308, y + 6)], fill=(120, 230, 140), width=3)
    d.polygon([(x + 296, y + 2), (x + 312, y + 4), (x + 300, y + 14)],
              fill=(120, 230, 140))


def ill_cricket(d, x, y, w, h):
    """Basin Reserve: green outfield, pitch strip, stumps, red ball."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 120, 58))
    d.rectangle([x + 120, y + 4, x + 196, y + h - 4], fill=(214, 190, 140))
    for sx in (150, 156, 162):
        d.line([(x + sx, y + 10), (x + sx, y + 22)], fill=(250, 250, 240), width=2)
    d.line([(x + 148, y + 9), (x + 166, y + 9)], fill=(250, 250, 240), width=2)
    d.ellipse([x + 250, y + 18, x + 262, y + 30], fill=(185, 28, 28))
    d.line([(x + 20, y + 36), (x + 90, y + 30)], fill=(255, 255, 255), width=2)


def ill_mercury(d, x, y, w, h):
    """BepiColombo: grey cratered Mercury and a panelled spacecraft."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 16))
    for sx, sy in ((30, 10), (90, 26), (260, 8), (300, 30), (200, 6)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 30, y + 4, x + 118, y + 44], fill=(168, 160, 148))
    for cx, cy, r in ((58, 18, 7), (86, 30, 5), (96, 14, 4), (44, 32, 4)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(128, 120, 110))
    # spacecraft: body + panels
    d.rectangle([x + 196, y + 16, x + 226, y + 32], fill=(200, 200, 210))
    d.rectangle([x + 158, y + 20, x + 196, y + 28], fill=(40, 90, 180))
    d.rectangle([x + 226, y + 20, x + 264, y + 28], fill=(40, 90, 180))
    d.line([(x + 226, y + 24), (x + 196, y + 24)], fill=(120, 120, 130), width=1)


def ill_eu(d, x, y, w, h):
    """EU sanctions: blue field, ring of stars, red slash."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    import math
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + int(96 * math.cos(a)), cy + int(15 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    d.line([(x + 40, y + h - 8), (x + w - 40, y + 8)], fill=(220, 38, 38), width=4)


def ill_khartoum(d, x, y, w, h):
    """Khartoum at dusk: skyline, smoke plume, UN-blue flag."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 196, 130))
    d.rectangle([x, y + 26, x + w, y + h], fill=(120, 96, 66))
    for bx, bw, bh in ((10, 44, 16), (62, 30, 24), (100, 52, 12), (160, 36, 20),
                       (204, 48, 14), (260, 40, 18)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(70, 56, 40))
    for cx, cy, r in ((150, 8, 12), (170, 2, 14), (190, 8, 10)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(90, 84, 76))
    d.line([(x + 288, y + 8), (x + 288, y + 30)], fill=(60, 60, 60), width=2)
    d.polygon([(x + 288, y + 8), (x + 310, y + 13), (x + 288, y + 18)],
              fill=(0, 122, 185))


def ill_ban(d, x, y, w, h):
    """Generic ban: dark chip / document with a red prohibition ring."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 36))
    d.rectangle([x + w // 2 - 34, y + 6, x + w // 2 + 34, y + h - 6],
                fill=(220, 220, 228))
    d.ellipse([x + w // 2 - 22, y + h // 2 - 14, x + w // 2 + 22,
               y + h // 2 + 14], outline=(185, 28, 28), width=4)
    d.line([(x + w // 2 - 15, y + h // 2 + 10), (x + w // 2 + 15, y + h // 2 - 10)],
           fill=(185, 28, 28), width=4)


def ill_bank(d, x, y, w, h):
    """Treasury: a bank front with columns and a dollar seal."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.polygon([(x + 40, y + 4), (x + w - 40, y + 4), (x + w // 2, y + 14)],
              fill=(90, 88, 80))
    for cx in (60, 110, 160, 210):
        d.rectangle([x + cx, y + 16, x + cx + 12, y + h - 8], fill=(120, 116, 104))
    d.rectangle([x + 40, y + h - 8, x + w - 40, y + h - 2], fill=(90, 88, 80))
    d.ellipse([x + w - 46, y + 2, x + w - 14, y + 22], fill=(21, 128, 61))
    d.text((x + w - 37, y + 5), "$", font=font(F_SANS_B, 12), fill=(255, 255, 255))


def ill_search(d, x, y, w, h):
    """FBI: a magnifier over a grid of database rows."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 42, 78))
    for ry in (6, 14, 22):
        d.rectangle([x + 8, y + ry, x + w - 8, y + ry + 4], fill=(70, 110, 170))
    d.ellipse([x + 96, y + 4, x + 140, y + 28], outline=(255, 210, 60), width=3)
    d.line([(x + 134, y + 24), (x + 152, y + 34)], fill=(255, 210, 60), width=3)


def ill_shield(d, x, y, w, h):
    """Cucuta: a police shield under a small drone."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    d.polygon([(x + 96, y + 4), (x + 140, y + 4), (x + 140, y + 20),
               (x + 118, y + 34), (x + 96, y + 20)], fill=(29, 78, 216))
    d.ellipse([x + 200, y + 4, x + 208, y + 10], fill=(40, 40, 44))
    d.line([(x + 188, y + 6), (x + 220, y + 6)], fill=(40, 40, 44), width=2)
    d.line([(x + 196, y + 10), (x + 212, y + 10)], fill=(40, 40, 44), width=1)


def ill_scan(d, x, y, w, h):
    """NHS: a pink-ribbon screening frame over a scan panel."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 246))
    d.rectangle([x + 84, y + 4, x + 152, y + h - 4], fill=(30, 30, 36))
    d.ellipse([x + 104, y + 10, x + 132, y + 26], fill=(233, 120, 170))
    d.polygon([(x + 118, y + 6), (x + 128, y + 16), (x + 118, y + 26),
               (x + 108, y + 16)], fill=(255, 255, 255))
    d.rectangle([x + 168, y + 10, x + w - 12, y + 16], fill=(233, 120, 170))
    d.rectangle([x + 168, y + 20, x + w - 40, y + 26], fill=(220, 180, 205))


def ill_ball(d, x, y, w, h):
    """U17 World Cup: green pitch, goal, ball on the spot."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 120, 58))
    d.rectangle([x + 30, y + 6, x + 90, y + 24], outline=(255, 255, 255), width=2)
    for gx in (36, 48, 60, 72, 84):
        d.line([(x + gx, y + 6), (x + gx, y + 24)], fill=(255, 255, 255), width=1)
    d.ellipse([x + 180, y + 12, x + 196, y + 28], fill=(255, 255, 255))
    d.ellipse([x + 250, y + 8, x + 258, y + 16], fill=(255, 255, 255))

# ---------------------------------------------------------------- world map
# Coarse land boxes (lon_min, lon_max, lat_min, lat_max) rasterised to dots.
LAND_BOXES = [
    (-168, -60, 50, 72), (-125, -66, 25, 50), (-118, -77, 8, 32),
    (-58, -20, 60, 84), (-80, -35, -55, 12),
    (-10, 40, 36, 70), (-5, 2, 50, 58), (-22, -14, 63, 66),
    (-17, 32, 15, 32), (-17, 35, -35, 15), (35, 51, 0, 12),
    (43, 50, -25, -12),
    (30, 180, 50, 72), (45, 90, 35, 55), (35, 60, 12, 42),
    (68, 88, 8, 35), (80, 122, 20, 53), (95, 110, 5, 28),
    (95, 141, -11, 6), (129, 146, 31, 46), (126, 130, 34, 42),
    (113, 154, -39, -11), (166, 178, -47, -34),
]
MAP_LAT_TOP, MAP_LAT_BOT = 80, -55

# (story no, lon, lat, dx, dy) - dx/dy nudge pins that would collide.
PINS = [
    (1, 20.1, 32.1, -5, -5), (2, 30.7, 36.9, 7, 6), (3, 106.3, -6.0, 0, 0),
    (4, 30.5, 50.5, -9, -4), (5, -121.0, 37.4, 0, 0), (6, 174.8, -41.3, -4, 0),
    (7, 8.7, 49.9, 10, -7), (8, 4.4, 50.9, 2, 7), (9, 32.5, 15.6, 5, 5),
    (10, -77.0, 38.9, 0, 0), (11, -77.0, 38.9, 9, -9), (12, -77.0, 38.9, -9, 8),
    (13, -72.5, 7.9, 0, 0), (14, -0.1, 51.5, -9, -6), (15, 51.5, 25.3, 0, 0),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cols, rows = 72, 27
    for r in range(rows):
        lat = MAP_LAT_TOP - (MAP_LAT_TOP - MAP_LAT_BOT) * (r + 0.5) / rows
        for c in range(cols):
            lon = -180 + 360 * (c + 0.5) / cols
            if any(lo <= lon <= hi and la0 <= lat <= la1
                   for lo, hi, la0, la1 in LAND_BOXES):
                cx = x + (c + 0.5) * w / cols
                cy = y + (r + 0.5) * h / rows
                d.ellipse([cx - 1.2, cy - 1.2, cx + 1.2, cy + 1.2],
                          fill=(150, 170, 205))
    for num, lon, lat, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * h + dy
        px = min(max(px, x + 7), x + w - 7)
        py = min(max(py, y + 7), y + h - 7)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(F_SANS_B, 7 if num < 10 else 6)
        t = str(num)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 4.5 if num < 10 else py - 4), t, font=f,
               fill=(255, 255, 255))

# ---------------------------------------------------------------- the day's news
# Every claim below was checked against reporting of Monday 23 November 2026.
# Datelines use the place of the story; sources name the wire or outlet.

FEATURED = [
    dict(num=1, region="AFRICA", place="BENGHAZI, LIBYA", section="WAR",
         tag="7 DRONES, ONE SINKING",
         head="Ukraine sinks Russian warship off Libya",
         body=("Seven sea drones sank the corvette Merkury at anchor, "
               "Zelensky confirmed on Monday, and hit the cargo ship "
               "MV Angara. A Ka-27 helicopter was destroyed too."),
         src="CNN", ill=ill_warship),
    dict(num=2, region="MIDDLE EAST", place="ANTALYA, TÜRKIYE", section="CLIMATE",
         tag="NO DEAL",
         head="COP31's wreckage: blame game",
         body=("The summit ended Sunday with no deal after the EU and UK "
               "rejected a fossil-free text. On Monday Erdogan spoke of "
               "groundwork; China was deeply disappointed."),
         src="Reuters", ill=ill_cop),
    dict(num=3, region="ASIA-PACIFIC", place="CIKANDE, INDONESIA", section="DISASTER",
         tag="24 DEAD, 30 MISSING",
         head="Factory fire toll now 24 dead, 30 missing",
         body=("Indonesia confirmed the toll on Monday. The blaze swept "
               "the Milkita sweets plant on Saturday; 29 workers are "
               "safe, five in hospital. An air-con fault is suspected."),
         src="Reuters", ill=ill_fire),
    dict(num=4, region="EUROPE", place="KYIV, UKRAINE", section="WAR",
         tag="153 DRONES",
         head="134 of 153 drones downed overnight",
         body=("Russia launched 153 drones from Sunday evening; defences "
               "downed 134. Fifteen died near Kyiv; a boy was pulled "
               "alive."),
         src="Ukrinform", ill=ill_drones),
    dict(num=5, region="AMERICAS", place="SANTA CLARA, US", section="BUSINESS",
         tag="HUANG RETURNS",
         head="Nvidia brings Huang back; shares jump 30%",
         body=("The board reinstated Jensen Huang as chief executive, and "
               "the share price rose about 30 per cent on the day."),
         src="BBC", ill=ill_chip),
    dict(num=6, region="OCEANIA", place="WELLINGTON, NZ", section="CRICKET",
         tag="238/5, DRAW",
         head="India's 720/9 ends in a draw",
         body=("New Zealand finished 238/5 on day five as Conway, Mitchell "
               "and Phillips defied India. Gill blamed tired fast "
               "bowlers for the draw."),
         src="IANS", ill=ill_cricket),
    dict(num=7, region="EUROPE", place="DARMSTADT, GERMANY", section="SPACE",
         tag="SAFE IN ORBIT",
         head="BepiColombo safe in Mercury orbit",
         body=("ESA said on Monday the probe is safe in a stable orbit "
               "after a thruster glitch cut its burn short. Its two "
               "orbiters split on 9 December."),
         src="ESA", ill=ill_mercury),
    dict(num=8, region="EUROPE", place="BRUSSELS, BELGIUM", section="SANCTIONS",
         tag="22ND PACKAGE",
         head="EU proposes 22nd Russia sanctions package",
         body=("Von der Leyen unveiled the package on Monday, covering "
               "banks, crypto and sport. It is the EU's 22nd round "
               "against Moscow."),
         src="The Brief", ill=ill_eu),
    dict(num=9, region="AFRICA", place="KHARTOUM, SUDAN", section="WAR",
         tag="KHARTOUM HIT",
         head="Drones hit homes and a UN building",
         body=("Drone attacks struck homes and a United Nations building "
               "in the capital, as Sudan's war grinds on into its "
               "fourth year."),
         src="Principia", ill=ill_khartoum),
    dict(num=10, region="AMERICAS", place="WASHINGTON, US", section="TRADE",
         tag="BLACKLISTED",
         head="US blacklists Nvidia partner Megaspeed",
         body=("The Commerce Dept. blacklisted the Singapore AI firm on "
               "Monday over suspected chip diversions to China."),
         src="The Brief", ill=ill_ban),
    dict(num=11, region="AMERICAS", place="WASHINGTON, US", section="TREASURY",
         tag="SANCTIONS",
         head="US sanctions Iranian shadow banks",
         body=("The Treasury sanctioned more than two dozen Iranian "
               "entities on Monday, accusing them of shadow banking."),
         src="The Brief", ill=ill_bank),
    dict(num=12, region="AMERICAS", place="WASHINGTON, US", section="CYBER",
         tag="FBI PROBE",
         head="FBI probes hack of police crime database",
         body=("The FBI is probing a hack of the national crime "
               "database, used to check fugitives and stolen property."),
         src="Off the Wire", ill=ill_search),
    dict(num=13, region="AMERICAS", place="CÚCUTA, COLOMBIA", section="ATTACK",
         tag="3 HURT, 60 HOMES",
         head="Drone hits base; infant among 3 hurt",
         body=("A drone hit a police base, hurting three civilians and "
               "damaging 60 homes. An infant was hurt."),
         src="The Brief", ill=ill_shield),
    dict(num=14, region="EUROPE", place="LONDON, UK", section="HEALTH",
         tag="700,000 INVITED",
         head="NHS trials AI in breast screening",
         body=("The EDITH trial will invite nearly 700,000 women to test "
               "whether AI can spot breast cancer earlier."),
         src="Principia", ill=ill_scan),
    dict(num=15, region="ASIA-PACIFIC", place="DOHA, QATAR", section="FOOTBALL",
         tag="2-1, 2-1",
         head="Mali and Italy win at U17 World Cup",
         body=("Mali beat Belgium 2-1 and Italy beat Ivory Coast 2-1 in "
               "Doha on Monday, both in group play."),
         src="Sportradar", ill=ill_ball),
]

BRIEFS = [
    (16, "Europe: Poland summons Russia's envoy"),
    (17, "Europe: NATO AWACS aircraft for Poland"),
    (18, "Europe: Russia accuses Estonia over drones"),
    (19, "Europe: Ukraine says it hit 16 launchers"),
    (20, "Europe: Drones hit Novoshakhtinsk refinery"),
    (21, "Europe: Euro-area inflation up to 4.0%"),
    (22, "Europe: UK to host 2035 Women's World Cup"),
    (23, "Middle East: Eisenkot condemns settler attacks"),
    (24, "Middle East: Israeli coalition talks stall"),
    (25, "Middle East: Saudi shadow over failed COP31"),
    (26, "Asia-Pacific: US Asia lead at record low"),
    (27, "Asia-Pacific: EU–Indonesia trade deal signed"),
    (28, "Asia-Pacific: Asian tech sell-off deepens"),
    (29, "Asia-Pacific: Tajikistan quits the ICC"),
    (30, "Africa: UN food chief warns on aid for 7.3m"),
    (31, "Africa: Ethiopia to host COP32 next year"),
    (32, "Americas: Mexico to try 'El Chapo Isidro'"),
    (33, "Americas: Gomez to quit Congress on 1 Dec"),
    (34, "Americas: Trump curbs Congress data access"),
    (35, "World: Riemann 'proof' no human understands"),
    (36, "Asia-Pacific: Afghanistan A beat Hong Kong"),
]

NUMBERS = [
    ("7", "drones that sank the Merkury"),
    ("153", "drones launched overnight"),
    ("24", "dead in Cikande fire"),
    ("30%", "shares jump as Huang returns"),
    ("4.0%", "euro-area inflation"),
    ("700,000", "NHS AI screening invites"),
]

REGION_COUNTS = [("EUROPE", 11), ("MIDDLE EAST", 4), ("AMERICAS", 8),
                 ("ASIA-PACIFIC", 7), ("AFRICA", 4), ("OCEANIA", 1),
                 ("WORLD", 1)]

UTC_LINE = [
    ("08:22", "Libya strike confirmed"),
    ("09:41", "One killed in Perm"),
    ("14:35", "Poland summons envoy"),
    ("15:33", "16 launchers hit"),
    ("16:33", "NATO urges support"),
    ("19:36", "Russia accuses Estonia"),
]

KICKER = ("7 drones sink a warship off Libya · COP31 blame game begins · "
          "Cikande toll now 24")

DATE_CHECK = (
    "Kept off this page because it was first reported before Monday: the COP31 "
    "collapse (Sun — Monday brought the blame game); the Cikande fire (Sat — "
    "Monday confirmed 24 dead); BepiColombo's orbit entry (Sat — Monday: ESA "
    "says safe); the Riemann 'proof' (Fri; Lean check Sat); Skubal's $450m Mets "
    "deal (Sun); Liverpool 4–0 United (Sun). Not Monday's news: Hormuz tankers "
    "(reported Tue). Tonight's true count: 153 drones, at the top of this page.")

SOURCES = (
    "Sources: Reuters, CNN, The Times, AP, France24, Ukrinform, IANS, ESA, "
    "Eurostat, Lowy Institute and the wires named with each story. CERTAINTY: "
    "REPORTED = the day's wires · CLAIM = one side's account · FORECAST = "
    "still to happen. Pictures and map: original, drawn in code.")

# ---------------------------------------------------------------- layout
MARG = 24
CW = W - 2 * MARG
COLW = (CW - 2 * 12) // 3
COLX = [MARG, MARG + COLW + 12, MARG + 2 * (COLW + 12)]


def draw_top_bar(d):
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((MARG, 5), "THE WORLD IN ONE DAY", font=font(F_SANS_B, 11),
           fill=(255, 255, 255))
    right = "36 STORIES · 7 REGIONS · EVERY ONE dated MONDAY 23 NOVEMBER 2026"
    f = font(F_SANS_B, 11)
    d.text((W - MARG - d.textlength(right, font=f), 5), right, font=f,
           fill=(255, 255, 255))


def draw_bottom_bar(d):
    d.rectangle([0, 1012, W, H], fill=NAVY)
    d.text((MARG, 1014), "THE WORLD IN ONE DAY", font=font(F_SANS_B, 9),
           fill=(255, 255, 255))
    right = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
    f = font(F_SANS_B, 9)
    d.text((W - MARG - d.textlength(right, font=f), 1014), right, font=f,
           fill=(255, 255, 255))


def draw_numbers(d):
    colw = CW / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MARG + colw * i + colw / 2
        f = font(F_SANS_B, 30 if len(num) <= 4 else 24)
        tw = d.textlength(num, font=f)
        d.text((cx - tw / 2, 98), num, font=f, fill=RED)
        lines = wrap(d, cap, F_SANS, 9, int(colw) - 14)
        centered(d, cx, 132, lines[0], F_SANS, 9, GREY)
        if i < 5:
            d.line([(MARG + colw * (i + 1), 102), (MARG + colw * (i + 1), 144)],
                   fill=(200, 196, 184), width=1)


def draw_regions(d):
    f = font(F_SANS_B, 11)
    chips = []
    total = 0
    for name, n in REGION_COUNTS:
        label = "%s %d" % (name, n)
        w = int(d.textlength(label, font=f)) + 14
        chips.append((name, label, w))
        total += w + 6
    total -= 6
    x = (W - total) // 2
    y = 150
    for name, label, w in chips:
        d.rectangle([x, y, x + w, y + 18], fill=REGION_COLORS[name])
        d.text((x + 7, y + 3), label, font=f, fill=(255, 255, 255))
        x += w + 6


def draw_utc(d):
    y = 172
    f = font(F_SANS_B, 11)
    label = "THE DAY IN UTC"
    lw = int(d.textlength(label, font=f)) + 12
    # pick the largest size (11 down to 8.5) whose items fit the line
    size = 11
    while size > 8.5:
        ft = font(F_SANS_B, size)
        fi = font(F_SANS, size)
        total = sum(int(d.textlength(t, font=ft)) + 4 +
                    int(d.textlength(item, font=fi)) + 6
                    for t, item in UTC_LINE) + 5 * 10
        if total <= W - 2 * MARG - lw - 10:
            break
        size -= 0.5
    ft = font(F_SANS_B, size)
    fi = font(F_SANS, size)
    d.rectangle([MARG, y, MARG + lw, y + 16], fill=INK)
    d.text((MARG + 6, y + 2), label, font=f, fill=(255, 255, 255))
    x = MARG + lw + 10
    for i, (t, item) in enumerate(UTC_LINE):
        if i:
            d.text((x, y + 2), "·", font=fi, fill=INK)
            x += 10
        d.text((x, y + 2), t, font=ft, fill=RED)
        x += int(d.textlength(t, font=ft)) + 4
        d.text((x, y + 2), item, font=fi, fill=INK)
        x += int(d.textlength(item, font=fi)) + 6


def draw_featured(d, s, x, y, img_h, kind):
    """kind: 'large' (3-up), 'medium' (6-up), 'small' (strip)."""
    if kind == "large":
        head_size, head_lead, body_size, body_lead = 20, 23, 11, 13
    elif kind == "medium":
        head_size, head_lead, body_size, body_lead = 15, 18, 10, 13
    else:
        head_size, head_lead, body_size, body_lead = 13, 16, 10, 12
    s["ill"](d, x, y, COLW, img_h)
    tag(d, x, y, s["tag"], 9 if kind == "small" else 10)
    ty = y + img_h + 5
    # dateline: red number + place
    fnum = font(F_SANS_B, 11 if kind != "small" else 10)
    d.text((x, ty), str(s["num"]), font=fnum, fill=RED)
    nx = x + int(d.textlength(str(s["num"]), font=fnum)) + 5
    d.text((nx, ty), "%s · %s" % (s["place"], s["section"]),
           font=font(F_SANS_B, 11 if kind != "small" else 10), fill=INK)
    ty += 15 if kind != "small" else 13
    # headline
    lines = wrap(d, s["head"], F_SERIF, head_size, COLW)
    ty = text_block(d, x, ty, lines, F_SERIF, head_size, INK, head_lead)
    # summary + source
    body = s["body"] + " (%s)" % s["src"]
    lines = wrap(d, body, F_SANS, body_size, COLW)
    text_block(d, x, ty + 2, lines, F_SANS, body_size, INK, body_lead)


def draw_map_section(d):
    y0 = 856
    centered(d, MARG + 165, y0, "WHERE IT HAPPENED", F_SANS_B, 11, INK)
    centered(d, 366 + 317, y0, "ALSO ON MONDAY 23 NOVEMBER — 21 MORE STORIES",
             F_SANS_B, 11, INK)
    draw_map(d, MARG, y0 + 14, 330, 76)
    # briefs in 3 columns
    bx = [366, 580, 794]
    bw = 206
    for ci in range(3):
        x = bx[ci]
        yy = y0 + 14
        for num, text in BRIEFS[ci * 7:(ci + 1) * 7]:
            fnum = font(F_SANS_B, 8)
            d.text((x, yy), str(num), font=fnum, fill=RED)
            nx = x + int(d.textlength(str(num), font=fnum)) + 4
            lines = wrap(d, text, F_SANS, 8, bw - (nx - x))
            yy = text_block(d, nx, yy, lines, F_SANS, 8, INK, 9.5)
            yy += 1


def draw_date_check(d):
    y0, y1 = 950, 990
    d.rectangle([MARG, y0, W - MARG, y1], outline=RED, width=2)
    d.text((MARG + 8, y0 + 6), "DATE CHECK", font=font(F_SANS_B, 11), fill=RED)
    lines = wrap(d, DATE_CHECK, F_SANS, 9, W - 2 * MARG - 108)
    text_block(d, MARG + 104, y0 + 4, lines, F_SANS, 9, INK, 12)


def draw_sources(d):
    lines = wrap(d, SOURCES, F_SANS, 8, CW)
    text_block(d, MARG, 993, lines, F_SANS, 8, GREY, 9)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_top_bar(d)
    centered(d, W // 2, 28, "Monday 23 November 2026", F_SERIF, 52, INK)
    centered(d, W // 2, 86, KICKER, F_SANS_B, 13, RED)
    draw_numbers(d)
    draw_regions(d)
    draw_utc(d)
    hline(d, MARG, W - MARG, 190, INK, 1)
    # large stories 1-3
    for i in range(3):
        draw_featured(d, FEATURED[i], COLX[i], 194, 78, "large")
    # medium stories 4-6, 7-9
    for i in range(3):
        draw_featured(d, FEATURED[3 + i], COLX[i], 388, 44, "medium")
    for i in range(3):
        draw_featured(d, FEATURED[6 + i], COLX[i], 524, 44, "medium")
    # small stories 10-12, 13-15
    for i in range(3):
        draw_featured(d, FEATURED[9 + i], COLX[i], 660, 30, "small")
    for i in range(3):
        draw_featured(d, FEATURED[12 + i], COLX[i], 756, 30, "small")
    hline(d, MARG, W - MARG, 852, INK, 1)
    draw_map_section(d)
    draw_date_check(d)
    draw_sources(d)
    draw_bottom_bar(d)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img = build()
    img.save(path, "JPEG", quality=88)
    size = os.path.getsize(path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()
