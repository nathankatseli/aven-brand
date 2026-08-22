#!/usr/bin/env python
"""The Avenue family - one idea, many drawings.
Cara's brief (Aug 2026): trees either side, a house in the middle, a road running down to it.
Simple, tasteful, fine line. Every variation shares the grammar: pine line, sage road/ground,
one rain-blue evening star, wordmark beneath.   python src/avenue.py  -> src/marks/2N-*.svg
Canvas 210x152; art lives in y 18-114, wordmark at y 133/147.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "marks"
PINE, SAGE, RAIN, INK, SAGE_T = "#2e4b3f", "#adbfae", "#5b7e8c", "#1c2b26", "#6f8579"
CX = 105
VP = (CX, 90)          # vanishing point = where the road meets the house
FORE = 113             # foreground ground line


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def line(x1, y1, x2, y2, c=PINE, w=1.3):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="round"/>'


def path(d, c=PINE, w=1.3, fill="none"):
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>'


def circle(cx, cy, r, c=PINE, w=1.3, fill="none"):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{c}" stroke-width="{f(w)}"/>'


def ellipse(cx, cy, rx, ry, c=PINE, w=1.3, fill="none"):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" stroke="{c}" stroke-width="{f(w)}"/>'


def dot(cx, cy, r=2.2, c=RAIN):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{c}"/>'


def star(cx=CX, cy=50, r=2.3):
    return dot(cx, cy, r)


# ---- vocabulary -------------------------------------------------------------
def tree(x, ground, h, r, w=1.3, kind="oval", c=PINE):
    """trunk from the ground up to the canopy; canopy centred r above the trunk top."""
    if kind == "oval":           # upright ellipse - the default, reads as a tree not a lollipop
        cy = ground - h + r * 1.2
        return line(x, ground, x, cy + r * 0.9, c, w) + ellipse(x, cy, r, r * 1.2, c, w)
    if kind == "round":
        cy = ground - h + r
        return line(x, ground, x, cy + r * 0.7, c, w) + circle(x, cy, r, c, w)
    if kind == "drop":           # teardrop canopy, point down into the trunk
        cy = ground - h + r * 1.2
        return line(x, ground, x, cy + r * 1.1, c, w) + path(
            f"M{f(x)} {f(cy + r * 1.2)} C{f(x - r * 1.3)} {f(cy + r * 0.2)} {f(x - r)} {f(cy - r * 1.1)} {f(x)} {f(cy - r * 1.2)} "
            f"C{f(x + r)} {f(cy - r * 1.1)} {f(x + r * 1.3)} {f(cy + r * 0.2)} {f(x)} {f(cy + r * 1.2)} Z", c, w)
    if kind == "lollipop":       # solid dot canopy
        return line(x, ground, x, ground - h + r, c, w) + dot(x, ground - h + r, r, c)
    if kind == "solid":          # filled oval canopy
        cy = ground - h + r * 1.2
        return line(x, ground, x, cy, c, w) + ellipse(x, cy, r, r * 1.2, c, 0, c)
    if kind == "arc":            # open umbrella arc
        top = ground - h
        return line(x, ground, x, top + r * 0.4, c, w) + path(f"M{f(x - r)} {f(top + r * 0.55)} A{f(r)} {f(r)} 0 0 1 {f(x + r)} {f(top + r * 0.55)}", c, w)
    if kind == "cypress":        # tall narrow pointed canopy
        top = ground - h
        return line(x, ground, x, top + h * 0.3, c, w) + path(f"M{f(x - r * 0.8)} {f(top + h * 0.62)} Q{f(x)} {f(top - 2)} {f(x + r * 0.8)} {f(top + h * 0.62)} Q{f(x)} {f(top + h * 0.72)} {f(x - r * 0.8)} {f(top + h * 0.62)} Z", c, w)
    if kind == "tick":
        return line(x, ground, x, ground - h, c, w)
    raise ValueError(kind)


def house(cx, base, w, h, kind="gable", c=PINE, sw=1.3, door=True):
    """gable house on a base line; apex at base-h."""
    left, right = cx - w / 2, cx + w / 2
    wall_top = base - h * 0.52
    apex = base - h
    if kind == "roof":
        return path(f"M{f(left)} {f(wall_top)} L{f(cx)} {f(apex)} L{f(right)} {f(wall_top)}", c, sw)
    if kind == "solid":
        return f'<path d="M{f(left)} {f(base)} L{f(left)} {f(wall_top)} L{f(cx)} {f(apex)} L{f(right)} {f(wall_top)} L{f(right)} {f(base)} Z" fill="{c}"/>'
    out = path(f"M{f(left)} {f(base)} L{f(left)} {f(wall_top)} L{f(cx)} {f(apex)} L{f(right)} {f(wall_top)} L{f(right)} {f(base)}", c, sw)
    if door and w >= 13:
        dw, dh = w * 0.24, h * 0.3
        out += path(f"M{f(cx - dw / 2)} {f(base)} L{f(cx - dw / 2)} {f(base - dh + dw / 2)} A{f(dw / 2)} {f(dw / 2)} 0 0 1 {f(cx + dw / 2)} {f(base - dh + dw / 2)} L{f(cx + dw / 2)} {f(base)}", c, sw * 0.8)
    return out


def road(half=46, fore=FORE, vp=VP, c=SAGE, w=1.3, gap=3.5):
    """two kerb lines converging from the foreground to the house's doorstep."""
    return line(vp[0] - half, fore, vp[0] - gap, vp[1], c, w) + line(vp[0] + half, fore, vp[0] + gap, vp[1], c, w)


def ground(y, half=52, c=SAGE, w=1.2):
    return line(CX - half, y, CX + half, y, c, w)


def rows(n, near_x=48, near_h=44, near_r=10, far_h=8, far_r=2.2, kind="oval", w_near=1.6, w_far=0.85, fore=FORE, vp=VP, k=0.42):
    """symmetrical rows of trees receding in true one-point perspective: trees are equally spaced
    in depth, so on the page they bunch toward the vanishing point; each foot sits on the line
    from (near_x, fore) to the vanishing point and the size shrinks with depth."""
    out = ""
    ts = [1 - 1 / (1 + i * k) for i in range(n)]
    tmax = ts[-1] if n > 1 else 1
    for side in (-1, 1):
        x0 = vp[0] + side * abs(vp[0] - near_x)
        for t in ts:
            u = t / tmax                                  # 0 near .. 1 far
            x = x0 + (vp[0] + side * 4.5 - x0) * t
            y = fore + (vp[1] - fore) * t
            h = near_h - (near_h - far_h) * u
            r = near_r - (near_r - far_r) * u
            w = w_near - (w_near - w_far) * u
            out += tree(x, y, h, r, w, kind)
    return out


def wordmark(y1=133, y2=147):
    return (f'<text x="105" y="{y1}" text-anchor="middle" fill="{INK}" font-size="15" letter-spacing="7" font-family="Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif">AVEN</text>\n'
            f'  <text x="105" y="{y2}" text-anchor="middle" fill="{SAGE_T}" font-size="8.5" letter-spacing="4.5" font-family="Avenir Next,Segoe UI,sans-serif">PROPERTY</text>')


def svg(label, body, wm=True):
    parts = "\n  ".join(x for x in body if x)
    return (f'<svg width="210" height="152" viewBox="0 0 210 152" role="img" aria-label="{label}">\n  {parts}\n'
            + (f'  {wordmark()}\n' if wm else "") + '</svg>\n')


# ---- variations -------------------------------------------------------------
# Family rules (judge panel, Aug 2026): road kerbs in PINE - the road is the idea and sage vanishes small;
# one or two trees a side, never a receding row; oval canopies (lollipops read as clip-art);
# star at (CX, 50) r2.3 where kept; house base 90, 17x17, stroke 1.4, arched door; nothing below y=116.
MARKS = []
CLOUD = "#f3f5f1"


def mark(num, slug, label):
    def deco(fn):
        MARKS.append((num, slug, label, fn))
        return fn
    return deco


def pair(x, y, h, r, w=1.5, kind="oval", c=PINE):
    """one tree a side, mirrored about CX"""
    return tree(x, y, h, r, w, kind, c) + tree(2 * CX - x, y, h, r, w, kind, c)


def kerb_y(x, x0, y0, x1, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def ring(r, cy, gap, w=1.2):
    """ring open at the base; returns (svg, y where the ring ends either side of the gap)"""
    yb = cy + (r * r - gap * gap) ** 0.5
    return path(f"M{f(CX - gap)} {f(yb)} A{r} {r} 0 1 1 {f(CX + gap)} {f(yb)}", PINE, w), yb


@mark(20, "avenue", "The Avenue - two trees a side recede along the road to the house, evening star above")
def m20():
    return [road(half=44, c=PINE, w=1.4), pair(50, 113, 44, 10, 1.5), pair(72, 103, 22, 5.5, 1.2),
            house(CX, 90, 17, 17, sw=1.4), star()]


@mark(21, "plain-avenue", "The Plain Avenue - the brief in four elements: road, two trees, house, star; nothing else")
def m21():
    return [road(half=44, c=PINE, w=1.4), pair(52, 113, 44, 10, 1.5), house(CX, 90, 17, 17, sw=1.4), star()]


@mark(22, "light-road", "The Light Road - the road is a sage shape, the only fill; trees and house stay fine line")
def m22():
    b = [f'<path d="M{f(CX - 44)} 113 L{f(CX - 3.5)} 90 L{f(CX + 3.5)} 90 L{f(CX + 44)} 113 Z" fill="{SAGE}"/>']
    b.append(pair(50, 113, 44, 10, 1.4))
    b.append(pair(72, 103, 22, 5.5, 1.2))
    b.append(house(CX, 90, 17, 17, sw=1.4))
    b.append(star())
    return b


@mark(23, "one-line", "The One Line - road, walls and roof drawn as a single unbroken stroke; one tree a side on the kerb")
def m23():
    d = f"M59 108 L96 88 L96 76 L{CX} 66 L114 76 L114 88 L151 108"
    b = [path(d, PINE, 1.6)]
    y = kerb_y(62, 59, 108, 96, 88)
    b.append(pair(62, y, 40, 9, 1.5))
    b.append(star())
    return b


@mark(24, "approach", "The Approach - house forward: a bigger house, one tree each side, the road arriving at the door")
def m24():
    b = [ground(90, 49), road(half=30, vp=(CX, 90), c=PINE, w=1.4, gap=5)]
    b.append(house(CX, 90, 26, 26, sw=1.5))
    b.append(pair(56, 90, 40, 13, 1.5))
    b.append(star(CX, 50))
    return b


@mark(25, "canopy", "The Canopy - two trees bow over the road and almost meet; the star sits in the gap, the house at the end")
def m25():
    x, top, gap = 46, 52, 8
    b = [road(half=40, c=PINE, w=1.3)]
    b.append(path(f"M{f(x)} 113 Q{f(x + 4)} {f(top + 6)} {f(CX - gap)} {top}", PINE, 1.6))
    b.append(path(f"M{f(210 - x)} 113 Q{f(210 - x - 4)} {f(top + 6)} {f(CX + gap)} {top}", PINE, 1.6))
    b.append(house(CX, 90, 17, 17, sw=1.4))
    b.append(star(CX, 50, 2.2))
    return b


@mark(26, "cypress", "The Cypress Avenue - the South West's windbreak rows: two tall narrow trees a side, road to the house")
def m26():
    b = [road(half=44, c=PINE, w=1.3)]
    b.append(pair(56, 113, 60, 7, 1.5, "cypress"))
    b.append(pair(80, kerb_y(80, 61, 113, 101.5, 90), 34, 4.8, 1.2, "cypress"))
    b.append(house(CX, 90, 17, 17, sw=1.4))
    b.append(star(CX, 46))
    return b


@mark(27, "evening", "The Evening Avenue - the road in sage, one lit window in the house; the window is the only light")
def m27():
    b = [road(half=44, c=SAGE, w=1.4)]
    b.append(pair(50, 113, 44, 10, 1.2))
    b.append(pair(72, 103, 22, 5.5, 1.0))
    b.append(house(CX, 90, 18, 18, sw=1.4, door=False))
    b.append(f'<rect x="{f(CX - 2.2)}" y="{f(83.2)}" width="4.4" height="4.4" fill="{RAIN}"/>')
    return b


@mark(28, "silhouette", "The Silhouette - solid trees, a solid house and a sage road; the version that survives anything")
def m28():
    b = [f'<path d="M{f(CX - 36)} 112 L{f(CX - 4)} 90 L{f(CX + 4)} 90 L{f(CX + 36)} 112 Z" fill="{SAGE}"/>']
    b.append(pair(55, 112, 50, 12, 1.9, "solid"))
    b.append(house(CX, 90, 17, 17, "solid"))
    b.append(star())
    return b


@mark(29, "full-avenue", "The Full Avenue - the avenue inside a ring; ring and road join as one keyhole line")
def m29():
    rg, yb = ring(42, 62, 14, 1.2)
    vp = (CX, 84)
    b = [rg, road(half=14, fore=yb, vp=vp, c=PINE, w=1.2, gap=3)]
    b.append(pair(80, 98, 26, 7, 1.4))
    b.append(house(CX, 84, 16, 16, sw=1.3))
    b.append(star(CX, 46))
    return b


@mark(30, "ring-air", "The Ring, with air - Cara's circle tile drawn with restraint: a small ring, a small house, room to breathe")
def m30():
    rg, yb = ring(36, 64, 12, 1.1)
    vp = (CX, 82)
    b = [rg, road(half=12, fore=yb, vp=vp, c=PINE, w=1.1, gap=2.5)]
    b.append(pair(88, 93, 16, 4.2, 1.0))
    b.append(house(CX, 82, 12, 12, sw=1.1, door=False))
    b.append(star(CX, 50, 2.0))
    return b


@mark(31, "monogram", "The A - the road's edges are the legs of an A, the horizon its bar, the roof its apex; a monogram companion")
def m31():
    b = [path(f"M65 113 L97 75 L{CX} 63 L113 75 L145 113", PINE, 1.6)]
    t = (113 - 96) / (113 - 75)
    bx = 65 + (97 - 65) * t
    b.append(line(bx, 96, 210 - bx, 96, SAGE_T, 1.5))
    b.append(star())
    return b


@mark(32, "lane", "The Lane - the family's small cut: heavy road into the house, two solid trees; survives a favicon")
def m32():
    b = [line(CX - 34, 113, CX - 11, 84, PINE, 2), line(CX + 34, 113, CX + 11, 84, PINE, 2)]
    b.append(path(f"M{f(CX - 11)} 84 L{f(CX - 11)} 77 L{f(CX)} 65 L{f(CX + 11)} 77 L{f(CX + 11)} 84", PINE, 2))
    b.append(pair(58, 113, 34, 8.5, 2, "solid"))
    b.append(star(CX, 49, 2.8))
    return b


@mark(33, "tile", "The Tile - the Lane reversed on a pine square: app icon, social avatar, favicon")
def m33():
    k = 0.72

    def S(x, y):
        return 105 + (x - 105) * k, 79 + (y - 87) * k
    b = [f'<rect x="57" y="18" width="96" height="96" rx="20" fill="{PINE}"/>']
    for sg in (-1, 1):
        (x0, y0), (x1, y1) = S(CX + sg * 34, 113), S(CX + sg * 11, 84)
        b.append(line(x0, y0, x1, y1, CLOUD, 2.2))
    pts = [S(CX - 11, 84), S(CX - 11, 77), S(CX, 65), S(CX + 11, 77), S(CX + 11, 84)]
    b.append(path("M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts), CLOUD, 2.2))
    tx, ty = S(58, 113)
    b.append(pair(tx, ty, 34 * k, 8.5 * k, 2.2, "solid", CLOUD))
    sx, sy = S(CX, 49)
    b.append(star(sx, sy, 2.6))
    return b


def build(out=OUT, only=None, marks=None):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    n = 0
    for num, slug, label, fn in (marks or MARKS):
        if only and num not in only:
            continue
        (out / f"{num}-{slug}.svg").write_text(svg(label, fn()), encoding="utf-8")
        n += 1
    print(f"wrote {n} avenue marks -> {out}")


def icon(out=ROOT / "kit" / "marks" / "icons" / "avenue-icon.svg"):
    """The Lane as a square icon with favicon-weight strokes (no wordmark; needs no outlining)."""
    b = [line(CX - 34, 113, CX - 11, 84, PINE, 4.2), line(CX + 34, 113, CX + 11, 84, PINE, 4.2),
         path(f"M{f(CX - 11)} 84 L{f(CX - 11)} 77 L{f(CX)} 65 L{f(CX + 11)} 77 L{f(CX + 11)} 84", PINE, 4.2),
         pair(58, 113, 34, 9.5, 4.2, "solid"), star(CX, 47, 4.5)]
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="44 20 122 122" role="img" aria-label="AVEN icon: road, roof, two trees, evening star">'
    out.write_text(head + "\n  " + "\n  ".join(b) + "\n</svg>\n", encoding="utf-8")
    print("icon ->", out)


if __name__ == "__main__":
    build()
    icon()
