const assert = require("node:assert/strict");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { createRequire } = require("node:module");
const fs = require("node:fs");

// Use an explicitly selected dependency installation, or this repo's local one.
const repoRequire = createRequire(path.join(
  process.env.MARINARA_REPO ? path.resolve(process.env.MARINARA_REPO) : path.resolve(__dirname, ".."),
  "package.json",
));
const { chromium } = repoRequire("@playwright/test");
const tagline = (description) => {
  const sentence = description.split(/(?<=\.)\s/)[0] ?? "";
  return sentence.length > 90 ? `${sentence.slice(0, 89)}…` : sentence;
};
const catalogRows = fs.readFileSync(path.resolve(__dirname, "../data/catalog-reviewed.tsv"), "utf8")
  .trim().split("\n").slice(1).map((line) => {
    const fields = line.split("\t");
    return { id: fields[0], englishName: fields[2], koreanName: fields[3],
      englishDescription: fields[4], koreanDescription: fields[5],
      englishSummary: tagline(fields[4]), koreanSummary: tagline(fields[5]) };
  });
const retiredLabels = ["All", "Conversation", "Roleplay", "Game", "Filter agents by supported chat mode",
  "Installed Agents", "Uninstalled Agents", "Writer Agents", "Tracker Agents", "Misc Agents",
  "Agent", "Conversation Game", "Maps", "Agents"];

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium" });
  let checks = 0;
  const equal = (actual, expected, message) => { assert.deepEqual(actual, expected, message); checks++; };
  try {
    const context = await browser.newContext({ offline: true, serviceWorkers: "block" });
    const externalRequests = [];
    await context.route(/^https?:/, (route) => { externalRequests.push(route.request().url()); return route.abort(); });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.addInitScript(() => { window.marinara = { onCleanup(callback) { window.__agentsKoCleanup = callback; } }; });
    await page.goto(pathToFileURL(path.join(__dirname, "fixture.html")).href);
    await page.evaluate(({ rows, labels }) => {
      const roots = [
        [document.querySelector('[data-component="AgentCatalogView"]'), "catalog"],
        [document.querySelector('[data-panel-key="agents"]'), "panel"],
        [document.querySelector('[data-component="FeatureAgentDetailHost"]'), "detail"],
      ];
      for (const row of rows) for (const [root, suffix] of roots) {
        const card = document.createElement("article");
        card.dataset.testPackage = `${row.id}-${suffix}`;
        const name = document.createElement("strong"); name.textContent = row.englishName;
        const description = document.createElement("p"); description.textContent = row.englishDescription;
        card.append(name, description);
        if (suffix === "catalog") {
          const summary = document.createElement("small"); summary.textContent = row.englishSummary; card.append(summary);
        }
        root.appendChild(card);
      }
      for (const label of labels) {
        const node = document.createElement("span"); node.textContent = label;
        document.querySelector("#official-english").appendChild(node);
      }
    }, { rows: catalogRows, labels: retiredLabels });
    await page.addScriptTag({ path: path.resolve(__dirname, "../extension.js") });
    await page.waitForFunction(() => document.querySelector("#not-installed").textContent === "설치되지 않음");
    equal(catalogRows.length, 44, "44 official packages");
    const checkPackages = async (korean) => {
      for (const row of catalogRows) for (const suffix of ["catalog", "panel", "detail"]) {
        const card = `[data-test-package="${row.id}-${suffix}"]`;
        equal(await page.textContent(`${card} strong`), korean ? row.koreanName : row.englishName, `${row.id} ${suffix} name`);
        equal(await page.textContent(`${card} p`), korean ? row.koreanDescription : row.englishDescription, `${row.id} ${suffix} description`);
        if (suffix === "catalog") equal(await page.textContent(`${card} small`), korean ? row.koreanSummary : row.englishSummary, `${row.id} summary`);
      }
    };
    await checkPackages(true);
    equal(await page.locator("#official-english span").allTextContents(), retiredLabels, "all 14 old UI overrides retired");
    for (const [selector, expected] of [
      ["#installed", "설치된 항목"], ["#official-writer", "작성 에이전트"], ["#panel-title", "에이전트"],
      ["#detail-ui", "Not installed"], ["#outside-ui", "Not installed"], ["#outside", "Inventory Tracker"],
      ["#other-panel", "Inventory Tracker"], ["#hidden-agent", "Inventory Tracker"],
      ["#textarea", "Inventory Tracker"], ["#editable", "Inventory Tracker"], ["#script", "Inventory Tracker"],
      ["#style", "/* Inventory Tracker */"], ["#unknown", "A new, unreviewed description."],
    ]) equal(await page.textContent(selector), expected, selector);
    equal(await page.inputValue("#input"), "Inventory Tracker", "input unchanged");
    equal(await page.getAttribute("#mode-filter", "aria-label"), "지원되는 채팅 모드로 에이전트 필터링", "official attribute unchanged");
    for (const attr of ["title", "aria-label"]) equal(await page.getAttribute("#metadata-attribute", attr), "인벤토리 트래커", attr);

    await page.evaluate(() => document.querySelector("#hidden-panel").setAttribute("aria-hidden", "false"));
    await page.waitForFunction(() => document.querySelector("#hidden-agent").textContent === "인벤토리 트래커");
    equal(await page.textContent("#hidden-agent"), "인벤토리 트래커", "panel activation triggers translation");
    await page.evaluate(() => {
      const node = document.createElement("h3"); node.id = "dynamic"; node.textContent = "  Relationship Tracker  ";
      document.querySelector('[data-component="AgentCatalogView"]').appendChild(node);
    });
    await page.waitForFunction(() => document.querySelector("#dynamic").textContent === "  관계 추적기  ");
    equal(await page.textContent("#dynamic"), "  관계 추적기  ", "SPA rerender and whitespace");

    await page.evaluate(() => { document.documentElement.lang = "en"; });
    await page.waitForFunction(() => document.querySelector("#not-installed").textContent === "Not installed");
    await checkPackages(false);
    equal(await page.getAttribute("#metadata-attribute", "title"), "Inventory Tracker", "attribute reversion");
    equal(await page.textContent("#installed"), "설치된 항목", "official text survives reversion");
    await page.evaluate(() => { document.documentElement.lang = "ko-KR"; });
    await page.waitForFunction(() => document.querySelector("#not-installed").textContent === "설치되지 않음");
    await checkPackages(true);

    // A late official translation and an application edit belong to the app, not our ledger.
    await page.evaluate(() => {
      document.querySelector("#not-installed").textContent = "미설치 항목";
      document.querySelector("#metadata-attribute").setAttribute("title", "앱에서 수정한 제목");
      window.__agentsKoCleanup(); window.__agentsKoCleanup();
    });
    await checkPackages(false);
    equal(await page.textContent("#not-installed"), "미설치 항목", "cleanup preserves official update");
    equal(await page.getAttribute("#metadata-attribute", "title"), "앱에서 수정한 제목", "cleanup preserves app edits");
    equal(await page.getAttribute("#metadata-attribute", "aria-label"), "Inventory Tracker", "cleanup restores owned attribute");
    await page.evaluate(() => { document.querySelector("#dynamic").textContent = "Quest Tracker"; });
    await page.waitForTimeout(50);
    equal(await page.textContent("#dynamic"), "Quest Tracker", "cleanup disconnects observers");
    equal(errors, [], "no browser errors");
    equal(externalRequests, [], "no external network requests");
    console.log(`PASS agents-ko-overlay: ${checks} assertions; 44 packages × 3 surfaces = 132 name/description pairs, plus 44 summaries`);
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
