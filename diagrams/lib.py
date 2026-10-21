"""Tiny helper for drawing block diagrams of cryptographic constructions.

Every figure in this repository is drawn from scratch with this file and
draw.py, so the diagrams can be edited and regenerated:  python3 diagrams/draw.py
"""
import re
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle

INK = "#333333"
MUTED = "#777777"
STYLES = {
    "blue": ("#E8F0FE", "#3B6FD8"),
    "green": ("#E6F4EA", "#2E8B57"),
    "orange": ("#FEF3E2", "#D9822B"),
    "purple": ("#F3E8FD", "#7B3FC4"),
    "red": ("#FDE8E8", "#C0392B"),
    "grey": ("#F4F4F4", "#666666"),
    "white": ("#FFFFFF", "#666666"),
}
FONT = "DejaVu Sans"


class Diagram:
    def __init__(self, w, h, scale=0.62):
        self.fig, self.ax = plt.subplots(figsize=(w * scale, h * scale))
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.subplots_adjust(0, 0, 1, 1)

    # basic shapes -------------------------------------------------------
    def box(self, x, y, w, h, text="", style="blue", fs=11, rounded=True, bold=False, dashed=False):
        """Box with lower-left corner (x, y)."""
        face, edge = STYLES[style]
        bs = "round,pad=0,rounding_size=0.18" if rounded else "square,pad=0"
        p = FancyBboxPatch((x, y), w, h, boxstyle=bs, fc=face, ec=edge, lw=1.5,
                           ls="--" if dashed else "-", zorder=2)
        self.ax.add_patch(p)
        if text:
            self.text(x + w / 2, y + h / 2, text, fs=fs, bold=bold)
        return (x, y, w, h)

    def cbox(self, cx, cy, w, h, text="", **kw):
        """Box centred on (cx, cy)."""
        return self.box(cx - w / 2, cy - h / 2, w, h, text, **kw)

    def region(self, x, y, w, h, label="", fs=10):
        p = Rectangle((x, y), w, h, fc="none", ec="#AAAAAA", lw=1.1, ls="--", zorder=0)
        self.ax.add_patch(p)
        if label:
            self.text(x + 0.15, y + h - 0.3, label, fs=fs, color=MUTED, ha="left")

    def xor(self, cx, cy, r=0.22):
        self.ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.3, zorder=3))
        self.ax.plot([cx - r, cx + r], [cy, cy], color=INK, lw=1.3, zorder=4)
        self.ax.plot([cx, cx], [cy - r, cy + r], color=INK, lw=1.3, zorder=4)

    def op(self, cx, cy, sym, r=0.24, fs=11):
        self.ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.3, zorder=3))
        self.text(cx, cy, sym, fs=fs, z=4)

    def text(self, x, y, s, fs=11, bold=False, color=INK, ha="center", va="center", z=5, italic=False,
             bg=False):
        # render X_Y as a subscript, e.g. E_K, MAC_K2, sk_A
        s = re.sub(r"(?<![\w$])([^\W\d_]\w*?)_([\w′]+)",
                   lambda m: "$\\mathrm{%s}_{\\mathrm{%s}}$" % (m[1], m[2].replace("′", "'")), s)
        self.ax.text(x, y, s, fontsize=fs, ha=ha, va=va, color=color, zorder=z, family=FONT,
                     fontweight="bold" if bold else "normal", style="italic" if italic else "normal",
                     bbox=dict(fc="white", ec="none", pad=1.5) if bg else None)

    def line(self, pts, color=INK, lw=1.4, ls="-"):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=1, solid_capstyle="round")

    def arrow(self, pts, color=INK, lw=1.4, ls="-", both=False):
        """Polyline whose last segment carries an arrow head."""
        if len(pts) > 2:
            self.line(pts[:-1], color=color, lw=lw, ls=ls)
        a = FancyArrowPatch(pts[-2], pts[-1], arrowstyle="<|-|>" if both else "-|>",
                            mutation_scale=13, color=color, lw=lw, ls=ls, zorder=1,
                            shrinkA=0, shrinkB=0)
        self.ax.add_patch(a)

    def save(self, path):
        self.fig.savefig(path + ".svg", format="svg", bbox_inches="tight", pad_inches=0.12,
                         facecolor="white")
        self.fig.savefig(path + ".png", format="png", dpi=170, bbox_inches="tight",
                         pad_inches=0.12, facecolor="white")
        plt.close(self.fig)
