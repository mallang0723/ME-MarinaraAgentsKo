// Offline DOM regression suite. Set TEST_DEPS to an installation containing linkedom.
// This exercises MutationObserver and real CSS selectors, not rendering/paint timing.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { createRequire } = require('node:module');
const dependency = createRequire(path.resolve(process.env.TEST_DEPS || '.', 'package.json'));
const { parseHTML } = dependency('linkedom');
const base = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(base, 'extension.js'), 'utf8');
const exact = JSON.parse(fs.readFileSync(path.join(base, 'data/exact-translations.json')));
const ui = JSON.parse(fs.readFileSync(path.join(base, 'data/ui-translations.json')));
const surfaces = JSON.parse(fs.readFileSync(path.join(base, 'data/surfaces.json')));
const fixtures = require('./surface-fixtures.json');
let checks = 0;
function equal(actual, expected, message) { assert.deepEqual(actual, expected, message); checks++; }
const settle = () => new Promise(resolve => setTimeout(resolve, 0));
(async () => {
  const { window, document } = parseHTML('<!doctype html><html lang="ko"><body></body></html>');
  window.NodeFilter = { SHOW_TEXT: 4, FILTER_ACCEPT: 1, FILTER_REJECT: 2 };
  let cleanup;
  window.marinara = { onCleanup(fn) { cleanup = fn; } };
  const roots = [];
  equal(fixtures.length, surfaces.metadata.length, 'fixture for every registered selector');
  fixtures.forEach((html, i) => {
    const host = document.createElement('section'); host.innerHTML = html; document.body.append(host);
    const root = host.querySelector(surfaces.metadata[i]); assert.ok(root, surfaces.metadata[i]);
    roots.push(root);
    for (const [english] of Object.entries(exact)) {
      const node = document.createElement(root.tagName === 'SELECT' ? 'option' : 'span');
      node.textContent = english; node.setAttribute('title', english); root.append(node);
    }
    for (const [english] of Object.entries(ui)) { const node = document.createElement('p'); node.textContent = english; root.append(node); }
  });
  const outside = document.createElement('div'); outside.innerHTML = '<div data-chat-scroll><p>Character Tracker</p></div><div data-component="Modal" aria-label="Edit character"><p>Character Tracker</p></div><li data-command-center-result-row data-result-id="character:one">Character Tracker</li>';
  document.body.append(outside); const originalOutside = outside.innerHTML;
  const edit = document.createElement('div'); edit.innerHTML = '<textarea title="Character Tracker">Character Tracker</textarea><div contenteditable="plaintext-only">Character Tracker</div><script type="text/plain">Character Tracker</script><p class="prose">Character Tracker</p><p>Attach lorebook for the specific agent</p><p>Not installed</p><p>constructor</p><p>__proto__</p>';
  roots[3].append(edit); const originalEdit = edit.innerHTML;
  let globalQueries = 0;
  const queryAll = document.querySelectorAll.bind(document);
  document.querySelectorAll = (...args) => { globalQueries++; return queryAll(...args); };
  vm.runInContext(script, vm.createContext(window));
  await settle();
  const checkRoots = korean => roots.forEach((root, i) => {
    const nodes = [...root.children].filter(node => node.hasAttribute('title'));
    Object.entries(exact).forEach(([english, translated], index) => {
      equal(nodes[index].textContent, korean ? translated : english, `surface ${i} ${english}`);
      equal(nodes[index].getAttribute('title'), korean ? translated : english, 'attribute');
    });
    const nodesUI = [...root.children].filter(node => node.tagName === 'P');
    Object.entries(ui).forEach(([english, translated], index) => equal(nodesUI[index].textContent,
      korean && i >= 3 && i <= 5 ? translated : english, 'section dictionary is scoped'));
  });
  checkRoots(true);
  equal(outside.innerHTML, originalOutside, 'chat, character search and unrelated modal untouched');
  equal(edit.innerHTML, originalEdit, 'editable, code, prose and real i18n keys untouched');
  globalQueries = 0;
  let fullRootWalks = 0;
  const walk = document.createTreeWalker.bind(document);
  document.createTreeWalker = (root, ...args) => { if (roots.includes(root) || root === document.body) fullRootWalks++; return walk(root, ...args); };
  for (let i = 0; i < 200; i++) { const p = document.createElement('p'); p.textContent = 'Character Tracker'; outside.append(p); }
  const dynamic = document.createElement('p'); dynamic.textContent = '  Character Tracker  '; roots[3].append(dynamic);
  await settle();
  equal(dynamic.textContent, `  ${exact['Character Tracker']}  `, 'dynamic before next task');
  equal(globalQueries, 0, 'no document queries on mutations');
  equal(fullRootWalks, 0, 'no full container walk on append');
  dynamic.textContent = 'Custom Tracker'; await settle();
  equal(dynamic.textContent, exact['Custom Tracker'], 'React child replacement (characterData covered by browser suite)');
  const highlighted = document.createElement('span'); highlighted.innerHTML = 'Character <mark>Track</mark>er'; roots[12].append(highlighted);
  const mark = highlighted.querySelector('mark'); await settle();
  equal(highlighted.textContent, exact['Character Tracker'], 'split search highlight');
  equal(highlighted.querySelector('mark'), mark, 'React highlight node retained');
  const joined = document.createElement('p'); joined.textContent = 'Character Tracker 1.2.3 · Custom Tracker 0.1.0'; roots[0].append(joined); await settle();
  equal(joined.textContent, `${exact['Character Tracker']} 1.2.3 · ${exact['Custom Tracker']} 0.1.0`, 'Organizer update names');
  joined.textContent = 'Character Tracker, Custom Tracker'; await settle();
  equal(joined.textContent, `${exact['Character Tracker']}, ${exact['Custom Tracker']}`, 'Organizer kit names');
  joined.textContent = 'Character Tracker, My custom package'; await settle();
  equal(joined.textContent, 'Character Tracker, My custom package', 'unknown compound left intact');
  joined.remove();
  const lateRoot = document.createElement('div'); lateRoot.setAttribute('data-chat-control-window', 'conversation-agents'); lateRoot.innerHTML = '<p>World State</p><p>Tracker Agents</p>'; document.body.append(lateRoot); await settle();
  equal(lateRoot.textContent, exact['World State'] + ui['Tracker Agents'], 'late portal');
  const reused = document.createElement('div'); reused.setAttribute('data-component', 'Modal'); reused.setAttribute('aria-label', 'Agent Suite');
  reused.innerHTML = '<p>Character Tracker</p>'; document.body.append(reused); await settle();
  equal(reused.textContent, exact['Character Tracker'], 'allowed modal');
  reused.setAttribute('aria-label', 'Edit character'); await settle();
  equal(reused.textContent, 'Character Tracker', 'reused modal leaves scope');
  reused.remove();
  const hidden = document.createElement('div'); hidden.innerHTML = '<div data-component="RightPanel"><div data-panel-key="agents" aria-hidden="true"><span>Character Tracker</span></div></div>'; document.body.append(hidden); await settle();
  equal(hidden.textContent, 'Character Tracker', 'hidden panel');
  hidden.querySelector('[data-panel-key]').setAttribute('aria-hidden', 'false'); await settle();
  equal(hidden.textContent, exact['Character Tracker'], 'activated panel');
  dynamic.remove(); await settle(); equal(dynamic.textContent, 'Custom Tracker', 'detached nodes restored');
  outside.append(dynamic); await settle(); equal(dynamic.textContent, 'Custom Tracker', 'moved outside remains original');
  document.documentElement.lang = 'en'; await settle(); checkRoots(false);
  equal(highlighted.innerHTML, 'Character <mark>Track</mark>er', 'highlight restored exactly');
  document.documentElement.lang = 'ko-KR'; await settle(); checkRoots(true);
  const owned = document.createElement('span'); owned.setAttribute('title', 'Character Tracker'); roots[3].append(owned); await settle();
  owned.setAttribute('title', '공식 번역');
  cleanup(); cleanup(); await settle(); owned.remove(); checkRoots(false); // attribute below intentionally app-owned
  equal(owned.getAttribute('title'), '공식 번역', 'app attribute preserved');
  lateRoot.innerHTML = '<p>Character Tracker</p>'; await settle();
  equal(lateRoot.textContent, 'Character Tracker', 'disabled observers');
  console.log(`PASS DOM regression: ${checks} assertions; ${roots.length} selectors, ${Object.keys(exact).length} exact strings`);
})().catch(error => { console.error(error); process.exitCode = 1; });
