"""Shared style for the Week 2 (embeddings) slide GIFs.

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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
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


def fig_to_pil(fig, close=True):
    fig.canvas.draw()
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
    print(f"saved {path} ({len(frames)} frames, {os.path.getsize(path) / 1e6:.1f} MB)")


def save_png(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, facecolor=BG)
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
    ax.add_patch(box)
    ax.text(
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
