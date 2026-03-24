import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_common import *

LEFT = [
    ("Sessions", [
        ("cmd",    "tmux",                       "Start a new unnamed session"),
        ("cmd",    "tmux new -s <name>",         "Start a new named session"),
        ("cmd",    "tmux ls",                    "List all sessions"),
        ("cmd",    "tmux attach -t <name>",      "Attach to a named session"),
        ("cmd",    "tmux kill-session -t <name>","Kill a session by name"),
        ("prefix", "d",                          "Detach from current session"),
        ("prefix", "$",                          "Rename current session"),
        ("prefix", "s",                          "Interactive session list"),
        ("prefix", "(",                          "Switch to previous session"),
        ("prefix", ")",                          "Switch to next session"),
    ]),
    ("Windows  (tabs)", [
        ("prefix", "c",                          "Create new window"),
        ("prefix", ",",                          "Rename current window"),
        ("prefix", "&",                          "Kill current window  (confirm y/n)"),
        ("prefix", "n",                          "Next window"),
        ("prefix", "p",                          "Previous window"),
        ("prefix", "l",                          "Last (most recently used) window"),
        ("prefix", "0-9",                        "Switch to window by number"),
        ("prefix", "w",                          "Interactive window list"),
        ("prefix", "f",                          "Find window by name"),
        ("prefix", ".",                          "Move window to new index"),
    ]),
    ("Config & misc", [
        ("prefix", "?",                          "List all keybindings"),
        ("prefix", ":",                          "Enter command prompt"),
        ("prefix", "t",                          "Show clock"),
        ("prefix", "~",                          "Show messages log"),
        ("prefix", "Ctrl+b",                     "Send prefix to a nested tmux session"),
        ("cmd",    "tmux source ~/.tmux.conf",   "Reload config without restarting"),
        ("config", "set -g mouse on",            "Enable mouse (Shift+click for native select)"),
        ("config", "set -g base-index 1",        "Start window index at 1"),
        ("config", "set -g renumber-windows on", "Keep window numbers contiguous"),
        ("prefix", "I / U",                      "Install / update plugins (TPM)"),
    ]),
]

RIGHT = [
    ("Panes  (splits)", [
        ("prefix", "\"",         "Split horizontally  (top / bottom)"),
        ("prefix", "%",          "Split vertically  (left / right)"),
        ("prefix", "x",          "Kill current pane  (confirm y/n)"),
        ("prefix", "arrow keys", "Move focus between panes"),
        ("prefix", ";",          "Switch to last active pane"),
        ("prefix", "o",          "Cycle through panes in order"),
        ("prefix", "q",          "Show pane numbers briefly"),
        ("prefix", "q 0-9",      "Jump to pane by number"),
        ("prefix", "z",          "Toggle pane zoom (fullscreen)"),
        ("prefix", "{",          "Rotate current pane position backward"),
        ("prefix", "}",          "Rotate current pane position forward"),
        ("prefix", "Space",      "Cycle through preset pane layouts"),
        ("prefix", "!",          "Break pane out into its own window"),
        ("prefix", "Ctrl+arrow", "Resize pane by 1 cell"),
        ("prefix", "Alt+arrow",  "Resize pane by 5 cells"),
    ]),
    ("Copy mode  (vi keys — requires  set -g mode-keys vi)", [
        ("prefix", "[",          "Enter copy / scroll mode"),
        ("config", "q  or  Esc", "Exit copy mode"),
        ("config", "hjkl",       "Navigate  (arrow keys also work)"),
        ("config", "Ctrl+d / u", "Scroll half page down / up"),
        ("config", "Space",      "Begin text selection"),
        ("config", "Enter",      "Copy selection to tmux buffer"),
        ("prefix", "]",          "Paste most recent buffer"),
        ("prefix", "=",          "Choose from all paste buffers"),
        ("config", "/ or ?",     "Search forward / backward"),
        ("config", "n / N",      "Next / previous search match"),
    ]),
]

def draw_tmux_row(cv, x, y, w, key_type, key, desc, shade):
    """tmux rows have prefix/cmd/config badge types."""
    row_by = y - ROW_H
    if shade:
        rr(cv, x, row_by, w, ROW_H, 0, C_ROW_ALT)
    yc = y - ROW_H / 2

    if key_type == "prefix":
        rx = x + COL_PAD
        rx = key_badge(cv, rx, yc, "prefix",
                       bg=C_PREFIX_BG, fg=C_PREFIX_FG, border=C_PREFIX_BR)
        rx += 3
        rx = key_badge(cv, rx, yc, key)
    elif key_type == "cmd":
        rx = x + COL_PAD
        rx = key_badge(cv, rx, yc, key,
                       bg=C_CMD_BG, fg=C_CMD_FG, border=C_CMD_BORDER)
    else:
        rx = x + COL_PAD
        rx = key_badge(cv, rx, yc, key)

    cv.setFillColor(C_MUTED)
    cv.circle(rx + 4, yc, 1, fill=1, stroke=0)

    desc_x   = rx + 10
    desc_max = w - (desc_x - x) - COL_PAD
    cv.setFont("Helvetica", DESC_FONT_SZ)
    d = desc
    while cv.stringWidth(d, "Helvetica", DESC_FONT_SZ) > desc_max and len(d) > 3:
        d = d[:-1]
    cv.setFillColor(C_DESC if not shade else C_DESC_ALT)
    cv.drawString(desc_x, yc - DESC_FONT_SZ / 2 + 1, d)
    return row_by

def render():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tmux_cheatsheet.pdf")
    cv = canvas.Canvas(out, pagesize=A4)

    cv.setFillColor(C_BG)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    draw_header(cv,
        title_bold  = "tmux",
        title_light = "Cheat Sheet",
        subtitle    = "Terminal multiplexer · Sessions · Windows · Panes · Copy mode",
        note_text   = "Default prefix:  Ctrl + b   — press prefix FIRST, then the key shown",
        version_tag = "tmux 3.x",
    )

    # Badge legend — drawn inside column area, below column label, before rows
    # Right-aligned in right column header area
    legend = [
        ("prefix key", C_PREFIX_BG, C_PREFIX_FG, C_PREFIX_BR),
        ("$ command",  C_CMD_BG,    C_CMD_FG,    C_CMD_BORDER),
        ("copy/config",C_KEY_BG,    C_KEY_FG,    C_KEY_BORDER),
    ]

    draw_col_cards(cv, "SESSIONS · WINDOWS · CONFIG", "PANES · COPY MODE")

    # Draw legend inside right column header row (right-aligned)
    lx = COL_R + COL_W - 6
    ly = TOP_Y - 14
    for label, bg, fg, br in reversed(legend):
        cv.setFont("Courier-Bold", KEY_FONT_SZ)
        lw = cv.stringWidth(label, "Courier-Bold", KEY_FONT_SZ) + KEY_PAD_X * 2
        lx -= lw + 3
        rr(cv, lx, ly - KEY_H, lw, KEY_H, 2.5, bg, br, 0.35)
        cv.setFillColor(fg)
        cv.drawString(lx + KEY_PAD_X,
                      ly - KEY_H + KEY_PAD_Y + 0.6, label)

    # Left column
    cy = TOP_Y - 11
    for (title, rows) in LEFT:
        cy -= 1
        cy = section_header(cv, COL_L + 3, cy, COL_W - 6, title, C_ACCENT_L)
        for i, (kt, k, d) in enumerate(rows):
            cy = draw_tmux_row(cv, COL_L + 3, cy, COL_W - 6, kt, k, d, i % 2 == 1)
        cy -= SEC_GAP

    # Right column (shifted down to clear badge legend)
    cy = TOP_Y - 22
    for (title, rows) in RIGHT:
        cy -= 1
        cy = section_header(cv, COL_R + 3, cy, COL_W - 6, title, C_ACCENT_R)
        for i, (kt, k, d) in enumerate(rows):
            cy = draw_tmux_row(cv, COL_R + 3, cy, COL_W - 6, kt, k, d, i % 2 == 1)
        cy -= SEC_GAP

    # Tips box
    tips = [
        ("Mouse mode: ",   "Shift+click for native terminal text selection when mouse is on"),
        ("Nested tmux: ",  "prefix Ctrl+b sends prefix through to an inner tmux session"),
        ("Vi copy mode: ", "Add  set -g mode-keys vi  to ~/.tmux.conf  (emacs is default)"),
    ]
    tip_box(cv, COL_R + 3, cy - 3, COL_W - 6, tips, C_ACCENT_R)

    draw_footer(cv,
        left_text  = "Ctrl+b is the default prefix  ·  tmux list-keys for full list  ·  man tmux",
        right_text = "tmux 3.x  ·  v2",
        version    = "v2",
    )

    cv.save()
    print("Done:", out)

render()
