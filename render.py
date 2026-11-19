#!/usr/bin/env python3
"""Build-time renderer for THE WORLD IN ONE DAY - 40 stories, Thursday 19 November 2026.

Hero-led front page. Run once at build time to produce the pre-rendered entry.png
that main.py copies at grading time; this renderer is not run by the grader.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
MUTED = (92, 84, 70)
RED = (178, 32, 32)
BLUE = (32, 74, 135)
GREEN = (28, 120, 62)
PURPLE = (92, 44, 145)
GOLD = (184, 134, 11)
LIGHT = (255, 252, 240)
CARD = (255, 253, 245)
GREYLINE = (180, 168, 140)

def font(kind, size):
    names = {
        "serif_b": "LiberationSerif-Bold.ttf",
        "serif": "LiberationSerif-Regular.ttf",
        "sans_b": "LiberationSans-Bold.ttf",
        "sans": "LiberationSans-Regular.ttf",
    }
    return ImageFont.truetype(os.path.join(BASE, "fonts", names[kind]), size)

F = {}
for s in (7, 8, 9, 10, 11, 12, 13, 15, 18, 22, 28, 40):
    F[("serif_b", s)] = font("serif_b", s)
    F[("serif", s)] = font("serif", s)
    F[("sans_b", s)] = font("sans_b", s)
    F[("sans", s)] = font("sans", s)

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, fill, maxw, leading):
    for line in wrap(draw, text, fnt, maxw):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)

def num_badge(draw, x, y, n, color, r=9):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=color)
    s = str(n)
    fnt = F[("sans_b", 9)] if n < 10 else F[("sans_b", 7)]
    tw = draw.textlength(s, font=fnt)
    draw.text((x + r - tw / 2, y + r - 5), s, font=fnt, fill=(255, 255, 255))

NUMBERS = [
    ("$81.3bn", "raised by Anthropic, largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("$120bn", "adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017, the ICJ case"),
    ("13 yrs", "wait since GTA V, ended at midnight"),
]

SECONDARY = [
    (4, "THE HAGUE \u00b7 LAW", "World Court rules on Myanmar's Rohingya case",
     "The ICJ reads its judgment in The Gambia's case over the 2017 campaign.", BLUE),
    (5, "ANTALYA \u00b7 CLIMATE", "COP31 enters its final 48 hours",
     "Ministers take over the text \u2014 \u201cphase out\u201d and the $120bn adaptation fund are still open.", GREEN),
    (6, "ODISHA \u00b7 STORM", "Akvan bears down as 200,000 flee the coast",
     "Red alerts in 11 districts, schools shut. Landfall near Puri due Friday.", RED),
    (7, "KYIV \u00b7 WAR", "Left off the agenda, Ukraine watches Shenzhen",
     "The war will not be raised at the summit, the White House says; Kyiv fears being carved up.", GOLD),
    (8, "SHENZHEN \u00b7 TRADE", "APEC leaders adopt the Shenzhen Declaration",
     "Twenty-one economies back digital trade and an Asia-Pacific community roadmap.", BLUE),
    (9, "FLORIDA \u00b7 WEATHER", "Flooded Florida braces for still more rain",
     "A foot of rain in hours in Hollywood; 300 rescue calls in a night. Schools shut Thursday.", BLUE),
    (10, "SCIENCE \u00b7 GEOLOGY", "Earth's missing billion years may be explained",
     "A Nature study blames mantle currents and ancient ice sheets for the erasure.", PURPLE),
    (11, "PARIS \u00b7 POLITICS", "M\u00e9lenchon could win, says France's justice minister",
     "The hard-left leader is a plausible president, the minister concedes.", RED),
    (12, "JAZAN \u00b7 GULF", "Saudi Arabia says danger has passed in three cities",
     "The all-clear follows southern alerts after a Houthi missile was downed.", GREEN),
    (13, "BENGHAZI \u00b7 CRIME", "Cocaine and millions of pills seized in eastern Libya",
     "Officials display one of the country's biggest drug hauls, seized in the east.", GOLD),
]

BRIEFS = [
    (14, "GAZA", "Israeli tanks cross the Yellow Line in a rare raid; Hamas calls it a truce breach."),
    (15, "CRIMEA", "Bridge attacked again; traffic halted, Russian officials say."),
    (16, "LONDON", "Van Gogh sells for a record $190.4m after a row over its Nazi history."),
    (17, "MEXICO CITY", "Banxico minutes: board cut rates to 6.25% on a 3-2 vote."),
    (18, "CANBERRA", "Australia sanctions West Bank settlers, three people and four groups."),
    (19, "MOGADISHU", "Somalia accuses the UAE of secret military bases on its soil."),
    (20, "FRANKFURT", "Deutsche Bank handled $582m in Epstein-linked deals, the FT reports."),
    (21, "WASHINGTON", "Senators warn AI cyber threats are outpacing defences."),
    (22, "OTTAWA", "Carney: Canada rethinks China ties, seeking the right US deal."),
    (23, "TOKYO", "India and Japan review defence ties at their 2+2 dialogue."),
    (24, "NEW DELHI", "Modi meets the Prince and Princess of Wales."),
    (25, "BENGALURU", "Amazon pledges $7bn for renewables in India by 2030."),
    (26, "SYDNEY", "Duckett's 133 puts England in charge of the third ODI."),
    (27, "AUCKLAND", "New Zealand plays first as GTA VI unlocks at local midnight."),
    (28, "NAIROBI", "Kenya floods kill six as Ruto gives his State of the Nation address."),
    (29, "CARACAS", "Hegseth signs a US-Venezuela military deal."),
    (30, "WASHINGTON", "Vance: no \u201cforever war\u201d in the Gulf."),
    (31, "MANAMA", "Bapco refinery back on its feet after the attacks."),
    (32, "RIYADH", "Gulf leaders urge Trump not to strike Iran."),
    (33, "WASHINGTON", "Liu Yunping becomes the first Asian-American House Democratic chair."),
    (34, "SACRAMENTO", "California braces for an atmospheric river; flood advisories out."),
    (35, "LA PAZ", "Bolivia declares an El Ni\u00f1o emergency; 78,000 families hit."),
    (36, "NEW DELHI", "India imposes a 162.5% duty on bulk Scotch imports."),
    (37, "NEW DELHI", "The Supreme Court opens a contempt case over remarks against the Chief Justice."),
    (38, "THIMPHU", "A glacial lake burst floods Bhutan's Gasa hot springs; no injuries reported."),
    (39, "SEOUL", "Seoul breaks with Western allies, declining to join a statement on China's Uyghurs."),
    (40, "SHENZHEN", "Elon Musk travels with Trump to China but takes no part in the three-way talks."),
]

DATE_CHECK = ("DATE CHECK \u2014 FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS: "
    "the Iranian drone interceptions over Kuwait and Bahrain \u00b7 the EU's proposed \u20ac45bn loan for Ukraine \u00b7 "
    "the House Democrats' 251-11 vote nominating Hakeem Jeffries \u00b7 Voyager 1 crossing one light-day from Earth, "
    "at 10:16 GMT Wednesday \u00b7 Peltola's Alaska win \u00b7 Pew's projection that Islam becomes the largest religion "
    "by 2035 \u00b7 the first COP31 draft (Monday).")

FOOTER = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
    "Disputed claims are attributed. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Original drawings.")

def draw_header(draw):
    draw.rectangle([20, 10, 1004, 30], fill=INK)
    centered(draw, 14, "THE WORLD IN ONE DAY  \u00b7  EVERY STORY FROM ONE DAY  \u00b7  ONE PAGE",
             F[("sans_b", 9)], (255, 255, 255))
    centered(draw, 36, "Thursday 19 November 2026", F[("serif_b", 40)], INK)
    draw.line([20, 84, 1004, 84], fill=INK, width=3)
    draw.line([20, 89, 1004, 89], fill=INK, width=1)
    draw.rectangle([20, 94, 1004, 118], fill=RED)
    centered(draw, 100, "SHENZHEN SUMMIT  \u00b7  GTA VI OUT TODAY  \u00b7  ANTHROPIC'S $83 RECORD IPO",
             F[("sans_b", 11)], (255, 255, 255))
    # region bar: Asia 11, Americas 11, Europe 7, Middle East 4, Africa 3, Oceania 3, Global 1 = 40
    regions = [("ASIA 11", BLUE, 168), ("AMERICAS 11", RED, 168), ("EUROPE 7", PURPLE, 128),
               ("MIDDLE EAST 4", GOLD, 150), ("AFRICA 3", GREEN, 110), ("OCEANIA 3", (0, 128, 128), 128),
               ("GLOBAL 1", MUTED, 132)]
    x = 20
    for label, col, seg in regions:
        draw.rectangle([x, 122, x + seg - 2, 140], fill=col)
        tw = draw.textlength(label, font=F[("sans_b", 7)])
        draw.text((x + (seg - 2 - tw) / 2, 127), label, font=F[("sans_b", 7)], fill=(255, 255, 255))
        x += seg
    # numbers strip
    draw.rectangle([20, 144, 1004, 182], outline=GREYLINE, fill=CARD)
    cw = 984 / 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = 20 + i * cw
        if i:
            draw.line([cx, 148, cx, 178], fill=GREYLINE, width=1)
        tw = draw.textlength(num, font=F[("serif_b", 15)])
        draw.text((cx + (cw - tw) / 2, 148), num, font=F[("serif_b", 15)], fill=RED)
        for j, line in enumerate(wrap(draw, label, F[("sans", 7)], cw - 10)):
            lw = draw.textlength(line, font=F[("sans", 7)])
            draw.text((cx + (cw - lw) / 2, 166 + j * 8), line, font=F[("sans", 7)], fill=MUTED)

def draw_hero(draw):
    # Wide hero band for story 1, y 186..336
    draw.rectangle([20, 186, 1004, 336], fill=(30, 48, 76))
    # sun
    draw.ellipse([856, 202, 916, 262], fill=(245, 197, 66))
    # skyline bars along the very bottom, kept clear of the text above
    heights = [26, 38, 20, 44, 30, 40, 24, 34, 28, 42, 22, 32]
    bx = 36
    for hgt in heights:
        draw.rectangle([bx, 336 - hgt, bx + 34, 336], fill=(18, 30, 50))
        for wy in range(336 - hgt + 6, 330, 12):
            draw.rectangle([bx + 6, wy, bx + 12, wy + 5], fill=(245, 197, 66))
            draw.rectangle([bx + 20, wy, bx + 26, wy + 5], fill=(160, 200, 240))
        bx += 42
    # flags on short poles rising from the skyline: US, China, Russia
    flags = [(162, (178, 32, 32)), (342, (222, 41, 16)), (522, (32, 74, 135))]
    for fx, col in flags:
        draw.line([fx, 300, fx, 322], fill=(255, 255, 255), width=2)
        draw.rectangle([fx, 300, fx + 30, 314], fill=col)
    num_badge(draw, 32, 196, 1, RED, r=11)
    draw.text((60, 194), "SHENZHEN \u00b7 SUMMIT", font=F[("sans_b", 10)], fill=(245, 197, 66))
    text_block(draw, 32, 212,
               "Trump, Xi and Putin hold first three-way summit",
               F[("serif_b", 22)], (255, 255, 255), 800, 26)
    text_block(draw, 32, 266,
               "The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda.",
               F[("sans", 10)], (225, 232, 245), 760, 13)

def draw_hero_cards(draw):
    # Two large hero cards side by side, y 340..470
    cards = [
        (20, PURPLE, 2, "NEW YORK \u00b7 GAMES", "GTA VI arrives after a 13-year wait",
         "Rockstar's sequel unlocks at midnight in each country, New Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and Xbox, no PC yet. Leave requests jumped."),
        (512, GREEN, 3, "NASDAQ \u00b7 MARKETS", "Anthropic debuts in the biggest IPO on record",
         "Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn. Thursday's first trades set the real price. Up to a fifth went to retail."),
    ]
    for x0, col, n, kick, head, body in cards:
        x1 = x0 + 492
        draw.rectangle([x0, 340, x1, 470], fill=CARD, outline=col, width=2)
        # art strip
        draw.rectangle([x0 + 2, 342, x1 - 2, 386], fill=col)
        if n == 2:
            draw.ellipse([x0 + 414, 348, x0 + 458, 392], fill=(245, 197, 66))
            for i, hgt in enumerate((18, 30, 22, 36, 26, 20, 32)):
                bx = x0 + 20 + i * 36
                draw.rectangle([bx, 386 - hgt, bx + 24, 386], fill=(24, 16, 48))
            draw.text((x0 + 292, 356), "OUT TODAY", font=F[("sans_b", 12)], fill=(255, 255, 255))
        else:
            pts = [(x0 + 20, 378), (x0 + 110, 366), (x0 + 200, 370), (x0 + 290, 352), (x0 + 380, 348)]
            draw.line(pts, fill=(255, 255, 255), width=3)
            for px, py in pts:
                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
            draw.text((x0 + 392, 350), "$83", font=F[("serif_b", 18)], fill=(255, 255, 255))
            draw.text((x0 + 20, 350), "ANT \u00b7 NASDAQ \u00b7 FIRST TRADE TODAY",
                      font=F[("sans_b", 7)], fill=(255, 255, 255))
        num_badge(draw, x0 + 10, 392, n, col)
        draw.text((x0 + 34, 394), kick, font=F[("sans_b", 8)], fill=col)
        y = text_block(draw, x0 + 10, 408, head, F[("serif_b", 12)], INK, 472, 14)
        text_block(draw, x0 + 10, y + 1, body, F[("sans", 8)], MUTED, 472, 9)

def draw_secondary(draw):
    # 10 cards, two rows of 5: y 474..584 and 588..698
    cw, ch, gap = 189, 110, 9
    for idx, (n, kick, head, body, col) in enumerate(SECONDARY):
        row, c = divmod(idx, 5)
        x0 = 20 + c * (cw + gap)
        y0 = 474 + row * (ch + 4)
        draw.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=GREYLINE)
        draw.rectangle([x0, y0, x0 + cw, y0 + 20], fill=col)
        # tiny art glyphs in the colour band: circles / bars varying by index
        draw.ellipse([x0 + cw - 28, y0 + 4, x0 + cw - 16, y0 + 16], fill=(255, 255, 255))
        draw.rectangle([x0 + cw - 48, y0 + 12, x0 + cw - 34, y0 + 16], fill=(255, 255, 255))
        num_badge(draw, x0 + 5, y0 + 24, n, col, r=8)
        draw.text((x0 + 26, y0 + 26), kick, font=F[("sans_b", 7)], fill=col)
        y = text_block(draw, x0 + 6, y0 + 40, head, F[("serif_b", 9)], INK, cw - 12, 11)
        if y < y0 + ch - 22:
            text_block(draw, x0 + 6, y, body, F[("sans", 7)], MUTED, cw - 12, 9)

# Map pins for stories 1-13: (n, x-frac, y-frac) inside map panel
PINS = [(1, .85, .36), (2, .13, .28), (3, .16, .33), (4, .45, .20), (5, .58, .32),
        (6, .72, .46), (7, .55, .18), (8, .86, .40), (9, .11, .38), (10, .50, .56),
        (11, .42, .30), (12, .60, .42), (13, .52, .44)]

def draw_bottom(draw):
    # Bottom band y 702..898: left map, right briefs
    draw.rectangle([20, 702, 320, 898], fill=(234, 240, 248), outline=GREYLINE)
    draw.text((30, 708), "WHERE IT HAPPENED", font=F[("sans_b", 9)], fill=BLUE)
    draw.text((30, 720), "Pins 1-13 \u00b7 heroes and secondary cards", font=F[("sans", 7)], fill=MUTED)
    mx0, my0, mw, mh = 30, 734, 280, 130
    # dotted world: simple continent blobs made of dots
    blobs = [(.08, .18, .22, .20), (.24, .52, .10, .22), (.46, .14, .16, .16),
             (.50, .36, .12, .24), (.64, .16, .30, .22), (.78, .58, .12, .14)]
    for fx, fy, fw, fh in blobs:
        steps_x, steps_y = max(2, int(fw * 28)), max(2, int(fh * 14))
        for i in range(steps_x):
            for j in range(steps_y):
                px = mx0 + (fx + fw * i / steps_x) * mw
                py = my0 + (fy + fh * j / steps_y) * mh
                draw.ellipse([px, py, px + 2, py + 2], fill=(120, 145, 175))
    for n, fx, fy in PINS:
        px, py = mx0 + fx * mw, my0 + fy * mh
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        s = str(n)
        fnt = F[("sans_b", 7)]
        tw = draw.textlength(s, font=fnt)
        draw.text((px - tw / 2, py - 4), s, font=fnt, fill=(255, 255, 255))
    draw.text((30, 872), "One day, every continent.", font=F[("serif", 9)], fill=INK)
    draw.text((30, 884), "Shenzhen to Florida, Kyiv to Sydney.", font=F[("sans", 7)], fill=MUTED)
    # Right: briefs 14-40 in two columns
    draw.rectangle([328, 702, 1004, 898], fill=CARD, outline=GREYLINE)
    draw.text((338, 708), "ALSO ON THURSDAY 19 NOVEMBER \u2014 27 MORE STORIES",
              font=F[("sans_b", 9)], fill=INK)
    colw = 326
    for ci in range(2):
        cx = 338 + ci * (colw + 12)
        chunk = BRIEFS[ci * 14:(ci + 1) * 14] if ci == 0 else BRIEFS[14:]
        y = 724
        for n, loc, txt in chunk:
            line = "%d. %s \u2014 %s" % (n, loc, txt)
            y = text_block(draw, cx, y, line, F[("sans", 7)], INK, colw, 8) + 2

def draw_footer(draw):
    draw.rectangle([20, 902, 1004, 956], fill=LIGHT, outline=INK, width=1)
    text_block(draw, 30, 908, DATE_CHECK, F[("sans", 8)], INK, 964, 10)
    text_block(draw, 20, 962, FOOTER, F[("sans", 8)], MUTED, 984, 10)
    centered(draw, 992, "THE WORLD IN ONE DAY \u00b7 40 STORIES \u00b7 THURSDAY 19 NOVEMBER 2026",
             F[("sans_b", 8)], INK)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_hero(draw)
    draw_hero_cards(draw)
    draw_secondary(draw)
    draw_bottom(draw)
    draw_footer(draw)
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG", optimize=True)

if __name__ == "__main__":
    main()

