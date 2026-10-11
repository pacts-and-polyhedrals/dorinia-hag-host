export const ACTORS = [
  {
    "name": "Babha Yagha \u2014 Grandma, Malevolent Matriarch",
    "faction": "Grandma",
    "role": "Supreme controller / soul attrition",
    "cr": 22,
    "ac": 17,
    "hp": 330,
    "abilities": {
      "str": 18,
      "dex": 16,
      "con": 16,
      "int": 22,
      "wis": 18,
      "cha": 24
    },
    "size": "lg",
    "type": "fiend",
    "subtype": "hag",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "abyssal",
      "common",
      "draconic",
      "sylvan"
    ],
    "saves": [
      "str",
      "dex",
      "con",
      "int",
      "wis",
      "cha"
    ],
    "skills": {
      "arc": 1,
      "dec": 1,
      "ins": 1,
      "itm": 1,
      "nat": 1,
      "prc": 1,
      "ste": 1
    },
    "res": [
      "necrotic"
    ],
    "imm": [
      "cold",
      "fire",
      "poison"
    ],
    "cond": [
      "charmed",
      "frightened",
      "poisoned"
    ],
    "traits": [
      "Legendary Resistance (3/Day). If Grandma fails a saving throw, she can choose to succeed instead.",
      "Magic Resistance. Grandma has advantage on saving throws against spells and other magical effects.",
      "Regeneration. Grandma regains 20 hit points at the start of her turn if she has at least 1 hit point.",
      "Doorinian Matriarch. Friendly Grandma units within 30 feet gain advantage on saving throws against frightened and charmed effects."
    ],
    "actions": [
      {
        "name": "Claw",
        "kind": "attack",
        "text": "Two claws are normally used after Frightening Gaze.",
        "tohit": 9,
        "damage": [
          [
            "2d8+4",
            "slashing"
          ],
          [
            "4d6",
            "poison"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Frightening Gaze",
        "kind": "save",
        "text": "One creature within 30 ft. that can see Grandma must save or become frightened for 1 minute; repeat at end of each turn.",
        "dc": 22,
        "ability": "wis"
      },
      {
        "name": "Soul Steal",
        "kind": "save",
        "text": "One creature within 60 ft. makes a Charisma save. On failure its hit point maximum is reduced by the necrotic damage rolled; a creature reduced to 0 maximum HP dies.",
        "dc": 22,
        "ability": "cha",
        "damage": [
          [
            "6d10",
            "necrotic"
          ]
        ],
        "onSave": "none"
      },
      {
        "name": "Summon Darklings (1/Day)",
        "kind": "utility",
        "text": "Summon 2d4 Grandma Darklings in unoccupied spaces within 60 ft. They roll their own initiative and remain for 1 hour or until dismissed."
      }
    ],
    "legendary": [
      "Cackle (1). Creatures within 30 ft. make DC 21 Wisdom saves or become frightened for 1 minute.",
      "Summon Servants (2). Summon 1d4+1 Darklings, Berbalangs, or other Grandma minions within 30 ft.",
      "Rotting Curse (3). One creature within 60 ft. makes DC 21 Constitution save, taking 8d8 necrotic damage on a failure and aging 1d6 x 10 years; half damage and no aging on success."
    ],
    "desc": "Once the architect of the coven's Highforest atrocities, Babha Yagha is now called Grandma throughout Doorinia. She drains captured Archfey to rewrite the Domain of Delight and rules through secrets, curses, and disciplined waves of expendable servants."
  },
  {
    "name": "Mama Yagha \u2014 Auntie, Venomous Fang",
    "faction": "Auntie",
    "role": "Poison commander / petrification",
    "cr": 15,
    "ac": 17,
    "hp": 330,
    "abilities": {
      "str": 22,
      "dex": 18,
      "con": 20,
      "int": 18,
      "wis": 14,
      "cha": 20
    },
    "size": "lg",
    "type": "fiend",
    "subtype": "hag",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "abyssal",
      "common",
      "draconic",
      "giant",
      "infernal",
      "yuan-ti"
    ],
    "saves": [
      "str",
      "dex",
      "con",
      "int",
      "wis",
      "cha"
    ],
    "skills": {
      "arc": 1,
      "dec": 1,
      "prc": 1,
      "ste": 1
    },
    "res": [
      "cold",
      "fire"
    ],
    "imm": [
      "poison"
    ],
    "cond": [
      "charmed",
      "poisoned"
    ],
    "traits": [
      "Rejuvenation. When slain, Auntie collapses into a stone serpent idol until next dawn; unless the idol is destroyed or specially warded, she returns at full hit points.",
      "Shapechanger. Auntie can assume a giant serpent form without changing her statistics.",
      "Snake Hair. A creature that starts its turn within 5 ft. of Auntie must make DC 19 Constitution save, taking 6d6 poison damage on failure or half on success.",
      "Spell Resistance. Auntie has advantage on saving throws against spells and magical effects.",
      "Venom Command. A poisoned enemy within 30 ft. of Auntie grants advantage to the first attack made against it by one of Auntie's minions each round."
    ],
    "actions": [
      {
        "name": "Claws",
        "kind": "attack",
        "text": "Auntie tears at a nearby victim.",
        "tohit": 12,
        "damage": [
          [
            "2d8+6",
            "slashing"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Venomous Bite",
        "kind": "attack",
        "text": "Auntie bites with serpent fangs.",
        "tohit": 12,
        "damage": [
          [
            "2d8+6",
            "piercing"
          ],
          [
            "4d6",
            "poison"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Cloud of Venom",
        "kind": "save",
        "text": "A 20-foot-radius cloud of venom erupts at a point within 90 ft. Creatures make Constitution saves; the cloud remains lightly obscuring until Auntie's next turn.",
        "dc": 19,
        "ability": "con",
        "damage": [
          [
            "6d8",
            "poison"
          ]
        ]
      },
      {
        "name": "Serpent Command",
        "kind": "utility",
        "text": "One Auntie minion within 60 ft. may move up to half its speed and make one attack as a reaction."
      }
    ],
    "legendary": [
      "Venomous Bite (1). Make one bite attack.",
      "Serpentine Coils (1). Move up to speed without provoking; creatures moved through make DC 17 Dexterity save or take 2d8+4 bludgeoning and fall prone.",
      "Snake Hair (1). Up to three creatures within 30 ft. make DC 17 Dexterity saves or take 2d8+4 piercing damage and become poisoned until they save at end of turn.",
      "Recharge Innate Magic (2). Roll d6; on 5-6 recharge one limited magical feature of Auntie or an allied coven caster."
    ],
    "desc": "The coven's venomous huntress, now called Auntie by Doorinia's terrified inhabitants. She breeds serpent troops, weaponizes petrification, and turns battlefields into poisonous kill-zones."
  },
  {
    "name": "Gahgah Yagha \u2014 Gaga, Tenebrous Troll",
    "faction": "Gaga",
    "role": "Shock commander / grapple breaker",
    "cr": 18,
    "ac": 16,
    "hp": 325,
    "abilities": {
      "str": 26,
      "dex": 14,
      "con": 28,
      "int": 14,
      "wis": 16,
      "cha": 20
    },
    "size": "huge",
    "type": "fiend",
    "subtype": "hag",
    "speed": {
      "walk": 40,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "abyssal",
      "common",
      "draconic",
      "giant",
      "infernal"
    ],
    "saves": [
      "str",
      "dex",
      "con",
      "int",
      "wis",
      "cha"
    ],
    "skills": {
      "ath": 1,
      "dec": 1,
      "prc": 1
    },
    "res": [
      "fire",
      "necrotic",
      "radiant"
    ],
    "imm": [
      "cold",
      "poison"
    ],
    "cond": [
      "charmed",
      "poisoned"
    ],
    "traits": [
      "Regeneration. Gaga regains 20 HP at the start of her turn. Acid damage suppresses this regeneration until the start of her following turn.",
      "Two Heads. Gaga has advantage on Perception checks and on saves against blinded, charmed, deafened, frightened, stunned, and unconscious.",
      "Spell Resistance. Gaga has advantage on saving throws against spells and magical effects.",
      "Break Their Line. When Gaga knocks a creature prone or moves it against its will, one allied Gaga minion within 30 ft. may move 10 ft. without provoking opportunity attacks."
    ],
    "actions": [
      {
        "name": "Bite",
        "kind": "attack",
        "text": "One of Gaga's heads tears into a target.",
        "tohit": 15,
        "damage": [
          [
            "2d12+8",
            "piercing"
          ],
          [
            "2d6",
            "poison"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Claw and Seize",
        "kind": "attack",
        "text": "On a hit the target is also grappled (escape DC 15) and restrained while grappled.",
        "tohit": 15,
        "damage": [
          [
            "2d10+8",
            "slashing"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Fling",
        "kind": "save",
        "text": "A creature grappled by Gaga is hurled up to 60 ft., takes 6d6 bludgeoning, falls prone, and may take additional collision damage.",
        "dc": 18,
        "ability": "str",
        "damage": [
          [
            "6d6",
            "bludgeoning"
          ]
        ],
        "onSave": "none"
      },
      {
        "name": "Enraging Howl",
        "kind": "save",
        "text": "Creatures within 30 ft. make Wisdom saves or must use their next available attack against the nearest creature, friend or foe.",
        "dc": 18,
        "ability": "wis"
      }
    ],
    "legendary": [
      "Multiattack (1). Gaga makes two claw or bite attacks.",
      "Enraging Howl (2). Use Enraging Howl.",
      "Stunning Slamalam (1). One creature hit by Gaga makes DC 18 Constitution save or is stunned until end of its next turn.",
      "Flying Headbutt (2). Hit a Large or smaller creature; DC 18 Strength save or prone and pushed 10 ft."
    ],
    "desc": "Gahgah Yagha, universally shortened to Gaga in Glass Home, is the coven's blunt instrument: a two-headed troll hag who believes every tactical problem can be solved by hitting it harder and sending more bodies through the breach."
  },
  {
    "name": "Grandma Darkling Knife",
    "faction": "Grandma",
    "role": "Scout / executioner",
    "cr": 1,
    "ac": 15,
    "hp": 27,
    "abilities": {
      "str": 10,
      "dex": 18,
      "con": 12,
      "int": 11,
      "wis": 12,
      "cha": 10
    },
    "size": "sm",
    "type": "fey",
    "subtype": "darkling",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 2,
      "prc": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Death Flash. When reduced to 0 HP, bright light erupts in 10 ft.; enemies make DC 12 Constitution save or are blinded until end of next turn.",
      "Veiled Advance. Gains advantage on its first attack each combat if it began its turn in dim light or darkness."
    ],
    "actions": [
      {
        "name": "Shadow Knife",
        "kind": "attack",
        "text": "A barbed black knife strike.",
        "tohit": 6,
        "damage": [
          [
            "1d6+4",
            "piercing"
          ],
          [
            "1d6",
            "necrotic"
          ]
        ],
        "reach": 5
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Grandma Darkling Knight",
    "faction": "Grandma",
    "role": "Line cavalry / flanker",
    "cr": 4,
    "ac": 18,
    "hp": 68,
    "abilities": {
      "str": 16,
      "dex": 16,
      "con": 16,
      "int": 11,
      "wis": 13,
      "cha": 12
    },
    "size": "med",
    "type": "fey",
    "subtype": "darkling",
    "speed": {
      "walk": 35,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 1,
      "prc": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Mounted Hunter. While within 5 ft. of a friendly mount or larger Grandma minion, AC increases by 1.",
      "Black Banner. Grandma allies within 10 ft. add +1 to attack rolls against frightened creatures."
    ],
    "actions": [
      {
        "name": "Gloom Lance",
        "kind": "attack",
        "text": "If the knight moved at least 20 ft. straight toward the target, add 2d6 piercing damage.",
        "tohit": 7,
        "damage": [
          [
            "1d10+4",
            "piercing"
          ],
          [
            "1d6",
            "necrotic"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Dread Pennant",
        "kind": "save",
        "text": "One enemy within 30 ft. makes Wisdom save or is frightened until end of its next turn.",
        "dc": 14,
        "ability": "wis"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Berbalang Secret-Eater",
    "faction": "Grandma",
    "role": "Flying artillery / anti-caster",
    "cr": 5,
    "ac": 16,
    "hp": 78,
    "abilities": {
      "str": 14,
      "dex": 16,
      "con": 14,
      "int": 18,
      "wis": 14,
      "cha": 15
    },
    "size": "med",
    "type": "aberration",
    "subtype": "berbalang",
    "speed": {
      "walk": 30,
      "fly": 40,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "deep speech",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "arc": 1,
      "prc": 1,
      "ste": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Thought Carrion. Advantage on attacks against a creature that cast a spell since the end of the berbalang's last turn.",
      "Secret Relay. While within 60 ft. of Grandma, it can communicate telepathically with every Grandma unit in that radius."
    ],
    "actions": [
      {
        "name": "Mind-Talon",
        "kind": "attack",
        "text": "A claw that tears memory as well as flesh.",
        "tohit": 7,
        "damage": [
          [
            "2d6+3",
            "slashing"
          ],
          [
            "2d6",
            "psychic"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Rake the Memory",
        "kind": "save",
        "text": "One creature within 60 ft. makes Intelligence save or takes psychic damage and cannot take reactions until start of its next turn.",
        "dc": 15,
        "ability": "int",
        "damage": [
          [
            "4d6",
            "psychic"
          ]
        ],
        "onSave": "half"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Rotbriar Hexer",
    "faction": "Grandma",
    "role": "Hex support / debuffer",
    "cr": 3,
    "ac": 14,
    "hp": 52,
    "abilities": {
      "str": 8,
      "dex": 14,
      "con": 14,
      "int": 16,
      "wis": 15,
      "cha": 16
    },
    "size": "med",
    "type": "fey",
    "subtype": "hag-servant",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Coven Relay. When a Grandma ally within 30 ft. imposes frightened, the Hexer can move its Hex Mark to that creature without an action.",
      "Briar Screen. Allies directly behind the Hexer gain half cover against ranged attacks."
    ],
    "actions": [
      {
        "name": "Withering Bolt",
        "kind": "attack",
        "text": "Ranged spell attack.",
        "tohit": 6,
        "damage": [
          [
            "3d8",
            "necrotic"
          ]
        ],
        "range": 90
      },
      {
        "name": "Hex Mark",
        "kind": "save",
        "text": "One creature within 60 ft. makes Charisma save or has disadvantage on its next saving throw before end of the Hexer's next turn.",
        "dc": 14,
        "ability": "cha"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Soul-Cage Porter",
    "faction": "Grandma",
    "role": "Tank / soul battery",
    "cr": 6,
    "ac": 19,
    "hp": 105,
    "abilities": {
      "str": 20,
      "dex": 10,
      "con": 20,
      "int": 9,
      "wis": 13,
      "cha": 8
    },
    "size": "lg",
    "type": "construct",
    "subtype": "soul-cage",
    "speed": {
      "walk": 25,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [
      "poison",
      "psychic"
    ],
    "cond": [
      "charmed",
      "frightened",
      "poisoned"
    ],
    "traits": [
      "Soul Battery. When a creature within 15 ft. drops to 0 HP, the Porter gains 10 temporary HP.",
      "Grim Conduit. Grandma can originate Soul Steal from a Soul-Cage Porter she can see within 120 ft."
    ],
    "actions": [
      {
        "name": "Cage Maul",
        "kind": "attack",
        "text": "Heavy iron cage-arm strike.",
        "tohit": 8,
        "damage": [
          [
            "2d10+5",
            "bludgeoning"
          ],
          [
            "1d8",
            "necrotic"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Siphon Spark",
        "kind": "save",
        "text": "One creature within 30 ft. makes Charisma save or takes necrotic damage; Porter gains half damage dealt as temporary HP.",
        "dc": 15,
        "ability": "cha",
        "damage": [
          [
            "4d8",
            "necrotic"
          ]
        ],
        "onSave": "half"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Thorn-Memory Stalker",
    "faction": "Grandma",
    "role": "Ambusher / zone denial",
    "cr": 4,
    "ac": 15,
    "hp": 66,
    "abilities": {
      "str": 16,
      "dex": 17,
      "con": 14,
      "int": 11,
      "wis": 15,
      "cha": 10
    },
    "size": "med",
    "type": "plant",
    "subtype": "fey-thorn",
    "speed": {
      "walk": 35,
      "fly": 0,
      "swim": 0,
      "climb": 35,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 2,
      "prc": 1
    },
    "res": [
      "necrotic"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Rooted Ambush. While motionless among plants it is indistinguishable from thorn growth.",
      "Memory Scent. Ignores disadvantage from frightened targets being hidden or invisible within 30 ft."
    ],
    "actions": [
      {
        "name": "Thorn Rake",
        "kind": "attack",
        "text": "Hooked branches drag a victim.",
        "tohit": 7,
        "damage": [
          [
            "2d8+4",
            "slashing"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Briar Snare",
        "kind": "save",
        "text": "One creature within 30 ft. makes Strength save or is restrained by spectral thorns until it uses an action to repeat the save.",
        "dc": 14,
        "ability": "str"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Yuan-ti Fangguard",
    "faction": "Auntie",
    "role": "Shield infantry / poison setup",
    "cr": 3,
    "ac": 18,
    "hp": 58,
    "abilities": {
      "str": 18,
      "dex": 14,
      "con": 16,
      "int": 11,
      "wis": 13,
      "cha": 12
    },
    "size": "med",
    "type": "monstrosity",
    "subtype": "yuan-ti",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "draconic",
      "yuan-ti"
    ],
    "saves": [],
    "skills": {},
    "res": [
      "poison"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Shield of Scales. Adjacent Auntie allies gain +1 AC against melee attacks.",
      "Venom Exploit. Deals +1d6 poison damage to poisoned targets."
    ],
    "actions": [
      {
        "name": "Serpent Spear",
        "kind": "attack",
        "text": "Disciplined spear thrust.",
        "tohit": 6,
        "damage": [
          [
            "1d8+4",
            "piercing"
          ],
          [
            "1d6",
            "poison"
          ]
        ],
        "reach": 10
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Coil Adept",
    "faction": "Auntie",
    "role": "Controller / grappler",
    "cr": 4,
    "ac": 16,
    "hp": 72,
    "abilities": {
      "str": 18,
      "dex": 16,
      "con": 16,
      "int": 12,
      "wis": 14,
      "cha": 14
    },
    "size": "med",
    "type": "monstrosity",
    "subtype": "yuan-ti",
    "speed": {
      "walk": 35,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "yuan-ti"
    ],
    "saves": [],
    "skills": {},
    "res": [
      "poison"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Constricting Formation. A creature grappled by a Coil Adept has disadvantage on saves against poison from other Auntie units.",
      "Slither Through. Can move through spaces of friendly Auntie units."
    ],
    "actions": [
      {
        "name": "Hooked Glaive",
        "kind": "attack",
        "text": "On hit target cannot take reactions until start of Adept's next turn.",
        "tohit": 7,
        "damage": [
          [
            "1d10+4",
            "slashing"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Constrict",
        "kind": "save",
        "text": "One creature within 5 ft. makes Strength save or is grappled and restrained (escape DC 14).",
        "dc": 14,
        "ability": "str",
        "damage": [
          [
            "2d6+4",
            "bludgeoning"
          ]
        ],
        "onSave": "none"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Spitebow Venom Archer",
    "faction": "Auntie",
    "role": "Ranged focus fire",
    "cr": 3,
    "ac": 15,
    "hp": 49,
    "abilities": {
      "str": 10,
      "dex": 18,
      "con": 14,
      "int": 12,
      "wis": 14,
      "cha": 12
    },
    "size": "med",
    "type": "monstrosity",
    "subtype": "yuan-ti",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 1,
      "prc": 1
    },
    "res": [
      "poison"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Marked Venom. Attacks against a target poisoned by an Auntie ally ignore half cover.",
      "Volley Discipline. If another Spitebow attacked the same target this round, add +2 to hit."
    ],
    "actions": [
      {
        "name": "Venom Arrow",
        "kind": "attack",
        "text": "Longbow attack with alchemical venom.",
        "tohit": 7,
        "damage": [
          [
            "1d8+4",
            "piercing"
          ],
          [
            "2d6",
            "poison"
          ]
        ],
        "range": 120
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Petrifying Eye Acolyte",
    "faction": "Auntie",
    "role": "Save pressure / petrify support",
    "cr": 5,
    "ac": 16,
    "hp": 76,
    "abilities": {
      "str": 12,
      "dex": 14,
      "con": 16,
      "int": 15,
      "wis": 16,
      "cha": 16
    },
    "size": "med",
    "type": "monstrosity",
    "subtype": "serpent seer",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "infernal",
      "yuan-ti"
    ],
    "saves": [],
    "skills": {},
    "res": [
      "poison"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Stone-Sight Choir. A creature restrained by petrification magic has disadvantage on its first save against Auntie poison each round.",
      "Snake Oracle. Cannot be surprised while conscious."
    ],
    "actions": [
      {
        "name": "Stone Glare",
        "kind": "save",
        "text": "One creature within 30 ft. makes Constitution save. On failure it is restrained until end of its next turn; if it fails again while already restrained, it is petrified until end of the acolyte's next turn.",
        "dc": 15,
        "ability": "con"
      },
      {
        "name": "Venom Ray",
        "kind": "attack",
        "text": "Ranged spell attack.",
        "tohit": 7,
        "damage": [
          [
            "4d8",
            "poison"
          ]
        ],
        "range": 60
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Basilisk Chainmaster",
    "faction": "Auntie",
    "role": "Monster handler / command support",
    "cr": 4,
    "ac": 17,
    "hp": 67,
    "abilities": {
      "str": 16,
      "dex": 14,
      "con": 16,
      "int": 13,
      "wis": 15,
      "cha": 14
    },
    "size": "med",
    "type": "humanoid",
    "subtype": "corrupted fey",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ani": 2,
      "prc": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Handler. Friendly basilisks and serpent warbeasts within 30 ft. gain +10 ft. speed.",
      "Chain the Stone. Advantage on attacks against restrained or petrified targets."
    ],
    "actions": [
      {
        "name": "Barbed Chain",
        "kind": "attack",
        "text": "On hit, Large or smaller target can be pulled 10 ft.",
        "tohit": 7,
        "damage": [
          [
            "2d6+4",
            "slashing"
          ]
        ],
        "reach": 15
      },
      {
        "name": "Drive the Beast",
        "kind": "utility",
        "text": "One allied beast or monstrosity within 60 ft. may move up to half its speed and make one attack as a reaction."
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Venomwell Alchemist",
    "faction": "Auntie",
    "role": "Artillery / area denial",
    "cr": 5,
    "ac": 15,
    "hp": 70,
    "abilities": {
      "str": 9,
      "dex": 14,
      "con": 16,
      "int": 17,
      "wis": 15,
      "cha": 13
    },
    "size": "med",
    "type": "fey",
    "subtype": "hag-apprentice",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan",
      "yuan-ti"
    ],
    "saves": [],
    "skills": {},
    "res": [
      "poison"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Toxic Logistics. Auntie units within 10 ft. gain resistance to acid as well as poison.",
      "Prepared Antivenom. Once per round, when an Auntie ally within 30 ft. fails a poison save, the Alchemist can allow it to reroll."
    ],
    "actions": [
      {
        "name": "Acid Flask",
        "kind": "attack",
        "text": "Ranged alchemical attack.",
        "tohit": 7,
        "damage": [
          [
            "3d8",
            "acid"
          ]
        ],
        "range": 60
      },
      {
        "name": "Venom Mortar",
        "kind": "save",
        "text": "20-ft-radius burst within 90 ft.; Constitution save or poison damage and poisoned until end of next turn.",
        "dc": 15,
        "ability": "con",
        "damage": [
          [
            "4d6",
            "poison"
          ]
        ],
        "onSave": "half"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Troll Linebreaker",
    "faction": "Gaga",
    "role": "Heavy infantry / breach",
    "cr": 5,
    "ac": 16,
    "hp": 94,
    "abilities": {
      "str": 20,
      "dex": 13,
      "con": 20,
      "int": 7,
      "wis": 10,
      "cha": 8
    },
    "size": "lg",
    "type": "giant",
    "subtype": "troll",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [
      "cold"
    ],
    "imm": [],
    "cond": [],
    "traits": [
      "Regeneration. Regains 10 HP at start of turn unless it took acid damage since previous turn.",
      "Breach Pair. If another Gaga unit is adjacent to the same target, Linebreaker deals +1d8 damage once per turn."
    ],
    "actions": [
      {
        "name": "Hooked Maul",
        "kind": "attack",
        "text": "Crushing maul strike.",
        "tohit": 8,
        "damage": [
          [
            "2d10+5",
            "bludgeoning"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Shoulder Break",
        "kind": "save",
        "text": "One Large or smaller creature within 5 ft. makes Strength save or is pushed 15 ft. and knocked prone.",
        "dc": 15,
        "ability": "str",
        "damage": [
          [
            "2d6+5",
            "bludgeoning"
          ]
        ],
        "onSave": "none"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Troll Flesh-Mender",
    "faction": "Gaga",
    "role": "Sustain support / healer",
    "cr": 4,
    "ac": 15,
    "hp": 82,
    "abilities": {
      "str": 18,
      "dex": 12,
      "con": 18,
      "int": 10,
      "wis": 15,
      "cha": 11
    },
    "size": "lg",
    "type": "giant",
    "subtype": "troll",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Regeneration. Regains 8 HP at start of turn unless it took acid damage since previous turn.",
      "Stitch the Host. Adjacent Gaga units regain +2 additional HP whenever they regenerate."
    ],
    "actions": [
      {
        "name": "Bone Saw",
        "kind": "attack",
        "text": "Jagged surgical cleaver.",
        "tohit": 7,
        "damage": [
          [
            "2d8+4",
            "slashing"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Filthy Stitching",
        "kind": "utility",
        "text": "One allied Gaga unit within 5 ft. regains 3d8+4 HP. A creature can benefit once per short rest."
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Darkling Snail Lancer",
    "faction": "Gaga",
    "role": "Mounted cavalry / anti-magic screen",
    "cr": 5,
    "ac": 18,
    "hp": 76,
    "abilities": {
      "str": 16,
      "dex": 16,
      "con": 16,
      "int": 11,
      "wis": 13,
      "cha": 12
    },
    "size": "med",
    "type": "fey",
    "subtype": "darkling",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Snail Screen. While within 10 ft. of a Flail Snail Warbeast, has advantage on saves against spells.",
      "Charge the Glitter. If it moves 20 ft. straight before hitting with its lance, target makes DC 14 Strength save or falls prone."
    ],
    "actions": [
      {
        "name": "Blackglass Lance",
        "kind": "attack",
        "text": "Mounted darkling lance.",
        "tohit": 7,
        "damage": [
          [
            "1d12+4",
            "piercing"
          ],
          [
            "1d6",
            "necrotic"
          ]
        ],
        "reach": 10
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Flail Snail Warbeast",
    "faction": "Gaga",
    "role": "Magic screen / siege mount",
    "cr": 6,
    "ac": 17,
    "hp": 110,
    "abilities": {
      "str": 17,
      "dex": 5,
      "con": 20,
      "int": 3,
      "wis": 10,
      "cha": 5
    },
    "size": "lg",
    "type": "elemental",
    "subtype": "flail snail",
    "speed": {
      "walk": 10,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [],
    "cond": [
      "prone"
    ],
    "traits": [
      "Antimagic Shell. The Warbeast has advantage on saves against spells; when it succeeds against a spell that targets only it, roll 1d6: on 6 the spell is reflected back at the caster using the original attack/save.",
      "Glittering Bastion. Friendly Gaga units within 10 ft. gain +2 on saves against spells."
    ],
    "actions": [
      {
        "name": "Flail Tentacles",
        "kind": "attack",
        "text": "Two heavy flails strike one target.",
        "tohit": 7,
        "damage": [
          [
            "3d8+4",
            "bludgeoning"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Scintillating Pulse",
        "kind": "save",
        "text": "Creatures of Gaga's choice within 15 ft. make Constitution save or are blinded until start of Warbeast's next turn.",
        "dc": 15,
        "ability": "con"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Spider-Rider Harrier",
    "faction": "Gaga",
    "role": "Skirmisher / pursuit",
    "cr": 3,
    "ac": 15,
    "hp": 52,
    "abilities": {
      "str": 12,
      "dex": 18,
      "con": 14,
      "int": 10,
      "wis": 13,
      "cha": 11
    },
    "size": "med",
    "type": "humanoid",
    "subtype": "goblin rider",
    "speed": {
      "walk": 35,
      "fly": 0,
      "swim": 0,
      "climb": 35,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "ste": 1,
      "prc": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Webline Mobility. Ignores difficult terrain from webs, vegetation, and rubble.",
      "Pack Harrier. Does not provoke opportunity attacks from a creature that is adjacent to another Gaga ally."
    ],
    "actions": [
      {
        "name": "Dung-Spear",
        "kind": "attack",
        "text": "A foul spear; target hit must also make DC 12 Constitution save or be poisoned until end of its next turn.",
        "tohit": 7,
        "damage": [
          [
            "1d6+4",
            "piercing"
          ]
        ],
        "range": 30
      },
      {
        "name": "Web Bola",
        "kind": "save",
        "text": "One Large or smaller creature within 30 ft. makes Dexterity save or is restrained until it uses an action to escape DC 13.",
        "dc": 13,
        "ability": "dex"
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Rage-Drum Goblin",
    "faction": "Gaga",
    "role": "Morale / command support",
    "cr": 2,
    "ac": 14,
    "hp": 38,
    "abilities": {
      "str": 10,
      "dex": 16,
      "con": 14,
      "int": 11,
      "wis": 12,
      "cha": 14
    },
    "size": "sm",
    "type": "humanoid",
    "subtype": "goblin",
    "speed": {
      "walk": 30,
      "fly": 0,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {
      "prf": 2,
      "ste": 1
    },
    "res": [],
    "imm": [],
    "cond": [],
    "traits": [
      "Marching Rhythm. Gaga allies that start within 20 ft. gain +5 ft. speed until start of their next turn.",
      "Drum of Bad Decisions. A frightened Gaga ally within 20 ft. ignores the frightened condition until it leaves the aura."
    ],
    "actions": [
      {
        "name": "Bone Mallet",
        "kind": "attack",
        "text": "Drum mallet to the face.",
        "tohit": 5,
        "damage": [
          [
            "1d6+3",
            "bludgeoning"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Warbeat",
        "kind": "utility",
        "text": "One allied Gaga minion within 30 ft. can use its reaction to move up to half speed without provoking opportunity attacks."
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Grandma's Flying Cauldron",
    "faction": "Grandma",
    "role": "Mobile artillery / transport",
    "cr": 9,
    "ac": 18,
    "hp": 200,
    "abilities": {
      "str": 20,
      "dex": 14,
      "con": 20,
      "int": 1,
      "wis": 10,
      "cha": 1
    },
    "size": "huge",
    "type": "construct",
    "subtype": "flying cauldron",
    "speed": {
      "walk": 30,
      "fly": 60,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [
      "poison",
      "psychic"
    ],
    "cond": [
      "charmed",
      "frightened",
      "paralyzed",
      "poisoned",
      "stunned"
    ],
    "traits": [
      "Immutable Form. Immune to effects that alter its form.",
      "Magic Resistance. Advantage on saves against spells and magical effects.",
      "Flyby. Does not provoke opportunity attacks when flying out of reach."
    ],
    "actions": [
      {
        "name": "Slam",
        "kind": "attack",
        "text": "The cauldron rams a target.",
        "tohit": 8,
        "damage": [
          [
            "4d8+2",
            "bludgeoning"
          ]
        ],
        "reach": 5
      },
      {
        "name": "Spit Acid",
        "kind": "attack",
        "text": "Boiling acid is hurled from the rim.",
        "tohit": 6,
        "damage": [
          [
            "5d8",
            "acid"
          ]
        ],
        "range": 60
      }
    ],
    "legendary": [],
    "desc": ""
  },
  {
    "name": "Grandma's Walking Hut",
    "faction": "Grandma",
    "role": "Siege engine / command bastion",
    "cr": 16,
    "ac": 20,
    "hp": 300,
    "abilities": {
      "str": 20,
      "dex": 10,
      "con": 20,
      "int": 1,
      "wis": 3,
      "cha": 1
    },
    "size": "grg",
    "type": "construct",
    "subtype": "walking hut",
    "speed": {
      "walk": 60,
      "fly": 90,
      "swim": 0,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [
      "poison",
      "psychic"
    ],
    "cond": [
      "charmed",
      "frightened",
      "paralyzed",
      "poisoned"
    ],
    "traits": [
      "False Appearance. While motionless, indistinguishable from a normal hut.",
      "Siege Monster. Deals double damage to objects and structures.",
      "Magic Resistance. Advantage on saves against spells and magical effects."
    ],
    "actions": [
      {
        "name": "Slam",
        "kind": "attack",
        "text": "A house-sized limb crushes a target.",
        "tohit": 14,
        "damage": [
          [
            "4d8+9",
            "bludgeoning"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Teleport (1/Day)",
        "kind": "utility",
        "text": "Teleports itself and creatures aboard it up to 10 miles to a place it has visited or can clearly visualize."
      }
    ],
    "legendary": [
      "Slam Attack (1). Make one Slam attack.",
      "Chicken Run (1). Move up to speed without provoking opportunity attacks."
    ],
    "desc": ""
  },
  {
    "name": "Valdershmort \u2014 Auntie's Greater Basilisk",
    "faction": "Auntie",
    "role": "Petrification monster / mount",
    "cr": 14,
    "ac": 18,
    "hp": 325,
    "abilities": {
      "str": 20,
      "dex": 10,
      "con": 20,
      "int": 1,
      "wis": 10,
      "cha": 1
    },
    "size": "huge",
    "type": "monstrosity",
    "subtype": "greater basilisk",
    "speed": {
      "walk": 50,
      "fly": 0,
      "swim": 50,
      "climb": 0,
      "burrow": 0
    },
    "languages": [
      "common",
      "sylvan"
    ],
    "saves": [],
    "skills": {},
    "res": [],
    "imm": [
      "poison",
      "psychic"
    ],
    "cond": [
      "petrified",
      "poisoned"
    ],
    "traits": [
      "Keen Smell. Advantage on Perception checks relying on smell.",
      "Petrifying Gaze. A creature starting within 30 ft. that can see Valdershmort makes DC 18 Constitution save; failure restrains, then a second failure at end of next turn petrifies until greater restoration or similar magic."
    ],
    "actions": [
      {
        "name": "Bite",
        "kind": "attack",
        "text": "A huge venomous bite.",
        "tohit": 14,
        "damage": [
          [
            "3d8+8",
            "piercing"
          ],
          [
            "12d6",
            "poison"
          ]
        ],
        "reach": 10
      },
      {
        "name": "Poison Breath",
        "kind": "save",
        "text": "60-ft cone; Constitution save for half.",
        "dc": 20,
        "ability": "con",
        "damage": [
          [
            "22d6",
            "poison"
          ]
        ],
        "onSave": "half"
      }
    ],
    "legendary": [
      "Move (1). Move up to half speed.",
      "Bite (2). Make one Bite attack.",
      "Petrifying Gaze (3). Force one creature to resolve Petrifying Gaze."
    ],
    "desc": ""
  }
];
