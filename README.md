# Cheatsheets

Dark-themed, single-page A4 cheat sheets generated with Python + ReportLab.

## Files

| File | Purpose |
|---|---|
| `src/sheet_common.py` | Shared drawing primitives, palette, layout constants |
| `src/vim_cheatsheet.py` | Vim cheat sheet content + render call |
| `src/tmux_cheatsheet.py` | tmux cheat sheet content + render call |

## Usage

```bash
# Build all cheatsheets
./build.sh

# Build specific ones
./build.sh tmux
./build.sh tmux vim
```

Requires Docker. The build script creates a lightweight image with `reportlab` and outputs PDFs to the repo root.

## Adding a new cheatsheet

1. Copy `src/vim_cheatsheet.py` as a starting point
2. Replace `LEFT` and `RIGHT` content lists
3. Call `draw_header()`, `draw_col_cards()`, `draw_footer()` from `src/sheet_common.py`
4. Content rows are plain tuples: `("key", "description")`
5. For tmux-style multi-badge rows, use the `draw_tmux_row()` pattern with `key_type` in `("prefix", "cmd", "config")`

## Layout system

- A4 single page, two-column grid
- Header: 26mm — three rows (title, subtitle, note pill) with verified non-overlapping positions
- Column cards: rounded rect containers from below header to above footer
- Sections: header bar with accent left bar + rows with alternating shade
- Footer: 7mm dark bar matching header style
- All constants in `sheet_common.py` — change `ROW_H`, `SEC_H`, `HEADER_H` etc. there

## Palette

Purple `#7c6af7` — left column accent
Sky blue `#38bdf8` — right column accent
Background `#0d0f18`, column card `#13161f`, section bg `#191c2a`
Key badge `#21243a` / `#ddd8ff`, prefix badge `#1e1a3a` / `#c4b5fd`
