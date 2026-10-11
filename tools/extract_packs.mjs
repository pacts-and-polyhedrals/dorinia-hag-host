// Extracts compiled LevelDB packs back to JSON so the validator checks what actually ships.
import { extractPack } from "@foundryvtt/foundryvtt-cli";
import path from "node:path";
const [packsRoot, dest, ...packs] = process.argv.slice(2);
for (const p of packs) await extractPack(path.join(packsRoot, p), path.join(dest, p), { clean: true, log: false });
