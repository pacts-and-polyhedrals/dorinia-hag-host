// usage: node render.mjs <jobs.json>   jobs: [{svg, png, size}]
import { createRequire } from "module";
const require = createRequire("/opt/npm-tools/node_modules/");
const { chromium } = require("playwright");
import fs from "fs";
const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch();
const page = await browser.newPage();
for (const j of jobs) {
  await page.setViewportSize({ width: j.size, height: j.size });
  const svg = fs.readFileSync(j.svg, "utf8");
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace("<svg ", `<svg width="${j.size}" height="${j.size}" `)}</body></html>`);
  await page.screenshot({ path: j.png, omitBackground: true, clip: { x: 0, y: 0, width: j.size, height: j.size } });
}
await browser.close();
