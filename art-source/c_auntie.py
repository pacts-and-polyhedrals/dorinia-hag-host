import math, random
from engine import *
from creatures import PAL

V = PAL["Auntie"]["glow"]
SCALE, BELLY = "#5f8a3e", "#d9c66a"


def coil(cx, cy, r, col, belly, seed=0, turns=1.4):
    """Coiled serpent lower body (front loop)."""
    o = []
    pts = []
    for i in range(16):
        a = math.pi * .9 + i * (turns * math.pi * 2 / 15)
        rr = r * (1 - i * .02)
        pts.append((cx + math.cos(a) * rr * 1.3, cy + math.sin(a) * rr * .45))
    o.append(part(tube(pts, r * .55, r * .4, seed=seed), col, sw=8))
    for i in range(2, len(pts) - 2):
        x, y = pts[i]
        o.append(f'<path d="M{x-14},{y+r*.12} q14,10 28,0" fill="none" stroke="{belly}" stroke-width="5" opacity=".9"/>')
    return "\n".join(o)


def mama_yagha():
    RIM["col"] = V
    skin, robe = "#7fa35a", "#2f4a26"
    o = [ground_shadow(500, 950, 360)]
    # coiled snake tail
    o.append(coil(500, 830, 300, SCALE, BELLY, seed=2))
    o.append(part(tube([(760, 800), (880, 760), (930, 650), (880, 560)], 70, 12, seed=4), SCALE, sw=7))
    o.append(f'<circle cx="880" cy="560" r="14" fill="{BELLY}" stroke="{INK}" stroke-width="4"/>')
    # torso robe
    o.append(part(tattered(500, 560, 790, 330, 440, seed=3, teeth=8, depth=40), robe, sw=8))
    o.append(folds(500, 620, 790, 360, n=5, seed=3))
    for i in range(7):  # fang necklace
        t = i / 6
        x, y = 360 + 280 * t, 615 + 40 * math.sin(math.pi * t)
        o.append(flat(f"M{x-8},{y} L{x+8},{y} L{x},{y+34} Z", "#efe6c4", sw=3))
    # arms
    o.append(arm([(340, 620), (250, 680), (210, 600)], 64, 46, skin, seed=5))
    o.append(hand(200, 570, 50, skin, angle=-100, spread=90, seed=6, curl=-.4))
    o.append(drips(160, 240, 600, V, n=3, seed=6, length=(20, 60)))
    o.append(arm([(660, 620), (740, 690), (700, 760)], 64, 46, skin, seed=7))
    o.append(hand(690, 775, 46, skin, angle=110, seed=8, curl=.6))
    # snake hair (behind + around head)
    rr = random.Random(5)
    heads = [(240, 230), (350, 120), (500, 85), (650, 120), (765, 235)]
    for i, (hx, hy) in enumerate(heads):
        base = (500 + (hx - 500) * .35, 330 + (hy - 330) * .35)
        mid = ((base[0] + hx) / 2 + rr.uniform(-60, 60), (base[1] + hy) / 2 + rr.uniform(-40, 40))
        o.append(snake([base, mid, (hx, hy)], 70, 52, ["#3e6a2a", "#557f34", "#2f5a26"][i % 3], BELLY, seed=i, head_size=58))
    # head
    o.append(part(blob(500, 390, 215, 195, .05, 16, seed=12, squash=pear(.95, 1.1)), skin, sw=9))
    for k in range(14):  # scale texture
        x, y = rr.uniform(330, 670), rr.uniform(230, 450)
        o.append(f'<path d="M{x-10},{y} q10,9 20,0" fill="none" stroke="{shade(skin,.55)}" stroke-width="3" opacity=".7"/>')
    o.append(pointy_ear(290, 410, 90, 60, skin, side=-1, seed=2, droop=.3))
    o.append(pointy_ear(710, 405, 90, 60, skin, side=1, seed=3, droop=.3))
    o.append(f'<circle cx="215" cy="400" r="12" fill="none" stroke="#e0b43a" stroke-width="6"/>')
    o.append(eye(415, 370, 58, iris="#ffd52a", pupil="slit", look=(.25, .1), bags=True))
    o.append(eye(588, 365, 54, iris="#ffd52a", pupil="slit", look=(-.25, .1), bags=True))
    o.append(brow(340, 290, 470, 320, sw=16, bend=-20))
    o.append(brow(530, 320, 660, 288, sw=16, bend=-20))
    o.append(grin(500, 500, 250, 80, teeth=6, seed=5, fangs=(1, 4), missing=(2, 3), curve=.65, tongue="#b0203a"))
    # forked tongue lolling
    o.append(part(tube([(500, 570), (510, 630), (490, 680)], 30, 16, seed=1), "#b0203a", sw=5, hatch=False))
    o.append(line([(490, 680), (465, 715)], sw=8, color="#b0203a"))
    o.append(line([(490, 680), (510, 718)], sw=8, color="#b0203a"))
    o.append(nose_bulb(495, 380, 90, 52, skin, hook=.4, seed=3))
    o.append(drips(380, 620, 560, V, n=3, seed=3, length=(25, 60)))
    RIM["col"] = None
    return "\n".join(o), (500, 360, 320)


def fangguard():
    RIM["col"] = V
    steel, skin = "#4c5a4a", "#6e9a48"
    o = [ground_shadow(500, 950, 260)]
    # spear behind
    o.append(shaft(760, 940, 760, 130, w=22, color="#4a3420"))
    o.append(spearhead(760, 130, -90, 42, color="#9aa08a"))
    o.append(drips(745, 775, 150, V, n=2, seed=3, length=(20, 40)))
    o.append(stubby_legs(500, 780, 940, 75, 64, skin, foot_col=steel, seed=3))
    o.append(armor_plate(500, 680, 170, 140, steel, seed=4))
    o.append(arm([(660, 620), (730, 650), (760, 560)], 58, 48, skin, seed=6))
    o.append(hand(760, 540, 40, skin, angle=-160, seed=7, curl=1.0))
    # scale shield
    o.append(arm([(340, 620), (290, 700)], 58, 50, skin, seed=4))
    o.append(part(blob(270, 700, 165, 190, .03, 16, seed=8), "#3e5a2e", sw=9, highlight=1.6))
    rr = random.Random(2)
    for row in range(6):
        for col in range(5):
            x = 170 + col * 50 + (25 if row % 2 else 0)
            y = 560 + row * 52
            if (x - 270) ** 2 / 165 ** 2 + (y - 700) ** 2 / 190 ** 2 < .8:
                o.append(f'<path d="M{x-24},{y} q24,30 48,0" fill="{shade("#5f8a3e", rr.uniform(.8,1.2))}" stroke="{INK}" stroke-width="4"/>')
    o.append(part(blob(270, 700, 40, 40, .05, 8, seed=9), "#c9a83a", sw=6, highlight=1.8))
    o.append(eye(270, 700, 18, iris=V, pupil="slit"))
    # cobra head
    o.append(cobra_head(500, 360, 185, "#8ab858", "#2a3f22", seed=3))
    o.append(part(blob(500, 180, 120, 40, .08, 10, seed=4), steel, sw=7, highlight=1.6))  # helmet band
    o.append(spearhead(500, 160, -90, 24, color="#c9a83a"))
    RIM["col"] = None
    return "\n".join(o), (500, 400, 300)


def coil_adept():
    RIM["col"] = V
    skin, robe = "#8cae66", "#3a2a4a"
    o = [ground_shadow(500, 950, 330)]
    o.append(coil(500, 830, 280, SCALE, BELLY, seed=5, turns=1.2))
    o.append(part(tube([(240, 790), (150, 720), (140, 620), (190, 560)], 66, 12, seed=2), SCALE, sw=7))
    # glaive with hook blade
    o.append(shaft(250, 900, 780, 150, w=22, color="#3a2a1e"))
    o.append(part("M760,170 Q860,120 900,40 Q910,160 820,230 Q860,240 870,280 Q800,270 770,220 Z", "#8d96a3", sw=7, highlight=1.8, texture=False))
    o.append(drips(800, 880, 250, V, n=2, seed=9, length=(20, 45)))
    # torso
    o.append(part(blob(500, 640, 170, 140, .05, 12, seed=4, squash=pear(.85, 1.05)), robe, sw=8))
    o.append(part("M380,600 Q500,700 620,600 L600,560 Q500,640 400,560 Z", "#c9a83a", sw=6))
    o.append(arm([(370, 620), (330, 700), (390, 760)], 54, 44, skin, seed=6))
    o.append(hand(400, 770, 40, skin, angle=-20, seed=7, curl=.9))
    o.append(arm([(630, 600), (700, 520), (690, 450)], 54, 44, skin, seed=8))
    o.append(hand(690, 430, 40, skin, angle=-60, seed=9, curl=1.1))
    # bald tattooed head with serpent eyes
    o.append(part(blob(500, 370, 200, 190, .05, 14, seed=10, squash=pear(1.05, .95)), skin, sw=9))
    o.append(line([(400, 230), (450, 260), (500, 230), (550, 260), (600, 230)], sw=8, color="#2f4a26"))
    o.append(line([(380, 280), (420, 300)], sw=6, color="#2f4a26"))
    o.append(line([(620, 280), (580, 300)], sw=6, color="#2f4a26"))
    rr = random.Random(9)
    for k in range(10):
        x, y = rr.uniform(330, 670), rr.uniform(300, 480)
        o.append(f'<path d="M{x-9},{y} q9,8 18,0" fill="none" stroke="{shade(skin,.5)}" stroke-width="3" opacity=".7"/>')
    o.append(eye(425, 370, 50, iris="#ffdc2e", pupil="slit", look=(.3, 0)))
    o.append(eye(580, 370, 50, iris="#ffdc2e", pupil="slit", look=(.3, 0)))
    o.append(brow(360, 300, 470, 335, sw=13, bend=-10))
    o.append(brow(530, 335, 640, 300, sw=13, bend=-10))
    o.append(f'<ellipse cx="490" cy="420" rx="6" ry="4" fill="{INK}"/><ellipse cx="515" cy="420" rx="6" ry="4" fill="{INK}"/>')
    o.append(grin(500, 465, 200, 50, teeth=6, seed=7, fangs=(1, 4), missing=(2, 3), curve=.4))
    o.append(pointy_ear(305, 385, 70, 50, skin, side=-1, seed=4, droop=.2))
    o.append(pointy_ear(695, 385, 70, 50, skin, side=1, seed=5, droop=.2))
    RIM["col"] = None
    return "\n".join(o), (500, 400, 300)


def spitebow():
    RIM["col"] = V
    skin, cloak = "#7aa050", "#2a3a22"
    o = [ground_shadow(500, 950, 240)]
    # quiver
    o.append(part("M600,560 L690,520 L760,760 L680,790 Z", "#5a3a22", sw=7))
    for k in range(4):
        x = 640 + k * 18
        o.append(line([(x, 545 - k * 8), (x - 20, 440 - k * 8)], sw=6, color=INK))
        o.append(flat(poly([(x - 20, 440 - k * 8), (x - 36, 420 - k * 8), (x - 14, 420 - k * 8)]), V, sw=3))
    o.append(stubby_legs(500, 790, 940, 65, 56, "#3a2a1e", seed=4))
    o.append(part(tattered(500, 560, 860, 300, 440, seed=6, teeth=8, depth=45), cloak, sw=8))
    # bow drawn, aimed left
    bow = [(240, 260), (170, 450), (180, 640), (250, 800)]
    o.append(line(bow, sw=26, color=INK))
    o.append(line(bow, sw=15, color="#4a3020"))
    o.append(line([(240, 260), (420, 530), (250, 800)], sw=3, color="#e8e0c8", smooth=False))
    o.append(line([(420, 530), (110, 530)], sw=9, color=INK, smooth=False))
    o.append(line([(420, 530), (110, 530)], sw=4, color="#7a5a3a", smooth=False))
    o.append(spearhead(110, 530, 180, 22, color="#9aa08a"))
    o.append(glow(80, 530, 40, V, .6))
    o.append(drips(70, 110, 540, V, n=3, seed=2, length=(20, 50)))
    o.append(arm([(370, 620), (260, 560), (190, 540)], 50, 40, skin, seed=5))
    o.append(hand(175, 530, 34, skin, angle=180, seed=6, curl=.9))
    o.append(arm([(600, 620), (520, 560), (430, 535)], 50, 40, skin, seed=7))
    o.append(hand(425, 530, 34, skin, angle=0, seed=8, curl=-.9))
    # hooded snake-face, squinting
    o.append(darkling_hood(500, 360, 220, cloak, seed=9, eye_col=V, grin_=False, tip=(80, -70)))
    o.append(part(blob(500, 400, 145, 120, .05, 12, seed=10), skin, sw=7))
    o.append(eye(445, 385, 40, iris="#ffdc2e", pupil="slit", look=(-.4, .1), lid=.35))
    o.append(eye(565, 385, 28, iris="#ffdc2e", pupil="slit", look=(-.4, .1), lid=.6))
    o.append(grin(490, 450, 150, 40, teeth=5, seed=9, fangs=(0, 4), missing=(2,), curve=.2))
    o.append(scars(560, 330, 60, 70, sw=3))
    RIM["col"] = None
    return "\n".join(o), (480, 420, 300)


def eye_acolyte():
    RIM["col"] = "#ffe15a"
    robe, skin, stone = "#5a4a2a", "#7a9a52", "#8a8a84"
    o = [ground_shadow(500, 950, 250)]
    # serpent staff
    o.append(snake([(220, 940), (240, 700), (200, 500), (240, 280), (200, 180)], 40, 34, SCALE, BELLY, seed=3, head_size=46))
    o.append(stubby_legs(500, 800, 940, 60, 50, "#3a2a1e", seed=4))
    o.append(part(tattered(500, 560, 880, 300, 500, seed=7, teeth=9, depth=50), robe, sw=8))
    o.append(folds(500, 620, 880, 380, n=5, seed=6))
    for k in range(6):  # gold trim
        o.append(f'<circle cx="{400 + k*40}" cy="630" r="9" fill="#d4a83a" stroke="{INK}" stroke-width="3"/>')
    o.append(arm([(350, 620), (270, 640), (235, 600)], 52, 42, robe, seed=4))
    o.append(hand(235, 580, 36, skin, angle=-160, seed=5, curl=1.0))
    o.append(arm([(650, 620), (720, 660), (740, 740)], 52, 42, robe, seed=6))
    o.append(hand(740, 760, 36, stone, angle=90, seed=7, curl=.4))
    # head, half turned to stone
    o.append(part(f"M260,460 Q240,210 400,140 Q500,100 600,140 Q760,210 740,460 Q620,560 500,560 Q380,560 260,460 Z", robe, sw=9))
    face = blob(500, 400, 190, 165, .05, 14, seed=12)
    o.append(part(face, skin, sw=8))
    cid = uid("st")
    o.append(f'<clipPath id="{cid}"><path d="{face}"/></clipPath><g clip-path="url(#{cid})">'
             f'<path d="M520,200 L560,330 L530,420 L580,520 L800,520 L800,200 Z" fill="{stone}"/>'
             f'<path d="M520,200 L560,330 L530,420 L580,520 L800,520 L800,200 Z" fill="url(#xhatch)" opacity=".5"/></g>')
    for pts in ([(560, 330), (620, 360), (650, 420)], [(530, 420), (600, 450)], [(600, 300), (660, 280)]):
        o.append(line(pts, sw=4))
    # giant third eye
    o.append(glow(500, 290, 90, "#ffe15a", .55))
    o.append(eye(500, 290, 60, iris="#ffe15a", pupil="slit", glow_col="#ffe15a", bloodshot=True))
    o.append(eye(430, 410, 34, iris="#ffdc2e", pupil="slit", lid=.3))
    o.append(eye(580, 410, 30, iris="#9a9a94", pupil="none", white="#b4b4ae"))
    o.append(grin(500, 475, 160, 45, teeth=6, seed=11, fangs=(1, 4), missing=(3,), curve=.3))
    o.append(scars(410, 350, 50, 120, sw=3))
    RIM["col"] = None
    return "\n".join(o), (500, 370, 290)


def chainmaster():
    RIM["col"] = V
    skin, leather = "#8a9a8a", "#4a3226"
    o = [ground_shadow(500, 950, 260)]
    o.append(stubby_legs(500, 790, 940, 70, 60, leather, seed=5))
    o.append(part(blob(500, 680, 175, 150, .06, 12, seed=4, squash=pear(.85, 1.1)), leather, sw=8))
    for k in range(3):  # straps
        o.append(line([(380, 590 + k * 40), (620, 640 + k * 40)], sw=10, color=INK))
        o.append(line([(380, 590 + k * 40), (620, 640 + k * 40)], sw=5, color="#7a5a3a"))
    o.append(armor_plate(360, 590, 70, 55, "#5a5a54", seed=2, rivets=False))
    # whirled barbed chain
    o.append(arm([(640, 610), (740, 540), (770, 450)], 56, 46, skin, seed=7))
    o.append(hand(770, 430, 40, skin, angle=-90, seed=8, curl=1.0))
    o.append(chain([(770, 420), (900, 300), (820, 150), (620, 120)], link=24))
    o.append(spearhead(620, 120, 190, 30, color="#8d96a3", barbed=True))
    o.append(arm([(360, 620), (290, 700), (300, 790)], 56, 46, skin, seed=9))
    o.append(hand(300, 810, 40, skin, angle=90, seed=10, curl=.5))
    o.append(chain([(300, 840), (200, 900), (90, 860)], link=22))  # leash to an offscreen beast
    # corrupted fey head with mirrored goggles
    o.append(pointy_ear(320, 370, 150, 70, skin, side=-1, seed=6, droop=.5))
    o.append(pointy_ear(680, 370, 150, 70, skin, side=1, seed=7, droop=.5))
    o.append(part(blob(500, 380, 190, 180, .06, 14, seed=11, squash=pear(1.0, 1.05)), skin, sw=9))
    o.append(hair_locks(500, 250, 160, 60, 9, "#d9d2b8", seed=4, length=(60, 120), spread=(190, 350), width=(20, 34), droop=2))
    o.append(line([(310, 360), (690, 360)], sw=20))
    for x in (420, 580):
        o.append(f'<circle cx="{x}" cy="360" r="66" fill="#2a2a2a" stroke="{INK}" stroke-width="9"/>')
        o.append(f'<circle cx="{x}" cy="360" r="52" fill="#9ad6c2"/>')
        o.append(f'<path d="M{x-40},{360-10} Q{x-20},{330} {x+10},{318}" fill="none" stroke="white" stroke-width="10" opacity=".8"/>')
        o.append(f'<circle cx="{x}" cy="360" r="52" fill="url(#hatch)" opacity=".25"/>')
        o.append(f'<ellipse cx="{x+15}" cy="375" rx="16" ry="10" fill="{V}" opacity=".7"/>')
    o.append(grin(500, 470, 230, 60, teeth=9, seed=12, missing=(2, 6), curve=.6))
    o.append(scars(610, 450, 70, 100, sw=3))
    o.append(nose_bulb(500, 400, 60, 44, skin, hook=-.3, seed=6))
    RIM["col"] = None
    return "\n".join(o), (500, 390, 300)


def alchemist():
    RIM["col"] = V
    skin, robe = "#a3b07a", "#3a2a3a"
    o = [ground_shadow(500, 950, 250)]
    # potion backpack
    o.append(part(blob(640, 600, 130, 160, .06, 12, seed=1), "#5a3a22", sw=8))
    for i, (x, y, c) in enumerate([(610, 450, V), (680, 470, "#c04ad6"), (720, 540, "#ffb02a")]):
        o.append(flask(x, y, 30, c, seed=i))
    o.append(stubby_legs(500, 800, 940, 60, 50, "#2a2026", seed=6))
    o.append(part(tattered(500, 560, 870, 300, 480, seed=8, teeth=9, depth=50), robe, sw=8))
    o.append(part(f"M380,620 L620,620 L600,860 L400,860 Z", "#c9b48a", sw=7))  # stained apron
    for (x, y, s) in [(450, 700, 30), (560, 780, 24), (480, 820, 18)]:
        o.append(f'<circle cx="{x}" cy="{y}" r="{s}" fill="{V}" opacity=".55"/>')
    o.append(drips(390, 610, 862, V, n=3, seed=4, length=(15, 40)))
    # belt flasks
    for i, x in enumerate((420, 480, 540)):
        o.append(flask(x, 640, 20, [V, "#c04ad6", "#ffb02a"][i], seed=i + 5))
    # raised flask
    o.append(arm([(640, 610), (720, 520), (740, 420)], 50, 40, robe, seed=5))
    o.append(flask(745, 330, 70, V, seed=9))
    o.append(bubbles(745, 220, 50, 50, 6, V, seed=3, size=(6, 14)))
    o.append(hand(745, 410, 36, skin, angle=-90, seed=6, curl=1.2))
    o.append(arm([(360, 620), (290, 680), (300, 760)], 50, 40, robe, seed=7))
    o.append(hand(300, 780, 36, skin, angle=90, seed=8, curl=.4))
    # crooked hat
    o.append(part(blob(470, 230, 230, 46, .08, 12, seed=4, rot=-.1), "#2a1e2a", sw=8))
    o.append(part("M380,230 Q410,110 470,60 Q520,10 600,40 Q540,70 540,130 Q560,190 570,230 Z", "#2a1e2a", sw=8))
    o.append(part(blob(470, 215, 120, 22, .1, 10, seed=6), "#7a5a2a", sw=5, hatch=False))
    # head: young hag with goggles pushed up
    o.append(part(blob(480, 400, 185, 165, .05, 14, seed=9), skin, sw=9))
    for x in (410, 540):
        o.append(f'<circle cx="{x}" cy="265" r="40" fill="#3a3a3a" stroke="{INK}" stroke-width="7"/>'
                 f'<circle cx="{x}" cy="265" r="28" fill="{V}" opacity=".7"/>')
    o.append(eye(420, 390, 52, iris="#c04ad6", pupil="dot", look=(.4, -.3), bloodshot=True))
    o.append(eye(555, 385, 44, iris="#c04ad6", pupil="dot", look=(.4, -.3)))
    o.append(nose_bulb(490, 380, 100, 52, skin, hook=1.0, seed=7))
    o.append(grin(480, 480, 200, 55, teeth=8, seed=13, missing=(1, 6), curve=.7))
    o.append(warts(480, 420, 150, 120, 4, shade(skin, .8), seed=4))
    o.append(scars(360, 450, 50, 70, sw=3))
    RIM["col"] = None
    return "\n".join(o), (490, 380, 300)


def valdershmort():
    RIM["col"] = V
    skin, belly, spike = "#5d7a46", "#c9b86a", "#2e3a22"
    o = [ground_shadow(500, 955, 420, 60)]
    # tail
    tail = [(700, 720), (820, 700), (920, 620), (960, 520)]
    o.append(part(tube(tail, 130, 20, seed=1), skin, sw=8))
    o.append(spikes_along(tail, 14, spike, side=-1, seed=1))
    # back legs (8 legs: show 6)
    for x, y, s in [(330, 800, 0), (450, 820, 1), (580, 820, 2), (690, 800, 3)]:
        o.append(part(tube([(x, 720), (x - 10, 860), (x + 5, 920)], 80, 60, seed=s), shade(skin, .8), sw=7))
        o.append(hand(x + 10, 925, 36, shade(skin, .8), fingers=3, spread=90, angle=90, seed=s, claws="#e9dfc4", curl=.1))
    # body
    body = blob(520, 660, 300, 190, .05, 16, seed=4)
    o.append(part(body, skin, sw=10))
    o.append(part(blob(520, 760, 230, 70, .05, 12, seed=5), belly, sw=6, hatch=False))
    for k in range(6):
        o.append(line([(330 + k * 75, 735), (340 + k * 75, 800)], sw=4, opacity=.7))
    back = [(260, 560), (380, 480), (520, 470), (660, 500), (780, 580)]
    o.append(spikes_along(back, 22, spike, side=-1, seed=3))
    # saddle for Auntie
    o.append(part("M440,470 Q520,410 620,470 L610,530 Q520,500 450,530 Z", "#6a2a2a", sw=7))
    o.append(line([(530, 470), (530, 600)], sw=8, color="#c9a83a"))
    # front legs
    for x, s in [(290, 7), (420, 8)]:
        o.append(part(tube([(x, 700), (x - 30, 840), (x - 20, 930)], 90, 64, seed=s), skin, sw=7))
        o.append(hand(x - 15, 935, 40, skin, fingers=3, spread=90, angle=90, seed=s, claws="#e9dfc4", curl=.1))
    # huge chibi head
    o.append(part(blob(260, 470, 240, 200, .05, 16, seed=10, squash=pear(1.0, .95)), skin, sw=10))
    o.append(spikes_along([(90, 380), (160, 300), (260, 270), (370, 300), (440, 380)], 18, spike, side=-1, seed=6))
    o.append(warts(260, 470, 200, 160, 6, shade(skin, .8), seed=2))
    # petrifying glowing eyes
    o.append(glow(200, 420, 110, "#e8ff7a", .55))
    o.append(glow(340, 420, 100, "#e8ff7a", .55))
    o.append(eye(190, 430, 66, iris="#e8ff7a", pupil="slit", glow_col="#e8ff7a", bloodshot=True))
    o.append(eye(345, 430, 58, iris="#e8ff7a", pupil="slit", glow_col="#e8ff7a"))
    o.append(brow(110, 340, 260, 370, sw=18, bend=-6))
    o.append(brow(290, 370, 430, 345, sw=18, bend=-6))
    o.append(grin(250, 570, 330, 80, teeth=10, seed=14, fangs=(1, 8), missing=(4,), curve=.5, tongue="#a02a3a"))
    o.append(drips(150, 360, 640, V, n=4, seed=5, length=(30, 80)))
    # petrified victim's hand
    o.append(hand(800, 900, 34, "#9a9a94", angle=-80, seed=11, claws="#8a8a84", curl=.3))
    o.append(f'<ellipse cx="800" cy="935" rx="60" ry="14" fill="#7a7a74" stroke="{INK}" stroke-width="5"/>')
    RIM["col"] = None
    return "\n".join(o), (270, 470, 300)
