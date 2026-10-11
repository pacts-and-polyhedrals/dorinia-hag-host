"""
Spell lists for the Yagha Coven War Host.

OFFICIAL spells are copied from the dnd5e system's SRD 5.1 source (CC-BY-4.0), vendored in
source/srd-spells/. HOMEBREW spells are defined below and built into full dnd5e 5.3.3 spell items.

Methods:  "spell"  = prepared, uses the actor's spell slots (attributes.spell.level)
          "atwill" = at will
          "innate" = N/day (uses)
          coven=True  = Shared Spellcasting; uses are synced across all three hags by the module script
"""

# --------------------------------------------------------------------------- casters
CASTERS = {
    "Babha Yagha": {"ability": "cha", "level": 17, "title": "Grandma"},
    "Mama Yagha": {"ability": "cha", "level": 11, "title": "Auntie"},
    "Gahgah Yagha": {"ability": "cha", "level": 9, "title": "Gaga"},
    "Rotbriar Hexer": {"ability": "cha", "level": 0},
    "Petrifying Eye Acolyte": {"ability": "wis", "level": 0},
    "Venomwell Alchemist": {"ability": "int", "level": 0},
    "Berbalang Secret-Eater": {"ability": "int", "level": 0},
    "Troll Flesh-Mender": {"ability": "wis", "level": 0},
}

# The Yagha Coven's shared list (MM hag-coven list; homebrew stands in for non-SRD spells)
COVEN = [
    ("identify", 1), ("Coven's Rot", 1),
    ("hold-person", 1), ("locate-object", 1),
    ("bestow-curse", 1), ("counterspell", 1), ("lightning-bolt", 1),
    ("phantasmal-killer", 1), ("polymorph", 1),
    ("contact-other-plane", 1), ("scrying", 1), ("Archfey Drain", 1),
    ("eyebite", 1), ("Hag-Ring of Highforest", 1),
]

# (spell, method, uses)  — slug = SRD file name, Title Case = homebrew
LISTS = {
    "Babha Yagha": [
        ("chill-touch", "spell", None), ("minor-illusion", "spell", None), ("mage-hand", "spell", None), ("vicious-mockery", "spell", None),
        ("bane", "spell", None), ("hideous-laughter", "spell", None), ("inflict-wounds", "spell", None),
        ("darkness", "spell", None), ("ray-of-enfeeblement", "spell", None), ("detect-thoughts", "spell", None),
        ("animate-dead", "spell", None), ("vampiric-touch", "spell", None), ("speak-with-dead", "spell", None), ("Soul Lantern Siphon", "spell", None),
        ("blight", "spell", None), ("black-tentacles", "spell", None),
        ("dominate-person", "spell", None), ("dream", "spell", None), ("modify-memory", "spell", None), ("Grandma's Lullaby", "spell", None),
        ("circle-of-death", "spell", None), ("magic-jar", "spell", None),
        ("finger-of-death", "spell", None), ("Hollow the Name", "spell", None),
        ("feeblemind", "spell", None),
        ("weird", "spell", None),
    ],
    "Mama Yagha": [
        ("poison-spray", "spell", None), ("acid-splash", "spell", None), ("minor-illusion", "spell", None), ("mage-hand", "spell", None),
        ("charm-person", "spell", None), ("animal-friendship", "spell", None), ("Viper's Kiss", "spell", None),
        ("acid-arrow", "spell", None), ("suggestion", "spell", None), ("protection-from-poison", "spell", None),
        ("stinking-cloud", "spell", None), ("slow", "spell", None), ("Coils of the Mother Serpent", "spell", None),
        ("confusion", "spell", None), ("giant-insect", "spell", None),
        ("cloudkill", "spell", None), ("insect-plague", "spell", None), ("Gorgon Bloom", "spell", None),
        ("flesh-to-stone", "spell", None),
    ],
    "Gahgah Yagha": [
        ("thaumaturgy", "spell", None), ("message", "spell", None),
        ("command", "spell", None), ("jump", "spell", None),
        ("enlarge-reduce", "spell", None), ("shatter", "spell", None), ("Twin-Throat Bellow", "spell", None),
        ("haste", "spell", None), ("Troll-Blood Boil", "spell", None),
        ("stoneskin", "spell", None), ("stone-shape", "spell", None), ("Earthshaker Stomp", "spell", None),
        ("telekinesis", "spell", None), ("wall-of-stone", "spell", None),
    ],
    "Rotbriar Hexer": [
        ("vicious-mockery", "atwill", None), ("minor-illusion", "atwill", None),
        ("bane", "innate", 2), ("Rotbriar Hex", "innate", 2),
        ("hold-person", "innate", 1), ("bestow-curse", "innate", 1),
    ],
    "Petrifying Eye Acolyte": [
        ("guidance", "atwill", None), ("thaumaturgy", "atwill", None),
        ("hold-person", "innate", 2), ("blindness-deafness", "innate", 2),
        ("slow", "innate", 1), ("Gorgon's Glance", "innate", 1),
    ],
    "Venomwell Alchemist": [
        ("mage-hand", "atwill", None), ("prestidigitation", "atwill", None),
        ("grease", "innate", 2), ("protection-from-poison", "innate", 2), ("Venomwell Bomb", "innate", 2),
        ("stinking-cloud", "innate", 1),
    ],
    "Berbalang Secret-Eater": [
        ("speak-with-dead", "atwill", None),
        ("detect-thoughts", "innate", 1), ("plane-shift", "innate", 2),
    ],
    "Troll Flesh-Mender": [
        ("spare-the-dying", "atwill", None),
        ("aid", "innate", 1), ("Gut-Stitch", "innate", 2),
        ("lesser-restoration", "innate", 1),
    ],
}

# Who gets the shared coven list
COVEN_MEMBERS = ["Babha Yagha", "Mama Yagha", "Gahgah Yagha"]

# --------------------------------------------------------------------------- homebrew
# kind: save | attack | heal | utility   ; dmg: [(formula, type)] ; scale: dice added per slot level above base
HOMEBREW = {
    # ---- Coven
    "Coven's Rot": dict(owner="Coven", level=1, school="nec", comps=["vocal", "somatic"], time="action", range=(60, "ft"),
        duration=(None, "inst"), target=("1", "creature"), kind="save", save="con", dmg=[("2d8", "poison")], on_save="half",
        statuses=[("poisoned", 1)], scale=1,
        text="A ray of green-black rot leaps from the casting hag's finger. The target makes a Constitution saving throw, taking 2d8 poison damage on a failure and becoming poisoned until the end of your next turn, or half as much damage on a success. <em>The Yagha Coven's stand-in for ray of sickness.</em>",
        higher="+1d8 poison damage for each slot level above 1st."),
    "Archfey Drain": dict(owner="Coven", level=5, school="nec", comps=["vocal", "somatic", "material"], material="a sliver of an Archfey's crown",
        time="action", range=(90, "ft"), duration=(None, "inst"), target=("1", "creature"), kind="save", save="cha",
        dmg=[("8d8", "necrotic")], on_save="half", scale=1, heal_self=True,
        text="The coven pulls the fey-glamour out of a creature like thread from a sleeve. The target makes a Charisma saving throw, taking 8d8 necrotic damage on a failure or half on a success. Fey and creatures with the Fey Ancestry trait have disadvantage on the save. Each hag of the coven within 30 feet of the caster regains hit points equal to half the damage dealt.",
        higher="+1d8 necrotic damage for each slot level above 5th."),
    "Hag-Ring of Highforest": dict(owner="Coven", level=6, school="enc", comps=["vocal", "somatic"], time="action", range=(None, "self"),
        duration=(1, "minute"), conc=True, template=("sphere", 30), kind="save", save="wis", dmg=[], on_save="none",
        statuses=[("frightened", 10)], scale=0,
        text="The three hags join hands—or claws—and the old Highforest ring reopens around them. Each creature of your choice within 30 feet of the caster makes a Wisdom saving throw or is frightened of the coven for the duration. A frightened creature that starts its turn inside the ring takes 4d6 psychic damage. While the ring holds, creatures inside it have disadvantage on saving throws against spells cast by members of the coven.",
        rider=[("4d6", "psychic")]),
    # ---- Grandma
    "Soul Lantern Siphon": dict(owner="Grandma", level=3, school="nec", comps=["vocal", "somatic", "material"], material="Grandma's soul lantern",
        time="action", range=(60, "ft"), duration=(None, "inst"), target=("1", "creature"), kind="save", save="cha",
        dmg=[("5d8", "necrotic")], on_save="half", scale=1, temp=True,
        text="A wisp of the target's soul is tugged into the lantern. The target makes a Charisma saving throw, taking 5d8 necrotic damage on a failure or half as much on a success. You gain temporary hit points equal to half the necrotic damage dealt, and a new screaming face appears in the lantern.",
        higher="+1d8 necrotic damage for each slot level above 3rd."),
    "Grandma's Lullaby": dict(owner="Grandma", level=5, school="enc", comps=["vocal"], time="action", range=(None, "self"),
        duration=(1, "minute"), conc=True, template=("sphere", 30), kind="save", save="wis", dmg=[("6d6", "psychic")], on_save="half",
        statuses=[("unconscious", 10)], scale=1,
        text="Grandma croons a bedtime song from a childhood nobody remembers having. Each creature of her choice within 30 feet makes a Wisdom saving throw, taking 6d6 psychic damage and falling unconscious for the duration on a failure, or half damage on a success. A sleeper wakes if it takes damage or someone uses an action to shake it awake—and dreams of the lantern until its next long rest.",
        higher="+1d6 psychic damage for each slot level above 5th."),
    "Hollow the Name": dict(owner="Grandma", level=7, school="nec", comps=["vocal", "somatic"], time="action", range=(60, "ft"),
        duration=(None, "inst"), target=("1", "creature"), kind="save", save="int", dmg=[("10d10", "psychic")], on_save="half",
        statuses=[("stunned", 1)], scale=0,
        text="Grandma speaks the target's true name backwards and eats it. The target makes an Intelligence saving throw. On a failure it takes 10d10 psychic damage, is stunned until the end of your next turn, and forgets its own name and the names of its companions until it finishes a long rest or receives greater restoration. On a success it takes half damage only."),
    # ---- Auntie
    "Viper's Kiss": dict(owner="Auntie", level=1, school="trs", comps=["vocal"], time="bonus", range=(None, "self"),
        duration=(1, "round"), target=("", "self"), kind="damage", dmg=[("2d10", "poison")], scale=1,
        statuses=[("poisoned", 10)],
        text="Venom wells in your fangs and claws. The next time you hit a creature with a melee weapon attack before the end of this turn, the attack deals an extra 2d10 poison damage and the target must succeed on a Constitution saving throw or be poisoned for 1 minute. A poisoned target repeats the save at the end of each of its turns, ending the effect on a success. Resistance to poison damage doesn't reduce this extra damage.",
        higher="+1d10 poison damage for each slot level above 1st."),
    "Coils of the Mother Serpent": dict(owner="Auntie", level=3, school="con", comps=["vocal", "somatic"], time="action", range=(60, "ft"),
        duration=(1, "minute"), conc=True, target=("1", "creature"), kind="save", save="str", dmg=[("3d8", "bludgeoning")], on_save="none",
        statuses=[("restrained", 10)], scale=1,
        text="A spectral python erupts from the ground and coils around a Large or smaller creature. The target makes a Strength saving throw. On a failure it takes 3d8 bludgeoning damage and is restrained for the duration, taking 3d8 bludgeoning damage again at the start of each of its turns. It can repeat the save at the end of each of its turns, ending the effect on a success. Poisoned targets have disadvantage on the save.",
        higher="+1d8 bludgeoning damage for each slot level above 3rd."),
    "Gorgon Bloom": dict(owner="Auntie", level=5, school="trs", comps=["vocal", "somatic"], time="action", range=(None, "self"),
        duration=(None, "inst"), template=("cone", 30), kind="save", save="con", dmg=[("6d8", "poison")], on_save="half",
        statuses=[("restrained", 1), ("petrified", 10)], scale=1,
        text="Auntie's snake-hair fans into a hood of staring eyes. Each creature in a 30-foot cone makes a Constitution saving throw, taking 6d8 poison damage and becoming restrained as its flesh greys on a failure, or half damage on a success. A creature restrained this way repeats the save at the end of its next turn; on a second failure it is petrified for 1 minute (or until greater restoration).",
        higher="+1d8 poison damage for each slot level above 5th."),
    # ---- Gaga
    "Twin-Throat Bellow": dict(owner="Gaga", level=2, school="evo", comps=["vocal"], time="action", range=(None, "self"),
        duration=(None, "inst"), template=("cone", 30), kind="save", save="con", dmg=[("4d8", "thunder")], on_save="half",
        statuses=[("prone", None)], scale=1,
        text="Both of Gaga's heads roar in different keys. Each creature in a 30-foot cone makes a Constitution saving throw, taking 4d8 thunder damage, being pushed 15 feet away and knocked prone on a failure, or half damage only on a success.",
        higher="+1d8 thunder damage for each slot level above 2nd."),
    "Troll-Blood Boil": dict(owner="Gaga", level=3, school="trs", comps=["vocal", "somatic"], time="bonus", range=(None, "self"),
        duration=(1, "minute"), target=("", "self"), kind="heal", heal=("4d10", "temphp"), scale=0,
        text="Gaga's blood boils green and the wounds slam shut. She gains 4d10 temporary hit points, and for the duration her Regeneration restores an extra 10 hit points and acid damage no longer suppresses it."),
    "Earthshaker Stomp": dict(owner="Gaga", level=4, school="evo", comps=["somatic"], time="action", range=(None, "self"),
        duration=(None, "inst"), template=("sphere", 20), kind="save", save="dex", dmg=[("6d8", "bludgeoning")], on_save="half",
        statuses=[("prone", None)], scale=1,
        text="Gaga stomps, and the ground buckles in a 20-foot radius around her. Each other creature in the area makes a Dexterity saving throw, taking 6d8 bludgeoning damage and falling prone on a failure, or half damage on a success. The area becomes difficult terrain until cleared.",
        higher="+1d8 bludgeoning damage for each slot level above 4th."),
    # ---- Servants
    "Rotbriar Hex": dict(owner="Servants", level=1, school="nec", comps=["vocal", "somatic", "material"], material="a thorn dipped in the target's blood",
        time="bonus", range=(90, "ft"), duration=(1, "hour"), conc=True, target=("1", "creature"), kind="damage", dmg=[("1d6", "necrotic")], scale=0,
        text="You mark a creature with a thorn-sigil. Until the spell ends you deal an extra 1d6 necrotic damage to it whenever you hit it with an attack, and it has disadvantage on ability checks made with one ability of your choice. If a Grandma ally imposes the frightened condition on another creature, you can move the mark to that creature without an action (Coven Relay)."),
    "Gorgon's Glance": dict(owner="Servants", level=3, school="trs", comps=["somatic"], time="action", range=(60, "ft"),
        duration=(1, "minute"), target=("1", "creature"), kind="save", save="con", dmg=[("4d8", "poison")], on_save="half",
        statuses=[("petrified", 10)], scale=1,
        text="The acolyte's third eye opens fully on one creature. The target makes a Constitution saving throw, taking 4d8 poison damage on a failure or half on a success. If the target was already restrained when it failed, it is instead petrified for 1 minute; it repeats the save at the end of each of its turns, ending the effect on a success. This is how the acolyte finishes what Stone Glare starts.",
        higher="+1d8 poison damage for each slot level above 3rd."),
    "Venomwell Bomb": dict(owner="Servants", level=2, school="con", comps=["somatic", "material"], material="a sealed flask of venomwell distillate",
        time="action", range=(60, "ft"), duration=(1, "minute"), conc=True, template=("sphere", 10), kind="save", save="dex",
        dmg=[("3d6", "acid")], on_save="half", statuses=[], scale=1,
        rider=[("3d6", "acid")], rider_name="Acid Pool (enter or start turn)",
        text="You lob a flask that bursts into a hissing pool of acid in a 10-foot radius. Each creature in the area makes a Dexterity saving throw, taking 3d6 acid damage on a failure or half on a success. Until the spell ends, the pool is difficult terrain, and a creature that enters it for the first time on a turn or starts its turn there takes 3d6 acid damage. Unlike Venom Mortar, this is a lasting acid hazard that also eats through nonmagical objects in the pool.",
        higher="+1d6 acid damage (initial and pool) for each slot level above 2nd."),
    "Gut-Stitch": dict(owner="Servants", level=2, school="nec", comps=["vocal", "somatic", "material"], material="a bone needle and gut thread",
        time="action", range=(5, "ft"), duration=(None, "inst"), target=("1", "ally"), kind="heal", heal=("3d8+3", "healing"), scale=1,
        text="You sew a wound shut with filthy thread. A creature you touch regains 3d8 + 3 hit points. A troll healed this way also regenerates 5 extra hit points at the start of its next turn; anyone else must succeed on a DC 11 Constitution saving throw or be poisoned for 1 hour.",
        higher="+1d8 healing for each slot level above 2nd."),
}

SCHOOL_ICON = {"nec": "icons/magic/death/skull-energy-light-purple.webp", "enc": "icons/magic/control/hypnosis-mesmerism-swirl.webp",
               "trs": "icons/magic/nature/snake-poison-green.webp", "evo": "icons/magic/sonic/explosion-shock-wave-teal.webp",
               "con": "icons/magic/nature/root-vine-entangled-humanoid.webp"}
