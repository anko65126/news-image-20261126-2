"""Draw a broadsheet front page summing up the world news of
Thursday 26 November 2026. Deterministic: same input, same PNG bytes.
Run: python3 make_front_page.py  ->  writes entry.png next to this file.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
TEAL = (15, 118, 110)
GOLD = (180, 130, 29)
RULE = (120, 110, 95)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def story_box(draw, x, y, w, h, kicker, kicker_color, headline, body):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 34], fill=kicker_color)
    draw.text((x + 12, y + 7), kicker, font=SANS_B(19), fill=(255, 255, 255))
    cx = x + 14
    cy = y + 48
    cy = draw_lines(draw, wrap(draw, headline, SERIF_B(27), w - 28), cx, cy,
                    SERIF_B(27), INK, 33)
    cy += 6
    draw_lines(draw, wrap(draw, body, SANS(19), w - 28), cx, cy,
               SANS(19), (60, 60, 60), 25)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 18), "THE WORLD TODAY", font=SERIF_B(64), fill=(255, 255, 255))
    d.text((32, 86), "T H U R S D A Y ,  2 6  N O V E M B E R  2 0 2 6",
           font=SANS_B(20), fill=(212, 175, 55))
    d.rectangle([0, 118, W, 124], fill=RED)

    # Lead story
    y = 148
    d.text((32, y), "TRADE WAR ESCALATES", font=SANS_B(22), fill=RED)
    y += 30
    y = draw_lines(
        d,
        wrap(d, "US proposes sweeping new tariffs on 14 partners",
             SERIF_B(44), W - 64),
        32, y, SERIF_B(44), INK, 52)
    y += 8
    y = draw_lines(
        d,
        wrap(d, "Washington says the duties fight factory overcapacity. "
                "China, blamed most for flooding world markets with cheap "
                "exports, faces the highest rates.",
             SANS(22), W - 64),
        32, y, SANS(22), (60, 60, 60), 30)
    y += 16
    # Simple tariff bar chart: China highest, others lower
    chart_x, chart_y = 32, y
    bars = [("CHINA", 300, RED), ("PARTNERS", 190, NAVY), ("OTHERS", 120, TEAL)]
    bx = chart_x
    for label, length, color in bars:
        d.rectangle([bx, chart_y, bx + 46, chart_y + 22], fill=color)
        d.text((bx + 56, chart_y + 1), label, font=SANS_B(17), fill=INK)
        bx += 46 + 56 + 8 + 150
        d.rectangle([bx, chart_y, bx + length, chart_y + 22], fill=color)
        bx = chart_x
        chart_y += 28
    d.text((chart_x, chart_y + 4),
           "Proposed tariff bite, illustrative: China highest of the 14 partners.",
           font=SANS(15), fill=(110, 100, 85))
    y = chart_y + 34
    d.line([32, y, W - 32, y], fill=RULE, width=2)
    y += 14

    # Two-by-two story grid
    grid_top = y
    box_w, box_h = 468, 200
    gap = 20
    stories = [
        ("MERCURY", NAVY,
         "Europe and Japan reach Mercury after eight years",
         "The joint BepiColombo mission arrives at the Solar System's "
         "smallest planet, ending a long cruise from Earth."),
        ("SPACE", TEAL,
         "First Pakistani astronaut rides to Tiangong",
         "Muhammad Zeeshan Ali joins China's Shenzhou-24 crew, the first "
         "foreign astronaut aboard the Tiangong station."),
        ("MIGRATION", GOLD,
         "Record day as boats reach the Canaries",
         "Nearly 2,000 migrants arrive in Spain's Canary Islands in a "
         "single day, the largest one-day landing on record."),
        ("WAGES", RED,
         "Bangladesh garment workers win 36% pay rise",
         "The minimum monthly wage for entry-level garment workers jumps "
         "by more than a third after months of pressure."),
    ]
    for i, (kicker, color, head, body) in enumerate(stories):
        bx = 32 + (i % 2) * (box_w + gap)
        by = grid_top + (i // 2) * (box_h + gap)
        story_box(d, bx, by, box_w, box_h, kicker, color, head, body)

    # Bottom strip: also in the news
    strip_y = grid_top + 2 * box_h + gap + 12
    d.rectangle([0, strip_y, W, strip_y + 56], fill=(235, 228, 210))
    d.text((32, strip_y + 6), "ALSO IN THE NEWS",
           font=SANS_B(18), fill=RED)
    d.text((32, strip_y + 30),
           "N. Korea orders Switzerland to shut its Pyongyang office  ·  "
           "Ukraine says it hit a Russian air base",
           font=SANS(18), fill=INK)
    d.text((32, H - 28),
           "Drawn by an AI agent  ·  All stories first reported on "
           "Thursday 26 November 2026",
           font=SANS(15), fill=(110, 100, 85))

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
