/**
 * Doorinia: The Yagha Coven War Host
 * Pacts & Polyhedrals — Foundry VTT v14 / dnd5e 5.3.3
 *
 * All content ships in compendium packs. This script only:
 *  - offers a one-time import of the packs into the world (GM only),
 *  - exposes an API: game.modules.get("dorinia-hag-host").api
 */
const ID = "dorinia-hag-host";
const ACTOR_PACK = `${ID}.hag-host-actors`;
const JOURNAL_PACK = `${ID}.hag-host-journal`;
const ROOT_FOLDER = "Doorinia — Yagha Coven War Host";

Hooks.once("init", () => {
  game.settings.register(ID, "promptShown", {
    name: "Import prompt shown", scope: "world", config: false, type: Boolean, default: false
  });
  game.settings.register(ID, "imported", {
    name: "Imported to world", scope: "world", config: false, type: Boolean, default: false
  });
});

Hooks.once("ready", async () => {
  const module = game.modules.get(ID);
  module.api = { importAll, removeImported, rebuild, isImported };
  if (!game.user.isGM) return;

  for (const p of [ACTOR_PACK, JOURNAL_PACK]) {
    if (!game.packs.get(p)) console.error(`${ID} | compendium ${p} not found — module install is incomplete.`);
  }
  if (game.settings.get(ID, "promptShown") || isImported()) return;
  // Only one GM should be prompted.
  if (game.users.activeGM && game.users.activeGM !== game.user) return;

  const DialogV2 = foundry.applications.api.DialogV2;
  const yes = await DialogV2.confirm({
    window: { title: "Doorinia: Yagha Coven War Host" },
    content: `<p>Import the <strong>24 Yagha Coven stat blocks</strong> and the <strong>GM Guide</strong> into this world?</p>
      <p>They will be placed in the <em>${ROOT_FOLDER}</em> folders. Everything also stays available in the module's compendiums,
      and you can import later with <code>game.modules.get("${ID}").api.importAll()</code>.</p>`,
    rejectClose: false
  });
  await game.settings.set(ID, "promptShown", true);
  if (yes) await importAll();
});

function generated(collection) {
  return collection.filter(d => d.getFlag(ID, "generated") || d._stats?.compendiumSource?.startsWith(`Compendium.${ACTOR_PACK}`)
    || d._stats?.compendiumSource?.startsWith(`Compendium.${JOURNAL_PACK}`));
}

function isImported() {
  return generated(game.actors).length > 0;
}

async function importAll() {
  if (!game.user.isGM) return ui.notifications.warn("Only a GM can import the Yagha Coven War Host.");
  if (isImported()) {
    ui.notifications.info("Yagha Coven War Host is already in this world. Use api.rebuild() to refresh it from the compendium.");
    return;
  }
  const actors = game.packs.get(ACTOR_PACK);
  const journal = game.packs.get(JOURNAL_PACK);
  if (!actors || !journal) return ui.notifications.error("Yagha Coven War Host compendiums are missing — reinstall the module.");

  try {
    // importAll recreates the pack's internal faction folders under the named world folder.
    const imported = await actors.importAll({ folderName: ROOT_FOLDER, keepId: true });
    await journal.importAll({ folderName: ROOT_FOLDER, keepId: true });
    await game.settings.set(ID, "imported", true);
    ui.notifications.info(`Yagha Coven War Host: ${imported?.length ?? "all"} actors and the GM Guide imported.`);
  } catch (err) {
    console.error(`${ID} | import failed`, err);
    ui.notifications.error("Yagha Coven War Host import failed — see the console (F12).");
  }
}

async function removeImported() {
  if (!game.user.isGM) return;
  const actors = generated(game.actors);
  const journals = generated(game.journal);
  if (actors.length) await Actor.deleteDocuments(actors.map(a => a.id));
  if (journals.length) await JournalEntry.deleteDocuments(journals.map(j => j.id));

  // Remove now-empty world folders created by the import.
  const roots = game.folders.filter(f => f.name === ROOT_FOLDER && ["Actor", "JournalEntry"].includes(f.type));
  for (const root of roots) {
    const subtree = [root, ...root.getSubfolders(true)];
    if (subtree.every(f => f.contents.length === 0)) await Folder.deleteDocuments(subtree.map(f => f.id));
  }
  await game.settings.set(ID, "imported", false);
  ui.notifications.info("Yagha Coven War Host world content removed (compendiums untouched).");
}

async function rebuild() {
  await removeImported();
  await importAll();
}
