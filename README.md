# Doorinia: The Yagha Coven War Host

Target: Foundry VTT v14 + D&D5e 5.3.3.

## Included
- Babha Yagha / Grandma, Mama Yagha / Auntie, Gahgah Yagha / Gaga.
- Six coordinated minion roles for each hag (18 army units total).
- Grandma's Flying Cauldron, Grandma's Walking Hut, and Valdershmort.
- Native D&D5e Activities for attacks/saves where accepted by 5.3.3, plus clickable inline-roll fallbacks on every damaging action.
- Automatic Actor-folder organization and GM tactics Journal.

## Install
1. Extract this folder into Foundry's `Data/modules/` directory.
2. Restart Foundry and enable **Doorinia: The Yagha Coven War Host** in the world.
3. On first load as GM, the actors are created automatically under **Doorinia — Yagha Coven War Host**.

## Rebuild / remove
From the browser console while logged in as GM:
```js
await game.modules.get("dorinia-hag-host").api.rebuild();
await game.modules.get("dorinia-hag-host").api.removeImported();
```

## Design note
The three hag stat blocks preserve the supplied campaign identities and core mechanics, while their armies are newly expanded to fit their current conquest of Doorinia. The army units are original homebrew intended to function as combined formations rather than isolated sacks of hit points.
