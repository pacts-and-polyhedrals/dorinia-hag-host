"""
Grotesque-chibi vector art engine for the Yagha Coven War Host.
Everything is drawn in a 1000x1000 space. Shapes are organic (jittered Catmull-Rom),
inked with thick dark outlines, shaded with hatched shadow + rim light, and the
whole figure is passed through an ink-wobble filter at render time.
"""
import math
import random

INK = "#140a10"
RIM = {"col": None}
_uid = [0]


def uid(prefix="g"):
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


# ------------------------------------------------------------------ geometry
def catmull(points, closed=True, tension=1.0):
    """Smooth path through points (Catmull-Rom -> cubic Bezier)."""
    n = len(points)
    if n < 2:
        return ""
    pts = points
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")


def blob_pts(cx, cy, rx, ry, jitter=0.06, n=14, seed=0, rot=0.0, squash=None):
    r = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rot
        k = 1 + r.uniform(-jitter, jitter)
        x, y = math.cos(a) * rx * k, math.sin(a) * ry * k
        if squash:  # squash(x,y)->(x,y) for pear/egg shapes
            x, y = squash(x, y)
        pts.append((cx + x, cy + y))
    return pts


def blob(cx, cy, rx, ry, jitter=0.06, n=14, seed=0, rot=0.0, squash=None):
    return catmull(blob_pts(cx, cy, rx, ry, jitter, n, seed, rot, squash))


def pear(top=0.8, bottom=1.15):
    """Squash fn: narrower top, wider bottom (for hunched bodies / chins)."""
    def f(x, y):
        k = top if y < 0 else bottom
        return x * k, y
    return f


def tube(points, w0, w1, seed=0, wobble=0.0):
    """Tapered limb/tail along a smoothed centreline. Returns closed path."""
    r = random.Random(seed)
    n = len(points)
    left, right = [], []
    for i, (x, y) in enumerate(points):
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) / 2 * (1 + r.uniform(-wobble, wobble))
        a = points[max(i - 1, 0)]
        b = points[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return catmull(left + right[::-1])


def bez(p0, p1, p2, steps=8):
    out = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        out.append((x, y))
    return out


def poly(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def shade(c, f):
    """Darken (f<1) or lighten (f>1) a hex colour."""
    c = c.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    if f < 1:
        r, g, b = (int(v * f) for v in (r, g, b))
    else:
        r, g, b = (int(v + (255 - v) * (f - 1)) for v in (r, g, b))
    return f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"


# ------------------------------------------------------------------ painting
def defs():
    return f"""
<defs>
  <filter id="ink" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 -0.18"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="mottle" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="3" seed="11" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.1 -0.45"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="14"/>
  </filter>
  <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
  <pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
    <line x1="0" y1="0" x2="0" y2="9" stroke="{INK}" stroke-width="2.2" opacity="0.75"/>
  </pattern>
  <pattern id="xhatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)">
    <line x1="0" y1="0" x2="0" y2="10" stroke="{INK}" stroke-width="2" opacity="0.6"/>
    <line x1="0" y1="0" x2="10" y2="0" stroke="{INK}" stroke-width="1.6" opacity="0.45"/>
  </pattern>
</defs>"""


def part(d, fill, *, sw=7, light=(-0.45, -0.55), shadow=0.42, hatch=True, rim=True, texture=True,
         highlight=1.35, stroke=INK, extra=""):
    """A filled, inked, shaded shape. Shadow & hatching are clipped to the shape."""
    cid = uid("c")
    lx, ly = light
    # shadow is a big offset copy of the shape opposite the light; done via clip + translated path
    sx, sy = -lx * 60, -ly * 60
    hx, hy = lx * 40, ly * 40
    out = [f'<clipPath id="{cid}"><path d="{d}"/></clipPath>',
           f'<path d="{d}" fill="{fill}"/>',
           f'<g clip-path="url(#{cid})">']
    if texture:
        out.append(f'<path d="{d}" fill="{shade(fill, 0.55)}" filter="url(#mottle)" opacity="0.55"/>')
    # inverse-shadow trick: fill everything dark, then cover with the shape shifted toward the light
    out.append(f'<rect x="-200" y="-200" width="1400" height="1400" fill="{shade(fill, shadow)}"/>')
    out.append(f'<path d="{d}" fill="{fill}" transform="translate({hx:.1f},{hy:.1f})"/>')
    if texture:
        out.append(f'<path d="{d}" fill="{shade(fill, 0.55)}" filter="url(#mottle)" opacity="0.5" transform="translate({hx:.1f},{hy:.1f})"/>')
    if hatch:
        mid = uid("m")
        out.append(f'<mask id="{mid}"><rect x="-200" y="-200" width="1400" height="1400" fill="white"/>'
                   f'<path d="{d}" fill="black" transform="translate({hx*1.25:.1f},{hy*1.25:.1f})"/></mask>')
        out.append(f'<rect x="-200" y="-200" width="1400" height="1400" fill="url(#hatch)" mask="url(#{mid})" opacity="0.8"/>')
    if rim:
        out.append(f'<path d="{d}" fill="none" stroke="{shade(fill, highlight)}" stroke-width="6" opacity="0.7" '
                   f'transform="translate({-lx*9:.1f},{-ly*9:.1f})"/>')
        if RIM["col"]:
            out.append(f'<path d="{d}" fill="none" stroke="{RIM["col"]}" stroke-width="7" opacity="0.55" '
                       f'transform="translate({lx*11:.1f},{ly*11:.1f})"/>')
    out.append(extra)
    out.append("</g>")
    if sw:
        out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    return "\n".join(out)


def flat(d, fill, sw=6, stroke=INK, opacity=1.0):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}"/>'


def line(pts, sw=6, color=INK, opacity=1.0, smooth=True):
    d = catmull(pts, closed=False) if smooth and len(pts) > 2 else "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'


def glow(cx, cy, r, color, opacity=0.8):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" filter="url(#glow)" opacity="{opacity}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="{color}" filter="url(#softglow)" opacity="{opacity}"/>')


# ------------------------------------------------------------------ features
def eye(cx, cy, r, *, iris="#d8c24a", pupil="slit", look=(0, 0), lid=0.0, glow_col=None, white="#f1e9d2",
        bags=False, bloodshot=False):
    out = []
    if glow_col:
        out.append(glow(cx, cy, r * 1.4, glow_col, 0.7))
    d = blob(cx, cy, r, r * 0.95, 0.04, 10, seed=int(cx + cy))
    out.append(flat(d, white, sw=max(4, r * 0.14)))
    cid = uid("e")
    out.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">')
    if bloodshot:
        rr = random.Random(int(cx))
        for _ in range(5):
            a = rr.uniform(0, 6.28)
            out.append(line([(cx + math.cos(a) * r, cy + math.sin(a) * r),
                             (cx + math.cos(a + .2) * r * .6, cy + math.sin(a + .2) * r * .6)], sw=1.6, color="#b02a2a"))
    ix, iy = cx + look[0] * r * 0.35, cy + look[1] * r * 0.35
    out.append(f'<circle cx="{ix}" cy="{iy}" r="{r*0.62}" fill="{iris}" stroke="{INK}" stroke-width="{r*0.08}"/>')
    out.append(f'<circle cx="{ix}" cy="{iy}" r="{r*0.62}" fill="{shade(iris,0.55)}" opacity="0.5" clip-path="inset(50% 0 0 0)"/>')
    if pupil == "slit":
        out.append(f'<ellipse cx="{ix}" cy="{iy}" rx="{r*0.12}" ry="{r*0.5}" fill="{INK}"/>')
    elif pupil == "dot":
        out.append(f'<circle cx="{ix}" cy="{iy}" r="{r*0.28}" fill="{INK}"/>')
    elif pupil == "none":
        pass
    if lid > 0:
        out.append(f'<rect x="{cx-r*1.2}" y="{cy-r*1.2}" width="{r*2.4}" height="{r*2.4*lid}" fill="{INK}" opacity="0.92"/>')
    out.append("</g>")
    out.append(f'<circle cx="{ix - r*0.25}" cy="{iy - r*0.28}" r="{r*0.16}" fill="white"/>')
    out.append(f'<circle cx="{ix + r*0.2}" cy="{iy + r*0.18}" r="{r*0.07}" fill="white" opacity="0.8"/>')
    if bags:
        out.append(line([(cx - r * .9, cy + r * 1.05), (cx, cy + r * 1.3), (cx + r * .9, cy + r * 1.05)], sw=3.5))
        out.append(line([(cx - r * .6, cy + r * 1.3), (cx + r * .2, cy + r * 1.45)], sw=2.5, opacity=.7))
    return "\n".join(out)


def glow_eye(cx, cy, r, color, shape="almond"):
    if shape == "almond":
        d = f"M{cx-r},{cy} Q{cx},{cy-r*0.9} {cx+r},{cy} Q{cx},{cy+r*0.7} {cx-r},{cy} Z"
    else:
        d = blob(cx, cy, r, r * .8, .05, 8, seed=int(cx))
    return glow(cx, cy, r * 1.2, color, 0.9) + flat(d, shade(color, 1.5), sw=4) + \
        f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.35}" ry="{r*0.25}" fill="white"/>'


def brow(x0, y0, x1, y1, sw=12, bend=-10):
    return line([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + bend), (x1, y1)], sw=sw)


def grin(cx, cy, w, h, *, teeth=7, seed=1, gum="#5a1020", tooth="#e8dcae", fangs=(), missing=(), curve=0.5,
         tongue=None):
    """Wide crooked grin with irregular teeth."""
    r = random.Random(seed)
    top = [(cx - w / 2, cy), (cx, cy + h * curve * 0.3), (cx + w / 2, cy)]
    mouth = (f"M{cx-w/2},{cy} Q{cx},{cy + h*curve*0.6} {cx+w/2},{cy} "
             f"Q{cx + w*0.25},{cy + h*1.15} {cx},{cy + h*1.1} Q{cx - w*0.25},{cy + h*1.15} {cx-w/2},{cy} Z")
    out = [flat(mouth, "#1c0508", sw=6)]
    cid = uid("mo")
    out.append(f'<clipPath id="{cid}"><path d="{mouth}"/></clipPath><g clip-path="url(#{cid})">')
    out.append(f'<ellipse cx="{cx}" cy="{cy+h*0.95}" rx="{w*0.35}" ry="{h*0.35}" fill="{gum}"/>')
    if tongue:
        out.append(f'<ellipse cx="{cx+w*0.08}" cy="{cy+h*0.9}" rx="{w*0.22}" ry="{h*0.3}" fill="{tongue}" stroke="{INK}" stroke-width="3"/>')
    for i in range(teeth):
        if i in missing:
            continue
        t = (i + 0.5) / teeth
        x = cx - w / 2 + w * t
        ytop = cy + h * curve * 0.6 * (1 - (2 * t - 1) ** 2) - 6
        tw = w / teeth * r.uniform(0.7, 1.05)
        th = h * r.uniform(0.35, 0.6) * (1.6 if i in fangs else 1)
        tilt = r.uniform(-8, 8)
        d = f"M{x-tw/2},{ytop} L{x+tw/2},{ytop} L{x+tw*0.3+tilt*0.3},{ytop+th} Q{x+tilt*0.2},{ytop+th*1.15} {x-tw*0.35},{ytop+th*0.9} Z"
        col = tooth if r.random() > 0.25 else shade(tooth, 0.75)
        out.append(flat(d, col, sw=3))
    # lower teeth
    for i in range(teeth - 2):
        t = (i + 1) / (teeth - 1)
        x = cx - w / 2 + w * t
        yb = cy + h * 1.05 - abs(2 * t - 1) * h * 0.4
        tw = w / teeth * 0.7
        th = h * r.uniform(0.2, 0.4)
        out.append(flat(f"M{x-tw/2},{yb+4} L{x+tw/2},{yb+4} L{x+r.uniform(-3,3)},{yb-th} Z", shade(tooth, 0.85), sw=2.5))
    out.append("</g>")
    out.append(f'<path d="{mouth}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # cheek creases
    out.append(line([(cx - w / 2 - 8, cy - 14), (cx - w / 2 - 14, cy + 4), (cx - w / 2 - 6, cy + 18)], sw=4))
    out.append(line([(cx + w / 2 + 8, cy - 14), (cx + w / 2 + 14, cy + 4), (cx + w / 2 + 6, cy + 18)], sw=4))
    return "\n".join(out)


def warts(cx, cy, rx, ry, n, color, seed=0, size=(6, 14)):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        a = r.uniform(0, 6.28)
        d = r.uniform(0.2, 0.9)
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        s = r.uniform(*size)
        out.append(part(blob(x, y, s, s * .9, .1, 7, seed=r.randint(0, 999)), color, sw=3, hatch=False, texture=False))
        if r.random() > 0.5:
            out.append(line([(x, y - s), (x + r.uniform(-6, 6), y - s - 10)], sw=1.8))
    return "\n".join(out)


def scars(cx, cy, length, angle, sw=4):
    a = math.radians(angle)
    x0, y0 = cx - math.cos(a) * length / 2, cy - math.sin(a) * length / 2
    x1, y1 = cx + math.cos(a) * length / 2, cy + math.sin(a) * length / 2
    out = [line([(x0, y0), (x1, y1)], sw=sw, color="#7a2a2a")]
    for i in range(1, 5):
        t = i / 5
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        px, py = -math.sin(a) * 9, math.cos(a) * 9
        out.append(line([(x - px, y - py), (x + px, y + py)], sw=2.5))
    return "\n".join(out)


def hag_nose(x, y, length, width, skin, droop=1.0, seed=0):
    d = (f"M{x-width*0.4},{y-length*0.25} Q{x-width*0.6},{y+length*0.4} {x+width*0.1},{y+length*0.75*droop} "
         f"Q{x+width*0.95},{y+length*1.05*droop} {x+width*0.7},{y+length*0.55} Q{x+width*0.55},{y} {x+width*0.25},{y-length*0.3} Z")
    return part(d, skin, sw=6) + warts(x + width * 0.4, y + length * 0.55, width * 0.3, length * 0.2, 2, shade(skin, 0.85), seed)


def hand(cx, cy, size, skin, *, claws="#2a1c14", fingers=4, spread=60, angle=-90, seed=0, curl=0.3):
    r = random.Random(seed)
    out = [part(blob(cx, cy, size, size * .85, .08, 9, seed=seed), skin, sw=6, hatch=True)]
    base = math.radians(angle)
    for i in range(fingers):
        a = base + math.radians(-spread / 2 + spread * i / max(fingers - 1, 1))
        L = size * r.uniform(1.0, 1.35)
        p0 = (cx + math.cos(a) * size * 0.7, cy + math.sin(a) * size * 0.7)
        p1 = (cx + math.cos(a) * (size * 0.7 + L * .6), cy + math.sin(a) * (size * 0.7 + L * .6))
        p2 = (cx + math.cos(a + curl) * (size * 0.7 + L), cy + math.sin(a + curl) * (size * 0.7 + L))
        out.append(part(tube([p0, p1, p2], size * .38, size * .22, seed=seed + i), skin, sw=5, hatch=False, texture=False))
        tip = p2
        ca = a + curl * 1.6
        claw = (f"M{tip[0] - math.sin(ca)*size*.12},{tip[1] + math.cos(ca)*size*.12} "
                f"Q{tip[0] + math.cos(ca)*size*.5},{tip[1] + math.sin(ca)*size*.5} "
                f"{tip[0] + math.cos(ca+0.6)*size*.55},{tip[1] + math.sin(ca+0.6)*size*.55} "
                f"L{tip[0] + math.sin(ca)*size*.12},{tip[1] - math.cos(ca)*size*.12} Z")
        out.append(flat(claw, claws, sw=3.5))
    return "\n".join(out)


def arm(points, w0, w1, skin, seed=0):
    return part(tube(points, w0, w1, seed=seed, wobble=0.08), skin, sw=7)


def hair_strands(cx, cy, rx, ry, n, color, *, seed=0, length=(60, 160), spread=(200, 340), sw=(5, 11)):
    r = random.Random(seed)
    out = []
    for i in range(n):
        a = math.radians(r.uniform(*spread))
        x0, y0 = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        L = r.uniform(*length)
        wild = r.uniform(-0.9, 0.9)
        x1 = x0 + math.cos(a + wild * .5) * L * .5
        y1 = y0 + math.sin(a + wild * .5) * L * .5
        x2 = x0 + math.cos(a + wild) * L
        y2 = y0 + math.sin(a + wild) * L
        w = r.uniform(*sw)
        out.append(f'<path d="{catmull([(x0,y0),(x1,y1),(x2,y2)], closed=False)}" fill="none" stroke="{INK}" '
                   f'stroke-width="{w+5}" stroke-linecap="round"/>')
        out.append(f'<path d="{catmull([(x0,y0),(x1,y1),(x2,y2)], closed=False)}" fill="none" stroke="{color}" '
                   f'stroke-width="{w}" stroke-linecap="round"/>')
        out.append(f'<path d="{catmull([(x0,y0),(x1,y1),(x2,y2)], closed=False)}" fill="none" stroke="{shade(color,1.4)}" '
                   f'stroke-width="{w*0.3}" stroke-linecap="round" opacity="0.6" transform="translate(-2,-2)"/>')
    return "\n".join(out)


def drips(x0, x1, y, color, n=5, seed=0, length=(20, 70)):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = r.uniform(x0, x1)
        L = r.uniform(*length)
        w = r.uniform(6, 13)
        d = f"M{x-w/2},{y} L{x+w/2},{y} L{x+w*0.35},{y+L} Q{x},{y+L+w*1.2} {x-w*0.35},{y+L} Z"
        out.append(flat(d, color, sw=3))
        out.append(f'<circle cx="{x-w*0.1}" cy="{y+L*0.6}" r="{w*0.15}" fill="white" opacity="0.7"/>')
    return "\n".join(out)


def snake(points, w0, w1, skin, belly, *, seed=0, head=True, eye_col="#ffdf3a", tongue=True, head_size=None):
    """Scaled serpent along centreline; head at the END of the points list."""
    out = [part(tube(points, w0, w1, seed=seed), skin, sw=6)]
    # belly stripe & scale arcs
    n = len(points)
    for i in range(1, n - 1):
        x, y = points[i]
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) / 2
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{w*0.35:.1f}" fill="none" stroke="{shade(skin,0.5)}" stroke-width="2.5" opacity="0.7"/>')
    if head:
        hx, hy = points[-1]
        px, py = points[-2]
        a = math.atan2(hy - py, hx - px)
        hs = head_size or w1 * 1.1
        d = blob(hx + math.cos(a) * hs * .4, hy + math.sin(a) * hs * .4, hs, hs * .75, .05, 10, seed=seed + 5, rot=a)
        out.append(part(d, skin, sw=6))
        ex, ey = hx + math.cos(a) * hs * .5 + math.cos(a - 1.57) * hs * .35, hy + math.sin(a) * hs * .5 + math.sin(a - 1.57) * hs * .35
        out.append(eye(ex, ey, hs * .3, iris=eye_col, pupil="slit"))
        mx, my = hx + math.cos(a) * hs * 1.3, hy + math.sin(a) * hs * 1.3
        out.append(line([(hx + math.cos(a + .5) * hs * .4, hy + math.sin(a + .5) * hs * .4), (mx, my)], sw=4))
        if tongue:
            tx, ty = mx + math.cos(a) * hs * .8, my + math.sin(a) * hs * .8
            out.append(line([(mx, my), (tx, ty)], sw=5, color="#b0203a"))
            out.append(line([(tx, ty), (tx + math.cos(a - .5) * 18, ty + math.sin(a - .5) * 18)], sw=4, color="#b0203a"))
            out.append(line([(tx, ty), (tx + math.cos(a + .5) * 18, ty + math.sin(a + .5) * 18)], sw=4, color="#b0203a"))
    return "\n".join(out)


def spikes_along(points, size, color, side=1, every=1, seed=0):
    r = random.Random(seed)
    out = []
    for i in range(1, len(points) - 1, every):
        x, y = points[i]
        a = points[i - 1]
        b = points[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * side, dx / L * side
        s = size * r.uniform(.7, 1.2)
        tip = (x + nx * s * 2.2, y + ny * s * 2.2)
        out.append(flat(f"M{x - dx/L*s},{y - dy/L*s} L{tip[0]},{tip[1]} L{x + dx/L*s},{y + dy/L*s} Z", color, sw=4))
    return "\n".join(out)


# ------------------------------------------------------------------ weapons & props
def blade(x0, y0, x1, y1, w, color="#8d96a3", edge="#d9e2ea", serrate=0):
    a = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(a), math.cos(a)
    L = math.hypot(x1 - x0, y1 - y0)
    pts = [(x0 + nx * w / 2, y0 + ny * w / 2)]
    steps = max(serrate, 1)
    for i in range(1, steps + 1):
        t = i / (steps + 1)
        bx, by = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        ww = w / 2 * (1 - t * 0.6) + (8 if serrate and i % 2 else 0)
        pts.append((bx + nx * ww, by + ny * ww))
    pts.append((x1, y1))
    pts.append((x0 - nx * w / 2 + (x1 - x0) * 0.75, y0 - ny * w / 2 + (y1 - y0) * 0.75))
    pts.append((x0 - nx * w / 2, y0 - ny * w / 2))
    d = poly(pts)
    return part(d, color, sw=5, texture=False, highlight=1.6) + line(
        [(x0 + nx * w * .1, y0 + ny * w * .1), (x1 - (x1 - x0) * .08, y1 - (y1 - y0) * .08)], sw=3, color=edge, opacity=.8)


def shaft(x0, y0, x1, y1, w=16, color="#5a3a22"):
    return part(tube([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)], w, w * 0.9), color, sw=5, texture=True)


def spearhead(x, y, angle, size, color="#7c8590", barbed=False):
    a = math.radians(angle)
    tip = (x + math.cos(a) * size * 2, y + math.sin(a) * size * 2)
    l = (x + math.cos(a + 1.9) * size * .7, y + math.sin(a + 1.9) * size * .7)
    rr = (x + math.cos(a - 1.9) * size * .7, y + math.sin(a - 1.9) * size * .7)
    pts = [rr, tip, l]
    if barbed:
        pts = [rr, (x + math.cos(a - .9) * size * .9, y + math.sin(a - .9) * size * .9), tip,
               (x + math.cos(a + .9) * size * .9, y + math.sin(a + .9) * size * .9), l,
               (x + math.cos(a + 2.6) * size * .9, y + math.sin(a + 2.6) * size * .9),
               (x - math.cos(a) * size * .3, y - math.sin(a) * size * .3),
               (x + math.cos(a - 2.6) * size * .9, y + math.sin(a - 2.6) * size * .9)]
    return part(poly(pts), color, sw=5, texture=False, highlight=1.6)


def chain(points, color="#6d6a66", link=22):
    out = []
    path = []
    for i in range(len(points) - 1):
        path += bez(points[i], ((points[i][0] + points[i + 1][0]) / 2, (points[i][1] + points[i + 1][1]) / 2 + 30), points[i + 1], 10)
    acc, last = 0, path[0]
    k = 0
    for p in path[1:]:
        acc += math.hypot(p[0] - last[0], p[1] - last[1])
        if acc >= link:
            a = math.degrees(math.atan2(p[1] - last[1], p[0] - last[0]))
            rx = link * .65 if k % 2 == 0 else link * .65
            ry = link * .38 if k % 2 == 0 else link * .14
            out.append(f'<ellipse cx="{p[0]:.1f}" cy="{p[1]:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({a:.1f} {p[0]:.1f} {p[1]:.1f})" '
                       f'fill="none" stroke="{INK}" stroke-width="10"/>'
                       f'<ellipse cx="{p[0]:.1f}" cy="{p[1]:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({a:.1f} {p[0]:.1f} {p[1]:.1f})" '
                       f'fill="none" stroke="{color}" stroke-width="5"/>')
            acc = 0
            k += 1
        last = p
    return "\n".join(out)


def bubbles(cx, cy, rx, ry, n, color, seed=0, size=(5, 18)):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = cx + r.uniform(-rx, rx), cy + r.uniform(-ry, ry)
        s = r.uniform(*size)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}" fill="{color}" stroke="{INK}" stroke-width="3" opacity="0.9"/>'
                   f'<circle cx="{x-s*.3:.1f}" cy="{y-s*.3:.1f}" r="{s*.25:.1f}" fill="white" opacity="0.8"/>')
    return "\n".join(out)


def wisp(cx, cy, size, color, seed=0, face=True):
    r = random.Random(seed)
    d = (f"M{cx},{cy-size} Q{cx+size*.9},{cy-size*.6} {cx+size*.7},{cy+size*.2} Q{cx+size*.5},{cy+size*.8} {cx+size*.1},{cy+size*1.2} "
         f"Q{cx+r.uniform(-.4,.4)*size},{cy+size*1.8} {cx-size*.3},{cy+size*2.2} Q{cx-size*.2},{cy+size*1.4} {cx-size*.6},{cy+size*.6} "
         f"Q{cx-size*.95},{cy-size*.3} {cx},{cy-size} Z")
    out = [glow(cx, cy, size * 1.2, color, .6), flat(d, shade(color, 1.35), sw=4, opacity=.9)]
    if face:
        out.append(f'<ellipse cx="{cx-size*.25}" cy="{cy-size*.1}" rx="{size*.12}" ry="{size*.2}" fill="{INK}"/>'
                   f'<ellipse cx="{cx+size*.25}" cy="{cy-size*.1}" rx="{size*.12}" ry="{size*.2}" fill="{INK}"/>'
                   f'<ellipse cx="{cx}" cy="{cy+size*.35}" rx="{size*.16}" ry="{size*.24}" fill="{INK}"/>')
    return "\n".join(out)


def smoke(cx, cy, n, color, seed=0, rise=200, size=(30, 60)):
    r = random.Random(seed)
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        x = cx + r.uniform(-30, 30) + t * r.uniform(-40, 40)
        y = cy - rise * t
        s = r.uniform(*size) * (1 + t * .6)
        out.append(part(blob(x, y, s, s * .8, .15, 9, seed=seed + i), color, sw=4, hatch=False, texture=False, shadow=.75))
    return "\n".join(out)


def ground_shadow(cx, cy, rx, ry=None):
    ry = ry or rx * 0.18
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{INK}" opacity="0.45"/>'


def nose_bulb(x, y, length, size, skin, hook=1.0, seed=0):
    """Hooked bridge + bulbous warty tip; x,y = bridge top."""
    tipx, tipy = x + size * 0.35 * hook, y + length
    bridge = tube([(x, y), (x + size * .45 * hook, y + length * .45), (tipx, tipy - size * .2)], size * .55, size * .8, seed=seed)
    o = [part(bridge, skin, sw=6)]
    o.append(part(blob(tipx, tipy, size * .62, size * .5, .12, 10, seed=seed + 1), skin, sw=6))
    o.append(f'<ellipse cx="{tipx - size*.32:.1f}" cy="{tipy + size*.22:.1f}" rx="{size*.13:.1f}" ry="{size*.09:.1f}" fill="{INK}"/>')
    o.append(f'<ellipse cx="{tipx + size*.28:.1f}" cy="{tipy + size*.24:.1f}" rx="{size*.13:.1f}" ry="{size*.09:.1f}" fill="{INK}"/>')
    o.append(warts(tipx, tipy - size * .1, size * .4, size * .3, 2, shade(skin, .82), seed, size=(6, 11)))
    return "\n".join(o)


def hair_locks(cx, cy, rx, ry, n, color, *, seed=0, length=(80, 200), spread=(190, 350), width=(22, 40), droop=0.6):
    """Clumped, tapered, curling locks of hair (drawn behind the head)."""
    r = random.Random(seed)
    o = []
    for i in range(n):
        a = math.radians(r.uniform(*spread))
        x0, y0 = cx + math.cos(a) * rx * .85, cy + math.sin(a) * ry * .85
        L = r.uniform(*length)
        curl = r.uniform(-1.1, 1.1)
        pts = [(x0, y0)]
        ang = a
        for k in range(1, 5):
            ang += curl * .35
            pts.append((pts[-1][0] + math.cos(ang) * L / 4, pts[-1][1] + math.sin(ang) * L / 4 + droop * k * 6))
        o.append(part(tube(pts, r.uniform(*width), 3, seed=seed + i), color, sw=5, texture=False, hatch=(i % 2 == 0)))
        o.append(line(pts[1:-1], sw=2, color=shade(color, .5), opacity=.7))
    return "\n".join(o)


def wrinkles(lines_, sw=3.5, opacity=.8):
    return "\n".join(line(pts, sw=sw, opacity=opacity) for pts in lines_)


def tattered(cx, top, bottom, wtop, wbot, seed=0, teeth=9, depth=40):
    """Robe/cloak silhouette with ragged hem."""
    r = random.Random(seed)
    pts = [(cx - wtop / 2, top), (cx - wtop * .2, top - 15), (cx + wtop * .2, top - 15), (cx + wtop / 2, top),
           (cx + wbot * .48, (top + bottom) / 2), (cx + wbot / 2, bottom)]
    for i in range(teeth, -1, -1):
        x = cx - wbot / 2 + wbot * i / teeth
        y = bottom + (r.uniform(depth * .4, depth) if i % 2 else r.uniform(-10, 8))
        pts.append((x, y))
    pts += [(cx - wbot / 2, bottom), (cx - wbot * .48, (top + bottom) / 2)]
    return catmull(pts, tension=0.6)


def pointy_ear(x, y, length, width, skin, side=-1, seed=0, droop=0.3):
    tip = (x + side * length, y - length * droop)
    d = catmull([(x, y - width / 2), ((x + tip[0]) / 2, y - width * .45 - length * droop * .4), tip,
                 ((x + tip[0]) / 2 + side * 10, y + width * .1), (x, y + width / 2)], tension=.8)
    return part(d, skin, sw=6) + line([(x + side * length * .2, y), (x + side * length * .6, y - length * droop * .55)], sw=4, color=shade(skin, .5))


def folds(cx, top, bottom, width, n=4, seed=0, color=None):
    r = random.Random(seed)
    o = []
    for i in range(n):
        x = cx - width / 2 + width * (i + .5) / n + r.uniform(-15, 15)
        y0 = top + r.uniform(0, (bottom - top) * .3)
        o.append(line([(x, y0), (x + r.uniform(-20, 20), (y0 + bottom) / 2), (x + r.uniform(-30, 30), bottom)],
                      sw=r.uniform(3, 6), color=color or INK, opacity=.75))
    return "\n".join(o)


# ------------------------------------------------------------------ creature parts
def stubby_legs(cx, top, ground, gap, w, col, foot_col=None, seed=0, feet="boot"):
    o = []
    for side in (-1, 1):
        x = cx + side * gap
        o.append(part(tube([(x, top), (x + side * 6, (top + ground) / 2), (x + side * 4, ground - 25)], w, w * .85, seed=seed + side), col, sw=6))
        fc = foot_col or shade(col, .7)
        if feet == "claw":
            o.append(hand(x + side * 20, ground - 18, w * .45, fc, fingers=3, spread=70, angle=90 - side * 50, seed=seed + 3 + side, curl=.2))
        else:
            o.append(part(blob(x + side * 22, ground - 18, w * .85, w * .45, .08, 9, seed=seed + 5 + side), fc, sw=6))
    return "\n".join(o)


def bat_wing(sx, sy, side, span, height, col, seed=0, bones="#2a1a22"):
    """Leathery wing from shoulder (sx,sy); side=-1 left, 1 right."""
    tips = [(sx + side * span * k, sy - height * h) for k, h in ((.55, 1.0), (.9, .7), (1.0, .25), (.85, -.2))]
    elbow = (sx + side * span * .35, sy - height * .75)
    pts = [(sx, sy), elbow, tips[0]]
    r = random.Random(seed)
    for i in range(1, len(tips)):
        mid = ((tips[i - 1][0] + tips[i][0]) / 2 - side * 25, (tips[i - 1][1] + tips[i][1]) / 2 + 35)
        pts += [mid, tips[i]]
    pts += [(sx + side * span * .35, sy + height * .25), (sx + side * 10, sy + 40)]
    o = [part(catmull(pts, tension=.5), col, sw=6)]
    for t in tips:
        o.append(line([(sx, sy), elbow, t], sw=8, color=INK))
        o.append(line([(sx, sy), elbow, t], sw=3, color=bones))
    o.append(hand(elbow[0], elbow[1] - 10, 14, shade(col, .8), fingers=1, spread=0, angle=-90, seed=seed))
    return "\n".join(o)


def spiral_shell(cx, cy, r, col, band, seed=0, gems=None):
    o = [part(blob(cx, cy, r, r * .92, .04, 16, seed=seed), col, sw=8)]
    pts = []
    for i in range(70):
        a = i * 0.2
        rr = r * (1 - i / 75) * .9
        pts.append((cx + math.cos(a) * rr * 0.98, cy + math.sin(a) * rr * .92))
    o.append(line(pts[::-1], sw=9))
    o.append(line(pts[::-1], sw=4, color=band, opacity=.9))
    if gems:
        rnd = random.Random(seed)
        for _ in range(9):
            a, d = rnd.uniform(0, 6.28), rnd.uniform(.2, .85)
            x, y = cx + math.cos(a) * r * d, cy + math.sin(a) * r * d
            s = rnd.uniform(10, 22)
            o.append(glow(x, y, s, gems, .35))
            o.append(flat(poly([(x, y - s), (x + s * .7, y), (x, y + s), (x - s * .7, y)]), shade(gems, 1.3), sw=3))
    return "\n".join(o)


def spider_legs(cx, cy, span, col, seed=0, n=4):
    o = []
    r = random.Random(seed)
    for side in (-1, 1):
        for i in range(n):
            a = -0.9 + i * 0.55
            knee = (cx + side * span * (.45 + .1 * i), cy - 110 + i * 25 + r.uniform(-10, 10))
            foot = (cx + side * span * (.7 + .12 * i), cy + 120 + i * 8)
            o.append(part(tube([(cx + side * 40, cy), knee], 34, 26, seed=seed + i), col, sw=6, texture=False))
            o.append(part(tube([knee, ((knee[0] + foot[0]) / 2 + side * 10, (knee[1] + foot[1]) / 2), foot], 26, 8, seed=seed + 9 + i), col, sw=6, texture=False))
            for k in range(3):
                t = (k + 1) / 4
                hx = knee[0] + (foot[0] - knee[0]) * t
                hy = knee[1] + (foot[1] - knee[1]) * t
                o.append(line([(hx, hy), (hx + side * 14, hy - 8)], sw=3))
    return "\n".join(o)


def goblin_head(cx, cy, r, skin, *, mouth="grin", seed=0, eye_col="#f2c12e", ear=1.0, nose=True, look=(0, 0)):
    o = [pointy_ear(cx - r * .85, cy - r * .05, r * 1.0 * ear, r * .55, skin, side=-1, seed=seed, droop=.15),
         pointy_ear(cx + r * .85, cy - r * .05, r * 1.0 * ear, r * .55, skin, side=1, seed=seed + 1, droop=.2)]
    o.append(part(blob(cx, cy, r, r * .9, .06, 14, seed=seed, squash=pear(1.05, .95)), skin, sw=8))
    o.append(warts(cx, cy, r * .8, r * .7, 3, shade(skin, .82), seed=seed))
    o.append(eye(cx - r * .38, cy - r * .12, r * .26, iris=eye_col, pupil="dot", look=look))
    o.append(eye(cx + r * .38, cy - r * .15, r * .22, iris=eye_col, pupil="dot", look=look))
    o.append(brow(cx - r * .65, cy - r * .5, cx - r * .15, cy - r * .35, sw=10, bend=-6))
    o.append(brow(cx + r * .12, cy - r * .38, cx + r * .62, cy - r * .5, sw=10, bend=-6))
    if mouth == "scream":
        d = blob(cx, cy + r * .5, r * .42, r * .38, .08, 10, seed=seed + 3)
        o.append(flat(d, "#2a0608", sw=7))
        o.append(f'<ellipse cx="{cx}" cy="{cy + r*.68}" rx="{r*.22}" ry="{r*.14}" fill="#a02236"/>')
        for i in range(5):
            x = cx - r * .3 + i * r * .15
            o.append(flat(poly([(x - 7, cy + r * .2), (x + 7, cy + r * .2), (x, cy + r * .36)]), "#efe2b0", sw=2.5))
    else:
        o.append(grin(cx, cy + r * .35, r * 1.05, r * .3, teeth=7, seed=seed + 2, fangs=(1, 5), missing=(3,), curve=.4))
    if nose:
        o.append(part(blob(cx + r * .05, cy + r * .15, r * .22, r * .16, .1, 8, seed=seed + 4), skin, sw=5, hatch=False))
    return "\n".join(o)


def troll_head(cx, cy, r, skin, *, seed=0, mood="roar", eye_col="#ffcf3a", tusks=True, hair="#2b2a24"):
    o = [hair_locks(cx, cy - r * .2, r * .9, r * .8, 10, hair, seed=seed + 7, length=(r * .6, r * 1.2), spread=(190, 350), width=(18, 30), droop=3)]
    o.append(pointy_ear(cx - r * .9, cy, r * .6, r * .45, skin, side=-1, seed=seed, droop=.4))
    o.append(pointy_ear(cx + r * .9, cy, r * .6, r * .45, skin, side=1, seed=seed + 1, droop=.4))
    o.append(part(blob(cx, cy, r, r * .95, .08, 14, seed=seed, squash=pear(.9, 1.15)), skin, sw=8))
    o.append(warts(cx, cy, r * .85, r * .75, 6, shade(skin, .8), seed=seed + 3))
    o.append(eye(cx - r * .36, cy - r * .2, r * .2, iris=eye_col, pupil="dot", look=(.2, 0), bloodshot=True))
    o.append(eye(cx + r * .36, cy - r * .22, r * .17, iris=eye_col, pupil="dot", look=(-.2, 0)))
    o.append(brow(cx - r * .7, cy - r * .55, cx - r * .1, cy - r * .35, sw=13, bend=-4))
    o.append(brow(cx + r * .1, cy - r * .35, cx + r * .68, cy - r * .58, sw=13, bend=-4))
    if mood == "roar":
        d = blob(cx, cy + r * .45, r * .55, r * .35, .08, 12, seed=seed + 2)
        o.append(flat(d, "#2a0608", sw=7))
        o.append(f'<ellipse cx="{cx}" cy="{cy + r*.62}" rx="{r*.3}" ry="{r*.12}" fill="#9c2a30"/>')
        rr = random.Random(seed)
        for i in range(6):
            x = cx - r * .42 + i * r * .17
            o.append(flat(poly([(x - 9, cy + r * .16), (x + 9, cy + r * .16), (x + rr.uniform(-4, 4), cy + r * .33)]), "#e6d9a8", sw=2.5))
    else:
        o.append(grin(cx, cy + r * .38, r * 1.1, r * .3, teeth=6, seed=seed + 2, missing=(2,), curve=.3))
    if tusks:
        for side in (-1, 1):
            x = cx + side * r * .42
            y = cy + r * .62
            o.append(flat(f"M{x-10},{y} Q{x + side*6},{y - r*.5} {x + side*28},{y - r*.55} Q{x + side*18},{y - r*.3} {x+12},{y} Z", "#efe4c0", sw=4))
    o.append(nose_bulb(cx - r * .05, cy - r * .25, r * .55, r * .45, skin, hook=-.4, seed=seed + 5))
    return "\n".join(o)


def darkling_hood(cx, cy, r, cloak, *, seed=0, eye_col="#e9f6ff", grin_=True, tip=(40, -60)):
    o = []
    d = catmull([(cx - r, cy + r * .55), (cx - r * 1.05, cy - r * .1), (cx - r * .6, cy - r * .8),
                 (cx + tip[0], cy - r + tip[1]), (cx + r * .7, cy - r * .7), (cx + r * 1.05, cy - r * .05), (cx + r * .95, cy + r * .6),
                 (cx, cy + r * .75)], tension=.8)
    o.append(part(d, cloak, sw=8))
    face = blob(cx, cy + r * .1, r * .72, r * .58, .05, 12, seed=seed)
    o.append(flat(face, "#0d0a12", sw=6))
    o.append(eye(cx - r * .3, cy, r * .2, iris="#e9f6ff", pupil="none", glow_col=eye_col, white=shade(eye_col, 1.2)))
    o.append(eye(cx + r * .3, cy - r * .02, r * .17, iris="#e9f6ff", pupil="none", glow_col=eye_col, white=shade(eye_col, 1.2)))
    if grin_:
        rr = random.Random(seed)
        y = cy + r * .32
        o.append(line([(cx - r * .38, y - 4), (cx, y + 10), (cx + r * .38, y - 6)], sw=4, color=eye_col, opacity=.9))
        for i in range(7):
            x = cx - r * .32 + i * r * .105
            o.append(flat(poly([(x - 6, y + 2 + abs(i - 3) * -2), (x + 6, y + 2 + abs(i - 3) * -2), (x + rr.uniform(-2, 2), y + 18)]), shade(eye_col, 1.1), sw=1.5))
    return "\n".join(o)


def cobra_head(cx, cy, r, skin, hood, *, seed=0, eye_col="#ffdc2e", mouth_open=True):
    o = [part(blob(cx, cy + r * .35, r * 1.55, r * 1.25, .06, 16, seed=seed + 1, squash=pear(.9, 1.0)), hood, sw=8)]
    for side in (-1, 1):  # hood markings
        o.append(part(blob(cx + side * r * .85, cy + r * .2, r * .25, r * .35, .1, 8, seed=seed + side), "#e3c84a", sw=4, hatch=False))
        o.append(f'<circle cx="{cx + side*r*.85}" cy="{cy + r*.2}" r="{r*.1}" fill="{INK}"/>')
    o.append(part(blob(cx, cy, r, r * .85, .05, 12, seed=seed, squash=pear(1.1, .85)), skin, sw=8))
    for i in range(6):  # scales
        o.append(f'<path d="M{cx - r*.5 + i*r*.2},{cy - r*.55} q{r*.1},{r*.12} {r*.2},0" fill="none" stroke="{INK}" stroke-width="3" opacity=".6"/>')
    o.append(eye(cx - r * .42, cy - r * .1, r * .26, iris=eye_col, pupil="slit"))
    o.append(eye(cx + r * .42, cy - r * .1, r * .26, iris=eye_col, pupil="slit"))
    o.append(brow(cx - r * .7, cy - r * .45, cx - r * .2, cy - r * .3, sw=9, bend=-4))
    o.append(brow(cx + r * .2, cy - r * .3, cx + r * .7, cy - r * .45, sw=9, bend=-4))
    o.append(f'<ellipse cx="{cx-r*.1}" cy="{cy+r*.18}" rx="5" ry="3" fill="{INK}"/><ellipse cx="{cx+r*.1}" cy="{cy+r*.18}" rx="5" ry="3" fill="{INK}"/>')
    if mouth_open:
        o.append(grin(cx, cy + r * .35, r * 1.2, r * .4, teeth=4, seed=seed, fangs=(0, 3), missing=(1, 2), curve=.4, tongue="#c0304a"))
    return "\n".join(o)


def armor_plate(cx, cy, rx, ry, col, seed=0, rivets=True):
    o = [part(blob(cx, cy, rx, ry, .04, 12, seed=seed), col, sw=7, highlight=1.6, texture=True)]
    if rivets:
        for k in range(6):
            a = math.pi * (1.1 + k * .16)
            o.append(f'<circle cx="{cx + math.cos(a)*rx*.8:.1f}" cy="{cy + math.sin(a)*ry*.8:.1f}" r="5" fill="{shade(col,1.6)}" stroke="{INK}" stroke-width="2.5"/>')
    o.append(scars(cx + rx * .2, cy, rx * .5, 30, sw=3))
    return "\n".join(o)


def flask(cx, cy, r, liquid, seed=0):
    o = [part(blob(cx, cy, r, r * .95, .04, 10, seed=seed), "#a9c7c4", sw=6, hatch=False, highlight=1.8)]
    o.append(f'<path d="M{cx-r*.9},{cy} Q{cx},{cy+r*.2} {cx+r*.9},{cy} A{r*.92},{r*.9} 0 0 1 {cx-r*.9},{cy} Z" fill="{liquid}" opacity=".9"/>')
    o.append(bubbles(cx, cy + r * .4, r * .4, r * .2, 3, shade(liquid, 1.3), seed=seed, size=(3, 7)))
    o.append(part(f"M{cx-r*.3},{cy-r*.85} L{cx+r*.3},{cy-r*.85} L{cx+r*.25},{cy-r*1.4} L{cx-r*.25},{cy-r*1.4} Z", "#a9c7c4", sw=5, hatch=False))
    o.append(part(blob(cx, cy - r * 1.48, r * .3, r * .15, .05, 8, seed=seed), "#7a4a2a", sw=4, hatch=False))
    o.append(glow(cx, cy, r * .8, liquid, .3))
    return "\n".join(o)
