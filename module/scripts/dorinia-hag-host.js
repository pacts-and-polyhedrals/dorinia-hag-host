/**
 * Doorinia: The Yagha Coven War Host
 * Pacts & Polyhedrals — Foundry VTT v14 / dnd5e 5.3.3
 *
 *  - Coven Manager (Game Settings → Configure Settings → this module → "Open Coven Manager"):
 *    import, update in place, rebuild, remove, open compendiums.
 *  - Prompts the GM when the module version is newer than the content imported into the world.
 *  - Shared coven spellcasting: coven spell uses are synced across the three hags, and (optionally)
 *    a coven spell is blocked unless all three hags are within 30 ft of each other on the scene.
 *  - API: game.modules.get("dorinia-hag-host").api
 */
const ID = "dorinia-hag-host";
const TITLE = "Doorinia: Yagha Coven War Host";
const ACTOR_PACK = `${ID}.hag-host-actors`;
const JOURNAL_PACK = `${ID}.hag-host-journal`;
const SPELL_PACK = `${ID}.hag-host-spells`;
const ROOT_FOLDER = "Doorinia — Yagha Coven War Host";
const COVEN_RANGE = 30;

const moduleVersion = () => game.modules.get(ID)?.version ?? "0.0.0";
const isNewer = (a, b) => foundry.utils.isNewerVersion(a, b);

/* ------------------------------------------------------------------ settings & menu */
Hooks.once("init", () => {
  game.settings.register(ID, "promptShown", { scope: "world", config: false, type: Boolean, default: false });
  game.settings.register(ID, "imported", { scope: "world", config: false, type: Boolean, default: false });
  game.settings.register(ID, "importedVersion", { scope: "world", config: false, type: String, default: "" });

  game.settings.register(ID, "promptOnUpdate", {
    name: "Prompt to update imported content",
    hint: "When the module updates, ask the GM whether to update the actors and GM Guide already imported into this world.",
    scope: "world", config: true, type: Boolean, default: true
  });
  game.settings.register(ID, "covenSync", {
    name: "Share coven spell uses",
    hint: "When one hag casts a coven spell, spend that spell's daily use on all three hags (Shared Spellcasting).",
    scope: "world", config: true, type: Boolean, default: true
  });
  game.settings.register(ID, "covenRange", {
    name: "Enforce coven range",
    hint: `Block a coven spell unless Grandma, Auntie and Gaga all have tokens on the current scene within ${COVEN_RANGE} ft of each other.`,
    scope: "world", config: true, type: Boolean, default: true
  });

  game.settings.registerMenu(ID, "manager", {
    name: "Coven Manager",
    label: "Open Coven Manager",
    hint: "Import, update, rebuild or remove the Yagha Coven War Host content in this world.",
    icon: "fa-solid fa-hat-wizard",
    type: buildManagerClass(),
    restricted: true
  });
});

Hooks.once("ready", async () => {
  const module = game.modules.get(ID);
  module.api = { importAll, updateInPlace, removeImported, rebuild, isImported, openManager, status };
  if (!game.user.isGM) return;
  for (const p of [ACTOR_PACK, JOURNAL_PACK, SPELL_PACK]) {
    if (!game.packs.get(p)) console.error(`${ID} | compendium ${p} not found — module install is incomplete.`);
  }
  if (game.users.activeGM && game.users.activeGM !== game.user) return;

  const DialogV2 = foundry.applications.api.DialogV2;
  // First run: offer import.
  if (!isImported() && !game.settings.get(ID, "promptShown")) {
    const yes = await DialogV2.confirm({
      window: { title: TITLE },
      content: `<p>Import the <strong>24 Yagha Coven stat blocks</strong> and the <strong>GM Guide</strong> into this world?</p>
        <p>You can do this any time from <strong>Game Settings → Configure Settings → ${TITLE} → Open Coven Manager</strong>.</p>`,
      rejectClose: false
    });
    await game.settings.set(ID, "promptShown", true);
    if (yes) await importAll();
    return;
  }
  // Module updated since the content was imported: offer an in-place update.
  const imported = game.settings.get(ID, "importedVersion") || "0.0.0";
  if (isImported() && isNewer(moduleVersion(), imported) && game.settings.get(ID, "promptOnUpdate")) {
    const choice = await DialogV2.wait({
      window: { title: `${TITLE} — update available` },
      content: `<p>This world has the Yagha Coven content from <strong>v${imported === "0.0.0" ? "?" : imported}</strong>; the module is now <strong>v${moduleVersion()}</strong>.</p>
        <p><strong>Update in place</strong> refreshes stats, spells, art and the GM Guide on the existing actors, keeps their IDs, folders and
        ownership, and updates the images of tokens already placed on scenes.</p>`,
      buttons: [
        { action: "update", label: "Update in place", icon: "fa-solid fa-rotate", default: true },
        { action: "manager", label: "Open Coven Manager", icon: "fa-solid fa-hat-wizard" },
        { action: "later", label: "Later", icon: "fa-solid fa-clock" }
      ],
      rejectClose: false
    });
    if (choice === "update") await updateInPlace();
    else if (choice === "manager") openManager();
  }
});

/* ------------------------------------------------------------------ helpers */
function fromModule(doc) {
  const src = doc._stats?.compendiumSource ?? "";
  return doc.getFlag(ID, "generated") || src.startsWith(`Compendium.${ACTOR_PACK}`) || src.startsWith(`Compendium.${JOURNAL_PACK}`);
}
const worldActors = () => game.actors.filter(fromModule);
const worldJournals = () => game.journal.filter(fromModule);
function isImported() { return worldActors().length > 0; }

function status() {
  return {
    moduleVersion: moduleVersion(),
    importedVersion: game.settings.get(ID, "importedVersion") || (isImported() ? "unknown (pre-1.3)" : "—"),
    worldActors: worldActors().length,
    worldJournals: worldJournals().length,
    packActors: game.packs.get(ACTOR_PACK)?.index.size ?? 0,
    packSpells: game.packs.get(SPELL_PACK)?.index.size ?? 0
  };
}

async function rootFolder(type) {
  return game.folders.find(f => f.type === type && f.name === ROOT_FOLDER && !f.folder)
    ?? Folder.create({ name: ROOT_FOLDER, type, color: "#4b2a5c" });
}

async function worldFolderFor(packDoc, type) {
  const root = await rootFolder(type);
  const name = packDoc.folder?.name;
  if (!name) return root.id;
  const f = game.folders.find(x => x.type === type && x.name === name && x.folder?.id === root.id)
    ?? await Folder.create({ name, type, folder: root.id, color: packDoc.folder.color });
  return f.id;
}

/* ------------------------------------------------------------------ import / update / remove */
async function importAll() {
  if (!game.user.isGM) return ui.notifications.warn("Only a GM can import the Yagha Coven War Host.");
  if (isImported()) {
    ui.notifications.info("Already imported — use Update in place or Rebuild in the Coven Manager.");
    return;
  }
  const actors = game.packs.get(ACTOR_PACK);
  const journal = game.packs.get(JOURNAL_PACK);
  if (!actors || !journal) return ui.notifications.error("Yagha Coven War Host compendiums are missing — reinstall the module.");
  try {
    const imported = await actors.importAll({ folderName: ROOT_FOLDER, keepId: true });
    await journal.importAll({ folderName: ROOT_FOLDER, keepId: true });
    await game.settings.set(ID, "imported", true);
    await game.settings.set(ID, "importedVersion", moduleVersion());
    ui.notifications.info(`Yagha Coven War Host: ${imported?.length ?? "all"} actors and the GM Guide imported.`);
  } catch (err) {
    console.error(`${ID} | import failed`, err);
    ui.notifications.error("Yagha Coven War Host import failed — see the console (F12).");
  }
}

async function updateInPlace() {
  if (!game.user.isGM) return;
  const pack = game.packs.get(ACTOR_PACK);
  const jpack = game.packs.get(JOURNAL_PACK);
  if (!pack || !jpack) return ui.notifications.error("Yagha Coven War Host compendiums are missing — reinstall the module.");
  const notice = ui.notifications.info("Updating the Yagha Coven War Host…", { permanent: true });
  let updated = 0, created = 0, tokens = 0;
  try {
    for (const doc of await pack.getDocuments()) {
      const data = doc.toObject();
      const key = doc.getFlag(ID, "sourceKey");
      const world = game.actors.get(doc.id) ?? game.actors.find(a => a.getFlag(ID, "sourceKey") === key);
      if (!world) {
        const createData = game.actors.fromCompendium(doc, { keepId: true });
        createData.folder = await worldFolderFor(doc, "Actor");
        await Actor.create(createData, { keepId: true });
        created++;
        continue;
      }
      // Replace module-generated items; keep anything the GM added by hand.
      const oldIds = world.items.filter(i => i.getFlag(ID, "generated")).map(i => i.id);
      if (oldIds.length) await world.deleteEmbeddedDocuments("Item", oldIds);
      await world.update({
        name: data.name, img: data.img, system: data.system,
        flags: { [ID]: data.flags[ID] },
        "prototypeToken.name": data.prototypeToken.name,
        "prototypeToken.texture.src": data.prototypeToken.texture.src,
        "prototypeToken.width": data.prototypeToken.width,
        "prototypeToken.height": data.prototypeToken.height
      });
      await world.createEmbeddedDocuments("Item", data.items, { keepId: true });
      updated++;
      // Refresh art on tokens already placed on scenes.
      for (const scene of game.scenes) {
        const ups = scene.tokens.filter(t => t.actorId === world.id && t.texture.src !== data.prototypeToken.texture.src)
          .map(t => ({ _id: t.id, "texture.src": data.prototypeToken.texture.src }));
        if (ups.length) { await scene.updateEmbeddedDocuments("Token", ups); tokens += ups.length; }
      }
    }
    // GM Guide: replace pages.
    for (const jdoc of await jpack.getDocuments()) {
      const world = game.journal.get(jdoc.id) ?? game.journal.find(j => j.name === jdoc.name && fromModule(j));
      const data = jdoc.toObject();
      if (!world) {
        const createData = game.journal.fromCompendium(jdoc, { keepId: true });
        createData.folder = (await rootFolder("JournalEntry")).id;
        await JournalEntry.create(createData, { keepId: true });
        continue;
      }
      await world.deleteEmbeddedDocuments("JournalEntryPage", world.pages.map(p => p.id));
      await world.createEmbeddedDocuments("JournalEntryPage", data.pages, { keepId: true });
      await world.update({ name: data.name, flags: { [ID]: data.flags?.[ID] ?? { generated: true } } });
    }
    await game.settings.set(ID, "imported", true);
    await game.settings.set(ID, "importedVersion", moduleVersion());
    ui.notifications.info(`Yagha Coven War Host updated to v${moduleVersion()}: ${updated} actors updated, ${created} added, ${tokens} placed tokens refreshed.`);
  } catch (err) {
    console.error(`${ID} | update failed`, err);
    ui.notifications.error("Yagha Coven War Host update failed — see the console (F12).");
  } finally {
    if (typeof notice?.remove === "function") notice.remove();
    else ui.notifications.remove?.(notice);
  }
}

async function removeImported() {
  if (!game.user.isGM) return;
  const actors = worldActors();
  const journals = worldJournals();
  if (actors.length) await Actor.deleteDocuments(actors.map(a => a.id));
  if (journals.length) await JournalEntry.deleteDocuments(journals.map(j => j.id));
  for (const root of game.folders.filter(f => f.name === ROOT_FOLDER && ["Actor", "JournalEntry"].includes(f.type))) {
    const subtree = [root, ...root.getSubfolders(true)];
    if (subtree.every(f => f.contents.length === 0)) await Folder.deleteDocuments(subtree.map(f => f.id));
  }
  await game.settings.set(ID, "imported", false);
  await game.settings.set(ID, "importedVersion", "");
  ui.notifications.info("Yagha Coven War Host world content removed (compendiums untouched).");
}

async function rebuild() {
  await removeImported();
  await importAll();
}

/* ------------------------------------------------------------------ Coven Manager window */
let managerClass;
function openManager() {
  const app = foundry.applications.instances?.get?.(`${ID}-manager`);
  if (app) return app.render({ force: true });
  return new managerClass().render({ force: true });
}

function buildManagerClass() {
  const { ApplicationV2, DialogV2 } = foundry.applications.api;
  const confirm = (title, content) => DialogV2.confirm({ window: { title }, content, rejectClose: false });
  managerClass = class HagHostManager extends ApplicationV2 {
    static DEFAULT_OPTIONS = {
      id: `${ID}-manager`,
      tag: "div",
      classes: [`${ID}-manager`],
      window: { title: "Yagha Coven Manager", icon: "fa-solid fa-hat-wizard", resizable: false },
      position: { width: 480, height: "auto" },
      actions: {
        import: async function () { await importAll(); this.render(); },
        update: async function () { await updateInPlace(); this.render(); },
        rebuild: async function () {
          if (await confirm("Rebuild from compendium?", "<p>This <strong>deletes</strong> the imported actors and GM Guide and imports fresh copies. Tokens already placed on scenes will lose their actor link. Prefer <em>Update in place</em> unless something is broken.</p>")) {
            await rebuild(); this.render();
          }
        },
        remove: async function () {
          if (await confirm("Remove imported content?", "<p>Delete the imported Yagha Coven actors and GM Guide from this world? The compendiums are untouched.</p>")) {
            await removeImported(); this.render();
          }
        },
        openActors: () => game.packs.get(ACTOR_PACK)?.render(true),
        openSpells: () => game.packs.get(SPELL_PACK)?.render(true),
        openGuide: async () => {
          const j = worldJournals()[0] ?? (await game.packs.get(JOURNAL_PACK)?.getDocuments())?.[0];
          j?.sheet.render(true);
        },
        settings: () => {
          const SC = foundry.applications?.settings?.SettingsConfig;
          (game.settings.sheet ?? (SC ? new SC() : null))?.render({ force: true });
        }
      }
    };

    async _renderHTML() {
      const s = status();
      const outdated = isImported() && isNewer(s.moduleVersion, game.settings.get(ID, "importedVersion") || "0.0.0");
      const el = document.createElement("section");
      el.style.cssText = "display:flex;flex-direction:column;gap:.6rem;padding:.25rem";
      el.innerHTML = `
        <table style="margin:0">
          <tr><th style="text-align:left">Module version</th><td>v${s.moduleVersion}</td></tr>
          <tr><th style="text-align:left">Imported content</th><td>${s.importedVersion}${outdated ? ' <strong style="color:#c0392b">— update available</strong>' : ""}</td></tr>
          <tr><th style="text-align:left">World actors / journals</th><td>${s.worldActors} / ${s.worldJournals}</td></tr>
          <tr><th style="text-align:left">Compendium actors / spells</th><td>${s.packActors} / ${s.packSpells}</td></tr>
        </table>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.4rem">
          <button type="button" data-action="import" ${isImported() ? "disabled" : ""}><i class="fa-solid fa-file-import"></i> Import into world</button>
          <button type="button" data-action="update" ${isImported() ? "" : "disabled"}><i class="fa-solid fa-rotate"></i> Update in place</button>
          <button type="button" data-action="rebuild" ${isImported() ? "" : "disabled"}><i class="fa-solid fa-hammer"></i> Rebuild (delete &amp; re-import)</button>
          <button type="button" data-action="remove" ${isImported() ? "" : "disabled"}><i class="fa-solid fa-trash"></i> Remove from world</button>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.4rem">
          <button type="button" data-action="openActors"><i class="fa-solid fa-users"></i> Actors</button>
          <button type="button" data-action="openSpells"><i class="fa-solid fa-book-sparkles"></i> Spells</button>
          <button type="button" data-action="openGuide"><i class="fa-solid fa-book-open"></i> GM Guide</button>
        </div>
        <p style="margin:0;font-size:.85em;opacity:.8"><strong>Update in place</strong> refreshes stats, spells, art and the GM Guide on the
        existing actors (same IDs, folders and ownership; items you added yourself are kept) and refreshes art on placed tokens.
        Use it after every module update or amendment.</p>
        <button type="button" data-action="settings"><i class="fa-solid fa-gears"></i> Coven spell settings</button>`;
      return el;
    }

    _replaceHTML(result, content) {
      content.replaceChildren(result);
    }
  };
  return managerClass;
}

/* ------------------------------------------------------------------ shared coven spellcasting */
const covenKey = item => item?.getFlag?.(ID, "coven");

function covenActorsInScope() {
  const linked = game.actors.contents;
  const synthetic = canvas?.scene?.tokens.filter(t => !t.actorLink && t.actor).map(t => t.actor) ?? [];
  return [...linked, ...synthetic];
}

Hooks.on("dnd5e.preUseActivity", (activity) => {
  const item = activity?.item;
  if (!covenKey(item) || !game.settings.get(ID, "covenRange") || !canvas?.ready) return;
  // One token per hag (by sourceKey) on the current scene.
  const byHag = new Map();
  for (const t of canvas.tokens.placeables) {
    const a = t.actor;
    if (!a?.items.some(i => covenKey(i))) continue;
    const k = a.getFlag(ID, "sourceKey") ?? a.name;
    if (!byHag.has(k) || a === activity.actor) byHag.set(k, t);
  }
  const members = [...byHag.values()];
  let ok = members.length >= 3;
  if (ok) {
    for (let i = 0; i < members.length && ok; i++) {
      for (let j = i + 1; j < members.length && ok; j++) {
        const d = canvas.grid.measurePath([members[i].center, members[j].center]).distance;
        if (d > COVEN_RANGE + 0.01) ok = false;
      }
    }
  }
  if (!ok) {
    ui.notifications.warn(`${item.name}: Shared Spellcasting needs Grandma, Auntie and Gaga on this scene within ${COVEN_RANGE} ft of one another. (Disable "Enforce coven range" in the module settings to override.)`);
    return false;
  }
});

Hooks.on("updateItem", async (item, changes, options, userId) => {
  if (userId !== game.user.id || options?.[ID]?.sync) return;
  if (!game.settings.get(ID, "covenSync")) return;
  const key = covenKey(item);
  if (!key || !foundry.utils.hasProperty(changes, "system.uses.spent")) return;
  const spent = item.system.uses.spent;
  for (const actor of covenActorsInScope()) {
    if (actor === item.actor) continue;
    for (const other of actor.items.filter(i => covenKey(i) === key && i.system.uses.spent !== spent)) {
      try { await other.update({ "system.uses.spent": spent }, { [ID]: { sync: true } }); }
      catch (err) { console.warn(`${ID} | could not sync coven spell on ${actor.name}`, err); }
    }
  }
});
