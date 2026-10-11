# Changelog

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
