import math, random
from engine import *
from creatures import PAL

G = PAL["Grandma"]["glow"]
NECRO = "#b06bff"


def darkling_knife():
    RIM["col"] = G
    cloak, skin = "#2c2836", "#8e8a9c"
    o = [ground_shadow(500, 945, 220)]
    o.append(stubby_legs(500, 760, 940, 70, 60, "#5a5466", foot_col="#6e6a5a", seed=1))
    o.append(part(tattered(500, 560, 860, 300, 470, seed=2, teeth=9, depth=60), cloak, sw=8))
    o.append(folds(500, 620, 860, 360, n=5, seed=4))
    o.append(part(blob(500, 700, 60, 18, .1, 8, seed=6), "#6b4a2a", sw=5, hatch=False))  # belt
    for i, x in enumerate((440, 470, 530, 560)):  # throwing knives on belt
        o.append(blade(x, 705, x + 4, 760, 12, color="#2e2a36", edge=NECRO))
    # off hand
    o.append(arm([(340, 620), (285, 690), (300, 760)], 52, 40, cloak, seed=2))
    o.append(hand(300, 780, 34, skin, angle=100, seed=3, curl=.4))
    # knife arm raised
    o.append(arm([(640, 600), (730, 520), (760, 420)], 56, 42, cloak, seed=4))
    for k in range(4):  # bandage wraps
        o.append(line([(735 + k * 4, 520 - k * 26), (775 + k * 4, 510 - k * 26)], sw=6, color="#d9cfb2"))
    o.append(blade(760, 380, 640, 130, 52, color="#2a2632", edge=NECRO, serrate=6))
    o.append(glow(700, 250, 60, NECRO, .35))
    o.append(part(tube([(745, 410), (775, 360)], 26, 26), "#3a2a1e", sw=5))
    o.append(hand(762, 400, 36, skin, angle=-120, seed=5, curl=.9))
    o.append(darkling_hood(500, 420, 230, cloak, seed=7, tip=(-60, -90)))
    RIM["col"] = None
    return "\n".join(o), (500, 430, 290)


def darkling_knight():
    RIM["col"] = G
    steel, cloak = "#3b3f4c", "#24202c"
    o = [ground_shadow(500, 945, 260)]
    # lance behind
    o.append(shaft(150, 900, 830, 120, w=22, color="#2a2430"))
    o.append(spearhead(830, 120, -48, 40, color="#2a2632", barbed=True))
    o.append(glow(860, 90, 60, NECRO, .4))
    # pennant
    o.append(part(catmull([(780, 175), (900, 150), (870, 205), (960, 220), (870, 260), (760, 245)], tension=.6), "#4b1f5e", sw=6))
    o.append(eye(845, 215, 18, iris=NECRO, pupil="slit"))
    o.append(part(tattered(500, 570, 870, 330, 520, seed=3, teeth=7, depth=40), cloak, sw=8))
    o.append(stubby_legs(500, 780, 940, 80, 70, steel, seed=2))
    o.append(armor_plate(500, 680, 175, 130, steel, seed=3))
    o.append(eye(500, 670, 26, iris=NECRO, pupil="slit"))  # sigil
    o.append(armor_plate(320, 590, 85, 65, steel, seed=5, rivets=False))
    o.append(armor_plate(680, 590, 85, 65, steel, seed=6, rivets=False))
    o.append(arm([(330, 640), (300, 730), (330, 790)], 60, 50, steel, seed=3))
    o.append(hand(340, 805, 40, "#5a5466", angle=40, seed=6, curl=.8))
    o.append(arm([(680, 640), (640, 690), (560, 700)], 60, 50, steel, seed=5))
    o.append(hand(545, 700, 40, "#5a5466", angle=200, seed=8, curl=.8))
    # helmet
    o.append(part(f"M300,320 Q280,170 420,130 L460,40 L500,120 L540,40 L580,130 Q720,170 700,320 Q700,500 500,540 Q300,500 300,320 Z", steel, sw=9, highlight=1.6))
    for side in (-1, 1):  # horns
        o.append(part(tube([(500 + side * 170, 220), (500 + side * 260, 160), (500 + side * 250, 60), (500 + side * 205, 30)], 60, 8, seed=side), "#d9cfb6", sw=6))
    o.append(flat("M340,330 Q500,300 660,330 L650,370 Q500,350 350,370 Z", "#0a0810", sw=6))
    o.append(glow_eye(430, 345, 34, "#e9f6ff"))
    o.append(glow_eye(570, 343, 30, "#e9f6ff"))
    for x in range(380, 640, 40):  # breath slits
        o.append(line([(x, 420), (x + 5, 470)], sw=6))
    o.append(scars(600, 250, 80, -30, sw=3))
    RIM["col"] = None
    return "\n".join(o), (500, 320, 290)


def berbalang():
    RIM["col"] = G
    skin, wing = "#867f93", "#3a2a40"
    o = [ground_shadow(500, 950, 160)]
    o.append(bat_wing(430, 600, -1, 400, 330, wing, seed=1))
    o.append(bat_wing(570, 600, 1, 400, 330, wing, seed=2))
    # gaunt body
    o.append(part(blob(500, 690, 120, 150, .08, 12, seed=3, squash=pear(.8, 1.0)), skin, sw=8))
    for k in range(4):  # ribs
        o.append(line([(430, 650 + k * 35), (500, 670 + k * 35), (570, 650 + k * 35)], sw=4, opacity=.8))
    o.append(stubby_legs(500, 790, 930, 50, 40, skin, seed=4, feet="claw"))
    # arms clutching a glowing stolen secret (scroll)
    o.append(arm([(420, 640), (380, 720), (430, 770)], 40, 28, skin, seed=5))
    o.append(arm([(580, 640), (620, 720), (570, 770)], 40, 28, skin, seed=6))
    o.append(glow(500, 790, 70, "#ffe9a8", .5))
    o.append(part("M430,760 L570,760 L560,830 L440,830 Z", "#efe0b0", sw=5, hatch=False))
    for k in range(3):
        o.append(line([(450, 780 + k * 15), (550, 780 + k * 15)], sw=2.5, opacity=.7))
    o.append(hand(440, 780, 26, skin, angle=-20, seed=7, curl=.9))
    o.append(hand(560, 780, 26, skin, angle=200, seed=8, curl=-.9))
    # huge veined cranium
    o.append(part(blob(500, 350, 250, 230, .05, 18, seed=9, squash=pear(1.08, .85)), skin, sw=9))
    rr = random.Random(4)
    for _ in range(9):  # brain folds / veins
        x0, y0 = rr.uniform(330, 670), rr.uniform(170, 330)
        o.append(line([(x0, y0), (x0 + rr.uniform(-50, 50), y0 + rr.uniform(10, 60)), (x0 + rr.uniform(-60, 60), y0 + rr.uniform(40, 110))],
                      sw=rr.uniform(4, 7), color="#5d3f6b", opacity=.85))
    # four eyes
    for (x, y, r) in [(415, 390, 42), (585, 390, 42), (455, 315, 24), (545, 315, 24)]:
        o.append(eye(x, y, r, iris="#d6f3ff", pupil="dot", glow_col=G))
    # small jaw full of needles
    o.append(part(blob(500, 520, 120, 70, .06, 12, seed=11), skin, sw=8))
    o.append(grin(500, 500, 190, 70, teeth=12, seed=9, curve=.2, tongue="#7a2a5a"))
    o.append(part(tube([(520, 560), (560, 640), (520, 700), (560, 740)], 26, 6, seed=3), "#a0306a", sw=5, hatch=False))
    RIM["col"] = None
    return "\n".join(o), (500, 380, 290)


def rotbriar_hexer():
    RIM["col"] = "#c27bff"
    robe, skin, briar = "#3c3a24", "#9fae8a", "#4a3a22"
    o = [ground_shadow(500, 945, 230)]
    # staff
    o.append(shaft(760, 940, 730, 210, w=24, color="#4a3420"))
    o.append(line([(730, 210), (690, 150), (720, 110)], sw=16, color=INK))
    o.append(line([(730, 210), (690, 150), (720, 110)], sw=9, color="#4a3420"))
    o.append(line([(732, 210), (780, 160), (760, 110)], sw=16, color=INK))
    o.append(line([(732, 210), (780, 160), (760, 110)], sw=9, color="#4a3420"))
    o.append(glow(740, 150, 80, "#b06bff", .6))
    _sp = [(740+4.0,150+0.0),(740+5.0,150+2.4),(740+4.5,150+5.6),(740+1.9,150+8.6),(740+-2.4,150+10.1),(740+-7.5,150+9.3),(740+-12.3,150+5.8),(740+-15.2,150+-0.1),(740+-15.1,150+-7.4),(740+-11.3,150+-14.5),(740+-4.2,150+-19.6),(740+5.1,150+-21.0),(740+14.7,150+-17.9),(740+22.5,150+-10.4),(740+26.4,150+0.4),(740+25.0,150+12.6),(740+18.0,150+23.5),(740+6.3,150+30.6),(740+-8.0,150+31.8),(740+-22.1,150+26.4),(740+-32.8,150+14.8),(740+-37.6,150+-0.9),(740+-34.9,150+-17.9),(740+-24.5,150+-32.6)]
    o.append(line(_sp, sw=12, color=INK))
    o.append(line(_sp, sw=6, color="#e6c9ff"))
    for _a in range(0, 360, 60):
        _r = math.radians(_a)
        o.append(line([(740 + math.cos(_r)*46, 150 + math.sin(_r)*46), (740 + math.cos(_r)*62, 150 + math.sin(_r)*62)], sw=6, color="#e6c9ff"))
    o.append(stubby_legs(500, 820, 940, 60, 50, skin, seed=3, feet="claw"))
    o.append(part(tattered(500, 560, 880, 300, 520, seed=5, teeth=10, depth=55), robe, sw=8))
    # briars wrapping body
    rr = random.Random(2)
    for k in range(5):
        y = 620 + k * 55
        pts = [(260 + k * 10, y + rr.uniform(-20, 20)), (420, y + 25), (560, y - 20), (740 - k * 10, y + rr.uniform(-10, 20))]
        o.append(line(pts, sw=13, color=INK))
        o.append(line(pts, sw=7, color=briar))
        o.append(spikes_along(bez(pts[0], pts[1], pts[3], 7), 7, "#2a1e10", side=1 if k % 2 else -1, seed=k))
    o.append(arm([(660, 610), (720, 560), (735, 470)], 50, 40, robe, seed=4))
    o.append(hand(735, 450, 34, skin, angle=-90, seed=4, curl=1.0))
    o.append(arm([(340, 610), (270, 660), (230, 610)], 50, 40, robe, seed=6))
    o.append(hand(220, 590, 38, skin, angle=-110, seed=6, curl=-.3))
    o.append(glow(200, 540, 40, "#b06bff", .5))
    # head under mossy hood
    o.append(part(f"M240,470 Q220,230 380,150 Q470,60 560,140 Q760,200 760,470 Q600,560 500,560 Q370,560 240,470 Z", robe, sw=9))
    o.append(part(blob(500, 400, 200, 170, .06, 14, seed=12, squash=pear(.95, 1.1)), skin, sw=8))
    o.append(eye(430, 380, 46, iris="#c7ff5a", pupil="slit", look=(.2, .1), bags=True))
    # thorn-sewn eye
    o.append(line([(540, 385), (620, 375)], sw=7))
    for x in range(550, 620, 16):
        o.append(line([(x, 362), (x + 4, 396)], sw=4, color="#7a2a2a"))
    o.append(nose_bulb(500, 360, 120, 60, skin, hook=1.6, seed=4))
    o.append(grin(490, 480, 200, 50, teeth=7, seed=6, missing=(2, 4), curve=.5))
    o.append(warts(500, 420, 160, 120, 5, shade(skin, .8), seed=9))
    # moss & blossom on hood
    for (x, y) in [(300, 260), (650, 230), (380, 170)]:
        o.append(part(blob(x, y, 40, 22, .3, 9, seed=x), "#4f6b2a", sw=4, hatch=False))
    o.append(part(blob(640, 200, 26, 26, .25, 8, seed=3), "#7a2a4a", sw=4, hatch=False))
    o.append(f'<circle cx="640" cy="200" r="8" fill="#e8c94a" stroke="{INK}" stroke-width="3"/>')
    RIM["col"] = None
    return "\n".join(o), (490, 390, 290)


def soul_cage_porter():
    RIM["col"] = G
    iron, rust = "#3d3a3a", "#6a3a22"
    o = [ground_shadow(500, 950, 330)]
    o.append(stubby_legs(500, 800, 945, 120, 95, iron, seed=2))
    # cage torso
    body = blob(500, 620, 270, 230, .04, 16, seed=3)
    o.append(f'<path d="{body}" fill="#0f1c2a"/>')
    o.append(glow(500, 640, 200, G, .55))
    rr = random.Random(5)
    for i in range(5):
        o.append(wisp(380 + i * 60 + rr.uniform(-15, 15), 560 + rr.uniform(-60, 80), rr.uniform(18, 30), G, seed=i))
    for x in range(260, 760, 55):  # bars
        o.append(line([(x, 410), (x + (500 - x) * .12, 620), (x, 840)], sw=17, color=INK))
        o.append(line([(x, 410), (x + (500 - x) * .12, 620), (x, 840)], sw=9, color=iron))
    for y in (420, 840):
        o.append(part(blob(500, y, 260, 40, .04, 12, seed=y), iron, sw=7, highlight=1.6))
    o.append(chain([(280, 430), (360, 520), (300, 610)]))
    # maul arm
    o.append(arm([(720, 470), (820, 520), (840, 620)], 90, 75, iron, seed=6))
    for _a in range(0, 360, 40):
        _r = math.radians(_a)
        o.append(flat(poly([(845 + math.cos(_r - .25) * 95, 720 + math.sin(_r - .25) * 95), (845 + math.cos(_r) * 150, 720 + math.sin(_r) * 150),
                            (845 + math.cos(_r + .25) * 95, 720 + math.sin(_r + .25) * 95)]), "#55504c", sw=5))
    o.append(part(blob(845, 720, 105, 100, .05, 12, seed=4), "#2c2a2a", sw=8, highlight=1.7))
    o.append(drips(790, 900, 760, rust, n=4, seed=3, length=(20, 50)))
    o.append(f'<circle cx="845" cy="720" r="40" fill="none" stroke="{INK}" stroke-width="6"/>')
    # other arm dragging chain
    o.append(arm([(280, 470), (190, 560), (180, 680)], 80, 64, iron, seed=7))
    o.append(hand(180, 700, 48, "#4a4646", angle=90, seed=8, curl=.4, claws="#1a1414"))
    o.append(chain([(180, 740), (240, 880), (380, 930)]))
    # lantern head
    o.append(part(f"M380,260 Q500,140 620,260 L640,420 L360,420 Z", iron, sw=9, highlight=1.7))
    o.append(f'<path d="M405,300 L595,300 L605,400 L395,400 Z" fill="#0a1420" stroke="{INK}" stroke-width="6"/>')
    o.append(glow_eye(455, 345, 34, G, shape="round"))
    o.append(glow_eye(545, 345, 34, G, shape="round"))
    o.append(line([(470, 385), (500, 395), (530, 385)], sw=5, color=G))
    o.append(part(blob(500, 150, 30, 30, .05, 8, seed=1), iron, sw=6))
    o.append(f'<path d="M405,300 L595,300 L605,400 L395,400 Z" fill="url(#hatch)" opacity=".3"/>')
    for x in (405, 500, 595):
        o.append(line([(x, 300), (x if x == 500 else x + (x - 500) * .05, 400)], sw=8, color=INK))
    RIM["col"] = None
    return "\n".join(o), (500, 480, 330)


def thorn_stalker():
    RIM["col"] = G
    wood, dark = "#4a3a26", "#2a2016"
    o = [ground_shadow(500, 950, 240)]
    # spindly root legs
    for side in (-1, 1):
        pts = [(500 + side * 50, 740), (500 + side * 130, 820), (500 + side * 120, 930), (500 + side * 170, 945)]
        o.append(part(tube(pts, 46, 14, seed=side), wood, sw=6))
        o.append(spikes_along(pts, 8, dark, side=side, seed=side + 3))
    # trunk body
    body = tube([(500, 760), (480, 660), (510, 560)], 170, 120, seed=3)
    o.append(part(body, wood, sw=8))
    rr = random.Random(7)
    for k in range(6):
        y = 580 + k * 30
        o.append(line([(430 + rr.uniform(0, 20), y), (500, y + rr.uniform(-10, 10)), (565 + rr.uniform(-20, 0), y + 5)], sw=3.5, opacity=.7))
    # raking branch arms (long, hooked)
    for side, seed in ((-1, 1), (1, 2)):
        pts = [(500 + side * 60, 590), (500 + side * 200, 520), (500 + side * 320, 600), (500 + side * 370, 720)]
        o.append(part(tube(pts, 46, 20, seed=seed), wood, sw=7))
        o.append(spikes_along(pts + [(500 + side * 390, 760)], 9, dark, side=-side, seed=seed))
        tip = pts[-1]
        for k in range(3):  # hooked twig claws
            a = math.radians(90 + side * (-20 + k * 25))
            p1 = (tip[0] + math.cos(a) * 50, tip[1] + math.sin(a) * 50)
            p2 = (p1[0] - side * 30, p1[1] + 20)
            o.append(part(tube([tip, p1, p2], 16, 4, seed=k), dark, sw=5, hatch=False, texture=False))
    # head: knot of briars
    o.append(part(blob(500, 380, 210, 200, .14, 16, seed=12), wood, sw=9))
    for k in range(10):
        a = rr.uniform(0, 6.28)
        pts = [(500 + math.cos(a) * 120, 380 + math.sin(a) * 110), (500 + math.cos(a + .4) * 210, 380 + math.sin(a + .4) * 200),
               (500 + math.cos(a + .8) * 260, 380 + math.sin(a + .8) * 240)]
        o.append(line(pts, sw=14, color=INK))
        o.append(line(pts, sw=8, color=wood))
        o.append(spikes_along(pts, 7, dark, side=1, seed=k))
    hollow = blob(500, 420, 130, 120, .1, 12, seed=4)
    o.append(flat(hollow, "#0a0a10", sw=7))
    o.append(eye(450, 395, 34, iris="#d6f3ff", pupil="none", glow_col=G, white="#b9e6ff"))
    o.append(eye(555, 402, 26, iris="#d6f3ff", pupil="none", glow_col=G, white="#b9e6ff"))
    o.append(flat(blob(505, 480, 50, 26, .2, 9, seed=6), "#160a10", sw=4))
    for i in range(5):
        x = 470 + i * 15
        o.append(flat(poly([(x - 5, 462), (x + 5, 462), (x, 482)]), "#cfc7a8", sw=2))
    # rose blooms with memory-eyes
    for (x, y, s) in [(330, 270, 34), (680, 300, 28), (600, 640, 26)]:
        o.append(part(blob(x, y, s, s, .3, 9, seed=x), "#8a1f35", sw=5, hatch=False))
        o.append(eye(x, y, s * .45, iris="#d6f3ff", pupil="dot"))
    RIM["col"] = None
    return "\n".join(o), (500, 410, 300)


def flying_cauldron():
    RIM["col"] = "#9dff3a"
    iron, acid = "#2b2a2e", "#8fe63a"
    o = [ground_shadow(500, 955, 200, 26)]
    # ragged bat wings
    o.append(bat_wing(320, 560, -1, 280, 260, "#3a2f3a", seed=3))
    o.append(bat_wing(680, 560, 1, 280, 260, "#3a2f3a", seed=4))
    # pot body
    pot = "M210,430 Q200,780 380,840 Q500,880 620,840 Q800,780 790,430 Z"
    o.append(part(pot, iron, sw=10, highlight=1.9))
    # angry face embossed on pot
    o.append(eye(400, 610, 48, iris="#ff9c2a", pupil="slit", glow_col="#ff6a2a", look=(.3, .1)))
    o.append(eye(600, 610, 48, iris="#ff9c2a", pupil="slit", glow_col="#ff6a2a", look=(-.3, .1)))
    o.append(brow(330, 540, 470, 580, sw=18, bend=6))
    o.append(brow(530, 580, 670, 540, sw=18, bend=6))
    o.append(grin(500, 700, 280, 70, teeth=9, seed=12, missing=(4,), fangs=(1, 7), curve=.6, tooth="#c9c2b0"))
    for x in (250, 750):  # rivets/handles
        o.append(f'<circle cx="{x}" cy="470" r="38" fill="none" stroke="{INK}" stroke-width="20"/>'
                 f'<circle cx="{x}" cy="470" r="38" fill="none" stroke="#4a4652" stroke-width="10"/>')
    # stubby chicken feet dangling
    for x in (420, 580):
        o.append(line([(x, 845), (x, 900)], sw=14))
        o.append(line([(x, 845), (x, 900)], sw=7, color="#d1a43a"))
        o.append(hand(x, 915, 16, "#d1a43a", fingers=3, spread=80, angle=90, seed=x, claws=INK))
    # brew + rim
    o.append(part(blob(500, 430, 300, 70, .03, 14, seed=5), "#3a393f", sw=10, highlight=1.9))
    o.append(f'<ellipse cx="500" cy="425" rx="255" ry="48" fill="{acid}" stroke="{INK}" stroke-width="6"/>')
    o.append(glow(500, 410, 220, acid, .45))
    o.append(bubbles(500, 400, 200, 25, 12, shade(acid, 1.2), seed=4, size=(8, 22)))
    o.append(eye(430, 390, 18, iris="#ff4a2a", pupil="dot"))  # something lurking in the brew
    o.append(eye(470, 395, 14, iris="#ff4a2a", pupil="dot"))
    o.append(drips(260, 740, 450, acid, n=7, seed=2, length=(40, 120)))
    # spitting acid arc
    o.append(part(tube([(680, 400), (780, 280), (880, 250), (940, 300)], 40, 12, seed=8), acid, sw=6, hatch=False))
    o.append(bubbles(900, 300, 40, 30, 4, acid, seed=9, size=(6, 12)))
    for _k, (_x, _y, _r) in enumerate([(470, 300, 34), (520, 230, 26), (480, 165, 18), (540, 110, 12)]):
        o.append(f'<circle cx="{_x}" cy="{_y}" r="{_r}" fill="#8fe63a" opacity="{0.35 - _k*0.06:.2f}" filter="url(#softglow)"/>')
        o.append(f'<circle cx="{_x}" cy="{_y}" r="{_r}" fill="none" stroke="{INK}" stroke-width="3" opacity=".5"/>')
    RIM["col"] = None
    return "\n".join(o), (500, 560, 320)


def walking_hut():
    RIM["col"] = "#ffcf5a"
    wood, thatch = "#5a3a22", "#8a6a2a"
    o = [ground_shadow(500, 955, 330)]
    # chicken legs
    for side, seed in ((-1, 1), (1, 2)):
        x = 500 + side * 120
        pts = [(x, 700), (x + side * 70, 790), (x - side * 10, 860), (x + side * 10, 930)]
        o.append(part(tube(pts[:2], 120, 70, seed=seed), "#8a5a3a", sw=7))  # drumstick
        o.append(part(tube(pts[1:], 34, 26, seed=seed + 3), "#d6a03a", sw=6, texture=False))
        for k in range(5):
            t = k / 5
            px = pts[2][0] + (pts[3][0] - pts[2][0]) * t
            py = pts[2][1] + (pts[3][1] - pts[2][1]) * t
            o.append(line([(px - 14, py), (px + 14, py)], sw=3))
        o.append(hand(pts[3][0], 935, 30, "#d6a03a", fingers=3, spread=110, angle=90 - side * 10, seed=seed, claws=INK, curl=.1))
    # cabin body (log house)
    body = "M230,420 L770,420 L760,720 Q500,760 240,720 Z"
    o.append(part(body, wood, sw=9))
    for y in range(460, 720, 42):
        o.append(line([(240, y), (500, y + 6), (760, y)], sw=4, opacity=.8))
    # window eyes
    for (x, r) in ((370, 66), (630, 58)):
        o.append(f'<rect x="{x-r}" y="{500-r*.8}" width="{r*2}" height="{r*1.6}" fill="#2a1a10" stroke="{INK}" stroke-width="8"/>')
        o.append(eye(x, 500, r * .7, iris="#ffcf3a", pupil="slit", glow_col="#ffb02a", look=(.2 if x < 500 else -.2, .1)))
        o.append(line([(x - r, 500 - r * .8), (x + r, 500 - r * .8 + (15 if x < 500 else -15))], sw=14))  # angry shutter brows
    # door mouth
    o.append(flat("M420,720 L420,620 Q500,560 580,620 L580,720 Z", "#1c0b06", sw=8))
    rr = random.Random(3)
    for i in range(5):
        x = 432 + i * 34
        o.append(flat(poly([(x, 625 - abs(i - 2) * 10), (x + 26, 625 - abs(i - 2) * 10), (x + 13, 670)]), "#e6d9b6", sw=3))
    o.append(f'<ellipse cx="500" cy="705" rx="55" ry="18" fill="#9c2a30" stroke="{INK}" stroke-width="4"/>')
    # thatch roof like messy hair
    roof = catmull([(170, 450), (240, 330), (380, 230), (520, 170), (650, 220), (780, 320), (840, 450), (700, 420), (560, 440), (400, 430), (300, 455)], tension=.7)
    o.append(part(roof, thatch, sw=9))
    for k in range(18):
        x = 200 + k * 35
        o.append(line([(x, 420 + rr.uniform(-10, 20)), (x + rr.uniform(-20, 20), 480 + rr.uniform(0, 30))], sw=6, color=INK))
        o.append(line([(x, 420), (x + rr.uniform(-15, 15), 470 + rr.uniform(0, 25))], sw=3, color=shade(thatch, 1.3)))
    # chimney + smoke
    o.append(part("M620,250 L690,240 L700,120 L630,125 Z", "#6a6460", sw=7))
    o.append(smoke(665, 90, 4, "#5a5466", seed=4, rise=120, size=(25, 45)))
    # skull on the roof peak
    o.append(part(blob(470, 175, 40, 36, .05, 9, seed=3), "#e9dfc4", sw=6, hatch=False))
    o.append(f'<circle cx="455" cy="172" r="9" fill="{INK}"/><circle cx="487" cy="172" r="9" fill="{INK}"/>')
    RIM["col"] = None
    return "\n".join(o), (500, 470, 330)
