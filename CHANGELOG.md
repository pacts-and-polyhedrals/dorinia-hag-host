# Changelog

## 1.4.0 — Low-level host, Sworn Host, art for everything
**18 new units (CR 1/4 to 5).** Each hag gets four household troops of her own plus two units she pledges to the coven.

| Hag | Household (personal) | Pledged to the coven (Sworn Host) |
|---|---|---|
| **Grandma** | Quickling Thief (1/2), Quickling Assassin (2), Darkling Lantern-Snuffer (1/4), Soul-Moth Swarm (2) | Coven Crow (1/4), Hollow Hound (3) |
| **Auntie** | Yuan-ti Foot Soldier (1/2), Yuan-ti Broodling Slinger (1/4), Stone-Scale Adder (1), Basilisk Hatchling (3) | Coven Toad (1), Petrified Thrall (2) |
| **Gaga** | Goblin Bone-Thrower (1/4), Troll Whelp (2), Bugbear Sack-Snatcher (1), Ogre Log-Ram (3) | Coven Bogle (1/2), Archfey Husk (5) |

- Sworn Host units have their own compendium folder and a gold faction palette. Each one is tagged with the hag who supplies it, and it counts as an ally of all three hosts.
- All new abilities were built against the same 2014 rules check as 1.3.1. None of them repeats what a condition, a core rule or another ability on the same creature already does.
- They are designed to combo with the existing host:
  - Quickling Assassins finish off frightened targets.
  - Bone-Thrower volleys knock targets prone for Troll Whelps and Gaga's *Break Their Line*.
  - Petrified Thralls set victims up for Valdershmort.
  - Archfey Husks raise the save DC of coven spells.
  - Soul-Moth Swarms silence casters.
- **Art:** portraits and tokens for all 18 new units in the same style.
- **Icons:** all 261 abilities and spells now have their own icon in the same ink style, coloured by host for abilities and by school for spells, each with a main motif and a corner emblem. Item icons are in `assets/icons/`.
- GM Guide: new **Sworn Host** page with a CR/XP roster.
- `ART-PROMPTS.md`: prompts for the 18 new units.

## 1.3.1 — Rules audit
Every trait, action, legendary action and homebrew spell was checked against the 2014 rules and the conditions it references. Anything redundant, contradictory or non-functional was changed.

**Redundant with the core rules**
- *Chain the Stone* (Chainmaster): restrained and petrified targets already grant advantage. Now Barbed Chain crits restrained targets on 18–20, ignores the petrified condition's damage resistance, and shatters a petrified creature reduced to 0 hp.
- *Briar Screen* (Hexer): an intervening creature already gives half cover. Now it gives three-quarters cover.
- *Slither Through* (Coil Adept): moving through allies' spaces is already allowed. Now the adept moves through hostile creatures of any size, and allied spaces aren't difficult terrain for it.
- *Veiled Advance* (Darkling Knife): unseen attackers already have advantage. Now it deals +2d6 necrotic on the first hit after starting the turn in dim light or darkness.
- *Two Heads* (Gaga): she is immune to charmed, so it no longer lists charmed.
- *Doorinian Matriarch* (Grandma): now applies only to units not already immune to charmed or frightened.
- *Hag-Ring of Highforest*: it granted advantage on saves against spells, which all three hags already have. Now creatures inside the ring have disadvantage on saves against the coven's spells.

**Redundant within a stat block**
- *Viper's Kiss*: it was a weaker copy of Auntie's Venomous Bite. It is now a bonus-action venom charge on her next melee hit that ignores poison resistance.
- *Gorgon's Glance*: it copied the Acolyte's Stone Glare. It now finishes Stone Glare's work, petrifying a target that is already restrained.
- *Venomwell Bomb*: it was a smaller copy of the at-will Venom Mortar. It is now a lingering acid pool and concentration hazard.
- *Filthy Stitching*: it duplicated the Gut-Stitch spell. It now restarts acid- or fire-suppressed troll Regeneration.
- *Prepared Antivenom*: it overlapped the new Toxic Logistics. It now rerolls any failed Constitution save, including concentration.
- *Toxic Logistics*: it now grants acid resistance, and makes poison-resistant allies immune to the poisoned condition.
- Spells outclassed by the caster's own actions were replaced:
  - Gaga: *shocking grasp* and *thunderwave* became *message* and *command*.
  - Grandma: *fear* and *sleep* became *animate dead* and *hideous laughter*. Cackle and Grandma's Lullaby already cover fear and sleep.
  - Acolyte: *poison spray* became *guidance*.
  - Alchemist: *acid splash*, *poison spray* and *acid arrow* became *mage hand*, *prestidigitation*, *grease* and *protection from poison*.
  - Flesh-Mender: *cure wounds* became *aid*.
- *Troll-Blood Boil*: it referenced a fire weakness Gaga doesn't have and shortened her acid suppression, which made it a nerf. Now acid no longer suppresses her Regeneration while it lasts.

**Missing or non-functional**
- Added **Multiattack** to Grandma (Frightening Gaze plus two Claws; her Claw text already referred to it), Auntie (Claws plus Bite) and Gaga (Bite plus Claw and Seize). Gaga's legendary "Multiattack" became *Rend* (one attack).
- *Recharge Innate Magic* (Auntie) referred to recharge features she doesn't have. It is now *Venom Renewal*: regain a spell slot of 3rd level or lower, or a servant's daily innate use.
- Valdershmort's 22d6 Poison Breath now has **Recharge 5–6**; it was usable every turn.
- *Rotbriar Hexer — Coven Relay* now moves its Rotbriar Hex. Hex Mark lasts only one turn and couldn't meaningfully be moved.
- *Memory Scent* (Stalker) is now blindsight 30 ft. against frightened creatures.
- *Thorn Rake* now actually pulls its target 10 ft.

**Consistency**
- Grandma's legendary DCs raised from 21 to 22 to match her other save DCs.
- Gaga's grapple escape DC raised from 15 to 18 to match her other DCs.
- Auntie's legendary "Snake Hair" renamed *Hair Lash* so it doesn't clash with her Snake Hair trait.
- Scintillating Pulse now says "the warbeast's choice" instead of "Gaga's".

## 1.3.0
- **Coven Manager:** Game Settings → Configure Settings → *Doorinia: Yagha Coven War Host* → **Open Coven Manager**. It shows the module version against the imported version and has Import, **Update in place**, Rebuild, Remove and quick-open buttons for the Actors, Spells and GM Guide compendiums.
- **Update in place:** refreshes stats, spells, art and the GM Guide on actors already in the world. IDs, folders and ownership stay the same, and items you added yourself are kept. It also refreshes the art on tokens already placed on scenes.
- **Update prompt:** when the module version is newer than the imported content, the GM is offered an in-place update on load (can be turned off in the settings).
- **Spellcasting for the coven hierarchy:** 125 spells assigned across 8 casters.
  - **Grandma** (17th-level, Cha): fear, darkness, soul theft and curses, up to *weird*.
  - **Auntie** (11th-level, Cha): poison, serpents and petrification, up to *flesh to stone*.
  - **Gaga** (9th-level, Cha): thunder, earth and brute force, up to *wall of stone*.
  - **Shared Spellcasting (Yagha Coven):** the 14-spell hag-coven list, once per day each for the whole coven.
  - **Servants (innate):** Rotbriar Hexer, Petrifying Eye Acolyte, Venomwell Alchemist, Berbalang Secret-Eater, Troll Flesh-Mender.
- **Spells compendium:** 64 official SRD 5.1 spells and 16 homebrew spells, in folders by list. Homebrew includes *Soul Lantern Siphon*, *Grandma's Lullaby*, *Hollow the Name*, *Viper's Kiss*, *Coils of the Mother Serpent*, *Gorgon Bloom*, *Twin-Throat Bellow*, *Troll-Blood Boil*, *Earthshaker Stomp*, *Coven's Rot*, *Archfey Drain* and *Hag-Ring of Highforest*.
- **Coven automation:** casting a coven spell spends it on all three hags. Optionally, a coven spell is blocked unless the three hags' tokens are within 30 ft of each other. Both behaviours can be toggled in the settings.
- **Legendary Resistance (3/Day)** added to Auntie and Gaga; all three hags now have it.
- GM Guide: new **Coven Spellbook** page with every list linked to the Spells compendium.

## 1.2.0
- **Art:** all 24 creatures now have a portrait (1000×1000) and a round faction-ringed token (512×512) in a grotesque-chibi gothic comic style: purple for Grandma's host, green for Auntie's, rust for Gaga's.
- Actor portraits and prototype tokens point at the new art (`assets/portraits`, `assets/tokens`).
- `ART-PROMPTS.md`: a ready-to-use image prompt for every creature, so painterly replacements can be dropped in under the same filenames.

## 1.1.0
Full rebuild. Fixes installation on The Forge and Foundry (1.0.0 shipped with an empty manifest/download URL and a wrapped zip).

- **Install fixed:** manifest and download URLs point at github.com/pacts-and-polyhedrals/dorinia-hag-host; release zip has files at its root.
- **Compendium packs:** all 24 stat blocks ship in *Yagha Coven War Host — Actors* (one folder per hag) and the *GM Guide* journal ships as its own compendium, instead of being generated into the world on every load.
- **dnd5e 5.3.3 Activities rebuilt:** flat attack bonuses, fixed save DCs, damage parts, heal activities (Filthy Stitching, all Regeneration traits).
- **Conditions as Active Effects:** frightened, poisoned, restrained, prone, stunned, blinded, petrified and grappled apply from the chat card.
- **Legendary automation:** legendary actions use the legendary activation type with their cost and spend the creature's legendary action pool; Grandma's Legendary Resistance spends her 3/day pool; 1/Day abilities track uses.
- **Clickable aura/trigger saves:** Snake Hair, Petrifying Gaze, Death Flash, Charge the Glitter, Dung-Spear rider.
- **GM Guide:** six pages — overview, a doctrine/synergy page per host with clickable CR/XP rosters, combined-army waves, Foundry notes.
- Token sizes match creature size; Deep Speech and Yuan-ti languages corrected.
- First-load import prompt for the GM, plus `importAll()`, `rebuild()` and `removeImported()` API.
- Credits corrected to Asmo (Pacts & Polyhedrals) and Ben Vale.

## 1.0.0
- Initial release (world-import script version).
