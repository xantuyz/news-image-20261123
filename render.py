#!/usr/bin/env python3
"""Render the news-image-20261123 entry: one 1024x1024 PNG summing up
Monday 23 November 2026 world news. Build-time only (PIL)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

TEAL_DARK = (11, 43, 51)      # #0B2B33
TEAL = (14, 58, 68)           # #0E3A44
TEAL_PANEL = (17, 66, 76)     # panel teal
TEAL_SEA = (9, 38, 46)
AMBER = (232, 163, 61)        # #E8A33D
CREAM = (245, 239, 227)       # #F5EFE3
CREAM_DIM = (206, 200, 184)
STEEL = (127, 168, 181)
BRICK = (198, 91, 60)
GREEN = (94, 155, 106)
GREY_SMOKE = (158, 168, 166)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap into lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines, shrink_to=18):
    """Wrap text; shrink font until it fits max_lines (returns font, lines)."""
    size = fnt.size
    while size > shrink_to:
        f = font(fnt.path, size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 2
    f = font(fnt.path, shrink_to)
    return f, wrap(draw, text, f, max_w)


def chip(draw, x, y, label, fg, bg=None):
    """Small category chip: outlined rounded box + capital text."""
    f = font(FONT_BOLD, 17)
    tw = draw.textlength(label, font=f)
    pad_x, pad_y = 9, 4
    box = [x, y, x + tw + 2 * pad_x, y + 26]
    if bg is not None:
        draw.rounded_rectangle(box, radius=6, fill=bg)
    draw.rounded_rectangle(box, radius=6, outline=fg, width=2)
    draw.text((x + pad_x, y + 3), label, font=f, fill=fg)
    return box[2]  # right edge


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def draw_lead_art(draw):
    """Lead illustration: Sparta II at anchor in the Gulf of Finland,
    smoke still rising, fire boats spraying water."""
    # sky
    vgrad(draw, (0, 150, 1024, 310), (13, 52, 62), (46, 96, 108))
    # low amber sun glow behind the smoke (kept below the date line)
    for r, a in ((85, 40), (60, 60), (38, 90)):
        draw.ellipse([700 - r, 245 - r, 700 + r, 245 + r], fill=(232, 163, 61, a))
    # sea
    draw.rectangle([0, 310, 1024, 352], fill=TEAL_SEA)
    for yy, col in ((316, (24, 84, 96)), (328, (20, 74, 86)), (340, (28, 94, 106))):
        draw.line([(0, yy), (1024, yy)], fill=col, width=3)
    # water-cannon spray arcs from both sides
    for cx, flip in ((60, 1), (964, -1)):
        for k in range(3):
            r = 150 + k * 26
            draw.arc([cx - r * flip - r, 352 - r, cx - r * flip + r, 352 + r],
                     start=270 if flip == 1 else 180,
                     end=360 if flip == 1 else 270,
                     fill=(190, 220, 228), width=4)
    # ship hull
    draw.polygon([(300, 280), (760, 280), (720, 332), (340, 332)], fill=(8, 30, 36))
    draw.line([(300, 280), (760, 280)], fill=AMBER, width=4)
    # containers on deck
    boxes = [(330, 242, 400, 280, AMBER), (408, 242, 478, 280, STEEL),
             (486, 242, 556, 280, BRICK), (564, 242, 634, 280, (90, 120, 110)),
             (642, 252, 700, 280, AMBER)]
    for x0, y0, x1, y1, c in boxes:
        draw.rectangle([x0, y0, x1, y1], fill=c, outline=(8, 30, 36), width=2)
    # bridge tower
    draw.rectangle([706, 218, 748, 280], fill=CREAM)
    draw.rectangle([712, 230, 742, 244], fill=TEAL_DARK)
    draw.rectangle([712, 250, 742, 264], fill=TEAL_DARK)
    # smoke columns rising from the containers (tops stay below y=150)
    for sx, sy, sr in ((420, 240, 22), (455, 210, 30), (505, 192, 36),
                       (560, 214, 26), (605, 240, 20)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GREY_SMOKE)
        draw.ellipse([sx - sr // 2, sy - sr // 2, sx + sr // 2, sy + sr // 2],
                     fill=(178, 186, 184))


def draw_shield(draw, x0, y0, x1, y1):
    """NATO cell icon: shield outline + four-point star."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.polygon([(cx - 52, y0 + 26), (cx + 52, y0 + 26), (cx + 52, cy + 6),
                  (cx, y1 - 22), (cx - 52, cy + 6)], outline=AMBER, width=5)
    # four-point compass star
    pts = [(cx, cy - 46), (cx + 12, cy - 12), (cx + 46, cy), (cx + 12, cy + 12),
           (cx, cy + 46), (cx - 12, cy + 12), (cx - 46, cy), (cx - 12, cy - 12)]
    draw.polygon(pts, fill=CREAM)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=AMBER)


def draw_rubble(draw, x0, y0, x1, y1):
    """Dymer cell icon: collapsed apartment block, tilted slabs + rubble."""
    cx = (x0 + x1) // 2
    # standing wall fragment
    draw.rectangle([x0 + 18, y0 + 34, x0 + 66, y1 - 30], fill=(120, 128, 124))
    for wy in (y0 + 52, y0 + 84, y0 + 116):
        draw.rectangle([x0 + 26, wy, x0 + 58, wy + 16], fill=TEAL_DARK)
    # fallen tilted slab
    draw.polygon([(x0 + 66, y0 + 70), (x1 - 16, y0 + 96), (x1 - 26, y0 + 132),
                  (x0 + 74, y0 + 108)], fill=(150, 148, 138))
    # rubble mound
    draw.polygon([(x0 + 14, y1 - 30), (cx - 6, y1 - 78), (cx + 30, y1 - 62),
                  (x1 - 14, y1 - 30)], fill=(178, 172, 158))
    draw.polygon([(cx - 30, y1 - 30), (cx + 6, y1 - 56), (cx + 44, y1 - 30)],
                 fill=(140, 134, 120))
    # rescue crane arm + hook
    draw.line([(x1 - 18, y0 + 20), (x1 - 18, y0 + 66)], fill=AMBER, width=5)
    draw.line([(x1 - 44, y0 + 20), (x1 - 18, y0 + 20)], fill=AMBER, width=5)
    draw.arc([x1 - 28, y0 + 66, x1 - 8, y0 + 86], start=0, end=270, fill=AMBER, width=4)


def draw_exam(draw, x0, y0, x1, y1):
    """Korea cell icon: exam paper + pencil, red X over AI cheating."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rectangle([x0 + 26, y0 + 26, x1 - 30, y1 - 26], fill=CREAM,
                   outline=AMBER, width=3)
    for i, ly in enumerate((y0 + 52, y0 + 78, y0 + 104)):
        draw.line([(x0 + 38, ly), (x1 - 44, ly)], fill=(120, 128, 124), width=3)
    f = font(FONT_BOLD, 30)
    draw.text((cx - 30, y0 + 116), "AI", font=f, fill=BRICK)
    # pencil across the corner
    draw.polygon([(x1 - 52, y1 - 30), (x1 - 14, y1 - 68), (x1 - 8, y1 - 56),
                  (x1 - 46, y1 - 18)], fill=AMBER)
    draw.polygon([(x1 - 14, y1 - 68), (x1 - 8, y1 - 56), (x1 - 16, y1 - 52)],
                 fill=TEAL_DARK)
    # red cross mark
    draw.line([(x0 + 30, y0 + 30), (x0 + 56, y0 + 56)], fill=BRICK, width=6)
    draw.line([(x0 + 56, y0 + 30), (x0 + 30, y0 + 56)], fill=BRICK, width=6)


def draw_pmi(draw, x0, y0, x1, y1):
    """Australia cell icon: falling bars + down arrow."""
    base = y1 - 34
    bars = [(x0 + 24, 92), (x0 + 58, 66), (x0 + 92, 40)]
    for bx, bh in bars:
        draw.rectangle([bx, base - bh, bx + 26, base], fill=AMBER)
    draw.line([(x0 + 18, base), (x1 - 14, base)], fill=CREAM, width=3)
    # down arrow
    ax = x1 - 34
    draw.line([(ax, y0 + 30), (ax, y0 + 92)], fill=BRICK, width=7)
    draw.polygon([(ax - 14, y0 + 80), (ax + 14, y0 + 80), (ax, y0 + 108)],
                 fill=BRICK)


def grid_cell(draw, x0, y0, x1, y1, icon_fn, chip_label, chip_fg,
              headline, deck):
    """One 2x2 grid cell: icon panel left, chip + headline + deck right."""
    draw.rectangle([x0, y0, x1, y1], fill=TEAL_PANEL)
    draw.rectangle([x0, y0, x0 + 150, y1], fill=TEAL_DARK)
    icon_fn(draw, x0, y0, x0 + 150, y1)
    tx = x0 + 164
    tw = x1 - tx - 14
    chip(draw, tx, y0 + 14, chip_label, chip_fg)
    hf, hlines = fit_lines(draw, headline, font(FONT_BOLD, 30), tw, 2)
    hy = y0 + 50
    for ln in hlines:
        draw.text((tx, hy), ln, font=hf, fill=CREAM)
        hy += hf.size + 4
    df = font(FONT_REG, 21)
    dlines = wrap(draw, deck, df, tw)
    if dlines:
        draw.text((tx, y1 - 34), dlines[0], font=df, fill=CREAM_DIM)


def main():
    img = Image.new("RGB", (W, H), TEAL_DARK)
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- Masthead 0-118 ----
    f_mast = font(FONT_BOLD, 62)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=f_mast)
    draw.text(((W - tw) / 2, 24), title, font=f_mast, fill=CREAM)
    draw.rectangle([28, 104, W - 28, 110], fill=AMBER)

    # ---- Date line 118-150 ----
    f_date = font(FONT_BOLD, 25)
    date_txt = "MONDAY, 23 NOVEMBER 2026"
    tw = draw.textlength(date_txt, font=f_date)
    draw.text(((W - tw) / 2, 118), date_txt, font=f_date, fill=AMBER)

    # ---- Lead hero 150-520 ----
    draw_lead_art(draw)
    # lead text band
    draw.rectangle([0, 350, 1024, 520], fill=TEAL_DARK)
    draw.rectangle([0, 350, 1024, 354], fill=AMBER)
    chip(draw, 28, 366, "CONFLICT", AMBER)
    lead_head = "Russian ship still smoulders off Finland"
    hf, hlines = fit_lines(draw, lead_head, font(FONT_BOLD, 40), 968, 2)
    hy = 400
    for ln in hlines:
        draw.text((28, hy), ln, font=hf, fill=CREAM)
        hy += hf.size + 2
    f_deck = font(FONT_REG, 24)
    draw.text((28, 484), "Flames out, cooling goes on; 16 crew safe",
              font=f_deck, fill=CREAM_DIM)

    # ---- Grid 2x2, 520-884 ----
    cells = [
        (0, 520, draw_shield, "POLITICS", AMBER,
         "NATO meets over missiles in Poland",
         "All three were Kh-101 missiles"),
        (512, 520, draw_rubble, "CONFLICT", STEEL,
         "Boy pulled alive from Kyiv rubble",
         "3 dead in Dymer; 10 missing"),
        (0, 702, draw_exam, "POLITICS", AMBER,
         "Seoul minister quits over AI exam cheating",
         "111 cases at Suneung exam"),
        (512, 702, draw_pmi, "ECONOMY", GREEN,
         "Australia business shrinks at 5-year pace",
         "Flash PMI 46.1, a 5-year low"),
    ]
    for cx0, cy0, icon_fn, clabel, cfg, head, deck in cells:
        grid_cell(draw, cx0 + 4, cy0 + 4, cx0 + 508, cy0 + 178,
                  icon_fn, clabel, cfg, head, deck)
    # grid dividers
    draw.line([(512, 520), (512, 884)], fill=TEAL_DARK, width=4)
    draw.line([(0, 702), (1024, 702)], fill=TEAL_DARK, width=4)

    # ---- Strip 884-952 ----
    draw.rectangle([0, 884, 1024, 952], fill=(13, 52, 62))
    draw.rectangle([0, 884, 10, 952], fill=AMBER)
    chip(draw, 28, 894, "CONFLICT", STEEL)
    f_strip = font(FONT_BOLD, 27)
    draw.text((28, 926), "Odesa schools go remote as grid hit",
              font=f_strip, fill=CREAM)
    # right-aligned short deck
    f_sdeck = font(FONT_REG, 20)
    sdeck = "Online classes to 27 Nov"
    sw = draw.textlength(sdeck, font=f_sdeck)
    draw.text((1024 - 28 - sw, 900), sdeck, font=f_sdeck, fill=CREAM_DIM)

    # ---- Footer 952-1024 ----
    f_foot = font(FONT_REG, 19)
    src = "Sources: Reuters  ·  CNN  ·  The Guardian  ·  Dow Jones"
    tw = draw.textlength(src, font=f_foot)
    draw.text(((W - tw) / 2, 962), src, font=f_foot, fill=CREAM_DIM)
    f_foot2 = font(FONT_BOLD, 19)
    note = "All stories first reported 23 November 2026"
    tw = draw.textlength(note, font=f_foot2)
    draw.text(((W - tw) / 2, 990), note, font=f_foot2, fill=AMBER)

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
