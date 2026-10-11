# Doorinia: The Yagha Coven War Host

*A Pacts & Polyhedrals module for Foundry VTT v14 + D&D 5e 5.3.3*

Three High Hags and their coordinated armies, rebuilt from their Highforest origins for the conquered Domain of Delight of Doorinia.

## Contents
- **Yagha Coven War Host — Actors** compendium (24 NPCs, foldered by host)
  - **Grandma — Babha Yagha** (CR 22): Darkling Knife & Knight, Berbalang Secret-Eater, Rotbriar Hexer, Soul-Cage Porter, Thorn-Memory Stalker, Grandma's Flying Cauldron, Grandma's Walking Hut
  - **Auntie — Mama Yagha** (CR 15): Yuan-ti Fangguard, Coil Adept, Spitebow Venom Archer, Petrifying Eye Acolyte, Basilisk Chainmaster, Venomwell Alchemist, Valdershmort
  - **Gaga — Gahgah Yagha** (CR 18): Troll Linebreaker, Troll Flesh-Mender, Darkling Snail Lancer, Flail Snail Warbeast, Spider-Rider Harrier, Rage-Drum Goblin
- **Yagha Coven War Host — GM Guide** compendium: doctrine, synergies, clickable rosters with CR/XP, wave structure, Foundry notes.

## Art
Every creature has a portrait and a round faction-ringed token in a grotesque-chibi gothic comic style. Replacement prompts are in `ART-PROMPTS.md`.

## Automation (no Midi-QOL / DAE required)
- Native dnd5e Activities for every attack, save, heal and utility action.
- Condition riders (frightened, poisoned, restrained, prone, stunned, blinded, petrified, grappled) ship as Active Effects you apply from the chat card.
- Legendary actions consume the legendary action pool; Grandma's Legendary Resistance consumes her 3/day pool; 1/Day abilities track their uses.
- Aura/trigger traits (Snake Hair, Petrifying Gaze, Death Flash, Charge the Glitter…) have clickable save activities; Regeneration traits have a Regenerate heal.
- Inline roll links in every description as a fallback.

## Install
Paste this manifest URL into **Add-on Modules → Install Module**:

```
https://github.com/pacts-and-polyhedrals/dorinia-hag-host/releases/latest/download/module.json
```

Enable the module in your world. On first load the GM is offered a one-click import into a world folder; everything is also usable straight from the compendiums.

## GM API
```js
const api = game.modules.get("dorinia-hag-host").api;
await api.importAll();       // import actors + guide into the world
await api.rebuild();         // delete imported copies and re-import from the compendium
await api.removeImported();  // remove imported copies (compendiums untouched)
```

## Credits
Campaign material by Asmo (Pacts & Polyhedrals) and Ben Vale. Army units are original homebrew.
[Patreon](https://www.patreon.com/pactsandpolyhedrals) · [StartPlaying](https://startplaying.games/gm/dmasmo)
