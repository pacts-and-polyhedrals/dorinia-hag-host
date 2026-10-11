import math
import random
from engine import *

PAL = {
    "Grandma": {"bg1": "#2a1638", "bg2": "#07040c", "glow": "#7fc8ff", "accent": "#8a4fb8", "ring": "#6b3a8f"},
    "Auntie": {"bg1": "#13302a", "bg2": "#030807", "glow": "#9dff3a", "accent": "#c9d43a", "ring": "#3f7a2a"},
    "Gaga": {"bg1": "#4a1a10", "bg2": "#0c0403", "glow": "#ff6a2a", "accent": "#c0392b", "ring": "#8a3a1e"},
}


def background(fac, seed=0):
    p = PAL[fac]
    r = random.Random(seed)
    out = [f'<radialGradient id="bgg" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="{p["bg1"]}"/>'
           f'<stop offset="1" stop-color="{p["bg2"]}"/></radialGradient>',
           '<rect width="1000" height="1000" fill="url(#bgg)"/>',
           f'<rect width="1000" height="1000" fill="{shade(p["bg1"],1.4)}" filter="url(#mottle)" opacity="0.35"/>']
    # speed/ink streaks
    for _ in range(26):
        a = r.uniform(0, 6.28)
        r0, r1 = r.uniform(380, 460), r.uniform(560, 760)
        out.append(line([(500 + math.cos(a) * r0, 480 + math.sin(a) * r0), (500 + math.cos(a) * r1, 480 + math.sin(a) * r1)],
                        sw=r.uniform(2, 6), color=INK, opacity=.55, smooth=False))
    # ink splatters
    for _ in range(14):
        x, y = r.choice([r.uniform(20, 200), r.uniform(800, 980)]), r.uniform(20, 980)
        s = r.uniform(4, 16)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="{INK}" opacity=".7"/>')
    out.append(glow(500, 470, 300, p["glow"], .12))
    return "\n".join(out)


def frame(fac):
    p = PAL[fac]
    return (f'<rect x="14" y="14" width="972" height="972" fill="none" stroke="{INK}" stroke-width="28"/>'
            f'<rect x="34" y="34" width="932" height="932" fill="none" stroke="{p["ring"]}" stroke-width="5" opacity=".8"/>'
            f'<rect x="0" y="0" width="1000" height="1000" fill="url(#xhatch)" opacity="0.18" '
            f'mask="url(#vig)"/>'
            '<mask id="vig"><radialGradient id="vg" cx="50%" cy="50%" r="72%"><stop offset=".6" stop-color="black"/>'
            '<stop offset="1" stop-color="white"/></radialGradient><rect width="1000" height="1000" fill="url(#vg)"/></mask>')


def portrait_svg(fac, figure, seed=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">{defs()}'
            f'{background(fac, seed)}<g filter="url(#ink)">{figure}</g>'
            f'<rect width="1000" height="1000" fill="#000" filter="url(#grain)" opacity="0.35"/>{frame(fac)}</svg>')


def token_svg(fac, figure, focus, seed=0):
    """Round token: figure zoomed to focus=(cx,cy,radius) inside a faction ring."""
    p = PAL[fac]
    cx, cy, rad = focus
    s = 400 / rad
    tr = f"translate(500,500) scale({s:.4f}) translate({-cx},{-cy})"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">{defs()}'
            '<clipPath id="tc"><circle cx="500" cy="500" r="430"/></clipPath>'
            f'<g clip-path="url(#tc)">{background(fac, seed)}<g transform="{tr}"><g filter="url(#ink)">{figure}</g></g>'
            f'<rect width="1000" height="1000" fill="#000" filter="url(#grain)" opacity="0.3"/>'
            f'<circle cx="500" cy="500" r="430" fill="none" stroke="{INK}" stroke-width="30" opacity=".35" filter="url(#softglow)"/></g>'
            f'<circle cx="500" cy="500" r="452" fill="none" stroke="{INK}" stroke-width="52"/>'
            f'<circle cx="500" cy="500" r="452" fill="none" stroke="{p["ring"]}" stroke-width="30"/>'
            f'<circle cx="500" cy="500" r="452" fill="none" stroke="url(#hatch)" stroke-width="30" opacity=".6"/>'
            f'<circle cx="500" cy="500" r="452" fill="none" stroke="{shade(p["ring"],1.5)}" stroke-width="4" opacity=".7" transform="translate(-3,-3)"/>'
            f'<circle cx="500" cy="500" r="476" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<circle cx="500" cy="500" r="428" fill="none" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<circle cx="{500+math.cos(a)*452:.1f}" cy="{500+math.sin(a)*452:.1f}" r="9" fill="{shade(p["ring"],1.6)}" stroke="{INK}" stroke-width="4"/>'
                      for a in [i * math.pi / 4 for i in range(8)])
            + '</svg>')


# =================================================================== GRANDMA
def grandma():
    RIM["col"] = PAL["Grandma"]["glow"]
    skin, robe, hair = "#a99cb3", "#4b2a5c", "#d6d0dc"
    o = [ground_shadow(500, 950, 340)]
    o.append(hair_locks(480, 360, 215, 190, 24, hair, seed=11, length=(140, 300), spread=(150, 390), width=(30, 52), droop=4.5))
    # tattered robe, hunched
    o.append(part(tattered(500, 560, 900, 380, 600, seed=3, teeth=11, depth=55), robe, sw=8))
    o.append(folds(500, 640, 900, 480, n=6, seed=2))
    o.append(part(f"M300,600 Q500,690 700,600 Q690,700 500,730 Q310,700 300,600 Z", shade(robe, .75), sw=7))  # shawl
    o.append(part(blob(430, 790, 40, 34, .2, 8, seed=31), "#6b4a2a", sw=5, hatch=False))  # patch
    o.append(line([(400, 775), (460, 805)], sw=3)); o.append(line([(405, 805), (455, 772)], sw=3))
    # bone & tooth necklace
    for i in range(9):
        t = i / 8
        x = 330 + 340 * t
        y = 650 + 45 * math.sin(math.pi * t)
        o.append(line([(x, y - 8), (x, y + 6)], sw=3))
        o.append(part(blob(x, y + 18, 9, 18, .12, 7, seed=i), "#ece2c4", sw=4, hatch=False, texture=False))
    # lantern arm (right)
    o.append(arm([(670, 640), (770, 690), (815, 770)], 78, 58, robe, seed=2))
    o.append(line([(840, 780), (840, 720)], sw=6))
    o.append(glow(840, 850, 120, PAL["Grandma"]["glow"], .5))
    o.append(part(f"M780,790 L900,790 L890,910 L790,910 Z", "#2b3240", sw=7, hatch=False, rim=False))
    o.append(f'<rect x="795" y="800" width="90" height="100" fill="#123048" stroke="{INK}" stroke-width="4"/>')
    o.append(wisp(840, 835, 24, PAL["Grandma"]["glow"], seed=2))
    o.append(wisp(815, 868, 12, PAL["Grandma"]["glow"], seed=5))
    for x in (812, 840, 868):
        o.append(line([(x, 795), (x, 905)], sw=5))
    o.append(part(blob(840, 785, 66, 16, .05, 8, seed=8), "#2b3240", sw=6, hatch=False))
    o.append(hand(808, 760, 42, skin, angle=70, seed=5, curl=.7))
    # reaching claw (left)
    o.append(arm([(330, 640), (235, 655), (165, 590)], 80, 52, robe, seed=6))
    o.append(part(blob(250, 660, 50, 30, .2, 8, seed=7), shade(robe, .8), sw=5))  # sleeve rag
    o.append(hand(140, 555, 60, skin, angle=-125, spread=100, seed=7, curl=-.4))
    # stray souls
    o.append(wisp(160, 380, 22, PAL["Grandma"]["glow"], seed=3))
    o.append(wisp(885, 470, 17, PAL["Grandma"]["glow"], seed=4))
    # ears
    o.append(pointy_ear(275, 410, 120, 70, skin, side=-1, seed=1, droop=.45))
    o.append(pointy_ear(690, 400, 110, 64, skin, side=1, seed=2, droop=.5))
    o.append(f'<circle cx="215" cy="400" r="13" fill="none" stroke="#d1a53a" stroke-width="6"/>')
    # head: lumpy, heavy jowls
    o.append(part(blob(482, 390, 225, 210, .06, 18, seed=12, squash=pear(.95, 1.12)), skin, sw=9))
    o.append(part(blob(380, 540, 70, 50, .1, 9, seed=21), skin, sw=0, hatch=False, rim=False))
    o.append(part(blob(590, 535, 70, 52, .1, 9, seed=22), skin, sw=0, hatch=False, rim=False))
    o.append(warts(470, 400, 200, 160, 8, shade(skin, .82), seed=3))
    o.append(wrinkles([[(380, 240), (480, 225), (585, 245)], [(400, 265), (480, 255), (560, 270)],
                       [(300, 360), (290, 395)], [(660, 345), (672, 380)], [(318, 430), (340, 460)]]))
    o.append(scars(610, 470, 70, 60))
    # eyes
    o.append(eye(388, 350, 66, iris="#e9d84a", pupil="dot", look=(.35, .15), bloodshot=True, bags=True))
    o.append(eye(585, 345, 40, iris="#e9d84a", pupil="slit", look=(-.2, .2), lid=.45, bags=True))
    o.append(brow(305, 268, 465, 300, sw=18, bend=-30))
    o.append(brow(530, 305, 650, 285, sw=15, bend=14))
    o.append(hair_strands(385, 260, 60, 10, 5, hair, seed=4, length=(20, 35), spread=(200, 330), sw=(3, 5)))
    # mouth
    o.append(grin(485, 505, 290, 78, teeth=9, seed=4, missing=(1, 5), fangs=(3, 7), curve=.75, tongue="#7a2040"))
    o.append(nose_bulb(470, 330, 175, 98, skin, hook=1.3, seed=2))
    # chin hairs + drool
    o.append(line([(470, 612), (462, 640), (476, 656)], sw=3))
    o.append(line([(510, 606), (518, 634)], sw=3))
    o.append(drips(560, 600, 560, "#bfe3d6", n=1, seed=1, length=(30, 50)))
    # crooked headscarf
    o.append(part(blob(470, 200, 165, 58, .12, 10, seed=15, rot=-.14), "#2f1a3c", sw=7))
    o.append(part(blob(620, 180, 48, 34, .15, 8, seed=16), "#2f1a3c", sw=6))
    o.append(part(tube([(655, 185), (720, 150), (770, 185), (790, 230)], 38, 10, seed=1), "#2f1a3c", sw=6))
    RIM["col"] = None
    return "\n".join(o), (480, 410, 300)


from c_grandma import *  # noqa
from c_auntie import *  # noqa
from c_gaga import *  # noqa

CREATURES = {
    "babha-yagha": ("Grandma", grandma),
    "grandma-darkling-knife": ("Grandma", darkling_knife),
    "grandma-darkling-knight": ("Grandma", darkling_knight),
    "berbalang-secret-eater": ("Grandma", berbalang),
    "rotbriar-hexer": ("Grandma", rotbriar_hexer),
    "soul-cage-porter": ("Grandma", soul_cage_porter),
    "thorn-memory-stalker": ("Grandma", thorn_stalker),
    "grandmas-flying-cauldron": ("Grandma", flying_cauldron),
    "grandmas-walking-hut": ("Grandma", walking_hut),
    "mama-yagha": ("Auntie", mama_yagha),
    "yuan-ti-fangguard": ("Auntie", fangguard),
    "coil-adept": ("Auntie", coil_adept),
    "spitebow-venom-archer": ("Auntie", spitebow),
    "petrifying-eye-acolyte": ("Auntie", eye_acolyte),
    "basilisk-chainmaster": ("Auntie", chainmaster),
    "venomwell-alchemist": ("Auntie", alchemist),
    "valdershmort": ("Auntie", valdershmort),
    "gahgah-yagha": ("Gaga", gahgah),
    "troll-linebreaker": ("Gaga", linebreaker),
    "troll-flesh-mender": ("Gaga", flesh_mender),
    "darkling-snail-lancer": ("Gaga", snail_lancer),
    "flail-snail-warbeast": ("Gaga", flail_snail),
    "spider-rider-harrier": ("Gaga", spider_rider),
    "rage-drum-goblin": ("Gaga", rage_drum),
}
