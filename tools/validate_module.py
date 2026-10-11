#!/usr/bin/env python3
"""Validates the built dorinia-hag-host module against dnd5e 5.3.3 keys and the P&P release rules."""
import json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE, DIST, TOOLS = ROOT / "module", ROOT / "dist", ROOT / "tools"
ID_RE = re.compile(r"^[A-Za-z0-9]{16}$")

K = {  # verified against foundryvtt/dnd5e release-5.3.3 module/config.mjs
 "abilities": set("str dex con int wis cha".split()),
 "skills": set("acr ani arc ath dec his ins itm inv med nat prc prf per rel slt ste sur".split()),
 "damage": set("acid bludgeoning cold fire force lightning necrotic piercing poison psychic radiant slashing thunder".split()),
 "conditions": set("bleeding blinded burning charmed cursed dehydration deafened diseased exhaustion falling frightened grappled incapacitated invisible malnutrition paralyzed petrified poisoned prone restrained silenced stunned suffocation surprised transformed unconscious".split()),
 "creature": set("aberration beast celestial construct dragon elemental fey fiend giant humanoid monstrosity ooze plant undead".split()),
 "sizes": set("tiny sm med lg huge grg".split()),
 "activation": set("action bonus reaction minute hour day longRest shortRest encounter turnStart turnEnd legendary mythic lair crew special".split()),
 "languages": set("common draconic dwarvish elvish giant gnomish goblin halfling orc sign aarakocra abyssal cant celestial deep druidic gith gnoll infernal primordial aquan auran ignan terran sylvan undercommon".split()),
 "activity": set("attack save heal utility damage check cast enchant forward order summon transform".split()),
 "targets": set(["", "self", "ally", "enemy", "creature", "object", "space", "creatureOrObject", "any", "willing"]),
}
errors, warns = [], []
def err(m): errors.append(m)

man = json.loads((MODULE / "module.json").read_text())
gh = "https://github.com/pacts-and-polyhedrals/dorinia-hag-host"
v = man["version"]
if man["url"] != gh: err("manifest url not P&P repo")
if man["manifest"] != f"{gh}/releases/latest/download/module.json": err("manifest URL wrong")
if man["download"] != f"{gh}/releases/download/v{v}/dorinia-hag-host.zip": err("download URL wrong")
for p in man["esmodules"]:
    if not (MODULE / p).is_file(): err(f"esmodule missing: {p}")
for p in man["packs"]:
    if not (MODULE / p["path"]).is_dir(): err(f"pack missing: {p['path']}")
if any("openai" in json.dumps(a).lower() for a in man["authors"]): err("stray author credit")

# release assets
z = zipfile.ZipFile(DIST / "dorinia-hag-host.zip")
names = z.namelist()
if "module.json" not in names: err("zip: module.json not at root (wrapper folder?)")
if any(n.startswith("dorinia-hag-host/") for n in names): err("zip: wrapper folder present")
if json.loads(z.read("module.json")) != man: err("zip module.json differs from module/module.json")
if json.loads((DIST / "module.json").read_text()) != man: err("dist/module.json differs")
if not man["download"].endswith("/" + "dorinia-hag-host.zip"): err("download asset name mismatch")

# extract compiled packs and check what actually ships
tmp = Path(tempfile.mkdtemp())
subprocess.run(["node", str(TOOLS / "extract_packs.mjs"), str(MODULE / "packs"), str(tmp),
                "hag-host-actors", "hag-host-journal"], check=True)
docs = [json.loads(f.read_text()) for f in (tmp / "hag-host-actors").glob("*.json")]
actors = [d for d in docs if d.get("type") == "npc"]
folders = {d["_id"] for d in docs if d["_key"].startswith("!folders!")}
ids = set()
counts = {"items": 0, "activities": 0, "effects": 0, "legendary": 0}
for a in actors:
    n = a["name"]; s = a["system"]
    if not ID_RE.match(a["_id"]) or a["_id"] in ids: err(f"{n}: bad/dup id")
    ids.add(a["_id"])
    if a["folder"] not in folders: err(f"{n}: folder missing")
    if s["traits"]["size"] not in K["sizes"]: err(f"{n}: size")
    if s["details"]["type"]["value"] not in K["creature"]: err(f"{n}: creature type")
    for k in s["skills"]:
        if k not in K["skills"]: err(f"{n}: skill {k}")
    for k in s["traits"]["languages"]["value"]:
        if k not in K["languages"]: err(f"{n}: language {k}")
    for f in ("dr", "di", "dv"):
        for k in s["traits"][f]["value"]:
            if k not in K["damage"]: err(f"{n}: {f} {k}")
    for k in s["traits"]["ci"]["value"]:
        if k not in K["conditions"]: err(f"{n}: ci {k}")
    for pth in (a["img"], a["prototypeToken"]["texture"]["src"]):
        local = MODULE / pth.replace("modules/dorinia-hag-host/", "")
        if not local.is_file(): err(f"{n}: missing art {pth}")
        if pth.replace("modules/dorinia-hag-host/", "") not in names: err(f"{n}: art not in zip {pth}")
    has_leg = False
    for it in a["items"]:
        counts["items"] += 1
        eff_ids = {e["_id"] for e in it.get("effects", [])}
        for e in it.get("effects", []):
            counts["effects"] += 1
            for st in e["statuses"]:
                if st not in K["conditions"]: err(f"{n}/{it['name']}: status {st}")
        for key, act in it["system"]["activities"].items():
            counts["activities"] += 1
            where = f"{n}/{it['name']}/{act['name']}"
            if key != act["_id"] or not ID_RE.match(key): err(f"{where}: activity id")
            if act["type"] not in K["activity"]: err(f"{where}: activity type")
            if act["activation"]["type"] not in K["activation"]: err(f"{where}: activation {act['activation']['type']}")
            if act["target"]["affects"]["type"] not in K["targets"]: err(f"{where}: target type")
            if act["activation"]["type"] == "legendary":
                has_leg = True; counts["legendary"] += 1
                if not act["activation"]["value"]: err(f"{where}: legendary cost")
                if any(t["target"].startswith("resources.legact") for t in act["consumption"]["targets"]):
                    err(f"{where}: double legendary consumption")
            for e in act.get("effects", []):
                if e["_id"] not in eff_ids: err(f"{where}: effect ref {e['_id']} not on item")
            for part in (act.get("damage") or {}).get("parts", []) + ([act["healing"]] if "healing" in act else []):
                for t in part["types"]:
                    if t not in K["damage"] | {"healing", "temphp"}: err(f"{where}: damage type {t}")
                if not part.get("number") and not part["custom"]["enabled"]: err(f"{where}: empty damage part")
            if act["type"] == "attack":
                if not act["attack"]["flat"] or not act["attack"]["bonus"]: err(f"{where}: attack bonus")
            if act["type"] == "save":
                if not act["save"]["ability"] or not all(x in K["abilities"] for x in act["save"]["ability"]): err(f"{where}: save ability")
                if act["save"]["dc"]["calculation"] != "" or not act["save"]["dc"]["formula"].isdigit(): err(f"{where}: save dc")
                if act["damage"]["onSave"] not in ("half", "none", "full"): err(f"{where}: onSave")
        desc = it["system"]["description"]["value"]
        if desc.count("[[") != desc.count("]]"): err(f"{n}/{it['name']}: unbalanced enricher")
    if bool(s["resources"]["legact"]["max"]) != has_leg: err(f"{n}: legendary pool/actions mismatch")
    if s["resources"]["legres"]["max"] and not any(i["system"]["identifier"] == "legendary-resistance" for i in a["items"]):
        err(f"{n}: legres without legendary-resistance item")

# journal links
jdocs = [json.loads(f.read_text()) for f in (tmp / "hag-host-journal").glob("*.json")]
links = 0
for j in jdocs:
    for p in j["pages"]:
        for uid in re.findall(r"@UUID\[Compendium\.dorinia-hag-host\.hag-host-actors\.Actor\.([A-Za-z0-9]{16})\]", p["text"]["content"]):
            links += 1
            if uid not in ids: err(f"journal {p['name']}: dead link {uid}")

# JS syntax
r = subprocess.run(["node", "--check", str(MODULE / "scripts/dorinia-hag-host.js")], capture_output=True, text=True)
if r.returncode: err("script syntax: " + r.stderr)

print(f"actors={len(actors)} folders={len(folders)} items={counts['items']} activities={counts['activities']} "
      f"effects={counts['effects']} legendary_activities={counts['legendary']} journal_pages={sum(len(j['pages']) for j in jdocs)} roster_links={links}")
print(f"zip entries={len(names)}")
if errors:
    print("FAIL"); [print(" -", e) for e in errors]; sys.exit(1)
print("PASS")
