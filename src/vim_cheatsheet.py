import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_common import *

LEFT = [
    ("Modes", [
        ("i / a",          "Insert before / after cursor"),
        ("o / O",          "New line below / above + insert"),
        ("I / A",          "Insert at line start / end"),
        ("R",              "Replace mode — overwrite characters"),
        ("Esc",            "Return to Normal mode (always works)"),
        ("v / V",          "Visual: character / line select"),
        ("Ctrl+v",         "Visual block — column select"),
    ]),
    ("Navigate — cursor", [
        ("h  j  k  l",     "Left  Down  Up  Right"),
        ("[n]j / [n]k",    "Move n lines down / up"),
        ("w / b / e",      "Next word / prev word / word end"),
        ("W / B / E",      "Same — ignores punctuation"),
        ("0  ^  $",        "Line start / first non-blank / end"),
        ("gg / G / [n]G",  "File top / bottom / line n"),
        ("{ / }",          "Prev / next blank line"),
        ("%",              "Jump to matching bracket / paren"),
    ]),
    ("Navigate — line  ( f / t )", [
        ("f{c} / F{c}",    "Jump to char c forward / backward"),
        ("t{c} / T{c}",    "Jump till char c forward / backward"),
        ("; / ,",          "Repeat last f/t forward / backward"),
        ("dt{c} / ct{c}",  "Delete / change up to char c"),
        ("df{c} / cf{c}",  "Delete / change through char c"),
    ]),
    ("Navigate — screen & jumps", [
        ("Ctrl+d / Ctrl+u","Half page down / up"),
        ("Ctrl+f / Ctrl+b","Full page down / up"),
        ("zz / zt / zb",   "Center / top / bottom cursor on screen"),
        ("Ctrl+o / Ctrl+i","Jump back / forward in jump list"),
        ("gj / gk",        "Move by visual line (wrapped text)"),
    ]),
    ("Undo, repeat & numbers", [
        ("u / Ctrl+r",     "Undo / redo"),
        (".",              "Repeat last change"),
        ("J",              "Join line below onto current line"),
        ("Ctrl+a / Ctrl+x","Increment / decrement number at cursor"),
    ]),
]

RIGHT = [
    ("Delete & change", [
        ("[n]dd",          "Delete n lines (default 1)"),
        ("D / dw / d$",    "Delete to end / word / end of line"),
        ("x / X",          "Delete char under / before cursor"),
        ("cc / C",         "Change whole line / to end of line"),
        ("cw / cb",        "Change word forward / backward"),
        ("s / S",          "Delete char+insert / line+insert"),
        ("u (Visual)",     "Lowercase selection"),
        ("U (Visual)",     "Uppercase selection"),
    ]),
    ("Copy, paste & indent", [
        ("[n]yy / yw / y$","Yank n lines / word / to end of line"),
        ("p / P",          "Paste after / before cursor"),
        ("\"*y / \"*p",    "Yank to / paste from system clipboard"),
        (">> / <<",        "Indent / dedent line"),
        ("gg=G",           "Auto-indent entire file"),
        ("~ (Normal)",     "Toggle case of char under cursor"),
        ("~ (Visual)",     "Toggle case of entire selection"),
    ]),
    ("Text objects  (use with d, c, y, v)", [
        ("iw / aw",        "Inner word / around word (+ space)"),
        ("i\" / a\"",      "Inside / around double quotes"),
        ("i( / a(",        "Inside / around parentheses"),
        ("i{ / a{",        "Inside / around curly braces"),
        ("it / at",        "Inside / around HTML/XML tag"),
    ]),
    ("Search & replace", [
        ("/pat  /  ?pat",  "Search forward / backward"),
        ("n / N",          "Next / previous match"),
        ("* / #",          "Search word under cursor fwd / bwd"),
        (":s/old/new/g",   "Replace all on current line"),
        (":%s/old/new/g",  "Replace all in file"),
        (":%s/old/new/gc", "Replace all — confirm each"),
        (":g/pat/d",       "Delete all lines matching pattern"),
    ]),
    ("Files, buffers & windows", [
        (":w / :wq / ZZ",  "Save / save+quit / save+quit"),
        (":q! / :qa!",     "Force quit / quit all without saving"),
        (":e file / :ls",  "Open file / list buffers"),
        (":bn / :bp / :bd","Next / prev / close buffer"),
        (":sp / :vsp",     "Split horizontal / vertical"),
        ("Ctrl+w hjkl",    "Move between windows"),
        (":tabnew / gt",   "New tab / next tab"),
    ]),
    ("Macros, marks & settings", [
        ("qa...q / @a",    "Record macro into a / play macro a"),
        ("{n}@a / @@",     "Play n times / repeat last macro"),
        ("ma / `a / 'a",   "Set mark / jump exact / jump to line"),
        (":set nu / rnu",  "Line numbers / relative numbers"),
        (":set paste",     "Paste mode — disables auto-indent"),
        (":!{cmd}",        "Run a shell command from vim"),
        ("gd",             "Go to local definition under cursor"),
    ]),
]

def render():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vim_cheatsheet.pdf")
    cv = canvas.Canvas(out, pagesize=A4)

    # Page bg
    cv.setFillColor(C_BG)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    draw_header(cv,
        title_bold  = "Vim",
        title_light = "Cheat Sheet",
        subtitle    = "Normal · Insert · Visual · Command — essential commands for developers",
        note_text   = "[n] prefix repeats most commands  ·  e.g.  5j   3dd   2w   10G",
        version_tag = "vim 8+ / neovim",
    )

    draw_col_cards(cv, "MOTION & MODES", "EDITING & COMMANDS")

    # Left column
    cy = TOP_Y - 11
    for (title, rows) in LEFT:
        cy -= 1
        cy = section_header(cv, COL_L + 3, cy, COL_W - 6, title, C_ACCENT_L)
        for i, (k, d) in enumerate(rows):
            cy = draw_row(cv, COL_L + 3, cy, COL_W - 6, k, d, i % 2 == 1)
        cy -= SEC_GAP

    # Right column
    cy = TOP_Y - 11
    for (title, rows) in RIGHT:
        cy -= 1
        cy = section_header(cv, COL_R + 3, cy, COL_W - 6, title, C_ACCENT_R)
        for i, (k, d) in enumerate(rows):
            cy = draw_row(cv, COL_R + 3, cy, COL_W - 6, k, d, i % 2 == 1)
        cy -= SEC_GAP

    draw_footer(cv,
        left_text  = "ESC always returns to Normal mode  ·  :help <topic> for built-in docs  ·  :h quickref",
        right_text = "vim 8+ / neovim  ·  v2",
        version    = "v2",
    )

    cv.save()
    print("Done:", out)

render()
