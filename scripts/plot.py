"""Erzeugt SVG-Funktionsplots mit exakt berechneten Koordinaten (nur Standardbibliothek).

Benutzung (eigenes Skript im Scratch-Ordner, nicht im Projekt):

    import sys; sys.path.insert(0, "<skill>/scripts")
    from plot import Plot
    p = Plot((-3, 5), (-3, 5), 34)                 # x-Bereich, y-Bereich, Pixel pro Einheit
    p.curve(lambda x: x**2, "s-mute", 2)           # Graph (Klasse = Farbe aus dem Theme)
    p.curve(lambda x: (x-2)**2 + 1, "s-acc", 2.6)
    p.point(2, 1, "S(2|1)", 8, 4, "f-acc", "t-xs t-acc")
    p.gline(2, -1, "s-water")                      # Gerade y = 2x - 1
    svg = p.svg("Kurzbeschreibung für Screenreader")

Optionen: sy (eigener y-Maßstab), ticks/xticks/yticks, grid, gridlines=False,
origin=False (keine 0 am Ursprung, z. B. bei gestapelten Plots), xlabel/ylabel.
Farbklassen: s-ink, s-mute, s-acc, s-water, s-ok (Linien) · f-* (Füllung) · t-* (Text).
Die Ausgabe nutzt class="plot" (css/extras.css) und begrenzt die Breite per
style="max-width:…px", damit Plots auf großen Bildschirmen nicht riesig werden.
Pfeilspitzen der Achsen brauchen <marker id="arr"> im <defs>-Block der Seite.
"""
import math, sys

def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s

class Plot:
    def __init__(self, xr, yr, sx, sy=None, pad=(26, 18, 18, 22), grid=1, ticks=1, xticks=None, yticks=None,
                 xlabel="x", ylabel="y", axes=True, gridlines=True, origin=True):
        self.xmin, self.xmax = xr
        self.ymin, self.ymax = yr
        self.sx = sx
        self.sy = sy if sy is not None else sx
        self.pl, self.pt, self.pr, self.pb = pad
        self.W = self.pl + (self.xmax - self.xmin) * self.sx + self.pr
        self.H = self.pt + (self.ymax - self.ymin) * self.sy + self.pb
        self.parts = []
        self.grid, self.ticks = grid, ticks
        self.xticks, self.yticks = xticks, yticks
        self.xlabel, self.ylabel = xlabel, ylabel
        self.origin = origin
        if gridlines:
            self._grid()
        if axes:
            self._axes()

    def X(self, x):
        return self.pl + (x - self.xmin) * self.sx

    def Y(self, y):
        return self.pt + (self.ymax - y) * self.sy

    def _range(self, a, b, step):
        out, v = [], math.ceil(a / step - 1e-9) * step
        while v <= b + 1e-9:
            out.append(round(v, 6))
            v += step
        return out

    def _grid(self):
        d = []
        for x in self._range(self.xmin, self.xmax, self.grid):
            d.append(f"M{fmt(self.X(x))},{fmt(self.Y(self.ymax))}V{fmt(self.Y(self.ymin))}")
        for y in self._range(self.ymin, self.ymax, self.grid):
            d.append(f"M{fmt(self.X(self.xmin))},{fmt(self.Y(y))}H{fmt(self.X(self.xmax))}")
        self.parts.append(f'<path class="grid" fill="none" d="{"".join(d)}"/>')

    def _axes(self):
        x0 = self.X(0) if self.xmin <= 0 <= self.xmax else self.X(self.xmin)
        y0 = self.Y(0) if self.ymin <= 0 <= self.ymax else self.Y(self.ymin)
        self.parts.append(f'<line class="axis" x1="{fmt(self.X(self.xmin) - 6)}" y1="{fmt(y0)}" x2="{fmt(self.X(self.xmax) + 12)}" y2="{fmt(y0)}" marker-end="url(#arr)"/>')
        self.parts.append(f'<line class="axis" x1="{fmt(x0)}" y1="{fmt(self.Y(self.ymin) + 6)}" x2="{fmt(x0)}" y2="{fmt(self.Y(self.ymax) - 12)}" marker-end="url(#arr)"/>')
        self.parts.append(f'<text x="{fmt(self.X(self.xmax) + 10)}" y="{fmt(y0 + 15)}" class="t-s t-b" text-anchor="end">{self.xlabel}</text>')
        self.parts.append(f'<text x="{fmt(x0 + 7)}" y="{fmt(self.Y(self.ymax) - 4)}" class="t-s t-b" text-anchor="start">{self.ylabel}</text>')
        xt = self.xticks if self.xticks is not None else [v for v in self._range(self.xmin, self.xmax, self.ticks) if abs(v) > 1e-9]
        yt = self.yticks if self.yticks is not None else [v for v in self._range(self.ymin, self.ymax, self.ticks) if abs(v) > 1e-9]
        tk = []
        for x in xt:
            tk.append(f"M{fmt(self.X(x))},{fmt(y0 - 3)}v6")
            lab = x if isinstance(x, str) else (f"{x:g}".replace("-", "−").replace(".", ","))
            self.parts.append(f'<text x="{fmt(self.X(x))}" y="{fmt(y0 + 14)}" class="t-xs" text-anchor="middle">{lab}</text>')
        for y in yt:
            tk.append(f"M{fmt(x0 - 3)},{fmt(self.Y(y))}h6")
            lab = f"{y:g}".replace("-", "−").replace(".", ",")
            self.parts.append(f'<text x="{fmt(x0 - 6)}" y="{fmt(self.Y(y) + 3.5)}" class="t-xs" text-anchor="end">{lab}</text>')
        if self.origin and self.xmin <= 0 <= self.xmax and self.ymin <= 0 <= self.ymax:
            self.parts.append(f'<text x="{fmt(x0 - 5)}" y="{fmt(y0 + 13)}" class="t-xs" text-anchor="end">0</text>')
        self.parts.append(f'<path class="axis" stroke-width="1" d="{"".join(tk)}"/>')

    def curve(self, f, cls="s-acc", w=2.4, dom=None, n=160, dash=None, clip=0.3):
        a, b = dom if dom else (self.xmin, self.xmax)
        d, pen = [], False
        for i in range(n + 1):
            x = a + (b - a) * i / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError):
                pen = False
                continue
            if y is None or y < self.ymin - clip or y > self.ymax + clip:
                pen = False
                continue
            d.append(("L" if pen else "M") + f"{fmt(self.X(x))},{fmt(self.Y(y))}")
            pen = True
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<path class="{cls}" fill="none" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{ds} d="{"".join(d)}"/>')

    def line(self, x1, y1, x2, y2, cls="s-ink", w=1.5, dash=None, marker=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        self.parts.append(f'<line class="{cls}" stroke-width="{w}"{ds}{mk} x1="{fmt(self.X(x1))}" y1="{fmt(self.Y(y1))}" x2="{fmt(self.X(x2))}" y2="{fmt(self.Y(y2))}"/>')

    def gline(self, m, c, cls="s-water", w=2, dom=None, dash=None):
        self.curve(lambda x: m * x + c, cls=cls, w=w, dom=dom, n=2 if not dom else 200, dash=dash)

    def point(self, x, y, label=None, dx=6, dy=-6, cls="f-ink", tcls="t-s t-b", anchor="start", r=3.6):
        self.parts.append(f'<circle cx="{fmt(self.X(x))}" cy="{fmt(self.Y(y))}" r="{r}" class="{cls}"/>')
        if label:
            self.text(x, y, label, dx, dy, tcls, anchor)

    def text(self, x, y, s, dx=0, dy=0, cls="t-s", anchor="start", raw=False):
        self.parts.append(f'<text x="{fmt(self.X(x) + dx)}" y="{fmt(self.Y(y) + dy)}" class="{cls}" text-anchor="{anchor}">{s}</text>')

    def raw(self, s):
        self.parts.append(s)

    def svg(self, label, cls="plot", scale=1.4):
        return (f'<svg class="{cls}" style="max-width:{fmt(self.W * scale)}px" viewBox="0 0 {fmt(self.W)} {fmt(self.H)}" role="img" aria-label="{label}">\n  '
                + "\n  ".join(self.parts) + "\n</svg>")
