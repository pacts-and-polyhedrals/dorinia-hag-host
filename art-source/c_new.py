import math, random
from engine import *
from creatures import PAL

GG, AG, FG, CG = PAL["Grandma"]["glow"], PAL["Auntie"]["glow"], PAL["Gaga"]["glow"], PAL["Coven"]["glow"]


def speed_lines(x0, x1, ys, color="#d6f3ff"):
    out = []
    for i, (y, w) in enumerate(ys):
        pts = [(x1, y), ((x0 + x1) / 2, y + (8 if i % 2 else -8)), (x0, y + (14 if i % 2 else -10))]
        out.append(part(tube(pts, w * 2.6, 2, seed=i), color, sw=4, hatch=False, texture=False, rim=False))
    return "\n".join(out)


def quickling(skin, cloth, eye_col, *, hooded=False, seed=0):
    o = [speed_lines(60, 330, [(560, 10), (620, 6), (690, 12), (760, 7), (820, 9)])]
    o.append(ground_shadow(520, 945, 170))
    # tiny body leaning forward, mid-sprint
    o.append(part(tube([(470, 900), (500, 820), (520, 760)], 34, 30, seed=seed), skin, sw=6))
    o.append(part(tube([(560, 905), (560, 830), (545, 760)], 34, 30, seed=seed + 1), skin, sw=6))
    o.append(part(blob(470, 905, 34, 16, .1, 8, seed=seed), "#2a1a22", sw=5, hatch=False))
    o.append(part(blob(575, 910, 34, 16, .1, 8, seed=seed + 2), "#2a1a22", sw=5, hatch=False))
    o.append(part(tattered(530, 600, 790, 170, 240, seed=seed + 3, teeth=6, depth=30), cloth, sw=7))
    # long ears
    o.append(pointy_ear(360, 400, 220, 80, skin, side=-1, seed=seed, droop=.15))
    o.append(pointy_ear(680, 395, 220, 80, skin, side=1, seed=seed + 1, droop=.2))
    if hooded:
        o.append(part(catmull([(300, 470), (290, 260), (420, 140), (520, 90), (640, 150), (750, 280), (740, 470), (520, 540)], tension=.8), cloth, sw=8))
    o.append(part(blob(520, 400, 185, 165, .05, 14, seed=seed + 4, squash=pear(1.0, .9)), skin, sw=9))
    if hooded:
        o.append(part(f"M330,410 Q520,470 710,410 L705,500 Q520,560 335,500 Z", shade(cloth, .8), sw=6))  # face mask
    o.append(eye(440, 380, 58, iris=eye_col, pupil="slit", look=(.5, .1), lid=.2 if hooded else 0))
    o.append(eye(605, 375, 54, iris=eye_col, pupil="slit", look=(.5, .1), lid=.2 if hooded else 0))
    o.append(brow(370, 300, 480, 330, sw=12, bend=-10))
    o.append(brow(560, 325, 670, 295, sw=12, bend=-10))
    if not hooded:
        o.append(grin(525, 465, 230, 55, teeth=11, seed=seed + 5, curve=.8))
        o.append(part(blob(525, 420, 22, 16, .1, 7, seed=seed), skin, sw=5, hatch=False))
    return o


def quickling_thief():
    RIM["col"] = GG
    o = quickling("#9fb0c8", "#3a2a40", "#ffd84a", seed=3)
    o.append(arm([(640, 640), (740, 600), (800, 520)], 30, 24, "#9fb0c8", seed=4))
    o.append(part(blob(820, 470, 60, 55, .1, 10, seed=5), "#7a4a22", sw=6))  # coin purse
    o.append(line([(790, 425), (850, 425)], sw=8))
    for x, y in [(800, 470), (835, 485), (820, 450)]:
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#e8c23a" stroke="{INK}" stroke-width="3"/>')
    o.append(hand(800, 520, 24, "#9fb0c8", angle=-60, seed=6, curl=1.0))
    o.append(arm([(420, 640), (330, 620), (260, 560)], 30, 24, "#9fb0c8", seed=7))
    o.append(blade(250, 560, 150, 470, 20, color="#8d96a3"))
    o.append(shaft(330, 700, 210, 760, w=12, color="#5a3a22"))  # stolen wand in belt
    o.append(glow(205, 762, 24, "#c27bff", .7))
    o.append(hand(255, 560, 24, "#9fb0c8", angle=-140, seed=8, curl=.9))
    RIM["col"] = None
    return "\n".join(o), (520, 420, 280)


def quickling_assassin():
    RIM["col"] = "#ff5a5a"
    o = quickling("#8c94b0", "#1c1822", "#ff4a4a", hooded=True, seed=11)
    for side, seed in ((-1, 12), (1, 13)):
        o.append(arm([(530 + side * 120, 640), (530 + side * 220, 600), (530 + side * 280, 520)], 30, 24, "#8c94b0", seed=seed))
        o.append(blade(530 + side * 280, 520, 530 + side * 380, 360, 14, color="#2a2a30", edge="#ff6a6a"))
        o.append(hand(530 + side * 280, 525, 24, "#8c94b0", angle=-90 - side * 30, seed=seed, curl=1.0))
    o.append(drips(820, 900, 380, "#7a2a5a", n=2, seed=4, length=(15, 35)))
    RIM["col"] = None
    return "\n".join(o), (520, 400, 280)


def lantern_snuffer():
    RIM["col"] = GG
    cloak = "#2c2836"
    o = [ground_shadow(500, 945, 200)]
    o.append(shaft(700, 940, 760, 140, w=16, color="#7a5a2a"))
    o.append(line([(760, 140), (800, 110), (830, 140), (815, 170)], sw=12))
    o.append(line([(760, 140), (800, 110), (830, 140), (815, 170)], sw=6, color="#c9a23a"))
    # snuffed lantern hanging from the hook, trailing smoke
    o.append(line([(815, 170), (815, 230)], sw=5))
    o.append(part("M780,230 L850,230 L845,320 L785,320 Z", "#3a3632", sw=6, hatch=False))
    o.append(f'<rect x="792" y="245" width="46" height="62" fill="#141018" stroke="{INK}" stroke-width="4"/>')
    o.append(line([(815, 300), (815, 280)], sw=6, color="#2a2a2a"))
    for k, (x, y, r) in enumerate([(820, 200, 14), (840, 160, 12), (830, 115, 10), (850, 70, 8)]):
        o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#8a8494" opacity="{.6 - k*.1:.2f}" stroke="{INK}" stroke-width="2"/>')
    o.append(stubby_legs(500, 780, 935, 55, 46, "#5a5466", foot_col="#6e6a5a", seed=2))
    o.append(part(tattered(500, 580, 860, 260, 400, seed=4, teeth=8, depth=50), cloak, sw=8))
    o.append(arm([(620, 620), (680, 560), (700, 480)], 44, 34, cloak, seed=3))
    o.append(hand(705, 470, 30, "#8e8a9c", angle=-80, seed=4, curl=1.0))
    o.append(arm([(380, 620), (320, 690), (330, 760)], 44, 34, cloak, seed=5))
    o.append(hand(335, 775, 28, "#8e8a9c", angle=90, seed=6, curl=.6))
    o.append(darkling_hood(490, 420, 220, cloak, seed=9, tip=(-90, -100)))
    # a pinched, smoking candle wick held up like a trophy
    o.append(part("M300,820 L330,820 L328,880 L302,880 Z", "#e9dfc4", sw=4, hatch=False))
    RIM["col"] = None
    return "\n".join(o), (490, 430, 290)


def moth(cx, cy, s, col, seed=0, face=False):
    r = random.Random(seed)
    a = r.uniform(-.5, .5)
    o = []
    for side in (-1, 1):
        w = catmull([(cx, cy), (cx + side * s * 1.1, cy - s * .9), (cx + side * s * 1.3, cy + s * .1), (cx + side * s * .4, cy + s * .5)], tension=.8)
        o.append(part(w, col, sw=3.5, hatch=False, texture=False, rim=False))
        o.append(f'<circle cx="{cx + side*s*.8:.1f}" cy="{cy - s*.2:.1f}" r="{s*.18:.1f}" fill="{shade(col,.5)}"/>')
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{s*.18:.1f}" ry="{s*.5:.1f}" fill="{INK}"/>')
    if face:
        o.append(f'<circle cx="{cx-s*.08:.1f}" cy="{cy-s*.2:.1f}" r="{s*.06:.1f}" fill="{GG}"/><circle cx="{cx+s*.08:.1f}" cy="{cy-s*.2:.1f}" r="{s*.06:.1f}" fill="{GG}"/>')
    return f'<g transform="rotate({math.degrees(a):.1f} {cx} {cy})">' + "\n".join(o) + "</g>"


def soul_moth_swarm():
    RIM["col"] = GG
    o = [ground_shadow(500, 950, 260, 30), glow(500, 520, 300, GG, .25)]
    r = random.Random(4)
    pts = []
    for k in range(70):
        a, d = r.uniform(0, 6.28), r.uniform(0, 1) ** .6
        pts.append((500 + math.cos(a) * 380 * d, 520 + math.sin(a) * 320 * d, r.uniform(22, 48)))
    pts.sort(key=lambda p: -p[2])
    for i, (x, y, s) in enumerate(pts):
        o.append(moth(x, y, s, r.choice(["#d9d2e6", "#c4bcd6", "#e8e2f0", "#b3a9c9"]), seed=i, face=s > 40))
    # the swarm's 'face': a gap in the moths with two soul-lights and a moth-mouth
    o.append(f'<ellipse cx="500" cy="470" rx="170" ry="110" fill="{INK}" opacity=".85"/>')
    o.append(eye(430, 455, 40, iris="#d6f3ff", pupil="none", glow_col=GG, white="#b9e6ff"))
    o.append(eye(570, 455, 40, iris="#d6f3ff", pupil="none", glow_col=GG, white="#b9e6ff"))
    o.append(flat(blob(500, 530, 60, 28, .2, 9, seed=6), "#0a0810", sw=4))
    for k in range(5):
        o.append(moth(470 + k * 15, 530, 10, "#cfc8d6", seed=50 + k))
    for (x, y) in [(330, 300), (690, 330), (300, 650), (720, 660)]:
        o.append(wisp(x, y, 16, GG, seed=x))
    RIM["col"] = None
    return "\n".join(o), (500, 480, 300)


def coven_crow():
    RIM["col"] = CG
    feather = "#22202a"
    o = [ground_shadow(500, 950, 200)]
    # skull perch
    o.append(part(blob(500, 860, 150, 110, .05, 12, seed=2), "#e9dfc4", sw=8, hatch=True))
    o.append(f'<ellipse cx="445" cy="860" rx="34" ry="30" fill="{INK}"/><ellipse cx="555" cy="860" rx="34" ry="30" fill="{INK}"/>')
    for x in range(430, 580, 30):
        o.append(f'<rect x="{x}" y="925" width="22" height="30" fill="#e9dfc4" stroke="{INK}" stroke-width="4"/>')
    # body + wings
    o.append(part(blob(500, 640, 190, 170, .06, 14, seed=3, squash=pear(.9, 1.05)), feather, sw=8, highlight=2.6))
    for side in (-1, 1):
        w = catmull([(500 + side * 120, 560), (500 + side * 300, 520), (500 + side * 360, 640), (500 + side * 280, 760), (500 + side * 140, 740)], tension=.8)
        o.append(part(w, feather, sw=7, highlight=2.6))
        for k in range(4):
            o.append(line([(500 + side * (180 + k * 40), 600 + k * 30), (500 + side * (220 + k * 40), 720 + k * 10)], sw=4, color="#4a4658"))
    for x in (440, 560):
        o.append(hand(x, 760, 22, "#3a3436", fingers=3, spread=70, angle=90, seed=x, claws="#d1a53a", curl=.3))
    # big head + beak
    o.append(part(blob(500, 360, 200, 180, .06, 14, seed=4), feather, sw=9, highlight=2.6))
    o.append(hair_strands(500, 210, 80, 20, 7, "#3a3640", seed=5, length=(40, 80), spread=(220, 320), sw=(6, 10)))
    o.append(part("M520,420 L760,470 L530,520 Z", "#c9b07a", sw=7, highlight=1.6, texture=False))
    o.append(line([(530, 470), (740, 472)], sw=4))
    o.append(eye(420, 360, 58, iris=CG, pupil="dot", look=(.4, 0), glow_col=CG))
    o.append(eye(570, 340, 40, iris=CG, pupil="dot", look=(.4, 0)))
    o.append(brow(350, 285, 470, 310, sw=12, bend=-6))
    # coven sigil: three-ring band on the leg
    o.append(f'<circle cx="560" cy="740" r="16" fill="none" stroke="{CG}" stroke-width="6"/>')
    RIM["col"] = None
    return "\n".join(o), (500, 420, 300)


def hollow_hound():
    RIM["col"] = GG
    skin = "#4a4652"
    o = [ground_shadow(500, 955, 360)]
    tail = [(760, 640), (860, 560), (900, 460)]
    o.append(part(tube(tail, 40, 10, seed=1), skin, sw=6))
    for x, s in [(650, 1), (750, 2)]:
        o.append(part(tube([(x, 680), (x + 10, 820), (x - 5, 920)], 54, 36, seed=s), shade(skin, .8), sw=6))
        o.append(hand(x, 925, 26, shade(skin, .8), fingers=3, spread=80, angle=90, seed=s, curl=.1))
    o.append(part(blob(650, 640, 220, 120, .06, 14, seed=3), skin, sw=8))
    for k in range(5):  # ribs
        o.append(line([(560 + k * 40, 590), (575 + k * 40, 690)], sw=6, opacity=.85))
    o.append(spikes_along([(470, 560), (600, 530), (760, 560)], 12, "#2a2630", side=-1, seed=2))
    for x, s in [(450, 3), (540, 4)]:
        o.append(part(tube([(x, 680), (x - 15, 820), (x - 10, 920)], 58, 40, seed=s), skin, sw=6))
        o.append(hand(x - 5, 925, 28, skin, fingers=3, spread=80, angle=90, seed=s, curl=.1))
    o.append(chain([(380, 560), (470, 640), (560, 590)], color="#8a8a90", link=20))
    # big gaunt head with iron jaw
    o.append(pointy_ear(250, 300, 120, 60, skin, side=-1, seed=3, droop=.9))
    o.append(pointy_ear(470, 280, 120, 60, skin, side=1, seed=4, droop=.9))
    o.append(part(blob(360, 420, 190, 170, .06, 14, seed=5), skin, sw=9))
    o.append(part("M200,470 L300,540 L520,540 L520,470 Z", "#6a6a72", sw=7, highlight=1.8, texture=False))  # iron jaw plate
    o.append(grin(360, 520, 300, 70, teeth=10, seed=6, curve=.3, tooth="#c9ccd0"))
    o.append(eye(300, 390, 48, iris="#d6f3ff", pupil="none", glow_col=GG, white="#b9e6ff"))
    o.append(eye(430, 385, 44, iris="#d6f3ff", pupil="none", glow_col=GG, white="#b9e6ff"))
    o.append(brow(240, 330, 340, 355, sw=13, bend=-4))
    o.append(brow(390, 350, 490, 325, sw=13, bend=-4))
    o.append(part(blob(250, 455, 40, 30, .1, 8, seed=2), "#1a1820", sw=5, hatch=False))
    RIM["col"] = None
    return "\n".join(o), (370, 430, 300)


def reptile_head(cx, cy, r, skin, *, seed=0, eye_col="#ffdc2e", helmet=None):
    o = [part(blob(cx, cy, r, r * .88, .05, 14, seed=seed, squash=pear(1.05, .9)), skin, sw=8)]
    rr = random.Random(seed)
    for _ in range(10):
        x, y = cx + rr.uniform(-r * .7, r * .7), cy + rr.uniform(-r * .6, r * .5)
        o.append(f'<path d="M{x-9},{y} q9,8 18,0" fill="none" stroke="{shade(skin,.5)}" stroke-width="3" opacity=".7"/>')
    o.append(eye(cx - r * .4, cy - r * .1, r * .28, iris=eye_col, pupil="slit", look=(.2, 0)))
    o.append(eye(cx + r * .4, cy - r * .1, r * .28, iris=eye_col, pupil="slit", look=(.2, 0)))
    o.append(brow(cx - r * .72, cy - r * .48, cx - r * .18, cy - r * .32, sw=10, bend=-4))
    o.append(brow(cx + r * .18, cy - r * .32, cx + r * .72, cy - r * .48, sw=10, bend=-4))
    o.append(grin(cx, cy + r * .38, r * 1.15, r * .32, teeth=4, seed=seed, fangs=(0, 3), missing=(1, 2), curve=.35, tongue="#c0304a"))
    o.append(f'<ellipse cx="{cx-r*.1}" cy="{cy+r*.2}" rx="5" ry="3" fill="{INK}"/><ellipse cx="{cx+r*.1}" cy="{cy+r*.2}" rx="5" ry="3" fill="{INK}"/>')
    if helmet:
        o.append(part(f"M{cx-r*1.02},{cy-r*.25} Q{cx},{cy-r*1.45} {cx+r*1.02},{cy-r*.25} Q{cx},{cy-r*.55} {cx-r*1.02},{cy-r*.25} Z", helmet, sw=7, highlight=1.7))
        o.append(spearhead(cx, cy - r * 1.05, -90, r * .12, color="#c9a83a"))
    return "\n".join(o)


def foot_soldier():
    RIM["col"] = AG
    skin, steel = "#7aa850", "#4c5a4a"
    o = [ground_shadow(500, 950, 240)]
    o.append(shaft(720, 940, 720, 120, w=20, color="#4a3420"))
    o.append(spearhead(720, 120, -90, 36, color="#9aa08a"))
    o.append(stubby_legs(500, 780, 940, 65, 56, skin, foot_col=steel, seed=4))
    o.append(armor_plate(500, 680, 150, 130, steel, seed=5))
    o.append(part(tube([(560, 800), (640, 870), (760, 880), (840, 840)], 50, 10, seed=2), skin, sw=6))  # tail
    o.append(arm([(620, 620), (690, 640), (715, 560)], 46, 38, skin, seed=6))
    o.append(hand(715, 545, 32, skin, angle=-160, seed=7, curl=1.0))
    o.append(arm([(380, 620), (320, 680)], 46, 40, skin, seed=8))
    o.append(part(blob(290, 700, 140, 150, .03, 14, seed=9), "#3e5a2e", sw=9, highlight=1.6))
    for k in range(3):
        o.append(f'<circle cx="290" cy="700" r="{40 + k*35}" fill="none" stroke="{INK}" stroke-width="4" opacity=".6"/>')
    o.append(part(blob(290, 700, 30, 30, .05, 8, seed=2), "#c9a83a", sw=5))
    o.append(reptile_head(500, 380, 190, skin, seed=3, helmet=steel))
    RIM["col"] = None
    return "\n".join(o), (500, 380, 280)


def broodling_slinger():
    RIM["col"] = AG
    skin = "#8cbc5a"
    o = [ground_shadow(500, 950, 200)]
    o.append(part(tube([(520, 860), (640, 900), (760, 870), (820, 800)], 60, 10, seed=1), skin, sw=6))
    o.append(stubby_legs(480, 800, 940, 50, 42, skin, seed=3))
    o.append(part(blob(480, 720, 120, 110, .06, 12, seed=4), "#4a3a2a", sw=7))
    o.append(arm([(560, 660), (650, 560), (700, 420)], 38, 30, skin, seed=5))
    o.append(hand(705, 405, 26, skin, angle=-90, seed=6, curl=1.0))
    # whirling sling with venom glob
    o.append(line([(705, 395), (790, 260), (870, 300)], sw=5, color="#7a5a3a"))
    o.append(f'<ellipse cx="820" cy="200" rx="150" ry="60" fill="none" stroke="{AG}" stroke-width="4" stroke-dasharray="14 12" opacity=".7"/>')
    o.append(part(blob(870, 300, 34, 30, .1, 8, seed=7), AG, sw=5, hatch=False))
    o.append(drips(850, 890, 325, AG, n=2, seed=2, length=(15, 30)))
    o.append(arm([(400, 660), (330, 720), (340, 790)], 38, 30, skin, seed=8))
    o.append(hand(345, 805, 26, skin, angle=90, seed=9, curl=.5))
    o.append(reptile_head(470, 420, 200, skin, seed=11, eye_col="#ffe55a"))
    o.append(f'<path d="M330,300 q60,-60 140,-50" fill="none" stroke="#e9dfc4" stroke-width="10"/>')  # eggshell cap
    o.append(part("M320,300 L360,230 L400,280 L440,210 L480,270 L520,215 L560,280 L610,250 L620,300 Q470,250 320,300 Z", "#e9dfc4", sw=5, hatch=False))
    RIM["col"] = None
    return "\n".join(o), (470, 420, 280)


def stone_adder():
    RIM["col"] = AG
    skin = "#8a8e7a"
    o = [ground_shadow(500, 955, 330)]
    body = [(150, 880), (330, 930), (560, 900), (720, 820), (700, 700), (520, 660), (400, 560), (420, 440)]
    o.append(part(tube(body, 120, 80, seed=3), skin, sw=8))
    rr = random.Random(2)
    for i in range(1, len(body) - 1):
        x, y = body[i]
        for _ in range(4):
            px, py = x + rr.uniform(-40, 40), y + rr.uniform(-30, 30)
            o.append(flat(blob(px, py, 14, 10, .2, 6, seed=rr.randint(0, 99)), shade(skin, .8), sw=2.5))
    for pts in ([(560, 900), (600, 860), (640, 870)], [(330, 930), (360, 890)]):
        o.append(line(pts, sw=4))
    o.append(part(blob(430, 360, 200, 150, .06, 14, seed=4, squash=pear(1.0, .9)), skin, sw=9))
    o.append(eye(360, 330, 52, iris="#ffe15a", pupil="slit", look=(.3, .1)))
    o.append(eye(500, 325, 48, iris="#ffe15a", pupil="slit", look=(.3, .1)))
    o.append(brow(290, 270, 400, 290, sw=12, bend=-4))
    o.append(brow(450, 285, 560, 265, sw=12, bend=-4))
    o.append(grin(440, 420, 260, 80, teeth=4, seed=5, fangs=(0, 3), missing=(1, 2), curve=.5, tongue="#c0304a", tooth="#d6d2c4"))
    o.append(drips(370, 510, 490, "#c9c8b0", n=3, seed=5, length=(25, 60)))
    o.append(line([(440, 500), (470, 590), (440, 620)], sw=8, color="#b0203a"))
    RIM["col"] = None
    return "\n".join(o), (440, 400, 280)


def basilisk_hatchling():
    RIM["col"] = AG
    skin, spike = "#6d8a52", "#2e3a22"
    o = [ground_shadow(500, 955, 330, 50)]
    tail = [(700, 760), (820, 720), (890, 640)]
    o.append(part(tube(tail, 90, 16, seed=1), skin, sw=7))
    for x, s in [(430, 1), (560, 2), (680, 3)]:
        o.append(part(tube([(x, 760), (x - 5, 880), (x, 925)], 56, 44, seed=s), shade(skin, .85), sw=6))
        o.append(hand(x, 930, 26, shade(skin, .85), fingers=3, spread=80, angle=90, seed=s, claws="#e9dfc4", curl=.1))
    o.append(part(blob(580, 720, 200, 120, .05, 14, seed=4), skin, sw=8))
    o.append(spikes_along([(420, 640), (560, 600), (700, 640)], 14, spike, side=-1, seed=3))
    # eggshell still stuck on the back
    o.append(part("M600,620 L640,560 L680,610 L720,550 L760,620 Q700,660 600,620 Z", "#e9dfc4", sw=5, hatch=False))
    o.append(part(blob(380, 480, 230, 200, .05, 16, seed=10), skin, sw=10))
    o.append(spikes_along([(200, 410), (300, 320), (440, 300), (560, 370)], 14, spike, side=-1, seed=6))
    o.append(glow(310, 450, 80, "#e8ff7a", .4))
    o.append(glow(460, 450, 70, "#e8ff7a", .4))
    o.append(eye(305, 460, 62, iris="#e8ff7a", pupil="slit", glow_col="#e8ff7a"))
    o.append(eye(465, 455, 56, iris="#e8ff7a", pupil="slit", glow_col="#e8ff7a"))
    o.append(grin(380, 580, 250, 60, teeth=8, seed=7, curve=.5, tongue="#a02a3a"))
    RIM["col"] = None
    return "\n".join(o), (390, 480, 290)


def coven_toad():
    RIM["col"] = CG
    skin = "#6b7a3a"
    o = [ground_shadow(500, 955, 380, 60)]
    for side in (-1, 1):
        o.append(part(tube([(500 + side * 250, 760), (500 + side * 360, 850), (500 + side * 330, 930)], 110, 60, seed=side), skin, sw=8))
        o.append(hand(500 + side * 340, 935, 40, skin, fingers=4, spread=110, angle=90, seed=side + 3, claws="#3a3a20", curl=.05))
    o.append(part(blob(500, 640, 360, 270, .05, 18, seed=3, squash=pear(.85, 1.08)), skin, sw=10))
    o.append(part(blob(500, 760, 230, 120, .05, 12, seed=4), "#c9c27a", sw=6, hatch=False))
    o.append(warts(500, 600, 320, 220, 14, shade(skin, 1.2), seed=5, size=(10, 22)))
    o.append(f'<path d="{blob(500, 620, 330, 240, .05, 18, seed=3)}" fill="#ff9adf" opacity=".12" filter="url(#mottle)"/>')  # hallucinogenic sheen
    # saddle with coven sigil
    o.append(part("M380,410 Q500,340 620,410 L610,470 Q500,430 390,470 Z", "#4a2a3a", sw=7))
    for k, x in enumerate((470, 500, 530)):
        o.append(f'<circle cx="{x}" cy="{420 + (k == 1) * -14}" r="14" fill="none" stroke="{CG}" stroke-width="5"/>')
    # eyes on top, wide mouth, tongue lash
    for x in (330, 670):
        o.append(part(blob(x, 430, 80, 70, .05, 10, seed=x), skin, sw=8))
        o.append(eye(x, 425, 56, iris="#ffb02a", pupil="slit", look=(.0, .2), lid=.35))
    o.append(line([(200, 600), (500, 680), (800, 600)], sw=10))
    o.append(part(tube([(700, 620), (820, 560), (900, 480), (930, 400)], 40, 24, seed=7), "#d0607a", sw=6, hatch=False))
    o.append(part(blob(935, 385, 38, 30, .1, 8, seed=8), "#d0607a", sw=5, hatch=False))
    RIM["col"] = None
    return "\n".join(o), (500, 520, 360)


def petrified_thrall():
    RIM["col"] = AG
    stone = "#8f8f88"
    o = [ground_shadow(500, 950, 260)]
    o.append(stubby_legs(500, 770, 945, 75, 70, stone, foot_col=shade(stone, .8), seed=3))
    o.append(part(blob(500, 650, 200, 170, .05, 14, seed=4, squash=pear(.9, 1.05)), stone, sw=9))
    o.append(f'<path d="{blob(500, 650, 200, 170, .05, 14, seed=4)}" fill="url(#xhatch)" opacity=".35"/>')
    for pts in ([(420, 560), (470, 620), (440, 700), (490, 760)], [(560, 590), (600, 660)], [(380, 700), (420, 740)]):
        o.append(line(pts, sw=5))
    # mossy patches and a carved coven brand
    for (x, y) in [(600, 720), (420, 600)]:
        o.append(part(blob(x, y, 40, 22, .3, 8, seed=x), "#4f6b2a", sw=4, hatch=False, rim=False))
    for k, x in enumerate((470, 500, 530)):
        o.append(f'<circle cx="{x}" cy="{660 + (k == 1) * -14}" r="14" fill="none" stroke="{INK}" stroke-width="5"/>')
    # reaching arms for the embrace
    for side, seed in ((-1, 6), (1, 7)):
        o.append(arm([(500 + side * 170, 580), (500 + side * 290, 540), (500 + side * 330, 430)], 80, 64, stone, seed=seed))
        o.append(hand(500 + side * 335, 400, 52, stone, angle=-90 + side * 20, spread=90, seed=seed, claws="#6a6a64", curl=.4))
    # sad stone face, mouth frozen mid-scream
    o.append(part(blob(500, 360, 180, 170, .05, 14, seed=8), stone, sw=9))
    o.append(f'<path d="{blob(500, 360, 180, 170, .05, 14, seed=8)}" fill="url(#xhatch)" opacity=".3"/>')
    o.append(eye(430, 340, 40, iris="#9a9a94", pupil="none", white="#b4b4ae"))
    o.append(eye(570, 340, 40, iris="#9a9a94", pupil="none", white="#b4b4ae"))
    o.append(brow(380, 300, 470, 280, sw=12, bend=6))
    o.append(brow(530, 280, 620, 300, sw=12, bend=6))
    o.append(flat(blob(500, 450, 60, 50, .1, 10, seed=3), "#3a3a36", sw=7))
    o.append(line([(560, 220), (600, 300), (580, 360)], sw=5))
    o.append(f'<path d="M420,380 q-6,40 -2,60" fill="none" stroke="{AG}" stroke-width="5" opacity=".6"/>')  # a green tear
    RIM["col"] = None
    return "\n".join(o), (500, 400, 300)


def bone_thrower():
    RIM["col"] = FG
    gob = "#8aa04a"
    o = [ground_shadow(500, 950, 220)]
    o.append(stubby_legs(500, 820, 945, 55, 44, gob, foot_col="#5a3a22", seed=2, feet="claw"))
    o.append(part(tattered(500, 640, 860, 200, 300, seed=3, teeth=6, depth=30), "#5a3a22", sw=7))
    for k in range(4):  # bone bandolier
        o.append(part(tube([(410 + k * 50, 650 + k * 30), (440 + k * 50, 670 + k * 30)], 14, 14), "#e9dfc4", sw=4, hatch=False, texture=False))
    o.append(arm([(580, 660), (680, 580), (740, 460)], 36, 28, gob, seed=4))
    o.append(hand(745, 445, 26, gob, angle=-90, seed=5, curl=1.0))
    o.append(line([(745, 435), (830, 290), (900, 340)], sw=5, color="#d9b9a0"))
    o.append(part(tube([(880, 330), (930, 350)], 22, 22), "#e9dfc4", sw=5, hatch=False))
    for a in range(-40, 50, 30):
        r_ = math.radians(a - 60)
        o.append(line([(830 + math.cos(r_) * 120, 300 + math.sin(r_) * 120), (830 + math.cos(r_) * 160, 300 + math.sin(r_) * 160)], sw=6, color=FG))
    o.append(arm([(420, 660), (340, 700), (330, 780)], 36, 28, gob, seed=6))
    o.append(hand(330, 800, 26, gob, angle=90, seed=7, curl=.6))
    o.append(goblin_head(500, 420, 165, gob, seed=13, eye_col="#ffcf3a", look=(.5, -.2)))
    o.append(part(blob(500, 270, 120, 40, .1, 10, seed=4), "#5a3a22", sw=6))  # skullcap
    RIM["col"] = None
    return "\n".join(o), (500, 430, 280)


def troll_whelp():
    RIM["col"] = FG
    skin = "#7a9a62"
    o = [ground_shadow(500, 950, 250)]
    o.append(stubby_legs(500, 790, 945, 75, 70, skin, seed=3, feet="claw"))
    o.append(part(blob(500, 680, 170, 150, .06, 12, seed=4, squash=pear(.85, 1.1)), skin, sw=9))
    o.append(part(tattered(500, 700, 840, 260, 300, seed=2, teeth=6, depth=30), "#5a3a22", sw=7))
    for side, seed in ((-1, 5), (1, 6)):
        o.append(arm([(500 + side * 150, 600), (500 + side * 250, 680), (500 + side * 250, 800)], 66, 52, skin, seed=seed))
        o.append(hand(500 + side * 255, 830, 42, skin, angle=90 + side * 10, spread=100, seed=seed, curl=.3))
    # gnawed bone
    o.append(part(tube([(640, 860), (760, 900)], 22, 22), "#e9dfc4", sw=5, hatch=False))
    o.append(troll_head(500, 380, 200, skin, seed=19, mood="grin", eye_col="#ffcf3a", tusks=True))
    o.append(drips(440, 560, 470, "#cfe8d6", n=2, seed=6, length=(25, 50)))
    RIM["col"] = None
    return "\n".join(o), (500, 400, 290)


def bugbear():
    RIM["col"] = FG
    fur, skin = "#7a4a2a", "#b0784a"
    o = [ground_shadow(500, 950, 280)]
    # sack over shoulder with kicking feet
    o.append(part(blob(720, 380, 150, 170, .1, 12, seed=1, rot=.4), "#a08a5a", sw=8))
    o.append(line([(630, 260), (680, 300), (650, 330)], sw=8))
    for k, (x, y) in enumerate([(790, 230), (840, 270)]):
        o.append(part(tube([(x - 20, y + 40), (x, y)], 30, 26, seed=k), "#e0b48a", sw=5, hatch=False))
        o.append(part(blob(x + 6, y - 12, 26, 16, .1, 7, seed=k), "#4a2a1a", sw=4, hatch=False))
    o.append(stubby_legs(500, 790, 945, 80, 70, fur, foot_col="#3a2a1a", seed=3))
    o.append(part(blob(500, 680, 190, 160, .06, 14, seed=4, squash=pear(.85, 1.1)), fur, sw=9))
    o.append(hair_strands(500, 640, 180, 150, 18, shade(fur, .8), seed=4, length=(20, 40), spread=(0, 360), sw=(3, 5)))
    o.append(arm([(650, 600), (700, 480), (680, 360)], 64, 50, fur, seed=5))
    o.append(hand(675, 345, 40, skin, angle=-100, seed=6, curl=1.0))
    o.append(arm([(350, 600), (280, 700), (260, 790)], 64, 50, fur, seed=7))
    o.append(shaft(250, 820, 140, 560, w=20, color="#5a3a22"))
    o.append(part(blob(130, 520, 60, 60, .05, 10, seed=2), "#4a4440", sw=7, highlight=1.7))
    for a in range(0, 360, 45):
        r_ = math.radians(a)
        o.append(flat(poly([(130 + math.cos(r_ - .3) * 52, 520 + math.sin(r_ - .3) * 52), (130 + math.cos(r_) * 88, 520 + math.sin(r_) * 88),
                            (130 + math.cos(r_ + .3) * 52, 520 + math.sin(r_ + .3) * 52)]), "#7a7470", sw=3))
    o.append(hand(255, 805, 40, skin, angle=60, seed=8, curl=.9))
    # furry head, bear ears, sly grin
    for x in (350, 640):
        o.append(part(blob(x, 230, 55, 50, .1, 9, seed=x), fur, sw=7))
        o.append(part(blob(x, 235, 28, 24, .1, 8, seed=x + 1), skin, sw=4, hatch=False))
    o.append(part(blob(495, 380, 190, 170, .06, 14, seed=9), fur, sw=9))
    o.append(hair_strands(495, 380, 185, 165, 22, shade(fur, .75), seed=9, length=(20, 45), spread=(0, 360), sw=(3, 6)))
    o.append(part(blob(495, 440, 120, 80, .06, 10, seed=10), skin, sw=7))
    o.append(eye(430, 360, 40, iris="#ffcf3a", pupil="dot", look=(.4, 0), lid=.3))
    o.append(eye(560, 355, 38, iris="#ffcf3a", pupil="dot", look=(.4, 0), lid=.3))
    o.append(part(blob(495, 410, 34, 24, .1, 8, seed=11), "#2a1a12", sw=5, hatch=False))
    o.append(grin(495, 455, 190, 45, teeth=7, seed=12, fangs=(0, 6), curve=.6))
    RIM["col"] = None
    return "\n".join(o), (495, 390, 290)


def ogre_log_ram():
    RIM["col"] = FG
    skin = "#a08a6a"
    o = [ground_shadow(500, 955, 360)]
    o.append(stubby_legs(500, 800, 945, 110, 100, skin, foot_col="#5a3a22", seed=3))
    o.append(part(blob(500, 680, 280, 200, .06, 14, seed=4, squash=pear(.85, 1.08)), skin, sw=10))
    o.append(part(tattered(500, 700, 850, 380, 420, seed=5, teeth=8, depth=40), "#5a4a2a", sw=8))
    # the log, carried under one arm like a ram
    o.append(part(tube([(120, 560), (500, 600), (930, 640)], 120, 110, seed=6), "#6a4a2a", sw=9))
    for x in range(180, 900, 90):
        o.append(line([(x, 545 + (x - 120) * .1), (x + 30, 600 + (x - 120) * .1)], sw=4, opacity=.7))
    o.append(f'<ellipse cx="940" cy="640" rx="40" ry="56" fill="#b08a5a" stroke="{INK}" stroke-width="7"/>')
    for r_ in (14, 26, 38):
        o.append(f'<ellipse cx="940" cy="640" rx="{r_*.7}" ry="{r_}" fill="none" stroke="{INK}" stroke-width="3" opacity=".7"/>')
    for x in (300, 700):
        o.append(hand(x, 560, 54, skin, angle=-90, spread=90, seed=x, curl=1.1))
    # small dim head on a huge body
    o.append(part(blob(500, 340, 170, 150, .06, 14, seed=9, squash=pear(.9, 1.15)), skin, sw=9))
    o.append(hair_locks(500, 230, 120, 40, 6, "#3a2a1a", seed=3, length=(40, 90), spread=(200, 340), width=(14, 22), droop=2))
    o.append(eye(440, 320, 30, iris="#c9a83a", pupil="dot", look=(-.3, .3)))
    o.append(eye(560, 322, 22, iris="#c9a83a", pupil="dot", look=(.3, .3)))
    o.append(brow(400, 280, 470, 275, sw=12, bend=-4))
    o.append(grin(500, 410, 220, 60, teeth=6, seed=10, missing=(1, 4), curve=.3))
    o.append(nose_bulb(500, 320, 60, 60, skin, hook=-.2, seed=4))
    for side in (-1, 1):
        o.append(flat(f"M{500 + side*70},450 Q{500 + side*80},390 {500 + side*100},380 Q{500 + side*90},420 {500 + side*90},450 Z", "#efe4c0", sw=4))
    RIM["col"] = None
    return "\n".join(o), (500, 360, 290)


def coven_bogle():
    RIM["col"] = CG
    mud = "#5a4a32"
    o = [ground_shadow(500, 955, 300, 50)]
    o.append(part(blob(500, 900, 300, 60, .15, 14, seed=2), shade(mud, .8), sw=7, hatch=False))  # mud puddle
    o.append(bubbles(500, 890, 250, 25, 6, shade(mud, 1.2), seed=3, size=(6, 14)))
    body = catmull([(330, 900), (300, 700), (350, 520), (500, 470), (650, 520), (700, 700), (670, 900)], tension=.8)
    o.append(part(body, mud, sw=9))
    o.append(drips(330, 670, 860, shade(mud, .9), n=6, seed=4, length=(20, 60)))
    o.append(arm([(640, 600), (740, 540), (790, 450)], 54, 44, mud, seed=5))
    o.append(part(blob(800, 410, 56, 50, .2, 10, seed=6), shade(mud, .7), sw=7))
    o.append(drips(770, 830, 450, shade(mud, .7), n=2, seed=7, length=(20, 40)))
    o.append(arm([(360, 600), (270, 660), (260, 760)], 54, 44, mud, seed=8))
    o.append(hand(260, 780, 34, mud, angle=90, seed=9, curl=.5, claws="#2a2016"))
    # head: lumpy mud with shiny-tooth collection
    o.append(part(blob(500, 360, 200, 170, .1, 14, seed=10), mud, sw=9))
    o.append(warts(500, 330, 170, 130, 8, shade(mud, 1.15), seed=11, size=(8, 18)))
    o.append(eye(430, 350, 48, iris=CG, pupil="dot", look=(.4, 0)))
    o.append(eye(570, 340, 54, iris=CG, pupil="dot", look=(.4, 0)))
    o.append(grin(500, 440, 230, 60, teeth=9, seed=12, missing=(2, 5), curve=.6, tooth="#f2e6b0"))
    for k in range(5):  # necklace of stolen gold teeth
        o.append(flat(f"M{420 + k*40},530 l10,0 l-5,24 Z", "#e8c23a", sw=3))
    o.append(part(blob(500, 210, 60, 26, .2, 8, seed=13), "#4f6b2a", sw=5, hatch=False))  # pondweed tuft
    RIM["col"] = None
    return "\n".join(o), (500, 400, 300)


def archfey_husk():
    RIM["col"] = CG
    glass, robe = "#c9d6e6", "#3a3048"
    o = [ground_shadow(500, 955, 200, 26), glow(500, 500, 320, CG, .2)]
    # hovering tattered court robe
    o.append(part(tattered(500, 520, 900, 300, 520, seed=3, teeth=12, depth=80), robe, sw=8))
    o.append(folds(500, 580, 880, 420, n=6, seed=3, color=shade(robe, 1.5)))
    for k in range(6):  # gold embroidery remnants
        o.append(f'<circle cx="{350 + k*60}" cy="600" r="10" fill="#c9a83a" stroke="{INK}" stroke-width="3"/>')
    o.append(chain([(260, 560), (500, 760), (740, 560)], color="#8a8a90", link=22))
    o.append(chain([(320, 820), (500, 900), (690, 820)], color="#8a8a90", link=22))
    # glass talons
    for side, seed in ((-1, 4), (1, 5)):
        o.append(arm([(500 + side * 140, 560), (500 + side * 260, 520), (500 + side * 300, 420)], 44, 34, robe, seed=seed))
        o.append(hand(500 + side * 305, 395, 40, glass, angle=-90 + side * 15, spread=100, seed=seed, claws="#e9f6ff", curl=.2))
    # cracked glass face, hollow glowing eyes
    o.append(pointy_ear(320, 360, 160, 60, glass, side=-1, seed=2, droop=.5))
    o.append(pointy_ear(680, 360, 160, 60, glass, side=1, seed=3, droop=.5))
    o.append(part(blob(500, 360, 175, 190, .03, 14, seed=6, squash=pear(1.0, .85)), glass, sw=8, highlight=1.9))
    for pts in ([(430, 200), (470, 290), (440, 350), (480, 420)], [(560, 230), (600, 300)], [(520, 470), (560, 520), (540, 540)]):
        o.append(line(pts, sw=4))
    o.append(eye(430, 360, 46, iris=CG, pupil="none", glow_col=CG, white="#1a1420"))
    o.append(eye(570, 360, 46, iris=CG, pupil="none", glow_col=CG, white="#1a1420"))
    o.append(flat(blob(500, 470, 50, 40, .1, 9, seed=7), "#1a1420", sw=6))
    # broken crown
    o.append(part("M370,200 L400,110 L440,180 L480,90 L520,170 L560,100 L590,180 L620,130 L630,210 Q500,170 370,200 Z", "#c9a83a", sw=6, highlight=1.8))
    o.append(line([(480, 90), (500, 150)], sw=4))
    for (x, y) in [(400, 110), (560, 100)]:
        o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#9fe8ff" stroke="{INK}" stroke-width="3"/>')
    RIM["col"] = None
    return "\n".join(o), (500, 360, 290)
