from __future__ import annotations

import csv
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with (root / "data" / "catalog-reviewed.tsv").open(encoding="utf-8", newline="") as source:
    rows = list(csv.DictReader(source, delimiter="\t"))
dictionary = {}
for row in rows:
    for field in ("name", "description"):
        english, korean = row[f"english_{field}"], row[f"korean_{field}"]
        if not english or not korean:
            raise ValueError(f"Missing {field}: {row['id']}")
        if english in dictionary and dictionary[english] != korean:
            raise ValueError(f"Conflicting translation: {english}")
        dictionary[english] = korean
ui_dictionary = json.loads((root / "data" / "ui-translations.json").read_text(encoding="utf-8"))


def organizer_tagline(description):
    # v2.5.2 organizer-model.ts:50: first sentence, at most 90 UTF-16 code units.
    sentence = re.split(r"(?<=\.)\s", description, maxsplit=1)[0]
    encoded = sentence.encode("utf-16-le")
    return encoded[:178].decode("utf-16-le", errors="surrogatepass") + "…" if len(encoded) > 180 else sentence


catalog_dictionary = dict(ui_dictionary)
for row in rows:
    english = organizer_tagline(row["english_description"])
    korean = organizer_tagline(row["korean_description"])
    if english in catalog_dictionary and catalog_dictionary[english] != korean:
        raise ValueError(f"Conflicting catalog summary: {english}")
    catalog_dictionary[english] = korean

template = r'''(() => {
  "use strict";

  const EXACT = Object.freeze(__DICTIONARY__);
  const CATALOG_EXACT = Object.freeze(__CATALOG_DICTIONARY__);
  const CATALOG_SELECTOR = '[data-component="AgentCatalogView"]';
  const ROOT_SELECTOR = `${CATALOG_SELECTOR}, [data-component="FeatureAgentDetailHost"], [data-component="RightPanel"] [data-panel-key="agents"]:not([aria-hidden="true"])`;
  const ledger = new Map();
  const attributeLedger = new Map();
  let bodyObserver = null;
  let languageObserver = null;
  let scheduled = false;
  let applying = false;
  let stopped = false;

  function isKorean() {
    const locale = String(document.documentElement.lang || "").toLowerCase();
    return locale === "ko" || locale.startsWith("ko-");
  }

  function replaceText(node, translated) {
    const current = node.nodeValue;
    const previous = ledger.get(node);
    if (!previous || current !== previous.translated) {
      ledger.set(node, { original: current, translated });
    }
    node.nodeValue = translated;
  }

  function translateTextNode(node) {
    if (!node.parentElement) return;
    if (node.parentElement.closest('script, style, input, textarea, [contenteditable="true"]')) return;
    const current = node.nodeValue;
    const leading = current.match(/^\s*/u)?.[0] ?? "";
    const trailing = current.match(/\s*$/u)?.[0] ?? "";
    const core = current.slice(leading.length, current.length - trailing.length);
    const translated = EXACT[core] || (node.parentElement.closest(CATALOG_SELECTOR) ? CATALOG_EXACT[core] : null);
    if (!translated || translated === core) return;
    replaceText(node, `${leading}${translated}${trailing}`);
  }

  function translateAttributes(element) {
    for (const attribute of ["aria-label", "title", "placeholder"]) {
      const current = element.getAttribute(attribute);
      const translated = current ? EXACT[current] : null;
      if (!translated || translated === current) continue;
      let records = attributeLedger.get(element);
      if (!records) {
        records = new Map();
        attributeLedger.set(element, records);
      }
      const previous = records.get(attribute);
      if (!previous || current !== previous.translated) {
        records.set(attribute, { original: current, translated });
      }
      element.setAttribute(attribute, translated);
    }
  }

  function translateRoot(rootNode) {
    if (rootNode.nodeType === Node.ELEMENT_NODE) translateAttributes(rootNode);
    rootNode.querySelectorAll?.("[aria-label], [title], [placeholder]").forEach(translateAttributes);
    const walker = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      translateTextNode(node);
    }
  }

  function revertAll() {
    applying = true;
    try {
      for (const [node, entry] of ledger) {
        if (node.isConnected && node.nodeValue === entry.translated) {
          node.nodeValue = entry.original;
        }
      }
      ledger.clear();
      for (const [element, records] of attributeLedger) {
        if (!element.isConnected) continue;
        for (const [attribute, entry] of records) {
          if (element.getAttribute(attribute) === entry.translated) {
            element.setAttribute(attribute, entry.original);
          }
        }
      }
      attributeLedger.clear();
    } finally {
      applying = false;
    }
  }

  function scan() {
    if (stopped) return;
    if (!isKorean()) {
      revertAll();
      return;
    }
    applying = true;
    try {
      document.querySelectorAll(ROOT_SELECTOR).forEach(translateRoot);
    } finally {
      applying = false;
    }
  }

  function schedule() {
    if (stopped || applying || scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      scan();
    });
  }

  function start() {
    if (stopped || bodyObserver || !document.body) return;
    bodyObserver = new MutationObserver(schedule);
    bodyObserver.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ["aria-label", "title", "placeholder", "aria-hidden", "data-panel-key"],
    });
    languageObserver = new MutationObserver(schedule);
    languageObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    scan();
  }

  function cleanup() {
    if (stopped) return;
    stopped = true;
    bodyObserver?.disconnect();
    languageObserver?.disconnect();
    bodyObserver = null;
    languageObserver = null;
    revertAll();
  }

  marinara.onCleanup(cleanup);
  if (document.body) start();
  else document.addEventListener("DOMContentLoaded", start, { once: true });
})();
'''
serialized = json.dumps(dictionary, ensure_ascii=False, indent=2)
output = template.replace("__DICTIONARY__", serialized).replace(
    "__CATALOG_DICTIONARY__", json.dumps(catalog_dictionary, ensure_ascii=False, indent=2)
)
(root / "data" / "exact-translations.json").write_text(serialized + "\n", encoding="utf-8")
(root / "extension.js").write_text(output, encoding="utf-8")
print(json.dumps({"packages": len(rows), "entries": len(dictionary), "catalog_entries": len(catalog_dictionary), "ui_entries": len(ui_dictionary), "bytes": len(output.encode())}))
