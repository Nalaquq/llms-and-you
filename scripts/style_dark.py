"""Shared style for the lecture-deck slide GIFs.

Dark theme matched to the course site's Material slate palette, with the
site's own accent tokens (--course-virtual #a48fff, --course-due #ff922b)
plus 3blue1brown-style blue/yellow for vectors. Animation idiom follows the
cv_course scripts: phase-based builds, PIL-assembled GIFs, loop=1, long
last-frame hold — but with eased motion tweens for the 3b1b feel.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image

# ── Palette (site-matched) ───────────────────────────────────────────
BG = "#1b1e26"  # slate background, a touch deeper than the site's #21222c
PANEL = "#262a36"  # info-panel fill
PANEL_EDGE = "#3a3f4e"
TEXT = "#e8eaf0"  # near the site's rgba(255,255,255,.87)
SUB = "#9aa0b0"  # secondary text
FAINT = "#565c6b"
BLUE = "#58c4dd"  # 3b1b blue — vector colour 1
YELLOW = "#ffd35a"  # 3b1b yellow — highlights
ORANGE = "#ff922b"  # site --course-due
RED = "#ff6e6e"  # soft red for negatives / failures
GREEN = "#7cd992"  # positives / results
PURPLE = "#a48fff"  # site --course-virtual
GRID = "#333845"

FIG_SIZE = (16, 9)
DPI = 100  # 1600x900 px — keeps 20-slide GIF decks projector-crisp but light

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "figure.facecolor": BG,
        "text.color": TEXT,
        "mathtext.fontset": "dejavusans",
    }
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "demo_photos")
os.makedirs(OUT_DIR, exist_ok=True)


# ── Easing / interpolation ───────────────────────────────────────────
def ease(t):
    """Smooth in-out (the 3b1b default feel)."""
    return t * t * (3.0 - 2.0 * t)


def lerp(a, b, t):
    return a + (b - a) * ease(t)


# ── Figure & frame plumbing ──────────────────────────────────────────
def new_fig():
    fig = plt.figure(figsize=FIG_SIZE, dpi=DPI)
    fig.patch.set_facecolor(BG)
    return fig


def title_block(fig, title, subtitle=None, kicker=None):
    """Title top-left, 3b1b style: understated, generous margin."""
    if kicker:
        fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
        ty = 0.905
    else:
        ty = 0.935
    fig.text(0.045, ty, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    if subtitle:
        fig.text(0.045, ty - 0.055, subtitle, fontsize=15.5, color=SUB, va="top")


def footer(fig, text):
    fig.text(0.045, 0.035, text, fontsize=11.5, color=FAINT, va="bottom")


# ── Layout check (opt-in: SLIDE_QC=1) ────────────────────────────────
# Text that runs off the slide, spills out of the panel it was placed in, or
# lands on other text only shows up once a slide is rendered, and on a
# projector. With SLIDE_QC=1 every frame is measured as it is drawn and the
# problems are printed when the slide is saved, named, once each.
_QC = os.environ.get("SLIDE_QC") == "1"
_QC_ISSUES = {}


def _text_boxes(fig, renderer):
    from matplotlib.text import Text

    out = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip() or t.get_alpha() == 0:
            continue
        out.append((t, t.get_window_extent(renderer)))
    return out


def _check_layout(fig):
    renderer = fig.canvas.get_renderer()
    w, h = fig.canvas.get_width_height()
    boxes = _text_boxes(fig, renderer)
    for t, bb in boxes:
        label = t.get_text().strip().replace("\n", " ")[:50]
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > w + 1 or bb.y1 > h + 1:
            _QC_ISSUES.setdefault(f"off the slide: {label!r}", None)
        box = getattr(t, "_qc_box", None)
        if box is not None:
            pb = box.get_window_extent(renderer)
            if bb.x0 < pb.x0 - 1 or bb.x1 > pb.x1 + 1 or bb.y0 < pb.y0 - 1 or bb.y1 > pb.y1 + 1:
                _QC_ISSUES.setdefault(f"spills out of its box: {label!r}", None)
        ax = t.axes
        if (
            ax is not None
            and getattr(ax, "_qc_region", False)
            and not getattr(ax, "_qc_panel", False)
        ):
            ab = ax.get_window_extent(renderer)
            if bb.x1 > ab.x1 + 6 or bb.y0 < ab.y0 - 6:
                _QC_ISSUES.setdefault(f"runs past its region: {label!r}", None)
        if ax is not None and getattr(ax, "_qc_panel", False):
            ab = ax.get_window_extent(renderer)
            if bb.x1 > ab.x1 + 2 or bb.y0 < ab.y0 - 2 or bb.x0 < ab.x0 - 2 or bb.y1 > ab.y1 + 2:
                _QC_ISSUES.setdefault(f"outside its panel: {label!r}", None)
    # Shapes are clipped to their axes by default, so a box drawn a hair past
    # the edge of its region is silently cut off -- the most common way a
    # slide ends up "cut off" without any text leaving the frame.
    for ax in fig.axes:
        ab = ax.get_window_extent(renderer)
        for patch in ax.patches:
            if not isinstance(patch, (FancyBboxPatch, Rectangle)) or not patch.get_clip_on():
                continue
            if not patch.get_visible() or patch.get_alpha() == 0:
                continue
            pb = patch.get_window_extent(renderer)
            if pb.width < 1 or pb.height < 1:
                continue
            if (
                pb.x0 < ab.x0 - 1.5
                or pb.x1 > ab.x1 + 1.5
                or pb.y0 < ab.y0 - 1.5
                or pb.y1 > ab.y1 + 1.5
            ):
                _QC_ISSUES.setdefault(
                    f"shape clipped by its region at ({pb.x0:.0f},{h - pb.y1:.0f}) px", None
                )
    for i, (t1, b1) in enumerate(boxes):
        for t2, b2 in boxes[i + 1 :]:
            ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
            iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            if ix > 3 and iy > 3:
                small = min(b1.width * b1.height, b2.width * b2.height)
                if ix * iy > 0.15 * small:
                    a = t1.get_text().strip().replace("\n", " ")[:30]
                    b = t2.get_text().strip().replace("\n", " ")[:30]
                    _QC_ISSUES.setdefault(f"overlap: {a!r} / {b!r}", None)


def _report(name):
    if _QC and _QC_ISSUES:
        print(f"LAYOUT {name}:")
        for issue in _QC_ISSUES:
            print(f"    {issue}")
    _QC_ISSUES.clear()


def fig_to_pil(fig, close=True):
    fig.canvas.draw()
    if _QC:
        _check_layout(fig)
    w, h = fig.canvas.get_width_height()
    img = Image.frombytes("RGBA", (w, h), bytes(fig.canvas.buffer_rgba())).convert("RGB")
    if close:
        plt.close(fig)
    return img


def save_gif(frames, durations, name):
    """loop=1, 60s hold on the final frame.

    Also writes ``<name>_final.png`` at full resolution — the slide's fully
    built state. PowerPoint and LibreOffice render a GIF's FIRST frame when
    printing or in the editor, which for a build-up animation is nearly blank;
    the print edition of the deck uses these finals instead. They double as
    the QC previews.
    """
    durations = list(durations)
    durations[-1] = 60_000
    path = os.path.join(OUT_DIR, name)
    frames[0].save(
        path, save_all=True, append_images=frames[1:], duration=durations, loop=1, optimize=True
    )
    frames[-1].save(path.replace(".gif", "_final.png"))
    _report(name)
    print(f"saved {path} ({len(frames)} frames, {os.path.getsize(path) / 1e6:.1f} MB)")


def save_png(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, facecolor=BG)
    if _QC:
        _check_layout(fig)
    _report(name)
    print(f"saved {path}")


# ── Drawing helpers ──────────────────────────────────────────────────
def chip(
    ax,
    x,
    y,
    w,
    h,
    label,
    face=PANEL,
    edge=PANEL_EDGE,
    color=TEXT,
    fontsize=15,
    alpha=1.0,
    lw=1.6,
    mono=False,
    bold=False,
):
    """Rounded token/word box in axes coords."""
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.02",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
        alpha=alpha,
        transform=ax.transAxes,
    )
    # A chip's rounded padding pokes past the point it was placed at; clipping it
    # to its axes shaves the edge off any chip set at x = 0. Never clip a chip.
    box.set_clip_on(False)
    ax.add_patch(box)
    txt = ax.text(
        x + w / 2,
        y + h / 2,
        label,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        alpha=alpha,
        fontfamily="monospace" if mono else "DejaVu Sans",
        fontweight="bold" if bold else "normal",
    )
    txt._qc_box = box  # the label must fit inside its chip


def arrow(ax, p0, p1, color=BLUE, lw=3.0, alpha=1.0, style="-|>", shrink=0.0, mutation=22):
    a = FancyArrowPatch(
        p0,
        p1,
        arrowstyle=style,
        color=color,
        lw=lw,
        alpha=alpha,
        mutation_scale=mutation,
        shrinkA=shrink,
        shrinkB=shrink,
        transform=ax.transData,
    )
    ax.add_patch(a)
    return a


def blank_axes(fig, rect, xlim=(0, 1), ylim=(0, 1)):
    ax = fig.add_axes(rect)
    ax._qc_region = True
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.set_facecolor(BG)
    return ax


def plane(fig, rect, xlim=(-1, 9), ylim=(-1, 7), grid=True):
    """A quiet dark coordinate plane."""
    ax = fig.add_axes(rect)
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if grid:
        ax.set_xticks(np.arange(np.ceil(xlim[0]), xlim[1] + 1))
        ax.set_yticks(np.arange(np.ceil(ylim[0]), ylim[1] + 1))
        ax.grid(True, color=GRID, lw=0.7, alpha=0.55)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    return ax


def hold(frames, durations, fig_render, ms=900, n=1):
    """Append n identical frames."""
    img = fig_render()
    for _ in range(n):
        frames.append(img)
        durations.append(ms)


def tween(frames, durations, render_at, n=16, ms=50):
    """Append an eased motion segment: render_at(t) for t in (0,1]."""
    for i in range(1, n + 1):
        frames.append(render_at(i / n))
        durations.append(ms)


# ── Review-slide furniture (Week 3's compressed recaps) ──────────────
# A review slide is one technique on one slide: a demo of it running, an
# honest pros/cons column, and the formula itself in a band along the
# bottom for the students who want to see the mathematics. The band sits
# ABOVE the study-guide footer, which keeps its meaning everywhere.
def math_strip(fig, exprs, note=None):
    """Formula band across the bottom. `exprs` is one mathtext string or a list.

    Mathtext, never Unicode subscripts -- the cv_course style guide's rule,
    and the only one that survives being projected.
    """
    if isinstance(exprs, str):
        exprs = [exprs]
    top, bottom = (0.158, 0.072) if len(exprs) == 1 else (0.174, 0.058)
    band = FancyBboxPatch(
        (0.045, bottom),
        0.91,
        top - bottom,
        boxstyle="round,pad=0.004,rounding_size=0.012",
        facecolor=PANEL,
        edgecolor=PANEL_EDGE,
        linewidth=1.4,
        transform=fig.transFigure,
        zorder=0,
    )
    fig.add_artist(band)
    fig.text(
        0.062,
        (top + bottom) / 2,
        "MATH",
        fontsize=9.5,
        color=FAINT,
        va="center",
        fontweight="bold",
    )
    step = (top - bottom) / (len(exprs) + 1)
    for i, expr in enumerate(exprs, start=1):
        fig.text(
            0.53,
            top - i * step,
            expr,
            fontsize=17 if len(exprs) == 1 else 13.5,
            color=TEXT,
            ha="center",
            va="center",
        )
    if note:
        fig.text(0.938, (top + bottom) / 2, note, fontsize=11, color=SUB, ha="right", va="center")


def pros_cons(fig, rect, pros, cons, header="the deal"):
    """Left-hand column: what the technique bought, and what it cost."""
    ax = blank_axes(fig, rect)
    box = FancyBboxPatch(
        (0.0, 0.0),
        1.0,
        1.0,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PANEL,
        edgecolor=PANEL_EDGE,
        linewidth=1.6,
        transform=ax.transAxes,
    )
    ax.add_patch(box)
    ax.text(0.06, 0.955, header.upper(), fontsize=10.5, color=FAINT, fontweight="bold", va="top")

    # Spacing adapts to how much was written. A panel that silently overflows
    # its box is the failure mode here, and it only shows up once the slide is
    # rendered -- so the layout is computed rather than tuned per slide.
    items = [*pros, *cons]
    lines = sum(1 + t.count("\n") for t in items)
    unit = min(0.058, 0.80 / (lines + 0.45 * len(items)))

    y = 0.885
    for mark, colour, group in (("+", GREEN, pros), ("−", RED, cons)):
        for text in group:
            ax.text(0.06, y, mark, fontsize=15, color=colour, fontweight="bold", va="top")
            ax.text(
                0.145,
                y + 0.004,
                text,
                fontsize=12.5,
                color=TEXT if mark == "+" else SUB,
                va="top",
                linespacing=1.4,
            )
            y -= unit * (1 + text.count("\n") + 0.45)
        y -= 0.03
    return ax


# ── Attention-grid furniture (Week 3's s15, s16, s22) ────────────────
# The picture is 3Blue1Brown's (Chapter 6, "Attention in transformers"): a
# grid of every word against every word, a dot at each cell whose size is the
# score, then softmax turning the dots into shares. Rows are the asking word
# and columns the words it looks at -- the orientation of every heatmap in
# Thursday's notebook -- so softmax runs along a row, not down a column as it
# does in the video.
def grid_axes(fig, rect, n):
    """Square cells whatever the figure's shape: equal aspect, anchored bottom-left.

    Cell (r, c) is the unit square with corner (c, n - 1 - r), so row 0 is the
    top row and reads like text.
    """
    ax = fig.add_axes(rect)
    ax.set_aspect("equal")
    ax.set_anchor("SW")
    ax.set_xlim(-0.15, n + 0.15)
    ax.set_ylim(-0.15, n + 0.15)
    ax.axis("off")
    ax.set_facecolor(BG)
    return ax


def grid_labels(ax, n, words, row_colours=None, col_colours=None, fontsize=11):
    row_colours = row_colours or {}
    col_colours = col_colours or {}
    for r, w in enumerate(words):
        ax.text(
            -0.35,
            n - 0.5 - r,
            w,
            ha="right",
            va="center",
            fontsize=fontsize,
            color=row_colours.get(r, SUB),
            fontweight="bold" if r in row_colours else "normal",
            clip_on=False,
        )
    for c, w in enumerate(words):
        ax.text(
            c + 0.55,
            n + 0.3,
            w,
            ha="left",
            va="bottom",
            rotation=45,
            rotation_mode="anchor",
            fontsize=fontsize - 1,
            color=col_colours.get(c, SUB),
            fontweight="bold" if c in col_colours else "normal",
            clip_on=False,
        )


def grid_cell(ax, n, r, c, score_norm, weight, t, wmax=1.0, alpha=1.0, dot_colour=SUB, label=None):
    """One cell, part-way (t) between a score-dot and a share-fill.

    Dot radius is the score (the video's convention); fill intensity is the
    share, scaled against `wmax` -- the largest share anywhere on the grid,
    not in the row -- so a row that concentrates its budget on one word reads
    brighter than a row that spreads it.
    """
    x, y = c, n - 1 - r
    ax.add_patch(
        Rectangle(
            (x + 0.04, y + 0.04),
            0.92,
            0.92,
            facecolor=GREEN,
            alpha=alpha * t * (0.08 + 0.92 * min(1.0, weight / wmax)),
            edgecolor=PANEL_EDGE,
            lw=0.7,
        )
    )
    if t < 1.0:
        ax.add_patch(
            Circle(
                (x + 0.5, y + 0.5),
                (0.07 + 0.38 * score_norm) * (1.0 - t),
                facecolor=dot_colour,
                edgecolor="none",
                alpha=alpha * 0.9,
            )
        )
    if label is not None and t > 0.5:
        ax.text(
            x + 0.5,
            y + 0.5,
            label,
            ha="center",
            va="center",
            fontsize=8.5,
            color=(BG if weight > 0.30 else TEXT),
            alpha=alpha * (t - 0.5) * 2,
            fontfamily="monospace",
        )


def grid_outline_row(ax, n, r, colour=YELLOW):
    ax.add_patch(
        Rectangle(
            (-0.02, n - 1 - r - 0.02),
            n + 0.04,
            1.04,
            facecolor="none",
            edgecolor=colour,
            lw=1.8,
        )
    )


def grid_legend(ax, text, y=-0.55):
    ax.text(0.0, y, text, fontsize=10.5, color=FAINT, va="top", clip_on=False)


# ── Paper cards (Week 6: the source first, then the redraw) ─────────
# A crop from an assigned paper, framed so it reads as a thing held up to the
# room rather than a hole punched in the slide. The crop stays true -- white
# page, the authors' colours -- because recognising it from the reading is the
# point; the dark frame and margin are what stop it glaring on a projector.
# Crops come from paper_crops.py, never from a saved screenshot.
def paper_card(fig, rect, img, cite, tag="FROM THE READING"):
    """Draw `img` as large as fits in `rect` (figure coords), framed, with a citation."""
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(img), interpolation="lanczos")
    ax.set_anchor("N")
    ax.axis("off")
    ax.apply_aspect()
    x0, y0, w, h = ax.get_position().bounds
    pad = 0.012
    fig.add_artist(
        FancyBboxPatch(
            (x0 - pad, y0 - pad),
            w + 2 * pad,
            h + 2 * pad,
            boxstyle="round,pad=0.0,rounding_size=0.01",
            facecolor="#f7f7f5",
            edgecolor=PANEL_EDGE,
            linewidth=2.0,
            transform=fig.transFigure,
            zorder=-1,
        )
    )
    fig.text(x0 - pad, y0 + h + pad + 0.012, tag, fontsize=10.5, color=FAINT, fontweight="bold")
    fig.text(x0 - pad, y0 - pad - 0.014, cite, fontsize=12, color=SUB, va="top", style="italic")
    return ax


# ── Week 6 furniture: kicker titles, token lines, equations taken apart ──
def kicker_title(fig, kicker, title, subtitle=None):
    """The purple section kicker, the title, and an optional subtitle."""
    fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    if subtitle:
        fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


def mono_advance(ax, fontsize):
    """One DejaVu Sans Mono character's width, in `ax`'s x units (0..1 axes).

    Token lines are laid out a token at a time so each can take its own colour;
    measuring the advance, rather than guessing a constant per slide, is what
    keeps a coloured line spaced exactly like the plain line above it.
    """
    fig = ax.figure
    width_in = ax.get_position().width * fig.get_figwidth()
    xspan = ax.get_xlim()[1] - ax.get_xlim()[0]
    return 0.6021 * fontsize / 72 / width_in * xspan


def token_line(ax, x, y, tokens, colours, fontsize=17, alpha=1.0, bold=None, sep=1):
    """Monospace tokens on one line, each in its own colour. Returns the end x."""
    step = mono_advance(ax, fontsize)
    bold = bold or ()
    for tok, colour in zip(tokens, colours, strict=True):
        ax.text(
            x,
            y,
            tok,
            fontsize=fontsize,
            color=colour,
            va="center",
            fontfamily="monospace",
            alpha=alpha,
            fontweight="bold" if tok in bold else "normal",
        )
        x += step * (len(tok) + sep)
    return x


def equation(fig, parts, y, fontsize=34, x=None, gap=0.006):
    """Set an equation as separately coloured pieces on one baseline.

    `parts` is a list of (mathtext without $, colour, alpha). The pieces are
    measured first and the whole line centred unless `x` is given, so a slide
    can dim every term but one and still have the equation sit still while the
    highlight moves -- the 3b1b way of reading a formula a term at a time.
    Returns each piece's box in figure coordinates: (x0, y0, x1, y1).
    """
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    widths = []
    for tex, _, _ in parts:
        t = fig.text(0, y, f"${tex}$", fontsize=fontsize, va="baseline")
        bb = t.get_window_extent(renderer=renderer).transformed(inv)
        widths.append(bb.width)
        t.remove()
    if x is None:
        x = 0.5 - (sum(widths) + gap * (len(parts) - 1)) / 2
    boxes = []
    for (tex, colour, alpha), w in zip(parts, widths, strict=True):
        t = fig.text(x, y, f"${tex}$", fontsize=fontsize, color=colour, alpha=alpha, va="baseline")
        bb = t.get_window_extent(renderer=renderer).transformed(inv)
        boxes.append((bb.x0, bb.y0, bb.x1, bb.y1))
        x += w + gap
    return boxes


def brace_note(fig, box, text, colour, below=True, dy=0.035, fontsize=13, alpha=1.0, x=None):
    """A bracket under (or over) one equation piece, with its meaning in words."""
    x0, y0, x1, y1 = box
    yb = y0 - 0.012 if below else y1 + 0.012
    tick = -0.01 if below else 0.01
    fig.add_artist(
        plt.Line2D(
            [x0, x0, x1, x1],
            [yb - tick, yb, yb, yb - tick],
            transform=fig.transFigure,
            color=colour,
            lw=2.0,
            alpha=alpha,
        )
    )
    cx = (x0 + x1) / 2 if x is None else x
    if x is not None:
        fig.add_artist(
            plt.Line2D(
                [(x0 + x1) / 2, cx],
                [yb, yb - dy + 0.012] if below else [yb, yb + dy - 0.012],
                transform=fig.transFigure,
                color=colour,
                lw=1.0,
                alpha=0.6 * alpha,
            )
        )
    fig.text(
        cx,
        yb - dy if below else yb + dy,
        text,
        fontsize=fontsize,
        color=colour,
        ha="center",
        va="top" if below else "bottom",
        alpha=alpha,
        linespacing=1.35,
    )


def panel_box(ax, x, y, w, h, edge=PANEL_EDGE, face=PANEL, lw=1.4, alpha=1.0, rounding=0.02):
    """A rounded panel in axes coordinates."""
    if (x, y, w, h) == (0, 0, 1, 1):
        ax._qc_panel = True  # the panel IS the axes: text must stay inside it
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0.0,rounding_size={rounding}",
            facecolor=face,
            edgecolor=edge,
            linewidth=lw,
            alpha=alpha,
            transform=ax.transAxes,
        )
    )
