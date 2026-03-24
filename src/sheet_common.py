"""
Shared drawing primitives for the cheatsheet series.
Both vim and tmux sheets import from here for consistent style.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

W, H = A4

# ── Palette ───────────────────────────────────────────────────────────────────
C_BG         = colors.HexColor("#0d0f18")
C_COL_BG     = colors.HexColor("#13161f")
C_COL_BORDER = colors.HexColor("#1e2133")
C_SECTION    = colors.HexColor("#191c2a")
C_ACCENT_L   = colors.HexColor("#7c6af7")   # purple
C_ACCENT_R   = colors.HexColor("#38bdf8")   # sky blue
C_KEY_BG     = colors.HexColor("#21243a")
C_KEY_FG     = colors.HexColor("#ddd8ff")
C_KEY_BORDER = colors.HexColor("#3a3d5c")
C_CMD_BG     = colors.HexColor("#0f2030")
C_CMD_FG     = colors.HexColor("#7dd3fc")
C_CMD_BORDER = colors.HexColor("#1e4060")
C_PREFIX_BG  = colors.HexColor("#1e1a3a")
C_PREFIX_FG  = colors.HexColor("#c4b5fd")
C_PREFIX_BR  = colors.HexColor("#3d3170")
C_DESC       = colors.HexColor("#9b98b8")
C_DESC_ALT   = colors.HexColor("#7a7898")
C_WHITE      = colors.white
C_MUTED      = colors.HexColor("#3d3c56")
C_ROW_ALT    = colors.HexColor("#161824")
C_FOOTER_FG  = colors.HexColor("#2e2c48")
C_HEAD_BG    = colors.HexColor("#0a0c14")
C_TIP_BG     = colors.HexColor("#191c2a")
C_TIP_FG     = colors.HexColor("#52506e")
C_NOTE_BG    = colors.HexColor("#16192a")

# ── Layout constants ──────────────────────────────────────────────────────────
M            = 8 * mm
GAP          = 3.5 * mm
COL_W        = (W - 2*M - GAP) / 2
COL_L        = M
COL_R        = M + COL_W + GAP
HEADER_H     = 26 * mm          # taller — 3 clean rows, no overlap
FOOTER_H     = 7 * mm
TOP_Y        = H - HEADER_H - 3*mm
BOT_Y        = FOOTER_H + 2*mm

ROW_H        = 13.5
SEC_H        = 16
SEC_GAP      = 5
COL_PAD      = 5
KEY_FONT_SZ  = 7.0
KEY_H        = 10.5
KEY_PAD_X    = 4.5
KEY_PAD_Y    = 1.5
DESC_FONT_SZ = 7.2

# ── Primitives ────────────────────────────────────────────────────────────────
def rr(c, x, y, w, h, r, fill, stroke=None, sw=0.4):
    c.saveState()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
        c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    c.restoreState()

def key_badge(c, x, y_center, text,
              bg=None, fg=None, border=None):
    bg     = bg     or C_KEY_BG
    fg     = fg     or C_KEY_FG
    border = border or C_KEY_BORDER
    c.saveState()
    c.setFont("Courier-Bold", KEY_FONT_SZ)
    tw = c.stringWidth(text, "Courier-Bold", KEY_FONT_SZ)
    bw = tw + KEY_PAD_X * 2
    by = y_center - KEY_H / 2
    rr(c, x, by, bw, KEY_H, 2.5, bg, border, 0.35)
    c.setFillColor(fg)
    c.drawString(x + KEY_PAD_X, by + KEY_PAD_Y + 0.6, text)
    c.restoreState()
    return x + bw   # right edge

def section_header(c, x, y, w, title, accent):
    """Returns bottom-y of header bar."""
    by = y - SEC_H
    rr(c, x, by, w, SEC_H, 3, C_SECTION)
    c.setFillColor(accent)
    c.roundRect(x, by, 3, SEC_H, 1.5, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 9, by + 5, title.upper())
    return by

def draw_row(c, x, y, w, key, desc, shade,
             key_bg=None, key_fg=None, key_br=None):
    """Generic single-badge row. Returns bottom-y."""
    row_by = y - ROW_H
    if shade:
        rr(c, x, row_by, w, ROW_H, 0, C_ROW_ALT)
    yc = y - ROW_H / 2
    rx = key_badge(c, x + COL_PAD, yc, key,
                   bg=key_bg, fg=key_fg, border=key_br)
    c.setFillColor(C_MUTED)
    c.circle(rx + 4, yc, 1, fill=1, stroke=0)
    desc_x = rx + 10
    desc_max = w - (desc_x - x) - COL_PAD
    c.setFont("Helvetica", DESC_FONT_SZ)
    d = desc
    while c.stringWidth(d, "Helvetica", DESC_FONT_SZ) > desc_max and len(d) > 3:
        d = d[:-1]
    c.setFillColor(C_DESC if not shade else C_DESC_ALT)
    c.drawString(desc_x, yc - DESC_FONT_SZ / 2 + 1, d)
    return row_by

def draw_header(c, title_bold, title_light, subtitle, note_text, version_tag):
    """
    Draw the page header with three clean non-overlapping rows:
      Row 1: bold title  +  version tag (right-aligned)
      Row 2: subtitle (muted)
      Row 3: note pill (centered, accent colour)
    """
    # Background
    c.setFillColor(C_HEAD_BG)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    # Split accent border at bottom
    c.setFillColor(C_ACCENT_L)
    c.rect(0, H - HEADER_H, W / 2, 1.5, fill=1, stroke=0)
    c.setFillColor(C_ACCENT_R)
    c.rect(W / 2, H - HEADER_H, W / 2, 1.5, fill=1, stroke=0)

    # ── Row 1: title left, version tag right ──────────────────────────────────
    row1_y = H - HEADER_H + (HEADER_H * 0.72)   # 72 % up from bottom
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(M, row1_y, title_bold)
    tw = c.stringWidth(title_bold, "Helvetica-Bold", 19)
    c.setFillColor(colors.HexColor("#3d3a62"))
    c.setFont("Helvetica", 19)
    c.drawString(M + tw + 3, row1_y, title_light)

    # Version tag — right-aligned, same row
    vtw = c.stringWidth(version_tag, "Helvetica-Bold", 6.5) + 12
    vx  = W - M - vtw
    vy  = row1_y - 1
    rr(c, vx, vy, vtw, 12, 3, C_SECTION)
    c.setFillColor(C_ACCENT_L)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(vx + vtw / 2, vy + 3.5, version_tag)

    # ── Row 2: subtitle ───────────────────────────────────────────────────────
    row2_y = H - HEADER_H + (HEADER_H * 0.44)
    c.setFillColor(C_TIP_FG)
    c.setFont("Helvetica", 7)
    c.drawString(M, row2_y, subtitle)

    # ── Row 3: centered note pill ─────────────────────────────────────────────
    row3_y = H - HEADER_H + (HEADER_H * 0.18)
    c.setFont("Helvetica-Bold", 6.8)
    nw = c.stringWidth(note_text, "Helvetica-Bold", 6.8)
    pill_w = nw + 16
    pill_x = (W - pill_w) / 2
    pill_h = 12
    rr(c, pill_x, row3_y - 2, pill_w, pill_h, 3, C_NOTE_BG)
    c.setFillColor(C_ACCENT_L)
    c.drawCentredString(W / 2, row3_y + 2.5, note_text)

def draw_footer(c, left_text, right_text, version):
    c.setFillColor(C_HEAD_BG)
    c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    c.setFillColor(C_ACCENT_L)
    c.rect(0, FOOTER_H, W / 2, 0.8, fill=1, stroke=0)
    c.setFillColor(C_ACCENT_R)
    c.rect(W / 2, FOOTER_H, W / 2, 0.8, fill=1, stroke=0)
    c.setFillColor(C_FOOTER_FG)
    c.setFont("Helvetica", 6.2)
    c.drawString(M, 2.5*mm, left_text)
    c.drawRightString(W - M, 2.5*mm, right_text)

def draw_col_cards(c, left_label, right_label):
    rr(c, COL_L, BOT_Y, COL_W, TOP_Y - BOT_Y, 4, C_COL_BG, C_COL_BORDER, 0.5)
    rr(c, COL_R, BOT_Y, COL_W, TOP_Y - BOT_Y, 4, C_COL_BG, C_COL_BORDER, 0.5)
    for cx, label, acc in [(COL_L, left_label,  C_ACCENT_L),
                            (COL_R, right_label, C_ACCENT_R)]:
        c.setFillColor(acc)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(cx + COL_PAD + 4, TOP_Y - 6, label)

def tip_box(c, x, y, w, lines, accent):
    """Multi-line tip/note box. Each line: (bold_prefix, rest_text). Returns bottom y."""
    line_h = 11
    pad_v  = 5
    h = pad_v + len(lines) * line_h + 2
    rr(c, x, y - h, w, h, 3, C_TIP_BG)
    c.setFillColor(accent)
    c.roundRect(x, y - h, 3, h, 1.5, fill=1, stroke=0)
    for i, (bold_part, rest) in enumerate(lines):
        ly = y - pad_v - (i + 0.75) * line_h
        if bold_part:
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 6.3)
            c.drawString(x + 9, ly, bold_part)
            bw = c.stringWidth(bold_part, "Helvetica-Bold", 6.3)
            c.setFillColor(C_TIP_FG)
            c.setFont("Helvetica", 6.3)
            c.drawString(x + 9 + bw + 2, ly, rest)
        else:
            c.setFillColor(C_TIP_FG)
            c.setFont("Helvetica", 6.3)
            c.drawString(x + 9, ly, rest)
    return y - h
