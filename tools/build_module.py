#!/usr/bin/env python3
"""
Build script for "Doorinia: The Yagha Coven War Host" (dorinia-hag-host).

Pacts & Polyhedrals module pipeline:
  source/creatures.json  ->  build/src/<pack>/*.json  ->  module/packs/<pack> (LevelDB)
                          ->  dist/dorinia-hag-host.zip + dist/module.json

Targets Foundry VTT v14 and dnd5e 5.3.3. No Midi-QOL / DAE dependency.

Usage:  python3 tools/build_module.py
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
MODULE = ROOT / "module"
BUILD = ROOT / "build" / "src"
DIST = ROOT / "dist"
TOOLS = ROOT / "tools"

# ---------------------------------------------------------------- release config
MODULE_ID = "dorinia-hag-host"
VERSION = "1.1.0"
GH_OWNER = "pacts-and-polyhedrals"
GH_REPO = MODULE_ID
GH = f"https://github.com/{GH_OWNER}/{GH_REPO}"
ZIP_NAME = f"{MODULE_ID}.zip"
SOURCE_LABEL = "Doorinia Hag Host"

ACTOR_PACK = "hag-host-actors"
JOURNAL_PACK = "hag-host-journal"

FACTIONS = {
    "Grandma": {"folder": "Grandma — Babha Yagha", "color": "#4b2a5c", "sort": 100000},
    "Auntie": {"folder": "Auntie — Mama Yagha", "color": "#2f5a2a", "sort": 200000},
    "Gaga": {"folder": "Gaga — Gahgah Yagha", "color": "#6b3a1e", "sort": 300000},
}

# Legendary actions that re-use an existing action of the same creature.
LEGENDARY_REFS = {
    ("Mama Yagha", "Venomous Bite"): ["Venomous Bite"],
    ("Gahgah Yagha", "Multiattack"): ["Claw and Seize", "Bite"],
    ("Gahgah Yagha", "Enraging Howl"): ["Enraging Howl"],
    ("Grandma's Walking Hut", "Slam Attack"): ["Slam"],
    ("Valdershmort", "Bite"): ["Bite"],
}
# Legendary actions that resolve a trait's save.
LEGENDARY_TRAIT_REFS = {
    ("Valdershmort", "Petrifying Gaze"): "Petrifying Gaze",
}

LANGUAGE_KEYS = {
    "abyssal": "abyssal", "common": "common", "draconic": "draconic", "sylvan": "sylvan",
    "giant": "giant", "infernal": "infernal", "deep speech": "deep", "goblin": "goblin",
    "undercommon": "undercommon", "celestial": "celestial", "elvish": "elvish",
}
ABILITY_WORDS = {
    "strength": "str", "dexterity": "dex", "constitution": "con",
    "intelligence": "int", "wisdom": "wis", "charisma": "cha",
}
CONDITIONS = ["frightened", "poisoned", "restrained", "prone", "stunned", "blinded",
              "petrified", "grappled", "charmed", "paralyzed"]
TOKEN_SIZE = {"tiny": 0.5, "sm": 1, "med": 1, "lg": 2, "huge": 3, "grg": 4}
CR_XP = {0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200, 2: 450, 3: 700, 4: 1100, 5: 1800,
         6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900, 11: 7200, 12: 8400, 13: 10000,
         14: 11500, 15: 13000, 16: 15000, 17: 18000, 18: 20000, 19: 22000, 20: 25000,
         21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000}

STATS = {"systemId": "dnd5e", "systemVersion": "5.3.3", "coreVersion": "14",
         "createdTime": 1760180000000, "modifiedTime": 1760180000000, "lastModifiedBy": None}


# ---------------------------------------------------------------- helpers
def did(*parts: str) -> str:
    """Deterministic 16-char Foundry ID so UUIDs stay stable between builds."""
    h = hashlib.sha1(("|".join(parts)).encode()).hexdigest()
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = int(h, 16)
    out = ""
    while len(out) < 16:
        n, r = divmod(n, 62)
        out += alphabet[r]
    return out


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=False)


def short(name: str) -> str:
    return name.split(" — ")[0]


def split_trait(text: str):
    name, _, body = text.partition(". ")
    return name.strip(), body.strip() or text


def parse_cost(name: str):
    m = re.search(r"\((\d)\)\s*$", name)
    return (re.sub(r"\s*\(\d\)\s*$", "", name), int(m.group(1))) if m else (name, 1)


def parse_per_day(name: str):
    m = re.search(r"\((\d+)/Day\)", name, re.I)
    return int(m.group(1)) if m else None


def parse_save(text: str):
    m = re.search(r"DC (\d+) (Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma) sav", text)
    return (int(m.group(1)), ABILITY_WORDS[m.group(2).lower()]) if m else None


def parse_damage(text: str):
    return [(f.replace(" ", ""), t.lower()) for f, t in
            re.findall(r"(\d+d\d+(?:\s*[+-]\s*\d+)?)\s+(acid|bludgeoning|cold|fire|force|lightning|necrotic|piercing|poison|psychic|radiant|slashing|thunder)\b", text, re.I)]


CONDITION_VERBS = {"restrains": "restrained", "petrifies": "petrified", "frightens": "frightened",
                   "poisons": "poisoned", "stuns": "stunned", "blinds": "blinded", "grapples": "grappled"}


def parse_conditions(text: str):
    low = text.lower()
    found = []
    for c in CONDITIONS:
        # "a creature grappled by X" is a precondition, not an outcome
        hits = [m for m in re.finditer(rf"\b{c}\b", low) if not low[m.end():m.end() + 3] == " by"]
        if hits:
            found.append(c)
    for verb, c in CONDITION_VERBS.items():
        if re.search(rf"\b{verb}\b", low) and c not in found:
            found.append(c)
    return found


def condition_rounds(text: str):
    low = text.lower()
    if "1 minute" in low:
        return 10
    if "next turn" in low or "end of turn" in low:
        return 1
    return None


def damage_part(formula: str, dtype: str):
    m = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", formula.replace(" ", ""), re.I)
    base = {"types": [dtype], "custom": {"enabled": False, "formula": ""},
            "scaling": {"mode": "", "number": None, "formula": ""}}
    if m:
        base.update(number=int(m.group(1)), denomination=int(m.group(2)), bonus=(m.group(3) or "").lstrip("+"))
    else:
        base.update(number=None, denomination=None, bonus="", custom={"enabled": True, "formula": formula})
    return base


def activity_base(aid, atype, name, *, activation="action", cost=None, rng=None, units="ft",
                  target_count="1", target_type="creature", template=None, uses=None, legendary=False):
    targets = []
    if uses:
        targets.append({"type": "itemUses", "target": "", "value": "1", "scaling": {"mode": "", "formula": ""}})
    tpl = {"count": "", "contiguous": False, "type": "", "size": "", "width": "", "height": "", "units": "ft"}
    if template:
        tpl.update(template)
        target_count, target_type = "", "creature"
    return {
        "_id": aid, "type": atype, "name": name, "img": None, "sort": 0,
        "activation": {"type": activation, "value": cost if activation == "legendary" else (1 if activation in ("action", "bonus", "reaction") else None),
                       "condition": "", "override": False},
        "consumption": {"scaling": {"allowed": False, "max": ""}, "spellSlot": False, "targets": targets},
        "description": {"chatFlavor": ""},
        "duration": {"concentration": False, "override": False, "value": "", "units": "inst", "special": ""},
        "effects": [], "flags": {},
        "range": {"override": False, "value": "" if rng is None else str(rng), "units": units if rng is not None else "self", "special": ""},
        "target": {"override": False, "prompt": True, "template": tpl,
                   "affects": {"count": target_count, "type": target_type, "choice": False, "special": ""}},
        "uses": {"spent": 0, "max": "", "recovery": []},
        "visibility": {"identifier": "", "level": {"min": None, "max": None},
                       "requireAttunement": False, "requireIdentification": False, "requireMagic": False},
    }


def template_from_text(text: str):
    m = re.search(r"(\d+)[- ](?:foot|ft)[- ]radius", text, re.I)
    if m:
        return {"type": "sphere", "size": m.group(1)}
    m = re.search(r"(\d+)[- ](?:foot|ft)[- ]cone", text, re.I)
    if m:
        return {"type": "cone", "size": m.group(1)}
    return None


def range_from_text(text: str, default=None):
    m = re.search(r"within (\d+) (?:ft|feet)", text)
    return int(m.group(1)) if m else default


# ---------------------------------------------------------------- effects
def status_effect(item_key: str, cond: str, rounds):
    eid = did(item_key, "effect", cond)
    return {
        "_id": eid, "name": cond.capitalize(),
        "img": f"systems/dnd5e/icons/svg/statuses/{cond}.svg",
        "statuses": [cond], "changes": [], "disabled": False, "transfer": False,
        "duration": {"rounds": rounds, "turns": None, "seconds": None, "startTime": None,
                     "startRound": None, "startTurn": None, "combat": None},
        "description": "", "origin": None, "tint": "#ffffff", "type": "base", "system": {},
        "sort": 0, "flags": {MODULE_ID: {"generated": True}}, "_stats": dict(STATS),
    }


# ---------------------------------------------------------------- items
def make_item(actor_key, name, img, desc_html, *, activities=None, effects=None, uses=None,
              activation_type="", sort=0, item_kind="monster", identifier=None, id_tag=""):
    iid = did(actor_key, "item", id_tag, name)
    return iid, {
        "_id": iid, "name": name, "type": "feat", "img": img, "sort": sort,
        "system": {
            "description": {"value": desc_html, "chat": ""},
            "identifier": identifier or re.sub(r"[^a-z0-9]+", "-", re.sub(r"\s*\(.*?\)", "", name).lower()).strip("-"),
            "source": {"custom": SOURCE_LABEL, "book": "", "page": "", "license": "", "rules": "2014"},
            "activities": activities or {},
            "uses": uses or {"spent": 0, "max": "", "recovery": []},
            "type": {"value": item_kind, "subtype": ""},
            "requirements": "", "properties": [], "enchant": {}, "prerequisites": {"level": None, "repeatable": False},
            "advancement": [], "crewed": False,
        },
        "effects": effects or [],
        "flags": {MODULE_ID: {"generated": True}},
        "folder": None, "ownership": {"default": 0}, "_stats": dict(STATS),
    }


def save_activity(item_key, name, text, dc, ability, damage, on_save, effects, *, activation, cost=None,
                  legendary=False, uses=None, rng_default=60):
    aid = did(item_key, "act", "save", name)
    tpl = template_from_text(text)
    rng = range_from_text(text, rng_default) if not tpl or "within" in text else None
    a = activity_base(aid, "save", name, activation=activation, cost=cost, rng=rng, template=tpl,
                      legendary=legendary, uses=uses)
    if tpl and rng is None:
        a["range"] = {"override": False, "value": "", "units": "self", "special": ""}
    a["save"] = {"ability": [ability], "dc": {"calculation": "", "formula": str(dc)}}
    a["damage"] = {"onSave": on_save, "parts": [damage_part(f, t) for f, t in damage]}
    a["effects"] = [{"_id": e["_id"], "onSave": False} for e in effects]
    return aid, a


def attack_activity(item_key, act, *, activation="action", cost=None, legendary=False, label=None):
    aid = did(item_key, "act", "attack", label or act["name"])
    ranged = "range" in act
    rng = act.get("range") or act.get("reach") or 5
    a = activity_base(aid, "attack", label or act["name"], activation=activation, cost=cost, rng=rng,
                      legendary=legendary)
    a["attack"] = {"ability": "none", "bonus": str(act["tohit"]), "critical": {"threshold": None}, "flat": True,
                   "type": {"value": "ranged" if ranged else "melee", "classification": "weapon"}}
    a["damage"] = {"critical": {"bonus": ""}, "includeBase": False,
                   "parts": [damage_part(f, t) for f, t in act["damage"]]}
    return aid, a


def roll_line_attack(act):
    ranged = "range" in act
    reach = f"range {act['range']} ft." if ranged else f"reach {act.get('reach', 5)} ft."
    dmg = " plus ".join(f"[[/damage {f} {t}]]" for f, t in act["damage"])
    return (f"<p><em>{'Ranged' if ranged else 'Melee'} Attack:</em> [[/attack +{act['tohit']}]], {reach} "
            f"<em>Hit:</em> {dmg}.</p>")


def roll_line_save(dc, ability, damage, on_save):
    s = f"<p><em>Saving Throw:</em> [[/save ability={ability} dc={dc}]]"
    if damage:
        s += ". <em>Failure:</em> " + " plus ".join(f"[[/damage {f} {t}]]" for f, t in damage)
        s += {"half": ". <em>Success:</em> half damage", "none": ". <em>Success:</em> no damage"}.get(on_save, "")
    return s + ".</p>"


def build_action(actor_key, short_name, act, sort):
    item_key = f"{actor_key}|{act['name']}"
    per_day = parse_per_day(act["name"])
    uses = {"spent": 0, "max": str(per_day), "recovery": [{"period": "day", "type": "recoverAll", "formula": ""}]} if per_day else None
    activities, effects = {}, []
    body = f"<p>{esc(act['text'])}</p>"
    text = act["text"]

    if act["kind"] == "attack":
        aid, a = attack_activity(item_key, act)
        conds = [c for c in parse_conditions(text) if c in ("grappled", "restrained", "prone", "poisoned")]
        rider = parse_save(text)
        if conds and not rider:
            for c in conds:
                effects.append(status_effect(item_key, c, condition_rounds(text)))
            a["effects"] = [{"_id": e["_id"]} for e in effects]
        activities[aid] = a
        body = roll_line_attack(act) + body
        if rider:
            dc, ab = rider
            r_eff = [status_effect(item_key, c, condition_rounds(text)) for c in conds]
            effects += r_eff
            sid, s = save_activity(item_key, f"{act['name']} — Rider Save", text, dc, ab, [], "none", r_eff,
                                   activation="special", rng_default=act.get("range") or act.get("reach") or 5)
            activities[sid] = s
    elif act["kind"] == "save":
        dmg = [tuple(d) for d in act.get("damage", [])]
        on_save = act.get("onSave", "half" if dmg else "none")
        conds = parse_conditions(text)
        effects = [status_effect(item_key, c, condition_rounds(text)) for c in conds]
        aid, a = save_activity(item_key, act["name"], text, act["dc"], act["ability"], dmg, on_save, effects,
                               activation="action", uses=bool(uses))
        activities[aid] = a
        body = roll_line_save(act["dc"], act["ability"], dmg, on_save) + body
    else:
        heal = re.search(r"regains (\d+d\d+(?:\s*\+\s*\d+)?) HP", text)
        if heal:
            aid = did(item_key, "act", "heal")
            a = activity_base(aid, "heal", act["name"], rng=range_from_text(text, 5), target_type="ally", uses=bool(uses))
            a["healing"] = damage_part(heal.group(1), "healing")
            body = f"<p><em>Healing:</em> [[/heal {heal.group(1).replace(' ', '')}]]</p>" + body
        else:
            aid = did(item_key, "act", "utility")
            a = activity_base(aid, "utility", act["name"], rng=range_from_text(text), target_type="", target_count="",
                              uses=bool(uses))
            a["roll"] = {"formula": "", "name": "", "prompt": False, "visible": False}
            summon = re.search(r"Summon (\d+d\d+(?:\+\d+)?)", text)
            if summon:
                a["roll"] = {"formula": summon.group(1), "name": "Number summoned", "prompt": False, "visible": True}
        activities[aid] = a
    return make_item(actor_key, act["name"], "icons/svg/sword.svg" if act["kind"] == "attack" else
                     ("icons/svg/explosion.svg" if act["kind"] == "save" else "icons/svg/upgrade.svg"),
                     body, activities=activities, effects=effects, uses=uses, sort=sort)


def build_trait(actor_key, short_name, trait_text, sort, *, legres=False):
    name, body = split_trait(trait_text)
    item_key = f"{actor_key}|{name}"
    activities, effects = {}, []
    desc = f"<p>{esc(body)}</p>"
    sv = parse_save(body)
    if legres:
        aid = did(item_key, "act", "legres")
        a = activity_base(aid, "utility", "Use Legendary Resistance", activation="special", target_type="self",
                          target_count="")
        a["activation"]["condition"] = "fails a saving throw"
        a["consumption"]["targets"] = [{"type": "attribute", "target": "resources.legres.value", "value": "1",
                                        "scaling": {"mode": "", "formula": ""}}]
        a["roll"] = {"formula": "", "name": "", "prompt": False, "visible": False}
        activities[aid] = a
    elif sv:
        dc, ab = sv
        dmg = parse_damage(body)
        on_save = "half" if ("half" in body.lower()) else "none"
        conds = parse_conditions(body)
        effects = [status_effect(item_key, c, condition_rounds(body)) for c in conds]
        aid, a = save_activity(item_key, name, body, dc, ab, dmg, on_save, effects, activation="special",
                               rng_default=range_from_text(body, 5))
        activities[aid] = a
        desc = roll_line_save(dc, ab, dmg, on_save) + desc
    regen = re.search(r"regains (\d+) (?:hit points|HP)", body, re.I)
    if regen:
        aid = did(item_key, "act", "regen")
        a = activity_base(aid, "heal", "Regenerate", activation="turnStart", target_type="self", target_count="")
        a["activation"]["value"] = None
        a["healing"] = damage_part(regen.group(1), "healing")
        a["healing"]["custom"] = {"enabled": True, "formula": regen.group(1)}
        activities[aid] = a
    return make_item(actor_key, name, "icons/svg/aura.svg", desc, activities=activities, effects=effects, sort=sort,
                     identifier="legendary-resistance" if legres else None)


def build_legendary(actor_key, actor_name, leg_text, sort, actions_by_name, traits_by_name):
    raw_name, body = split_trait(leg_text)
    name, cost = parse_cost(raw_name)
    item_key = f"{actor_key}|legendary|{name}"
    activities, effects = {}, []
    desc_prefix = ""
    refs = next((v for (who, ln), v in LEGENDARY_REFS.items() if actor_name.startswith(who) and ln == name), None)
    trait_ref = next((v for (who, ln), v in LEGENDARY_TRAIT_REFS.items() if actor_name.startswith(who) and ln == name), None)
    if refs:
        multi = len(refs) > 1
        if multi:
            aid = did(item_key, "act", "utility")
            a = activity_base(aid, "utility", name, activation="legendary", cost=cost, target_type="", target_count="")
            a["roll"] = {"formula": "", "name": "", "prompt": False, "visible": False}
            activities[aid] = a
        for ref in refs:
            act = actions_by_name[ref]
            if act["kind"] == "attack":
                aid, a = attack_activity(item_key, act, activation="special" if multi else "legendary",
                                         cost=None if multi else cost, label=ref)
                activities[aid] = a
                desc_prefix += roll_line_attack(act)
            else:
                dmg = [tuple(d) for d in act.get("damage", [])]
                on_save = act.get("onSave", "half" if dmg else "none")
                eff = [status_effect(item_key, c, condition_rounds(act["text"])) for c in parse_conditions(act["text"])]
                effects += eff
                aid, a = save_activity(item_key, ref, act["text"], act["dc"], act["ability"], dmg, on_save, eff,
                                       activation="legendary", cost=cost, legendary=True)
                activities[aid] = a
                desc_prefix += roll_line_save(act["dc"], act["ability"], dmg, on_save)
    elif trait_ref:
        tname, tbody = split_trait(traits_by_name[trait_ref])
        dc, ab = parse_save(tbody)
        eff = [status_effect(item_key, c, condition_rounds(tbody)) for c in parse_conditions(tbody)]
        effects += eff
        aid, a = save_activity(item_key, name, tbody, dc, ab, [], "none", eff, activation="legendary", cost=cost,
                               legendary=True, rng_default=30)
        activities[aid] = a
        desc_prefix += roll_line_save(dc, ab, [], "none")
    else:
        sv = parse_save(body)
        if sv:
            dc, ab = sv
            dmg = parse_damage(body)
            on_save = "half" if "half" in body.lower() else "none"
            eff = [status_effect(item_key, c, condition_rounds(body)) for c in parse_conditions(body)]
            effects += eff
            aid, a = save_activity(item_key, name, body, dc, ab, dmg, on_save, eff, activation="legendary",
                                   cost=cost, legendary=True)
            activities[aid] = a
            desc_prefix += roll_line_save(dc, ab, dmg, on_save)
        else:
            aid = did(item_key, "act", "utility")
            a = activity_base(aid, "utility", name, activation="legendary", cost=cost, legendary=True,
                              rng=range_from_text(body), target_type="", target_count="")
            a["roll"] = {"formula": "", "name": "", "prompt": False, "visible": False}
            summon = re.search(r"Summon (\d+d\d+(?:\+\d+)?)", body)
            if summon:
                a["roll"] = {"formula": summon.group(1), "name": "Number summoned", "prompt": False, "visible": True}
            roll = re.search(r"\bRoll (d\d+)", body)
            if roll:
                a["roll"] = {"formula": "1" + roll.group(1), "name": "Recharge roll", "prompt": False, "visible": True}
            activities[aid] = a
    label = name if cost == 1 else f"{name} (Costs {cost} Actions)"
    desc = desc_prefix + f"<p>{esc(body)}</p>"
    iid, item = make_item(actor_key, label, "icons/svg/lightning.svg", desc, activities=activities,
                          effects=effects, sort=sort, id_tag="legendary")
    return iid, item, cost


# ---------------------------------------------------------------- actors
def build_actor(m, folder_id, sort):
    actor_key = m["name"]
    aid = did("actor", actor_key)
    sname = short(m["name"])
    actions_by_name = {a["name"]: a for a in m["actions"]}
    traits_by_name = {split_trait(t)[0]: t for t in m["traits"]}

    items = []
    s = 100000
    legres_uses = 0
    for t in m["traits"]:
        tname = split_trait(t)[0]
        is_lr = tname.lower().startswith("legendary resistance")
        if is_lr:
            legres_uses = parse_per_day(tname) or 3
        items.append(build_trait(actor_key, sname, t, s, legres=is_lr)[1]); s += 1000
    for a in m["actions"]:
        items.append(build_action(actor_key, sname, a, s)[1]); s += 1000
    leg_max = 0
    if m["legendary"]:
        leg_max = 3
        for lt in m["legendary"]:
            _, it, _cost = build_legendary(actor_key, m["name"], lt, s, actions_by_name, traits_by_name)
            items.append(it); s += 1000

    # embedded keys for the CLI
    for it in items:
        it["_key"] = f"!actors.items!{aid}.{it['_id']}"
        for e in it["effects"]:
            e["_key"] = f"!actors.items.effects!{aid}.{it['_id']}.{e['_id']}"

    langs, custom_langs = [], []
    for lg in m["languages"]:
        k = LANGUAGE_KEYS.get(lg.lower())
        (langs.append(k) if k else custom_langs.append(lg.title() if lg.islower() else lg))

    abilities = {k: {"value": m["abilities"][k], "proficient": 1 if k in m["saves"] else 0,
                     "bonuses": {"check": "", "save": ""}, "check": {"roll": {"min": None, "max": None, "mode": 0}},
                     "save": {"roll": {"min": None, "max": None, "mode": 0}}} for k in ["str", "dex", "con", "int", "wis", "cha"]}
    skills = {k: {"value": v, "ability": "", "bonuses": {"check": "", "passive": ""},
                  "roll": {"min": None, "max": None, "mode": 0}} for k, v in (m.get("skills") or {}).items()}
    spd = m["speed"]
    size = m["size"]
    tsize = TOKEN_SIZE.get(size, 1)
    bio = (f"<p><strong>Army role:</strong> {esc(m['role'])}</p>"
           f"<p><strong>Host:</strong> {esc(FACTIONS[m['faction']]['folder'])}</p>"
           + (f"<p>{esc(m['desc'])}</p>" if m.get("desc") else ""))

    actor = {
        "_id": aid, "_key": f"!actors!{aid}", "name": m["name"], "type": "npc",
        "img": "icons/svg/mystery-man.svg", "folder": folder_id, "sort": sort,
        "system": {
            "abilities": abilities,
            "skills": skills,
            "attributes": {
                "ac": {"calc": "flat", "flat": m["ac"], "formula": ""},
                "hp": {"value": m["hp"], "max": m["hp"], "temp": None, "tempmax": None, "formula": ""},
                "movement": {"walk": spd.get("walk") or None, "fly": spd.get("fly") or None,
                             "swim": spd.get("swim") or None, "climb": spd.get("climb") or None,
                             "burrow": spd.get("burrow") or None, "units": "ft",
                             "hover": bool(spd.get("fly")) and "construct" == m["type"]},
                "spellcasting": "cha",
            },
            "details": {
                "cr": m["cr"], "alignment": "Chaotic Evil" if m["type"] != "construct" else "Unaligned",
                "type": {"value": m["type"], "subtype": m.get("subtype", "").title(), "swarm": "", "custom": ""},
                "biography": {"value": bio, "public": ""},
                "habitat": {"value": [], "custom": "Doorinia"}, "treasure": {"value": []},
            },
            "resources": {
                "legact": {"max": leg_max, "spent": 0},
                "legres": {"max": legres_uses, "spent": 0},
                "lair": {"value": False, "initiative": None, "inside": False},
            },
            "source": {"custom": SOURCE_LABEL, "book": "", "page": "", "license": "", "rules": "2014"},
            "traits": {
                "size": size,
                "languages": {"value": langs, "custom": "; ".join(custom_langs), "communication": {}},
                "dr": {"value": m.get("res", []), "custom": "", "bypasses": []},
                "di": {"value": m.get("imm", []), "custom": "", "bypasses": []},
                "dv": {"value": [], "custom": "", "bypasses": []},
                "ci": {"value": m.get("cond", []), "custom": ""},
            },
        },
        "prototypeToken": {
            "name": sname, "displayName": 20, "disposition": -1, "actorLink": False,
            "width": tsize, "height": tsize,
            "texture": {"src": "icons/svg/mystery-man.svg", "scaleX": 1, "scaleY": 1},
            "bar1": {"attribute": "attributes.hp"}, "bar2": {"attribute": None}, "displayBars": 20,
            "sight": {"enabled": False},
        },
        "items": items, "effects": [],
        "flags": {MODULE_ID: {"generated": True, "sourceKey": m["name"], "faction": m["faction"], "role": m["role"]}},
        "ownership": {"default": 0}, "_stats": dict(STATS),
    }
    return actor


# ---------------------------------------------------------------- journal
def actor_uuid(name):
    return f"Compendium.{MODULE_ID}.{ACTOR_PACK}.Actor.{did('actor', name)}"


def faction_table(creatures, faction):
    rows = []
    for m in sorted([c for c in creatures if c["faction"] == faction], key=lambda c: -c["cr"]):
        rows.append(f"<tr><td>@UUID[{actor_uuid(m['name'])}]{{{esc(m['name'])}}}</td><td>{m['cr']}</td>"
                    f"<td>{CR_XP.get(m['cr'], 0):,}</td><td>{m['ac']}</td><td>{m['hp']}</td><td>{esc(m['role'])}</td></tr>")
    return ("<table><thead><tr><th>Unit</th><th>CR</th><th>XP</th><th>AC</th><th>HP</th><th>Role</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table>")


def build_journal(creatures):
    jid = did("journal", "gm-guide")
    pages_src = [
        ("Overview", """
<h1>Doorinia: The Yagha Coven War Host</h1>
<p>The three High Hags began as the terror of Highforest. They now rule conquered regions of Doorinia by draining Archfey power and reorganising their old followers into standing armies.</p>
<ul>
<li><strong>Grandma — Babha Yagha</strong>: fear, darkness, soul attrition, layered control.</li>
<li><strong>Auntie — Mama Yagha</strong>: poison stacking and petrification.</li>
<li><strong>Gaga — Gahgah Yagha</strong>: shock assault, forced movement, regeneration.</li>
</ul>
<p>Every army unit is a homebrew formation piece: its traits reference its own faction's allies, so a mixed squad behaves very differently from the same creatures fielded alone. Pages in this journal give each host's doctrine and a clickable roster.</p>
"""),
        ("Grandma's Host", f"""
<h2>Grandma — Babha Yagha</h2>
<p><strong>Doctrine:</strong> fear, darkness, soul attrition, layered control. Darklings screen for Hexers and Berbalangs; Soul-Cage Porters anchor the line; Stalkers punish flanks. Grandma fights behind the line and uses minions as conduits and sacrifices.</p>
<h3>Synergies</h3>
<ul>
<li>Darkling Knights' <em>Dread Pennant</em> and Grandma's <em>Frightening Gaze</em> feed <em>Black Banner</em> (+1 to hit vs. frightened) and the Hexer's <em>Coven Relay</em>.</li>
<li><em>Grim Conduit</em> lets Grandma originate <em>Soul Steal</em> from any Soul-Cage Porter within 120 ft. — keep Porters forward.</li>
<li>Berbalang <em>Secret Relay</em> gives the whole host telepathic coordination within 60 ft. of Grandma.</li>
<li>The Flying Cauldron and Walking Hut are her war engines: artillery/transport and a mobile command bastion.</li>
</ul>
{faction_table(creatures, 'Grandma')}
"""),
        ("Auntie's Host", f"""
<h2>Auntie — Mama Yagha</h2>
<p><strong>Doctrine:</strong> poison stacking and petrification. Fangguards hold, Coil Adepts restrain, archers exploit poisoned targets, Eye Acolytes force Constitution saves, Chainmasters move warbeasts, and Alchemists deny areas.</p>
<h3>Synergies</h3>
<ul>
<li><em>Venom Command</em>: the first minion attack each round against a poisoned enemy near Auntie has advantage.</li>
<li>Coil Adepts' grapples impose disadvantage on poison saves from other Auntie units; Eye Acolytes punish the restrained.</li>
<li>Valdershmort is both monster and mount — the Chainmaster's <em>Handler</em> and <em>Drive the Beast</em> make it far more mobile.</li>
</ul>
{faction_table(creatures, 'Auntie')}
"""),
        ("Gaga's Host", f"""
<h2>Gaga — Gahgah Yagha</h2>
<p><strong>Doctrine:</strong> shock assault. Trolls breach and regenerate, Snail Lancers create an antimagic spearhead, Flail Snails shelter the advance, Spider-Riders pin escape routes, and Rage-Drummers keep the whole host moving.</p>
<h3>Synergies</h3>
<ul>
<li><em>Break Their Line</em>: every time Gaga knocks prone or forces movement, a minion slides 10 ft. free.</li>
<li>Flesh-Menders' <em>Stitch the Host</em> adds +2 to adjacent troll regeneration; acid shuts the whole engine down.</li>
<li>Snail Lancers near a Flail Snail gain advantage on saves against spells — the spearhead is a moving antimagic wedge.</li>
</ul>
{faction_table(creatures, 'Gaga')}
"""),
        ("Combined-Army Waves", """
<h2>Recommended Combined-Army Wave</h2>
<p>Start with scouts/skirmishers, then a control layer, then the heavy line, and only then reveal the hag. Mixing factions works best when Grandma supplies control, Auntie supplies poison/petrification, and Gaga supplies forced movement and finishers.</p>
<ol>
<li><strong>Screen:</strong> Darkling Knives, Spider-Rider Harriers, Spitebow archers.</li>
<li><strong>Control:</strong> Rotbriar Hexers, Coil Adepts, Petrifying Eye Acolytes, Rage-Drum Goblins.</li>
<li><strong>Heavy line:</strong> Soul-Cage Porters, Troll Linebreakers, Flail Snail Warbeasts, Fangguards.</li>
<li><strong>Reveal:</strong> a hag, her signature war asset, and her legendary actions.</li>
</ol>
<p>XP values on each host page use the standard CR-to-XP table so you can budget waves with your usual encounter math.</p>
"""),
        ("Foundry Notes", f"""
<h2>Using this module in Foundry</h2>
<ul>
<li>All 24 stat blocks live in the <strong>Yagha Coven War Host — Actors</strong> compendium, foldered by host. Drag any actor onto a scene, or use <em>Import All Content</em> from the compendium's context menu.</li>
<li>On first load as GM you're offered a one-click import into a world folder. You can run it later from the console: <code>game.modules.get("{MODULE_ID}").api.importAll()</code>.</li>
<li>Attacks and saves are native dnd5e Activities. Saves that inflict conditions carry Active Effects you can apply from the chat card.</li>
<li>Legendary actions consume the creature's legendary action pool automatically; Grandma's Legendary Resistance consumes her 3/day pool.</li>
<li>Regeneration traits include a <em>Regenerate</em> heal activity — click it at the start of the creature's turn (skip it if acid suppression applies).</li>
<li>Every description also carries inline roll links as a fallback.</li>
</ul>
"""),
    ]
    pages = []
    for i, (name, content) in enumerate(pages_src):
        pid = did("journal", "gm-guide", name)
        pages.append({
            "_id": pid, "_key": f"!journal.pages!{jid}.{pid}", "name": name, "type": "text",
            "title": {"show": True, "level": 1}, "image": {}, "video": {"controls": True, "volume": 0.5},
            "src": None, "system": {}, "sort": (i + 1) * 100000,
            "text": {"content": content.strip(), "format": 1, "markdown": ""},
            "ownership": {"default": -1}, "flags": {}, "_stats": dict(STATS), "category": None,
        })
    return {"_id": jid, "_key": f"!journal!{jid}", "name": "Doorinia Hag Host — GM Guide",
            "pages": pages, "folder": None, "sort": 0, "categories": [],
            "ownership": {"default": 0}, "flags": {MODULE_ID: {"generated": True}}, "_stats": dict(STATS)}


# ---------------------------------------------------------------- manifest
def manifest():
    return {
        "id": MODULE_ID,
        "title": "Doorinia: The Yagha Coven War Host",
        "description": "Three High Hags and their coordinated armies, rebuilt from their Highforest origins for the conquered Domain of Delight of Doorinia. 24 dnd5e stat blocks (3 boss hags, 18 army units, 3 signature war assets) with native Activities, condition effects and legendary-action automation, plus a GM tactics journal.",
        "version": VERSION,
        "compatibility": {"minimum": "14", "verified": "14"},
        "authors": [
            {"name": "Asmo — Pacts & Polyhedrals", "url": "https://www.patreon.com/pactsandpolyhedrals",
             "flags": {"startplaying": "dmasmo"}},
            {"name": "Ben Vale"},
        ],
        "relationships": {
            "systems": [{"id": "dnd5e", "type": "system", "compatibility": {"minimum": "5.3.3", "verified": "5.3.3"}}],
        },
        "esmodules": ["scripts/dorinia-hag-host.js"],
        "packs": [
            {"name": ACTOR_PACK, "label": "Yagha Coven War Host — Actors", "path": f"packs/{ACTOR_PACK}",
             "type": "Actor", "system": "dnd5e", "ownership": {"PLAYER": "NONE", "ASSISTANT": "OWNER"}},
            {"name": JOURNAL_PACK, "label": "Yagha Coven War Host — GM Guide", "path": f"packs/{JOURNAL_PACK}",
             "type": "JournalEntry", "ownership": {"PLAYER": "NONE", "ASSISTANT": "OWNER"}},
        ],
        "packFolders": [{"name": "Pacts & Polyhedrals", "sorting": "m", "color": "#3b1f4a", "packs": [],
                         "folders": [{"name": "Doorinia: Yagha Coven War Host", "sorting": "a", "color": "#4b2a5c",
                                      "packs": [ACTOR_PACK, JOURNAL_PACK]}]}],
        "languages": [],
        "url": GH,
        "manifest": f"{GH}/releases/latest/download/module.json",
        "download": f"{GH}/releases/download/v{VERSION}/{ZIP_NAME}",
        "bugs": f"{GH}/issues",
        "readme": f"{GH}/blob/main/README.md",
        "changelog": f"{GH}/blob/main/CHANGELOG.md",
        "flags": {"allowBugReporter": False},
    }


# ---------------------------------------------------------------- main
def write_docs(dirpath: Path, docs):
    if dirpath.exists():
        shutil.rmtree(dirpath)
    dirpath.mkdir(parents=True)
    for d in docs:
        slug = re.sub(r"[^a-z0-9]+", "-", d["name"].lower()).strip("-")
        (dirpath / f"{slug}_{d['_id']}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    creatures = json.loads((SOURCE / "creatures.json").read_text(encoding="utf-8"))

    folders, folder_ids = [], {}
    for fac, cfg in FACTIONS.items():
        fid = did("folder", fac)
        folder_ids[fac] = fid
        folders.append({"_id": fid, "_key": f"!folders!{fid}", "name": cfg["folder"], "type": "Actor",
                        "folder": None, "sorting": "m", "sort": cfg["sort"], "color": cfg["color"],
                        "description": "", "flags": {MODULE_ID: {"generated": True}}, "_stats": dict(STATS)})

    actors = []
    order = {f: 0 for f in FACTIONS}
    for m in sorted(creatures, key=lambda c: (list(FACTIONS).index(c["faction"]), -c["cr"])):
        order[m["faction"]] += 1
        actors.append(build_actor(m, folder_ids[m["faction"]], order[m["faction"]] * 1000))

    write_docs(BUILD / ACTOR_PACK, actors + folders)
    write_docs(BUILD / JOURNAL_PACK, [build_journal(creatures)])

    (MODULE / "module.json").write_text(json.dumps(manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # compile LevelDB packs with the official Foundry CLI
    packs_dir = MODULE / "packs"
    if packs_dir.exists():
        shutil.rmtree(packs_dir)
    subprocess.run(["node", str(TOOLS / "compile_packs.mjs"), str(BUILD), str(packs_dir), ACTOR_PACK, JOURNAL_PACK],
                   check=True)

    # release assets: zip with files at root + standalone module.json
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    with zipfile.ZipFile(DIST / ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(MODULE.rglob("*")):
            if p.is_file() and p.name not in ("LOCK", "LOG", "LOG.old"):
                z.write(p, p.relative_to(MODULE).as_posix())
    shutil.copy(MODULE / "module.json", DIST / "module.json")
    print(f"Built {len(actors)} actors, {len(folders)} folders, 1 journal -> {DIST / ZIP_NAME}")


if __name__ == "__main__":
    sys.exit(main())
