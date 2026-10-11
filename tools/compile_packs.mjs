// Compiles JSON source docs into LevelDB compendium packs with the official Foundry CLI.
// usage: node tools/compile_packs.mjs <srcRoot> <packsRoot> <pack...>
import { compilePack } from "@foundryvtt/foundryvtt-cli";
import path from "node:path";
const [src, dest, ...packs] = process.argv.slice(2);
for (const p of packs) {
  await compilePack(path.join(src, p), path.join(dest, p), { log: false });
  console.log(`compiled pack ${p}`);
}
