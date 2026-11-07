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


catalog_dictionary = {}
for row in rows:
    if ":" in row["id"]:
        continue
    english = organizer_tagline(row["english_description"])
    korean = organizer_tagline(row["korean_description"])
    if english in catalog_dictionary and catalog_dictionary[english] != korean:
        raise ValueError(f"Conflicting catalog summary: {english}")
    catalog_dictionary[english] = korean

template = r'''(() => {
  "use strict";

  const EXACT = Object.freeze(__DICTIONARY__);
  const CATALOG_EXACT = Object.freeze(__CATALOG_DICTIONARY__);
  const UI_EXACT = Object.freeze(__UI_DICTIONARY__);
  const NAMES = Object.freeze(__NAMES__);
  const MODAL_TITLES = new Set(__MODAL_TITLES__);
  const ROOT_SELECTOR = __ROOT_SELECTOR__;
  const SECTION_SELECTOR = __SECTION_SELECTOR__;
  const EXCLUDE = 'script, style, input, textarea, [contenteditable]:not([contenteditable="false"]), [data-chat-message-editor], .prose';
  const ownedContainers = new WeakSet();
  const ledger = new Map();
  const attributeLedger = new Map();
  let observer = null;
  let languageObserver = null;
  let stopped = false;

  function isKorean() {
    return /^ko(?:-|$)/i.test(document.documentElement.lang || "");
  }

  function eligible(element) {
    if (!element || element.closest(EXCLUDE)) return false;
    const root = element.closest(ROOT_SELECTOR);
    if (root?.matches('[data-component="Modal"]')) return MODAL_TITLES.has(root.getAttribute("aria-label"));
    return root;
  }

  function lookup(dictionary, key) {
    return Object.hasOwn(dictionary, key) ? dictionary[key] : null;
  }

  function translation(current, element) {
    const core = current.trim();
    // UI labels belong to the locale pack except this hardcoded drawer array.
    let value = lookup(EXACT, core) || lookup(CATALOG_EXACT, core) ||
      (element.closest(SECTION_SELECTOR) ? lookup(UI_EXACT, core) : null);
    // OrganizerHome joins package names for update/kit summaries (118, 156).
    // Every complete name must be reviewed; never replace an arbitrary substring.
    if (!value && element.closest('[data-component="AgentCatalogView"]')) {
      const updates = core.split(" · ").map(part => {
        const match = part.match(/^(.*?) (\d+\.\d+\.\d+(?:[-+][\w.+-]+)?)$/);
        return match && lookup(NAMES, match[1]) ? `${lookup(NAMES, match[1])} ${match[2]}` : null;
      });
      if (updates.every(Boolean)) value = updates.join(" · ");
      else if (core.includes(", ")) {
        const names = core.split(", ").map(name => lookup(NAMES, name));
        if (names.every(Boolean)) value = names.join(", ");
      }
    }
    return value && value !== core ? current.replace(core, () => value) : null;
  }

  function markOwned(element) {
    for (; element && element !== document.body; element = element.parentElement) ownedContainers.add(element);
  }

  function replaceText(node, value) {
    if (node.nodeValue === value) return;
    const previous = ledger.get(node);
    if (!previous || node.nodeValue !== previous.translated) {
      ledger.set(node, { original: node.nodeValue, translated: value });
    } else previous.translated = value;
    markOwned(node.parentElement);
    node.nodeValue = value;
  }

  function translateText(node) {
    const element = node.parentElement;
    if (!eligible(element)) return;
    // Omnibar highlights split a single metadata string across text/mark nodes.
    // Retain all React-owned nodes so subsequent reconciliation and cleanup work.
    const label = element.tagName === "MARK" ? element.parentElement : element;
    if (label && label.children.length && [...label.children].every(child => child.tagName === "MARK")) {
      const value = translation(label.textContent, label);
      if (value) {
        const walker = document.createTreeWalker(label, NodeFilter.SHOW_TEXT);
        let first = true;
        for (let text = walker.nextNode(); text; text = walker.nextNode()) {
          replaceText(text, first ? value : "");
          first = false;
        }
        return;
      }
    }
    const value = translation(node.nodeValue, element);
    if (value) replaceText(node, value);
  }

  function translateAttributes(element) {
    if (!eligible(element)) return;
    for (const attribute of ["aria-label", "title", "alt", "placeholder"]) {
      const current = element.getAttribute(attribute);
      const value = current ? translation(current, element) : null;
      if (!value) continue;
      let records = attributeLedger.get(element);
      if (!records) attributeLedger.set(element, records = new Map());
      const previous = records.get(attribute);
      if (!previous || current !== previous.translated) records.set(attribute, { original: current, translated: value });
      else previous.translated = value;
      markOwned(element);
      element.setAttribute(attribute, value);
    }
  }

  function translateTree(root) {
    if (!root.isConnected) return;
    if (root.nodeType === Node.TEXT_NODE) return translateText(root);
    if (root.nodeType !== Node.ELEMENT_NODE || root.closest(EXCLUDE)) return;
    translateAttributes(root);
    root.querySelectorAll("[aria-label], [title], [alt], [placeholder]").forEach(translateAttributes);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: node => node.parentElement.closest(EXCLUDE) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
    });
    for (let node = walker.nextNode(); node; node = walker.nextNode()) translateText(node);
  }

  function discover(node) {
    if (!node.isConnected) return;
    if (node.nodeType === Node.TEXT_NODE) return translateText(node);
    if (node.nodeType !== Node.ELEMENT_NODE || node.closest(EXCLUDE)) return;
    if (eligible(node)) translateTree(node);
    else node.querySelectorAll(ROOT_SELECTOR).forEach(translateTree);
  }

  function restore(records, attributes = false) {
    for (const [node, entry] of records) {
      if (attributes) {
        for (const [attribute, value] of entry) {
          if (node.getAttribute(attribute) === value.translated) node.setAttribute(attribute, value.original);
        }
      } else if (node.nodeValue === entry.translated) node.nodeValue = entry.original;
    }
    records.clear();
  }

  function revertAll() {
    restore(ledger);
    restore(attributeLedger, true);
  }

  function prune() {
    // Release detached nodes; restore before React can reuse them elsewhere.
    for (const [node, entry] of ledger) if (!node.isConnected || !eligible(node.parentElement)) {
      if (node.nodeValue === entry.translated) node.nodeValue = entry.original;
      ledger.delete(node);
    }
    for (const [node, entries] of attributeLedger) if (!node.isConnected || !eligible(node)) {
      for (const [attribute, entry] of entries) if (node.getAttribute(attribute) === entry.translated) node.setAttribute(attribute, entry.original);
      attributeLedger.delete(node);
    }
  }

  function onMutations(mutations) {
    if (stopped || !isKorean()) return;
    const pending = new Set();
    let removed = false;
    let scopeChanged = false;
    for (const mutation of mutations) {
      if (mutation.type === "attributes") {
        const changesScope = !["aria-label", "title", "alt", "placeholder"].includes(mutation.attributeName) ||
          (mutation.attributeName === "aria-label" && mutation.target.matches('[data-component="Modal"]'));
        scopeChanged ||= changesScope && ownedContainers.has(mutation.target);
        if (!changesScope) { translateAttributes(mutation.target); continue; }
      }
      if (mutation.type === "childList") {
        if ([...mutation.removedNodes].some(node => ledger.has(node) || ownedContainers.has(node))) removed = true;
        for (const node of mutation.addedNodes) pending.add(node);
        // Removing/replacing a search highlight may change the aggregate label.
        if (eligible(mutation.target) && [...mutation.target.childNodes].every(node =>
          node.nodeType === Node.TEXT_NODE || node.nodeName === "MARK")) pending.add(mutation.target);
      } else if (mutation.type === "characterData" || eligible(mutation.target) ||
        (mutation.attributeName === "data-component" &&
          ["RightPanel", "HomeBrowserHub"].includes(mutation.target.getAttribute("data-component")))) {
        pending.add(mutation.target);
      }
    }
    if (removed || scopeChanged) prune();
    for (const node of pending) {
      let covered = false;
      for (let parent = node.parentNode; parent; parent = parent.parentNode) {
        if (pending.has(parent)) { covered = true; break; }
      }
      if (!covered) discover(node);
    }
    // Drop only our synchronous writes; no observer loop or animation-frame delay.
    observer.takeRecords();
  }

  function start() {
    if (stopped || observer || !document.body) return;
    observer = new MutationObserver(onMutations);
    observer.observe(document.body, {
      childList: true, subtree: true, characterData: true, attributes: true,
      attributeFilter: ["aria-label", "title", "alt", "placeholder", "aria-hidden", "data-panel-key",
        "data-component", "data-drawer", "data-chat-settings-section", "data-chat-control-window",
        "data-result-id", "data-chat-agent-entry", "id"],
    });
    languageObserver = new MutationObserver(() => {
      if (stopped) return;
      if (isKorean()) document.querySelectorAll(ROOT_SELECTOR).forEach(translateTree);
      else revertAll();
      observer.takeRecords();
    });
    languageObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    if (isKorean()) document.querySelectorAll(ROOT_SELECTOR).forEach(translateTree);
    observer.takeRecords();
  }

  function cleanup() {
    if (stopped) return;
    stopped = true;
    observer?.disconnect();
    languageObserver?.disconnect();
    document.removeEventListener("DOMContentLoaded", start);
    revertAll();
  }

  marinara.onCleanup(cleanup);
  if (document.body) start();
  else document.addEventListener("DOMContentLoaded", start, { once: true });
})();
'''
surfaces = json.loads((root / "data/surfaces.json").read_text())
serialized = json.dumps(dictionary, ensure_ascii=False, indent=2)
output = template.replace("__DICTIONARY__", serialized).replace(
    "__CATALOG_DICTIONARY__", json.dumps(catalog_dictionary, ensure_ascii=False, indent=2)
)
modal_titles = {"Agent Suite", "에이전트 모음", "Start a game", "게임 시작", "Review Character Card Updates", "캐릭터 카드 업데이트 검토"}
for row in rows:
    for name in (row["english_name"], row["korean_name"]):
        modal_titles.update((name, "Add " + name, name + " 추가"))
output = output.replace("__NAMES__", json.dumps({r["english_name"]: r["korean_name"] for r in rows}, ensure_ascii=False))
output = output.replace("__MODAL_TITLES__", json.dumps(sorted(modal_titles), ensure_ascii=False))
output = output.replace("__UI_DICTIONARY__", json.dumps(ui_dictionary, ensure_ascii=False, indent=2)).replace(
    "__ROOT_SELECTOR__", json.dumps(", ".join(surfaces["metadata"]))).replace(
    "__SECTION_SELECTOR__", json.dumps(", ".join(surfaces["sections"])))
(root / "data" / "exact-translations.json").write_text(serialized + "\n", encoding="utf-8")
(root / "extension.js").write_text(output, encoding="utf-8")
print(json.dumps({"packages": sum(":" not in r["id"] for r in rows), "rows": len(rows), "entries": len(dictionary), "catalog_entries": len(catalog_dictionary), "ui_entries": len(ui_dictionary), "bytes": len(output.encode())}))
