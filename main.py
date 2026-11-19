"""The World Today - Thursday, 19 November 2026.

Draws a 1024x1024 newspaper front page that sums up the world news of
Thursday 19 November 2026 and writes it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR when that is set). Python standard library only,
no network, fully deterministic: two runs write byte-identical bytes.
"""

import os
import struct
import sys
import zlib

# The grader runs `python3 -P -s /bot/main.py`; -P drops this script's
# directory from sys.path, so put it back before importing fontdata.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fontdata import GLYPHS

W = 1024
H = 1024

PAPER = (246, 241, 226)
INK = (24, 24, 28)
RED = (168, 32, 32)
BLUE = (28, 62, 124)
GREY = (112, 105, 92)
WHITE = (250, 250, 248)
CHINA_RED = (206, 32, 40)
GOLD = (240, 190, 40)
RU_BLUE = (30, 70, 160)
RU_RED = (200, 40, 45)


def new_canvas():
    return bytearray(bytes(PAPER) * (W * H))


def set_px(buf, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = color[0]
        buf[i + 1] = color[1]
        buf[i + 2] = color[2]


def rect(buf, x, y, w, h, color):
    for yy in range(y, y + h):
        if 0 <= yy < H:
            base = (yy * W) * 3
            for xx in range(x, x + w):
                if 0 <= xx < W:
                    i = base + xx * 3
                    buf[i] = color[0]
                    buf[i + 1] = color[1]
                    buf[i + 2] = color[2]


def text_width(text, scale):
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def draw_text(buf, text, x, y, scale, color):
    cx = x
    for ch in text.upper():
        glyph = GLYPHS.get(ch, GLYPHS[" "])
        for row_i, row in enumerate(glyph):
            for col_i, cell in enumerate(row):
                if cell == "#":
                    rect(buf, cx + col_i * scale, y + row_i * scale,
                         scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_center(buf, text, cx, y, scale, color):
    x = cx - text_width(text, scale) // 2
    return draw_text(buf, text, x, y, scale, color)


def wrap(text, max_chars):
    lines = []
    cur = ""
    for word in text.split():
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur = cur + " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(buf, text, x, y, scale, color, max_chars, pitch,
               center_cx=None):
    """Draw word-wrapped text; return the y just below the last line."""
    for line in wrap(text, max_chars):
        if center_cx is None:
            draw_text(buf, line, x, y, scale, color)
        else:
            draw_text_center(buf, line, center_cx, y, scale, color)
        y += pitch
    return y


def draw_flag_us(buf, x, y, w, h):
    stripe = h // 7
    for i in range(7):
        color = RED if i % 2 == 0 else WHITE
        rect(buf, x, y + i * stripe, w, stripe if i < 6 else h - 6 * stripe,
             color)
    canton_w = int(w * 0.44)
    canton_h = stripe * 4
    rect(buf, x, y, canton_w, canton_h, BLUE)
    for r in range(3):
        for c in range(4):
            rect(buf, x + 6 + c * 12, y + 5 + r * 8, 4, 4, WHITE)


def draw_flag_china(buf, x, y, w, h):
    rect(buf, x, y, w, h, CHINA_RED)
    rect(buf, x + 10, y + 8, 10, 10, GOLD)
    for dx, dy in ((26, 4), (30, 12), (30, 21), (26, 29)):
        rect(buf, x + dx, y + dy, 5, 5, GOLD)


def draw_flag_russia(buf, x, y, w, h):
    band = h // 3
    rect(buf, x, y, w, band, WHITE)
    rect(buf, x, y + band, w, band, RU_BLUE)
    rect(buf, x, y + 2 * band, w, h - 2 * band, RU_RED)


def draw_flags(buf, y):
    fw, fh, gap = 132, 48, 24
    total = 3 * fw + 2 * gap
    x = (W - total) // 2
    for draw in (draw_flag_us, draw_flag_china, draw_flag_russia):
        draw(buf, x, y, fw, fh)
        rect(buf, x, y, fw, 1, INK)
        rect(buf, x, y + fh - 1, fw, 1, INK)
        rect(buf, x, y, 1, fh, INK)
        rect(buf, x + fw - 1, y, 1, fh, INK)
        x += fw + gap


LEAD_KICKER = "APEC SUMMIT - SHENZHEN, CHINA"
LEAD_HEADLINE = ("TRUMP, XI AND PUTIN", "HOLD FIRST THREE-WAY",
                 "SUMMIT IN SHENZHEN")
LEAD_SUMMARY = (
    "THE U.S., CHINESE AND RUSSIAN PRESIDENTS MET AT THE APEC SUMMIT "
    "- THE FIRST TRILATERAL OF THE THREE NUCLEAR POWERS. NUCLEAR "
    "ARMS AND THE IRAN WAR TOPPED THE AGENDA."
)

STORIES = (
    ("UKRAINE HITS CRIMEAN BRIDGE A THIRD TIME",
     "KYIV STRUCK THE KERCH BRIDGE FOR THE THIRD TIME IN A WEEK. "
     "TRAFFIC WAS HALTED WHILE DAMAGE WAS ASSESSED."),
    ("U.S. AND IRAN TRADE FIRE AGAIN",
     "IRAN WIDENED ITS ATTACKS ON GULF STATES AFTER U.S. JETS "
     "STRUCK A MISSILE SITE ON QESHM ISLAND."),
    ("ISRAEL PUSHES INTO CENTRAL GAZA",
     "ISRAELI FORCES CROSSED THE YELLOW LINE IN THE FIRST BIG "
     "GROUND OFFENSIVE SINCE THE 2025 TRUCE."),
    ("N. KOREA EXPANDS URANIUM ENRICHMENT",
     "THE U.N. NUCLEAR WATCHDOG SAYS PYONGYANG EXPANDED ENRICHMENT "
     "AT ITS YONGBYON COMPLEX."),
    ("WORLD COURT TO RULE ON MYANMAR CASE",
     "THE U.N.'S TOP COURT NEARS JUDGMENT IN THE ROHINGYA GENOCIDE "
     "CASE BROUGHT AGAINST MYANMAR."),
    ("JEFFRIES SET AS FIRST BLACK SPEAKER",
     "DEMOCRATS NOMINATED HAKEEM JEFFRIES, SET TO BE THE FIRST "
     "AFRICAN-AMERICAN SPEAKER OF THE HOUSE."),
)

BRIEFS = (
    "IN BRIEF - VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
    "EU OKAYS INDONESIA TRADE PACT - FED MINUTES POINT TO MORE HIKES",
)


def draw_front_page():
    buf = new_canvas()
    # Double-rule border.
    rect(buf, 10, 10, W - 20, 2, INK)
    rect(buf, 10, H - 12, W - 20, 2, INK)
    rect(buf, 10, 10, 2, H - 20, INK)
    rect(buf, W - 12, 10, 2, H - 20, INK)
    rect(buf, 17, 17, W - 34, 1, INK)
    rect(buf, 17, H - 18, W - 34, 1, INK)
    rect(buf, 17, 17, 1, H - 34, INK)
    rect(buf, W - 18, 17, 1, H - 34, INK)

    # Masthead and date bar.
    draw_text_center(buf, "THE WORLD TODAY", W // 2, 32, 9, INK)
    rect(buf, 44, 108, W - 88, 3, INK)
    rect(buf, 44, 115, W - 88, 1, INK)
    rect(buf, 44, 124, W - 88, 42, INK)
    draw_text_center(buf, "THURSDAY - NOVEMBER 19 - 2026", W // 2, 131,
                     4, PAPER)

    # Lead story: the first Trump-Xi-Putin trilateral, at APEC.
    draw_text_center(buf, LEAD_KICKER, W // 2, 180, 4, RED)
    y = 220
    for line in LEAD_HEADLINE:
        draw_text_center(buf, line, W // 2, y, 8, INK)
        y += 66
    draw_flags(buf, 424)
    draw_block(buf, LEAD_SUMMARY, 0, 488, 3, INK, 52, 27,
               center_cx=W // 2)
    rect(buf, 44, 604, W - 88, 2, INK)

    # Six stories in two columns of three.
    rect(buf, 511, 612, 1, 320, GREY)
    rect(buf, 44, 716, W - 88, 1, GREY)
    rect(buf, 44, 826, W - 88, 1, GREY)
    col_x = (44, 532)
    row_y = (612, 722, 832)
    for i, (headline, body) in enumerate(STORIES):
        x = col_x[i % 2]
        y0 = row_y[i // 2]
        draw_block(buf, headline, x, y0, 3, INK, 24, 25)
        draw_block(buf, body, x, y0 + 52, 2, INK, 36, 17)

    # Briefs strip.
    rect(buf, 44, 950, W - 88, 52, INK)
    draw_text_center(buf, BRIEFS[0], W // 2, 959, 2, PAPER)
    draw_text_center(buf, BRIEFS[1], W // 2, 982, 2, PAPER)
    return buf


def write_png(path, buf):
    raw = bytearray()
    row_len = W * 3
    for yy in range(H):
        raw.append(0)
        raw += buf[yy * row_len:(yy + 1) * row_len]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", comp) + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    buf = draw_front_page()
    write_png(os.path.join(outdir, "entry.png"), buf)


if __name__ == "__main__":
    main()
