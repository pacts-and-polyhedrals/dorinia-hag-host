import math, random
from engine import *
from creatures import PAL
from c_auntie import coil  # noqa

F = PAL["Gaga"]["glow"]
TROLL = "#6f8a62"


def gahgah():
    RIM["col"] = F
    skin, rags = "#6a8060", "#5a3a22"
    o = [ground_shadow(500, 955, 400)]
    o.append(stubby_legs(500, 790, 945, 130, 110, skin, seed=2, feet="claw"))
    # massive hunched body
    o.append(part(blob(500, 680, 340, 230, .06, 16, seed=3, squash=pear(.85, 1.05)), skin, sw=10))
    o.append(warts(500, 700, 280, 170, 10, shade(skin, .8), seed=4))
    o.append(part(tattered(500, 700, 850, 480, 560, seed=5, teeth=10, depth=50), rags, sw=8))
    o.append(folds(500, 720, 850, 480, n=6, seed=5))
    o.append(scars(380, 640, 90, 30))
    # knuckle-dragging arms
    for side, seed in ((-1, 6), (1, 7)):
        pts = [(500 + side * 290, 590), (500 + side * 400, 700), (500 + side * 400, 860)]
        o.append(part(tube(pts, 120, 90, seed=seed), skin, sw=9))
        o.append(hand(500 + side * 400, 890, 70, skin, angle=90 + side * 20, spread=110, seed=seed, curl=.3))
    # victim held in one claw (a tiny adventurer's boot)
    o.append(part(blob(130, 930, 34, 20, .1, 8, seed=2), "#4a2a1a", sw=5, hatch=False))
    # two heads
    o.append(troll_head(330, 360, 175, skin, seed=11, mood="roar", eye_col="#ff8a2a"))
    o.append(troll_head(670, 380, 160, skin, seed=21, mood="grin", eye_col="#ffcf3a"))
    o.append(f'<circle cx="760" cy="300" r="14" fill="none" stroke="#d1a53a" stroke-width="6"/>')
    # bone & skull trophies on the shoulders
    o.append(part(blob(500, 520, 52, 46, .06, 9, seed=3), "#e9dfc4", sw=6, hatch=False))
    o.append(f'<circle cx="482" cy="515" r="12" fill="{INK}"/><circle cx="518" cy="515" r="12" fill="{INK}"/>')
    o.append(line([(470, 548), (530, 548)], sw=4))
    RIM["col"] = None
    return "\n".join(o), (500, 380, 360)


def linebreaker():
    RIM["col"] = F
    skin, iron = TROLL, "#4a4440"
    o = [ground_shadow(500, 955, 320)]
    # hooked maul over shoulder
    o.append(shaft(330, 780, 820, 180, w=28, color="#4a3020"))
    o.append(part("M740,110 L900,190 L860,300 L700,220 Z", iron, sw=9, highlight=1.7))
    o.append(part("M880,240 Q980,240 960,340 Q930,300 880,300 Z", "#7a7470", sw=6, highlight=1.8, texture=False))
    o.append(drips(720, 880, 270, "#7a1a1a", n=3, seed=5, length=(20, 60)))
    o.append(stubby_legs(500, 790, 945, 100, 90, skin, seed=3, feet="claw"))
    o.append(part(blob(500, 660, 270, 210, .06, 14, seed=4, squash=pear(.85, 1.05)), skin, sw=10))
    o.append(armor_plate(430, 680, 140, 110, iron, seed=5))
    o.append(armor_plate(640, 560, 90, 70, iron, seed=6, rivets=False))
    o.append(chain([(300, 600), (500, 760), (700, 600)], link=22))
    o.append(arm([(720, 580), (760, 450), (700, 360)], 90, 70, skin, seed=7))
    o.append(hand(690, 340, 56, skin, angle=-120, seed=8, curl=1.0))
    o.append(arm([(280, 600), (210, 720), (250, 830)], 90, 70, skin, seed=9))
    o.append(hand(260, 860, 56, skin, angle=90, seed=10, curl=.4))
    o.append(troll_head(470, 330, 200, skin, seed=13, mood="roar", eye_col="#ffcf3a"))
    o.append(part(blob(470, 150, 150, 40, .08, 10, seed=4), iron, sw=7, highlight=1.6))  # dented helm band
    RIM["col"] = None
    return "\n".join(o), (470, 360, 310)


def flesh_mender():
    RIM["col"] = F
    skin, apron = "#7a9068", "#c9b89a"
    o = [ground_shadow(500, 955, 300)]
    o.append(stubby_legs(500, 790, 945, 95, 84, skin, seed=4, feet="claw"))
    o.append(part(blob(500, 660, 260, 210, .06, 14, seed=5, squash=pear(.85, 1.05)), skin, sw=10))
    ap = catmull([(350, 570), (500, 545), (650, 570), (640, 720), (660, 880), (500, 900), (340, 880), (360, 720)], tension=.7)
    o.append(part(ap, apron, sw=8))
    cid = uid("ap")
    o.append(f'<clipPath id="{cid}"><path d="{ap}"/></clipPath><g clip-path="url(#{cid})">')
    for (x, y, s_, sd) in [(430, 660, 55, 1), (575, 750, 42, 2), (470, 830, 30, 3), (610, 610, 22, 4)]:
        o.append(f'<path d="{blob(x, y, s_, s_*.8, .35, 12, seed=sd)}" fill="#7a1018" opacity=".8"/>')
        o.append(drips(x - s_ * .5, x + s_ * .5, y + s_ * .5, "#7a1018", n=2, seed=sd, length=(20, 60)))
    o.append("</g>")
    o.append(line([(350, 570), (290, 540)], sw=8)); o.append(line([(650, 570), (710, 540)], sw=8))
    o.append(drips(370, 630, 878, "#8a1a22", n=4, seed=3, length=(15, 45)))
    # stitched arm holding needle & gut thread
    o.append(arm([(280, 600), (200, 680), (230, 760)], 84, 66, skin, seed=6))
    for k in range(4):
        y = 640 + k * 30
        o.append(line([(190 + k * 5, y), (250 + k * 5, y + 10)], sw=4))
        o.append(line([(205 + k * 5, y - 8), (215 + k * 5, y + 18)], sw=3))
        o.append(line([(235 + k * 5, y - 4), (240 + k * 5, y + 22)], sw=3))
    o.append(hand(240, 790, 50, skin, angle=60, seed=7, curl=.9))
    o.append(line([(260, 800), (330, 880)], sw=10))
    o.append(line([(260, 800), (330, 880)], sw=4, color="#c9ccd0"))
    o.append(line([(330, 880), (380, 920), (300, 940), (200, 920)], sw=4, color="#d9b9a0"))
    # bone saw
    o.append(arm([(720, 590), (790, 500), (780, 420)], 84, 66, skin, seed=8))
    o.append(part("M760,400 L780,160 L870,140 L860,390 Z", "#9aa0a8", sw=7, highlight=1.8, texture=False))
    for k in range(9):
        y = 165 + k * 26
        o.append(flat(poly([(780 - k * .4, y), (760 - k * .4, y + 13), (780 - k * .4, y + 26)]), "#9aa0a8", sw=3))
    o.append(drips(780, 860, 380, "#8a1a22", n=2, seed=1, length=(20, 50)))
    o.append(part(blob(810, 420, 40, 26, .05, 8, seed=3), "#e9dfc4", sw=6, hatch=False))
    o.append(hand(800, 410, 52, skin, angle=-100, seed=9, curl=1.1))
    o.append(troll_head(480, 330, 190, skin, seed=17, mood="grin", eye_col="#ffcf3a", tusks=False))
    # monocle + stitched scalp
    o.append(f'<circle cx="548" cy="290" r="48" fill="#bfe3e6" fill-opacity=".35" stroke="#c9a83a" stroke-width="9"/>')
    o.append(line([(590, 320), (640, 420), (620, 500)], sw=3, color="#c9a83a"))
    o.append(line([(360, 200), (480, 160), (600, 190)], sw=6))
    for x in range(380, 600, 28):
        o.append(line([(x, 170 + abs(x - 480) * .12), (x + 6, 200 + abs(x - 480) * .12)], sw=4))
    RIM["col"] = None
    return "\n".join(o), (480, 350, 300)


def snail_lancer():
    RIM["col"] = "#9fe8ff"
    snail_skin, cloak = "#a08a6a", "#24202c"
    o = [ground_shadow(500, 955, 380)]
    # snail foot/body
    foot = catmull([(110, 940), (130, 820), (230, 760), (420, 790), (700, 800), (880, 860), (900, 940)], tension=.8)
    o.append(part(foot, snail_skin, sw=9))
    o.append(f'<path d="M110,940 Q500,960 900,940" fill="none" stroke="#cfe8d6" stroke-width="10" opacity=".55"/>')  # slime
    # snail head with eyestalks
    o.append(part(tube([(220, 800), (160, 680), (150, 600)], 120, 90, seed=3), snail_skin, sw=8))
    for x0, x1 in ((130, 60), (175, 210)):
        o.append(part(tube([(x0, 590), ((x0 + x1) / 2, 520), (x1, 440)], 26, 18, seed=x0), snail_skin, sw=6))
        o.append(eye(x1, 430, 30, iris="#ffcf3a", pupil="dot", look=(.3, 0)))
    o.append(grin(155, 690, 90, 26, teeth=5, seed=4, curve=.2))
    # glittering shell
    o.append(spiral_shell(560, 620, 230, "#6a5a8a", "#c9b0ff", seed=5, gems="#9fe8ff"))
    # saddle + darkling rider
    o.append(part("M480,410 Q560,370 650,410 L640,450 Q560,430 490,450 Z", "#5a2a2a", sw=7))
    o.append(part(tattered(565, 300, 440, 170, 240, seed=6, teeth=6, depth=30), cloak, sw=7))
    o.append(arm([(500, 330), (440, 360), (400, 330)], 40, 32, cloak, seed=6))
    # blackglass lance couched forward
    o.append(shaft(640, 380, 120, 230, w=20, color="#1a1620"))
    o.append(part(poly([(140, 210), (40, 220), (140, 260)]), "#2a2440", sw=6, highlight=2.0, texture=False))
    o.append(glow(80, 230, 40, "#b06bff", .5))
    o.append(hand(400, 320, 30, "#5a5466", angle=200, seed=7, curl=.8))
    o.append(darkling_hood(560, 220, 120, cloak, seed=8, tip=(70, -40)))
    RIM["col"] = None
    return "\n".join(o), (420, 470, 360)


def flail_snail():
    RIM["col"] = "#c9b0ff"
    skin = "#8a9a7a"
    o = [ground_shadow(500, 955, 400)]
    foot = catmull([(140, 940), (160, 830), (300, 770), (600, 780), (860, 830), (900, 940)], tension=.8)
    o.append(part(foot, skin, sw=9))
    o.append(f'<path d="M140,940 Q500,960 900,940" fill="none" stroke="#e8d0ff" stroke-width="10" opacity=".5"/>')
    o.append(spiral_shell(620, 560, 270, "#4a3a6a", "#e8d0ff", seed=9, gems="#e8d0ff"))
    # antimagic shimmer
    o.append(f'<ellipse cx="620" cy="560" rx="300" ry="290" fill="none" stroke="#e8d0ff" stroke-width="4" stroke-dasharray="20 18" opacity=".6"/>')
    # head
    o.append(part(blob(260, 720, 170, 140, .06, 12, seed=4), skin, sw=9))
    o.append(eye(210, 700, 46, iris="#ff7a2a", pupil="slit", look=(-.2, .1), lid=.25))
    o.append(eye(320, 695, 40, iris="#ff7a2a", pupil="slit", look=(-.2, .1), lid=.25))
    o.append(brow(160, 640, 260, 665, sw=14, bend=-4))
    o.append(brow(280, 660, 370, 640, sw=14, bend=-4))
    o.append(grin(260, 780, 170, 50, teeth=7, seed=5, fangs=(1, 5), missing=(3,), curve=.5))
    # flail tentacles
    rr = random.Random(3)
    for k, (tx, ty) in enumerate([(90, 380), (220, 300), (360, 330), (60, 560)]):
        base = (230 + k * 30, 600)
        mid = ((base[0] + tx) / 2 + rr.uniform(-60, 60), (base[1] + ty) / 2 - 40)
        o.append(part(tube([base, mid, (tx, ty)], 40, 24, seed=k), skin, sw=7))
        o.append(part(blob(tx, ty, 46, 46, .05, 10, seed=k), "#5a5660", sw=7, highlight=1.8, texture=False))
        for a in range(0, 360, 45):
            r_ = math.radians(a)
            o.append(flat(poly([(tx + math.cos(r_ - .3) * 40, ty + math.sin(r_ - .3) * 40), (tx + math.cos(r_) * 70, ty + math.sin(r_) * 70),
                                (tx + math.cos(r_ + .3) * 40, ty + math.sin(r_ + .3) * 40)]), "#8a8690", sw=3.5))
    RIM["col"] = None
    return "\n".join(o), (420, 560, 400)


def spider_rider():
    RIM["col"] = F
    gob, spider = "#8aa04a", "#2a2226"
    o = [ground_shadow(500, 955, 380)]
    o.append(spider_legs(500, 720, 430, spider, seed=3))
    # spider abdomen & body
    o.append(part(blob(560, 700, 230, 170, .05, 14, seed=4), spider, sw=9))
    o.append(part(blob(560, 700, 60, 90, .1, 8, seed=5), "#a02a2a", sw=5, hatch=False))  # hourglass mark
    rr = random.Random(5)
    for _ in range(26):
        a = rr.uniform(3.4, 6.0)
        x, y = 560 + math.cos(a) * 225, 700 + math.sin(a) * 165
        o.append(line([(x, y), (x + math.cos(a) * 20, y + math.sin(a) * 20)], sw=3))
    # spider head with cluster eyes + fangs
    o.append(part(blob(330, 760, 120, 100, .05, 12, seed=6), spider, sw=8))
    for (x, y, r) in [(290, 740, 22), (340, 730, 26), (390, 745, 20), (310, 780, 14), (365, 778, 14), (270, 770, 10)]:
        o.append(eye(x, y, r, iris="#ff3a2a", pupil="none", white="#ff6a4a"))
    for x in (300, 360):
        o.append(flat(f"M{x-12},820 Q{x-20},870 {x+5},900 Q{x+2},860 {x+12},825 Z", "#e6d9b6", sw=4))
    o.append(drips(300, 365, 895, "#9dff3a", n=2, seed=4, length=(15, 30)))
    # saddle + goblin
    o.append(part("M470,560 Q560,520 660,560 L650,600 Q560,580 480,600 Z", "#6a4a22", sw=7))
    o.append(part(blob(560, 510, 90, 80, .06, 10, seed=7), "#5a3a22", sw=7))
    o.append(arm([(500, 480), (420, 420), (370, 380)], 34, 28, gob, seed=7))
    o.append(shaft(620, 470, 170, 230, w=16, color="#5a3a22"))
    o.append(spearhead(170, 230, 208, 30, color="#8a8a84", barbed=True))
    o.append(part(blob(200, 250, 24, 20, .15, 8, seed=2), "#6a5a2a", sw=4, hatch=False))  # dung lump
    o.append(hand(370, 370, 26, gob, angle=200, seed=8, curl=.8))
    o.append(goblin_head(560, 350, 120, gob, seed=9, eye_col="#ffcf3a", look=(-.4, 0)))
    for x in (520, 600):  # goggles
        o.append(f'<circle cx="{x}" cy="260" r="26" fill="#3a2a1e" stroke="{INK}" stroke-width="6"/>'
                 f'<circle cx="{x}" cy="260" r="16" fill="#ffcf3a" opacity=".6"/>')
    o.append(line([(470, 265), (650, 265)], sw=8))
    RIM["col"] = None
    return "\n".join(o), (480, 520, 380)


def rage_drum():
    RIM["col"] = F
    gob = "#8aa04a"
    o = [ground_shadow(500, 955, 260)]
    o.append(stubby_legs(500, 820, 945, 70, 56, gob, foot_col="#5a3a22", seed=5, feet="claw"))
    o.append(part(blob(500, 700, 150, 130, .06, 12, seed=4), "#5a3a22", sw=8))
    # huge drum
    o.append(part("M300,640 L700,640 L680,880 L320,880 Z", "#7a4a2a", sw=9))
    o.append(part(blob(500, 640, 205, 55, .02, 14, seed=5), "#e3d2a8", sw=8, hatch=False))
    for k in range(7):
        x = 320 + k * 60
        o.append(line([(x, 650), (x + 30, 870)], sw=6, color=INK))
        o.append(line([(x + 60, 650), (x + 30, 870)], sw=6, color=INK))
    o.append(eye(500, 760, 46, iris="#ff4a2a", pupil="slit"))  # painted eye
    o.append(f'<ellipse cx="500" cy="640" rx="200" ry="52" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="6 14" opacity=".6"/>')
    # sound shock lines
    for a in range(-60, 70, 30):
        r_ = math.radians(a - 90)
        o.append(line([(500 + math.cos(r_) * 260, 620 + math.sin(r_) * 120), (500 + math.cos(r_) * 330, 620 + math.sin(r_) * 160)], sw=8, color=F))
    # arms with bone mallets mid-swing
    for side, seed in ((-1, 6), (1, 7)):
        o.append(arm([(500 + side * 130, 560), (500 + side * 240, 500), (500 + side * 250, 400)], 46, 38, gob, seed=seed))
        o.append(part(tube([(500 + side * 250, 420), (500 + side * 310, 300), (500 + side * 330, 250)], 20, 16, seed=seed), "#e9dfc4", sw=5, hatch=False))
        o.append(part(blob(500 + side * 335, 225, 46, 38, .12, 9, seed=seed), "#e9dfc4", sw=6, hatch=False))
        o.append(f'<circle cx="{500 + side*322}" cy="218" r="8" fill="{INK}"/><circle cx="{500 + side*348}" cy="218" r="8" fill="{INK}"/>')
        o.append(hand(500 + side * 250, 410, 32, gob, angle=-90, seed=seed, curl=1.1))
    o.append(goblin_head(500, 360, 160, gob, mouth="scream", seed=12, eye_col="#ff4a2a", ear=1.2))
    o.append(part(f"M370,230 L400,140 L430,220 L470,120 L500,215 L540,110 L560,220 L600,150 L620,235 Z", "#c0392b", sw=6))  # mohawk/war-crest
    RIM["col"] = None
    return "\n".join(o), (500, 400, 300)
