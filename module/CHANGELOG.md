# Changelog

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
