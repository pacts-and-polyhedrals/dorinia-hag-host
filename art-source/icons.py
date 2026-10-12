"""Ability & spell icons in the same grotesque-chibi ink style as the creature art."""
import hashlib, json, math, random, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from engine import *
from creatures import PAL

ICON_PAL = {
    "Grandma": ("#3a1f4c", "#8a4fb8", PAL["Grandma"]["glow"]),
    "Auntie": ("#16342a", "#4f8a3a", PAL["Auntie"]["glow"]),
    "Gaga": ("#4a1c10", "#a0442a", PAL["Gaga"]["glow"]),
    "Coven": ("#322a12", "#9a7a2a", PAL["Coven"]["glow"]),
    "school-nec": ("#1e2a1e", "#5a7a4a", "#b6ff7a"),
    "school-enc": ("#3a1838", "#a04a90", "#ff9adf"),
    "school-trs": ("#2a3416", "#7a8a2a", "#e8ff5a"),
    "school-evo": ("#3a2010", "#c0602a", "#ffb04a"),
    "school-con": ("#103030", "#2a8a8a", "#7affe8"),
    "school-div": ("#1a2a3e", "#5a7aa8", "#bfe6ff"),
    "school-abj": ("#1a2440", "#4a6ab0", "#ffe08a"),
    "school-ill": ("#261a40", "#6a4ab0", "#d0b0ff"),
}

C = (500, 520)


# ------------------------------------------------------------------ motifs (all centred ~ (500,520))
def m_claw(a, g):
    o = []
    for k, dx in enumerate((-150, 0, 150)):
        o.append(part(f"M{430+dx},{260} Q{560+dx},{420} {470+dx},{800} Q{520+dx},{560} {400+dx},{300} Z", "#e9dfc4", sw=8, highlight=1.4))
        o.append(drips(450 + dx, 480 + dx, 760, "#9a1a22", n=1, seed=k, length=(30, 60)))
    return o


def m_fangs(a, g):
    o = [part(blob(500, 520, 330, 250, .05, 14, seed=1), "#5a1020", sw=9)]
    for side in (-1, 1):
        o.append(part(f"M{500+side*160},{310} Q{500+side*120},{560} {500+side*60},{700} Q{500+side*170},{560} {500+side*240},{340} Z", "#efe6c4", sw=7, highlight=1.3))
    for x in (-60, 0, 60):
        o.append(flat(poly([(500 + x - 25, 330), (500 + x + 25, 330), (500 + x, 410)]), "#e3d8b0", sw=4))
        o.append(flat(poly([(500 + x - 25, 720), (500 + x + 25, 720), (500 + x, 640)]), "#e3d8b0", sw=4))
    o.append(drips(380, 620, 700, g, n=3, seed=2, length=(30, 80)))
    return o


def m_eye(a, g):
    return [glow(500, 520, 260, g, .45), flat("M160,520 Q500,200 840,520 Q500,820 160,520 Z", "#efe6d0", sw=10),
            eye(500, 520, 170, iris=g, pupil="slit", bloodshot=True, glow_col=None)]


def m_skull(a, g):
    o = [part(blob(500, 470, 250, 230, .04, 14, seed=3), "#e9dfc4", sw=10, highlight=1.3)]
    o.append(f'<ellipse cx="410" cy="470" rx="70" ry="80" fill="{INK}"/><ellipse cx="590" cy="470" rx="70" ry="80" fill="{INK}"/>')
    o.append(glow(410, 480, 40, g, .9)); o.append(glow(590, 480, 40, g, .9))
    o.append(flat(poly([(500, 560), (470, 620), (530, 620)]), INK, sw=4))
    o.append(part("M360,640 L640,640 L620,780 L380,780 Z", "#e9dfc4", sw=9, highlight=1.3))
    for x in range(390, 640, 50):
        o.append(line([(x, 645), (x + 5, 775)], sw=6))
    return o


def m_wisp(a, g):
    return [wisp(500, 430, 170, g, seed=4)]


def m_snake(a, g):
    pts = [(220, 800), (380, 760), (420, 620), (300, 520), (330, 380), (520, 330), (640, 400)]
    return [snake(pts, 90, 70, "#4e7a32", "#d9c66a", seed=5, head_size=110, eye_col=g)]


def m_poison(a, g):
    o = [glow(500, 560, 240, g, .5)]
    d = "M500,180 Q650,420 680,560 Q690,780 500,800 Q310,780 320,560 Q350,420 500,180 Z"
    o.append(part(d, shade(g, .7), sw=10, highlight=1.5))
    o.append(part(blob(500, 640, 110, 80, .06, 10, seed=6), "#e9dfc4", sw=6, hatch=False))
    o.append(f'<circle cx="460" cy="630" r="22" fill="{INK}"/><circle cx="540" cy="630" r="22" fill="{INK}"/>')
    o.append(line([(470, 690), (530, 690)], sw=6))
    o.append(bubbles(500, 360, 140, 60, 4, g, seed=7, size=(10, 22)))
    return o


def m_cloud(a, g):
    o = []
    for k, (x, y, r) in enumerate([(380, 560, 150), (520, 470, 180), (650, 580, 140), (500, 640, 160)]):
        o.append(part(blob(x, y, r, r * .8, .12, 10, seed=k), shade(g, .55), sw=8, highlight=1.4))
    o.append(f'<circle cx="460" cy="560" r="20" fill="{INK}"/><circle cx="560" cy="555" r="20" fill="{INK}"/>')
    o.append(line([(450, 620), (500, 640), (560, 615)], sw=7))
    return o


def m_flask(a, g):
    return [flask(500, 580, 210, g, seed=8)]


def m_chain(a, g):
    return [chain([(150, 300), (420, 560), (650, 420), (860, 760)], color="#9a9aa2", link=70)]


def m_spear(a, g):
    return [shaft(220, 820, 720, 320, w=40, color="#5a3a22"), spearhead(740, 300, -45, 110, color="#9aa4b0", barbed=True),
            drips(720, 800, 380, g, n=2, seed=3, length=(30, 70))]


def m_blade(a, g):
    return [blade(250, 800, 760, 230, 120, color="#8d96a3", edge=g, serrate=6),
            part(tube([(220, 830), (300, 750)], 50, 50), "#3a2a1e", sw=7)]


def m_arrow(a, g):
    return [line([(200, 800), (760, 280)], sw=28), line([(200, 800), (760, 280)], sw=14, color="#7a5a3a"),
            spearhead(770, 270, -43, 70, color="#9aa08a"),
            flat(poly([(200, 800), (150, 740), (240, 760)]), shade(g, .8), sw=5), flat(poly([(200, 800), (260, 850), (240, 760)]), shade(g, .8), sw=5),
            drips(760, 830, 300, g, n=2, seed=1, length=(30, 60))]


def m_drum(a, g):
    o = [part("M260,420 L740,420 L710,800 L290,800 Z", "#7a4a2a", sw=10)]
    o.append(part(blob(500, 420, 245, 70, .02, 12, seed=5), "#e3d2a8", sw=9, hatch=False))
    for k in range(5):
        x = 290 + k * 105
        o.append(line([(x, 430), (x + 52, 790)], sw=8)); o.append(line([(x + 105, 430), (x + 52, 790)], sw=8))
    for aa in range(-60, 70, 30):
        r = math.radians(aa - 90)
        o.append(line([(500 + math.cos(r) * 300, 380 + math.sin(r) * 140), (500 + math.cos(r) * 400, 380 + math.sin(r) * 200)], sw=12, color=g))
    return o


def m_sound(a, g):
    o = [part(blob(330, 520, 180, 170, .06, 12, seed=2), "#2a0608", sw=10)]
    o.append(f'<ellipse cx="330" cy="560" rx="80" ry="40" fill="#a02236"/>')
    for k in range(5):
        o.append(flat(poly([(240 + k * 45, 400), (275 + k * 45, 400), (258 + k * 45, 450)]), "#efe2b0", sw=4))
    for k, r in enumerate((150, 240, 330)):
        o.append(f'<path d="M{480 + r*.3},{520 - r} Q{520 + r},{520} {480 + r*.3},{520 + r}" fill="none" stroke="{INK}" stroke-width="{26 - k*4}"/>')
        o.append(f'<path d="M{480 + r*.3},{520 - r} Q{520 + r},{520} {480 + r*.3},{520 + r}" fill="none" stroke="{g}" stroke-width="{12 - k*2}"/>')
    return o


def m_bolt(a, g):
    return [glow(500, 520, 260, g, .5), part(poly([(560, 150), (330, 560), (480, 560), (400, 880), (700, 430), (540, 430), (640, 150)]), shade(g, 1.2), sw=10, highlight=1.6)]


def m_shield(a, g):
    d = "M500,170 Q680,240 800,230 Q800,620 500,860 Q200,620 200,230 Q320,240 500,170 Z"
    o = [part(d, "#5a6470", sw=11, highlight=1.8)]
    o.append(part("M500,280 Q610,320 690,315 Q690,580 500,740 Q310,580 310,315 Q390,320 500,280 Z", shade(g, .55), sw=7))
    o.append(eye(500, 500, 70, iris=g, pupil="slit"))
    return o


def m_heal(a, g):
    d = "M500,820 Q180,600 230,380 Q280,200 500,330 Q720,200 770,380 Q820,600 500,820 Z"
    o = [part(d, "#b0243a", sw=10, highlight=1.6)]
    o.append(line([(500, 330), (480, 450), (530, 560), (490, 700)], sw=8))
    for k in range(5):
        y = 380 + k * 70
        o.append(line([(440, y), (560, y + 15)], sw=6, color="#e9dfc4"))
    return o


def m_blood(a, g):
    d = "M500,160 Q680,450 690,600 Q690,800 500,820 Q310,800 310,600 Q320,450 500,160 Z"
    return [part(d, "#3a7a3a" if g != "#b6ff7a" else "#5a9a3a", sw=10, highlight=1.6),
            part(blob(500, 640, 90, 70, .1, 9, seed=3), "#8ab858", sw=6, hatch=False),
            line([(450, 620), (470, 600), (490, 625)], sw=6), line([(510, 620), (530, 600), (550, 625)], sw=6)]


def m_thorn(a, g):
    pts = [(160, 780), (330, 640), (460, 690), (600, 520), (760, 470), (840, 260)]
    return [line(pts, sw=46), line(pts, sw=30, color="#4a3a22"), spikes_along(pts, 22, "#2a1e10", side=1, seed=1),
            spikes_along(pts, 18, "#2a1e10", side=-1, seed=2), part(blob(800, 300, 70, 70, .3, 9, seed=3), "#8a1f35", sw=6, hatch=False)]


def m_spiral(a, g):
    pts = [(500 + math.cos(i * .42) * (10 + i * 7.5), 520 + math.sin(i * .42) * (10 + i * 7.5)) for i in range(48)]
    o = [glow(500, 520, 260, g, .45), line(pts, sw=40), line(pts, sw=22, color=shade(g, 1.2))]
    for aa in range(0, 360, 45):
        r = math.radians(aa)
        o.append(line([(500 + math.cos(r) * 330, 520 + math.sin(r) * 330), (500 + math.cos(r) * 390, 520 + math.sin(r) * 390)], sw=14, color=g))
    return o


def m_stone(a, g):
    o = [part(blob(500, 540, 300, 260, .14, 12, seed=4), "#8f8f88", sw=11, highlight=1.6)]
    o.append(f'<path d="{blob(500, 540, 300, 260, .14, 12, seed=4)}" fill="url(#xhatch)" opacity=".4"/>')
    for pts in ([(380, 320), (440, 470), (400, 560), (470, 700)], [(600, 340), (560, 470), (640, 560)], [(300, 600), (380, 640)]):
        o.append(line(pts, sw=8))
    o.append(eye(560, 600, 60, iris="#9a9a94", pupil="none", white="#b4b4ae"))
    return o


def m_web(a, g):
    o = []
    for k in range(8):
        r = math.radians(k * 45)
        o.append(line([(500, 520), (500 + math.cos(r) * 380, 520 + math.sin(r) * 380)], sw=7, color="#e8e8f0"))
    for rr in (100, 200, 300):
        pts = [(500 + math.cos(math.radians(k * 45)) * rr, 520 + math.sin(math.radians(k * 45)) * rr) for k in range(9)]
        o.append(line(pts, sw=6, color="#e8e8f0", smooth=False))
    return o


def m_mud(a, g):
    return [part(blob(500, 640, 340, 180, .2, 14, seed=2), "#5a4a32", sw=10), bubbles(500, 600, 220, 80, 7, "#7a6a4a", seed=3, size=(14, 34)),
            drips(250, 750, 760, "#4a3a28", n=5, seed=4, length=(40, 90))]


def m_moon(a, g):
    return [glow(500, 520, 280, g, .35), part("M560,170 Q260,260 270,520 Q290,800 600,860 Q400,700 400,520 Q410,320 560,170 Z", "#2a2438", sw=11, highlight=2.2),
            eye(470, 470, 50, iris=g, pupil="slit", glow_col=g)]


def m_feather(a, g):
    o = [part("M300,820 Q260,500 520,240 Q760,200 740,280 Q600,520 300,820 Z", "#22202a", sw=10, highlight=2.6)]
    o.append(line([(300, 820), (450, 560), (700, 280)], sw=7, color="#5a5668"))
    for k in range(6):
        o.append(line([(380 + k * 50, 690 - k * 70), (330 + k * 50, 600 - k * 70)], sw=4, color="#4a4658"))
    return o


def m_wing(a, g):
    return [bat_wing(380, 620, 1, 460, 380, "#3a2f3a", seed=3)]


def m_feet(a, g):
    o = []
    for k, (x, y) in enumerate([(360, 700), (560, 520), (420, 330)]):
        o.append(part(blob(x, y, 70, 100, .1, 9, seed=k, rot=-.4), "#6a5a4a", sw=8, hatch=False))
        for t in range(4):
            o.append(f'<circle cx="{x - 50 + t*30}" cy="{y - 110 + abs(t-1.5)*10}" r="18" fill="#6a5a4a" stroke="{INK}" stroke-width="5"/>')
    for k in range(4):
        o.append(line([(620, 700 + k * 40), (840, 700 + k * 40)], sw=8, color=g, opacity=.7))
    return o


def m_fear(a, g):
    o = [glow(500, 520, 280, g, .35), part(blob(500, 500, 260, 300, .06, 14, seed=7), "#d9d2c4", sw=10, highlight=1.3)]
    o.append(f'<ellipse cx="410" cy="430" rx="60" ry="80" fill="{INK}"/><ellipse cx="590" cy="430" rx="60" ry="80" fill="{INK}"/>')
    o.append(f'<ellipse cx="500" cy="660" rx="80" ry="120" fill="{INK}"/>')
    o.append(f'<circle cx="410" cy="440" r="16" fill="{g}"/><circle cx="590" cy="440" r="16" fill="{g}"/>')
    return o


def m_moths(a, g):
    from c_new import moth
    r = random.Random(3)
    return [moth(500 + r.uniform(-260, 260), 520 + r.uniform(-260, 260), r.uniform(50, 90), "#d9d2e6", seed=k, face=True) for k in range(9)] + \
           [moth(500, 520, 150, "#e8e2f0", seed=99, face=True)]


def m_sack(a, g):
    return [part(blob(500, 600, 260, 260, .1, 12, seed=1), "#a08a5a", sw=10), line([(380, 360), (500, 400), (620, 360)], sw=14),
            part(tube([(560, 330), (600, 230)], 50, 40, seed=2), "#e0b48a", sw=7, hatch=False),
            part(blob(605, 205, 50, 30, .1, 7, seed=3), "#4a2a1a", sw=6, hatch=False)]


def m_hammer(a, g):
    return [shaft(240, 830, 620, 390, w=44, color="#5a3a22"),
            part(poly([(500, 220), (820, 420), (720, 580), (400, 380)]), "#4a4440", sw=10, highlight=1.8),
            drips(640, 780, 520, "#9a1a22", n=2, seed=3, length=(30, 70))]


def m_toad(a, g):
    return [part(blob(500, 600, 320, 220, .05, 14, seed=3), "#6b7a3a", sw=10), warts(500, 580, 260, 160, 8, "#8a9a4a", seed=4, size=(12, 26)),
            eye(360, 430, 70, iris="#ffb02a", pupil="slit", lid=.3), eye(640, 430, 70, iris="#ffb02a", pupil="slit", lid=.3),
            line([(260, 640), (500, 700), (740, 640)], sw=12)]


def m_flame(a, g):
    return [glow(500, 560, 260, "#ff8a2a", .5), part("M500,170 Q720,420 680,620 Q640,820 500,830 Q340,820 320,620 Q300,450 420,330 Q440,480 500,500 Q470,330 500,170 Z", "#ff7a2a", sw=10, highlight=1.6)]


def m_crown(a, g):
    return [glow(500, 520, 260, g, .35), part("M200,700 L230,320 L360,520 L500,260 L640,520 L770,320 L800,700 Z", "#c9a83a", sw=11, highlight=1.8),
            *[f'<circle cx="{x}" cy="{y}" r="34" fill="{g}" stroke="{INK}" stroke-width="7"/>' for x, y in ((230, 320), (500, 260), (770, 320))],
            line([(220, 640), (780, 640)], sw=10)]


def m_book(a, g):
    return [glow(500, 520, 260, g, .4), part("M180,280 Q340,230 500,300 Q660,230 820,280 L820,780 Q660,730 500,800 Q340,730 180,780 Z", "#4a2a3a", sw=10),
            line([(500, 300), (500, 800)], sw=10), eye(340, 520, 60, iris=g, pupil="slit"), wisp(660, 500, 60, g, seed=1, face=False)]


def m_hand(a, g):
    return [hand(500, 560, 170, "#8a9a7a", fingers=4, spread=90, angle=-90, seed=3, curl=.35), chain([(360, 760), (500, 860), (660, 780)], link=40)]


def m_crossed(a, g):
    return [blade(220, 820, 780, 230, 80, color="#8d96a3", edge=g), blade(780, 820, 220, 230, 80, color="#8d96a3", edge=g)]


def m_star(a, g):
    pts = []
    for k in range(16):
        r = 360 if k % 2 == 0 else 150
        a_ = math.radians(k * 22.5 - 90)
        pts.append((500 + math.cos(a_) * r, 520 + math.sin(a_) * r))
    return [glow(500, 520, 240, g, .6), part(poly(pts), shade(g, 1.1), sw=10, highlight=1.5)]


MOTIFS = [
    (r"legendary resistance", m_crown), (r"^(spellcasting|innate spellcasting|shared spellcasting)", m_book), (r"^multiattack", m_crossed),
    (r"regenerat|troll-blood|boil", m_blood), (r"stitch|mend|heal|cure|\baid\b|restoration|spare the dying|gut-|antivenom", m_heal),
    (r"\bdrum|warbeat|rhythm|marching", m_drum),
    (r"\bmoth|swarm|insect|servants|summon|brood", m_moths), (r"crow|feather|mimic", m_feather), (r"toad|tongue|amphib|hallucinogen", m_toad),
    (r"sack|bag it|snatch|steal|pilfer|light-finger", m_sack),
    (r"web|bola|snare|grease", m_web), (r"mud|muck|bogle|puddle", m_mud),
    (r"legendary|crown|matriarch|command\b|archfey|glamour|battery", m_crown),
    (r"bite|fang|kiss|gnaw|jaw|maw", m_fangs), (r"claw|talon|rake|rend", m_claw),
    (r"skull|death|necro|soul|lantern|siphon|harm|inflict|blight|animate dead|speak with dead|magic jar|vampiric|chill touch|hollow|grave|sip", m_skull),
    (r"wisp|spirit|steal|stolen breath|drain", m_wisp),
    (r"stone|petrif|calcif|stiffen|gorgon|earth|stomp|meld into|stoneskin|thrall", m_stone),
    (r"\beye|gaze|glare|glance|sight|scry|clairvoy|seeing|detect|locate|identify|contact other|divination|oracle|scent|smell", m_eye),
    (r"snake|serpent|coil|viper|yuan|slither|constrict|hair|adder|venom command", m_snake),
    (r"cloud|stinking|cloudkill|fog", m_cloud), (r"poison|venom|toxic|spray|rot\b|coven's rot", m_poison),
    (r"acid|flask|bomb|alchem|mortar|potion|logistics", m_flask),
    (r"chain|leash|drive the beast|handler|grip|embrace|seize|grapple|hold (person|monster)|tentacle|fling", m_chain),
    (r"\bbow\b|arrow|sling|volley|marked", m_arrow),
    (r"lightning|shock|thunder|shatter", m_bolt),
    (r"howl|bellow|cackle|song|lullaby|mockery|message|suggestion|laughter|scream|break their line", m_sound),
    (r"shield|screen|scales|drill|protection|bastion|ward|resistance|immutable|antimagic|evasion", m_shield),
    (r"thorn|briar|bramble|rooted|wall of", m_thorn), (r"hex|curse|bane", m_spiral),
    (r"dark|shadow|veil|snuff|light|moon|death flash|false appearance", m_moon),
    (r"fear|fright|phantasmal|weird|nightmare|dream|terror|prey on", m_fear),
    (r"charm|enchant|dominate|memory|feeblemind|confusion|polymorph|hypnot|name|enraging|enlarge", m_spiral),
    (r"spear|lance|glaive|needle|dagger|knife|hook|blade|saw", m_spear),
    (r"log|ram|door|siege|breach|slam|maul|mallet|morningstar|headbutt|sweep|stun|pelting|brute|surprise", m_hammer),
    (r"fly|wing|flyby|haste|jump|run|blur|escape|nimble|disengage|teleport|plane shift|misty|charge|speed|harrier|webline|chicken", m_feet),
    (r"fire|flame|burn", m_flame),
    (r"counterspell|mounted hunter", m_shield), (r"thought carrion|blindness|pulse", m_eye), (r"secret relay|guidance", m_spiral),
    (r"telekinesis", m_hand), (r"shoulder break", m_hammer),
]


OVERRIDES = [
    (r"eyebite|two heads|pack bound", m_eye), (r"coils of the mother", m_snake), (r"animal friendship", m_snake),
    (r"charm person|minor illusion|hag-ring", m_spiral), (r"grim conduit|ray of enfeeblement", m_skull),
    (r"soul battery|soul steal", m_wisp), (r"hooked maul", m_hammer), (r"mage hand", m_hand),
    (r"prestidigitation|thaumaturgy", m_star), (r"hollow song|grave howl", m_sound),
    (r"bone saw|shadow knife|pilfering dagger|thorn needle|glass talon", m_blade),
    (r"chill touch|finger of death", m_hand), (r"inflict wounds|mind-talon", m_claw), (r"vampiric touch", m_fangs),
    (r"circle of death|weird", m_fear), (r"magic jar", m_flask), (r"speak with dead", m_sound), (r"^blight", m_thorn),
    (r"siphon spark|withering bolt|ray of", m_bolt), (r"soul sip", m_moths), (r"death flash|scintillating", m_star),
    (r"soul lantern", m_wisp), (r"hollow the name|feeblemind", m_fear), (r"archfey drain", m_wisp),
    (r"slam attack|siege monster", m_hammer), (r"dread pennant|black banner", m_spear), (r"snuffing hook", m_spear),
    (r"stinking cloud|cloudkill", m_cloud), (r"insect plague|giant insect", m_moths), (r"flesh to stone|wall of stone|stone shape", m_stone),
]


def pick(name, text):
    for rx, fn in OVERRIDES:
        if re.search(rx, name, re.I):
            return fn
    for rx, fn in MOTIFS:
        if re.search(rx, name, re.I):
            return fn
    for rx, fn in MOTIFS:
        if re.search(rx, text, re.I):
            return fn
    return m_star


def pick2(name, text, first):
    seen = []
    for rx, fn in OVERRIDES + MOTIFS:
        if fn is not first and fn not in seen and (re.search(rx, text, re.I) or re.search(rx, name, re.I)):
            seen.append(fn)
    return seen[0] if seen else None


ACCENTS = [m_wisp, m_star, m_eye, m_spiral, m_poison, m_skull, m_moon]


def icon_svg(key, info):
    bg, mid, g = ICON_PAL.get(info["pal"], ICON_PAL["Coven"])
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    rot = (h % 21) - 10
    fn = pick(info["name"], info["text"])
    fn2 = pick2(info["name"], info["text"], fn) or ACCENTS[h % len(ACCENTS)]
    if fn2 is fn:
        fn2 = ACCENTS[(h + 1) % len(ACCENTS)]
    RIM["col"] = g
    motif = "\n".join(fn(None, g))
    badge = ("<g transform='translate(640 640) scale(.36)'>"
             f"<circle cx='500' cy='520' r='430' fill='{bg}' stroke='{INK}' stroke-width='40'/>"
             f"<circle cx='500' cy='520' r='390' fill='none' stroke='{shade(mid,1.4)}' stroke-width='14'/>"
             + "\n".join(fn2(None, g)) + "</g>")
    RIM["col"] = None
    rr = random.Random(h)
    splat = "".join(f'<circle cx="{rr.uniform(60,940):.0f}" cy="{rr.uniform(60,940):.0f}" r="{rr.uniform(4,14):.0f}" fill="{INK}" opacity=".6"/>' for _ in range(10))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">{defs()}'
            f'<radialGradient id="ibg" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="{mid}"/><stop offset="1" stop-color="{bg}"/></radialGradient>'
            f'<clipPath id="ic"><rect x="30" y="30" width="940" height="940" rx="90"/></clipPath>'
            f'<g clip-path="url(#ic)"><rect width="1000" height="1000" fill="url(#ibg)"/>'
            f'<rect width="1000" height="1000" fill="{shade(mid,1.3)}" filter="url(#mottle)" opacity=".3"/>{splat}'
            f'<g transform="translate(-60 -60) scale(.92) rotate({rot} 560 580)"><g filter="url(#ink)">{motif}</g></g><g filter="url(#ink)">{badge}</g>'
            f'<rect width="1000" height="1000" fill="#000" filter="url(#grain)" opacity=".35"/>'
            f'<rect x="30" y="30" width="940" height="940" rx="90" fill="none" stroke="{INK}" stroke-width="40" opacity=".35" filter="url(#softglow)"/></g>'
            f'<rect x="30" y="30" width="940" height="940" rx="90" fill="none" stroke="{INK}" stroke-width="36"/>'
            f'<rect x="58" y="58" width="884" height="884" rx="66" fill="none" stroke="{shade(mid,1.4)}" stroke-width="8" opacity=".8"/></svg>')


if __name__ == "__main__":
    needs = json.loads(Path(sys.argv[1]).read_text())
    out = Path(__file__).parent / "out" / "icons"
    (out / "svg").mkdir(parents=True, exist_ok=True)
    (out / "png").mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[3:])
    jobs = []
    for key, info in needs.items():
        if only and key not in only:
            continue
        (out / "svg" / f"{key}.svg").write_text(icon_svg(key, info))
        jobs.append({"svg": str(out / "svg" / f"{key}.svg"), "png": str(out / "png" / f"{key}.png"), "size": 256})
    (out / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(Path(__file__).parent / "render.mjs"), str(out / "jobs.json")], check=True)
    from PIL import Image
    dest = Path(sys.argv[2]); dest.mkdir(parents=True, exist_ok=True)
    for j in jobs:
        k = Path(j["png"]).stem
        Image.open(j["png"]).save(dest / f"{k}.webp", "WEBP", quality=88, method=6)
    print("icons", len(jobs))
