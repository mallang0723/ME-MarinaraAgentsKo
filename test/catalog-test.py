"""Offline catalog/build checks; optional upstream snapshots are local files only."""
import csv
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ROWS = list(csv.DictReader((ROOT / "data/catalog-reviewed.tsv").open(encoding="utf-8"), delimiter="\t"))
EXACT = json.loads((ROOT / "data/exact-translations.json").read_text(encoding="utf-8"))
UI = json.loads((ROOT / "data/ui-translations.json").read_text(encoding="utf-8"))
RETIRED_UI = {"All", "Conversation", "Roleplay", "Game", "Filter agents by supported chat mode",
              "Installed Agents", "Uninstalled Agents", "Writer Agents", "Tracker Agents", "Misc Agents",
              "Agent", "Conversation Game", "Maps", "Agents"}
NEW_IDS = {"2d-avatars", "3d-avatars", "otome-forge", "quartermaster", "relationship-tracker",
           "saucelings", "slurp2", "story-writer"}


class CatalogTests(unittest.TestCase):
    def test_44_complete_unique_packages(self):
        self.assertEqual(len(ROWS), 44)
        self.assertEqual(len({r["id"] for r in ROWS}), 44)
        for row in ROWS:
            with self.subTest(package=row["id"]):
                self.assertTrue(all(row.values()))
                self.assertIn(row["category"], {"writer", "tracker", "misc"})
                self.assertIn(row["confidence"], {"high", "medium"})
                self.assertRegex(row["korean_description"], "[가-힣]")

    def test_migration_and_new_names(self):
        rows = {r["id"]: r for r in ROWS}
        self.assertTrue(NEW_IDS <= rows.keys())
        self.assertNotIn("slurp", rows)
        self.assertEqual(rows["slurp2"]["english_name"], "Slurp")
        self.assertEqual(rows["otome-forge"]["english_name"], "Otome Hearth")
        self.assertNotIn("Otome Forge", EXACT)

    def test_dictionary_covers_only_reviewed_metadata(self):
        expected = {row[f"english_{field}"]: row[f"korean_{field}"]
                    for row in ROWS for field in ("name", "description")}
        self.assertEqual(EXACT, expected)
        self.assertEqual(len(EXACT), 88)
        self.assertEqual(EXACT["Calls"], "통화")  # Still a package name.

    def test_retired_ui_and_single_fallback(self):
        self.assertFalse(RETIRED_UI & EXACT.keys())
        self.assertFalse(RETIRED_UI & UI.keys())
        self.assertEqual(UI, {"Not installed": "설치되지 않음"})

    def test_catalog_summaries_are_separate_from_full_metadata(self):
        script = (ROOT / "extension.js").read_text(encoding="utf-8")
        summaries = json.loads(re.search(r"const CATALOG_EXACT = Object.freeze\((\{.*?\})\);", script, re.S)[1])
        self.assertEqual(len(summaries), 45)
        self.assertEqual(summaries["A co-writing book."], "함께 집필하는 책입니다.")
        self.assertEqual(summaries["Keeps track of your money, gear, and what you're carrying."], "돈, 장비, 소지품을 추적합니다.")
        self.assertNotIn("A co-writing book.", EXACT)
        self.assertTrue(any(key.endswith("…") for key in summaries))

    def build_copy(self, mutate=None):
        with tempfile.TemporaryDirectory(prefix="agents-ko-build-") as directory:
            target = Path(directory)
            (target / "tools").mkdir()
            shutil.copy(ROOT / "tools/build.py", target / "tools/build.py")
            shutil.copytree(ROOT / "data", target / "data")
            if mutate:
                mutate(target / "data/catalog-reviewed.tsv")
            result = subprocess.run([sys.executable, str(target / "tools/build.py")],
                                    capture_output=True, text=True)
            generated = {name: (target / name).read_bytes() for name in
                         ("extension.js", "data/exact-translations.json") if (target / name).exists()}
            return result, generated

    def test_reproducible_build(self):
        result, generated = self.build_copy()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["packages"], 44)
        for name, content in generated.items():
            self.assertEqual(content, (ROOT / name).read_bytes(), name)
        self.assertEqual(len(generated), 2)

    def test_conflicting_translation_rejected(self):
        def mutate(path):
            row = ROWS[0].copy()
            row["korean_name"] = "충돌하는 번역"
            with path.open("a", encoding="utf-8", newline="") as f:
                csv.DictWriter(f, ROWS[0].keys(), delimiter="\t").writerow(row)
        result, _ = self.build_copy(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Conflicting translation", result.stderr)

    def test_missing_translation_rejected(self):
        def mutate(path):
            rows = [r.copy() for r in ROWS]
            rows[0]["korean_description"] = ""
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, ROWS[0].keys(), delimiter="\t")
                writer.writeheader(); writer.writerows(rows)
        result, _ = self.build_copy(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing description", result.stderr)

    @unittest.skipUnless(os.environ.get("OFFICIAL_CATALOG"), "set OFFICIAL_CATALOG to a local JSON snapshot")
    def test_official_catalog_snapshot(self):
        official = json.loads(Path(os.environ["OFFICIAL_CATALOG"]).read_text(encoding="utf-8"))
        expected = {p["manifest"]["id"]: (p["category"], p["manifest"]["name"], p["manifest"]["description"])
                    for p in official["packages"]}
        actual = {r["id"]: (r["category"], r["english_name"], r["english_description"]) for r in ROWS}
        self.assertEqual(actual, expected)

    @unittest.skipUnless(os.environ.get("OFFICIAL_KO"), "set OFFICIAL_KO to a local Korean UI pack")
    def test_official_ui_ownership(self):
        ko = json.loads(Path(os.environ["OFFICIAL_KO"]).read_text(encoding="utf-8"))
        keys = ["ui.agents.agentcatalogview." + suffix for suffix in
                ("allModes", "conversationMode", "roleplayMode", "gameMode", "filterByChatMode",
                 "writerAgents", "trackerAgents", "miscAgents")]
        keys += ["ui.agents.organizer.types.agent", "ui.game.gamesessionhistory.maps", "navigation.topbar.agents"]
        self.assertEqual(len(keys), 11)
        for key in keys:
            self.assertRegex(ko[key], "[가-힣]", key)
        self.assertEqual(ko["ui.agents.organizer.installedTitle"], "설치된 항목")
        self.assertNotIn("ui.agents.organizer.notInstalledTitle", ko)
        self.assertEqual(UI["Not installed"], ko["ui.agents.organizer.statusNotInstalled"])

    @unittest.skipUnless(os.environ.get("MARINARA_REPO"), "set MARINARA_REPO to read-only v2.5.2 source")
    def test_engine_252_selector_and_label_contract(self):
        source = Path(os.environ["MARINARA_REPO"])
        self.assertEqual(json.loads((source / "package.json").read_text())["version"], "2.5.2")
        client = source / "packages/client/src"
        catalog = (client / "components/agents/AgentCatalogView.tsx").read_text()
        detail = (client / "components/agents/FeatureAgentDetailHost.tsx").read_text()
        panel = (client / "components/layout/RightPanel.tsx").read_text()
        self.assertIn('data-component="AgentCatalogView"', catalog)
        self.assertIn('data-component="FeatureAgentDetailHost"', detail)
        self.assertIn('data-component="RightPanel"', panel)
        self.assertIn('data-panel-key={key}', panel)
        self.assertIn('aria-hidden={!active}', panel)
        self.assertIn('agents: AgentsPanel', panel)
        self.assertIn('ui.agents.organizer.installedTitle', catalog)
        self.assertIn('ui.agents.organizer.notInstalledTitle', catalog)
        en = json.loads((client / "localization/locales/en.json").read_text())
        self.assertEqual(en["ui.agents.organizer.installedTitle"], "Installed")
        self.assertEqual(en["ui.agents.organizer.notInstalledTitle"], "Not installed")
        for obsolete in ("Installed Agents", "Uninstalled Agents", "Conversation Game"):
            self.assertNotIn(obsolete, en.values())

    @unittest.skipUnless(os.environ.get("MARINARA_REPO"), "set MARINARA_REPO to read-only v2.5.2 source")
    def test_all_summaries_match_engine_tagline_function(self):
        model = Path(os.environ["MARINARA_REPO"]) / "packages/client/src/components/agents/organizer/organizer-model.ts"
        body = re.search(r"export function taglineOf\([^\n]+\{\n(.*?)\n\}", model.read_text(), re.S)[1]
        # Execute only the pure function body from the reference source, without imports or network.
        runner = """const fs = require('node:fs');
const {body, rows} = JSON.parse(fs.readFileSync(0, 'utf8'));
const tagline = new Function('entry', 'description', body);
process.stdout.write(JSON.stringify(rows.map(r => [tagline({}, r.english_description), tagline({}, r.korean_description)])));
"""
        result = subprocess.run(["node", "-e", runner], input=json.dumps({"body": body, "rows": ROWS}),
                                capture_output=True, text=True, check=True)
        script = (ROOT / "extension.js").read_text(encoding="utf-8")
        summaries = json.loads(re.search(r"const CATALOG_EXACT = Object.freeze\((\{.*?\})\);", script, re.S)[1])
        for english, korean in json.loads(result.stdout):
            self.assertEqual(summaries[english], korean, english)


if __name__ == "__main__":
    unittest.main(verbosity=2)
