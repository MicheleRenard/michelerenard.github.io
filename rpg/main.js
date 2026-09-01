// Emberrest — a 16-bit portfolio RPG.
// One file, deliberately: === ENGINE === === WORLD === === PLAYER ===
// === UI (FF windows, DOM) === === CONTENT === === AUDIO ===
// Assets come from tools/build-rpg-sprites.py; data.js from tools/build-rpg-data.py.

/* global kaplay */

"use strict";

const DATA = window.RPG_DATA || { publications: [], skills: [], headline: {} };

// ============================== ENGINE =====================================

const TILE = 16;
const MAP_W = 25;
const MAP_H = 18;

// Integer pixel scaling: size the canvas box to a whole multiple of the game
// resolution so pixels stay square (non-integer scaling reads as stretched).
// Registered before KAPLAY's own resize listener so it sees the new box size.
(() => {
  const box = document.getElementById("game-box");
  const stage = document.getElementById("stage");
  const fit = () => {
    const availW = stage.clientWidth || window.innerWidth;
    const availH = (stage.clientHeight || window.innerHeight - 60) - 8;
    const s = Math.floor(Math.min(availW / (MAP_W * TILE), availH / (MAP_H * TILE)));
    if (s >= 1) {
      box.style.width = MAP_W * TILE * s + "px";
      box.style.height = MAP_H * TILE * s + "px";
    } else {
      box.style.width = "100%";   // tiny screens: fall back to fractional fit
      box.style.height = "";
    }
  };
  window.addEventListener("resize", fit);
  fit();
})();

const k = kaplay({
  canvas: document.getElementById("game"),
  width: MAP_W * TILE,
  height: MAP_H * TILE,
  letterbox: true,
  crisp: true,
  pixelDensity: 1,
  background: [27, 36, 50],
  global: false,
  touchToMouse: true,
});

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

k.onLoadError((name, err) => console.error("[rpg] failed to load asset:", name, err));
k.onLoad(() => console.log("[rpg] all assets loaded"));

// Debug handle (harmless in production; used by the walkthrough tests).
window.__rpg = { k };

// KAPLAY receives keys via the canvas element, so it must hold focus for
// arrow keys to work without a click first.
const gameCanvas = document.getElementById("game");
gameCanvas.setAttribute("tabindex", "0");
window.addEventListener("load", () => gameCanvas.focus({ preventScroll: true }));
gameCanvas.focus({ preventScroll: true });

k.loadSprite("michele", "assets/sprites/michele-walk.png", {
  sliceX: 3,
  sliceY: 4,
  anims: {
    "idle-down": 0, "walk-down": { frames: [1, 0, 2, 0], speed: 7, loop: true },
    "idle-up": 3, "walk-up": { frames: [4, 3, 5, 3], speed: 7, loop: true },
    "idle-right": 6, "walk-right": { frames: [7, 6, 8, 6], speed: 7, loop: true },
    "idle-left": 9, "walk-left": { frames: [10, 9, 11, 9], speed: 7, loop: true },
  },
});
k.loadSprite("crier", "assets/sprites/crier.png", {
  sliceX: 2, anims: { bob: { from: 0, to: 1, speed: 2, loop: true } },
});
k.loadSprite("cat", "assets/sprites/cat.png", {
  sliceX: 2, anims: { flick: { from: 0, to: 1, speed: 1.6, loop: true } },
});
k.loadSprite("sign", "assets/sprites/sign.png");
k.loadSprite("tiles", "assets/tiles/tiles.png", { sliceX: 9 });
for (const b of ["lab", "library", "guild", "inn", "shop", "fountain"]) {
  k.loadSprite(b, `assets/tiles/${b}.png`);
}

// ============================== WORLD ======================================

// Ground legend: g grass, s speckled, f flowers, p path, z plaza,
// w water (solid), h fence (solid), t tree (solid).
const GROUND = [
  "ttttttttttttttttttttttttt",
  "tgfggggggggggggggggggggst",
  "tgggggggggggggggggggggggt",
  "tsggggggggggggggggggggfgt",
  "tgggggggggggggggggggggggt",
  "tggpppppppppppppppppppggt",
  "tggggggggzzzzzzzggggggggt",
  "tggggggggzzzzzzzggggggggt",
  "tggggggggzzzzzzzggggggggt",
  "tggggggggzzzzzzzggggggggt",
  "tggggggggzzzzzzzggggggggt",
  "tppppppppppppppppppppppgt",
  "tgggggggggggpgggggggggggt",
  "twwwwgggggggpgggggggghhht",
  "twwwwgggggggpggggggggggst",
  "tfgggggggggspggggggggfggt",
  "ttttttttttttptttttttttttt",
  "ttttttttttttptttttttttttt",
];

for (const [i, row] of GROUND.entries()) {
  if (row.length !== MAP_W) throw new Error(`GROUND row ${i} is ${row.length} tiles, expected ${MAP_W}`);
}

const groundTiles = {
  g: () => [k.sprite("tiles", { frame: 0 })],
  s: () => [k.sprite("tiles", { frame: 1 })],
  f: () => [k.sprite("tiles", { frame: 2 })],
  p: () => [k.sprite("tiles", { frame: 3 })],
  z: () => [k.sprite("tiles", { frame: 8 })],
  t: () => [k.sprite("tiles", { frame: 5 }), k.area(), k.body({ isStatic: true })],
  w: () => [k.sprite("tiles", { frame: 6 }), k.area(), k.body({ isStatic: true })],
  h: () => [k.sprite("tiles", { frame: 7 }), k.area(), k.body({ isStatic: true })],
};

// Solid props and buildings: sprite, position, size. Bottom edges align with
// the paths (y=80 top row, y=176 side row); heights differ per building.
// Only the lower `solid` px block, the walls, collides — the player can walk
// behind a tall roof and be drawn behind it (y-sorted).
const BUILDINGS = [
  { spr: "lab", x: 52, y: 12, w: 72, h: 68, solid: 42 },
  { spr: "library", x: 212, y: 22, w: 56, h: 58, solid: 36 },
  { spr: "guild", x: 308, y: 22, w: 56, h: 58, solid: 36 },
  { spr: "inn", x: 20, y: 104, w: 64, h: 72, solid: 48 },
  { spr: "shop", x: 308, y: 118, w: 56, h: 58, solid: 36 },
  { spr: "fountain", x: 184, y: 104, w: 32, h: 32, solid: 24 },
];

// ============================== UI (FF windows) ============================

const ui = {
  root: document.getElementById("ui"),
  dialogue: document.getElementById("dialogue"),
  dialogueTitle: document.getElementById("dialogue-title"),
  dialogueText: document.getElementById("dialogue-text"),
  dialogueAdvance: document.getElementById("dialogue-advance"),
  menu: document.getElementById("menu"),
  menuTitle: document.getElementById("menu-title"),
  menuList: document.getElementById("menu-list"),
  status: document.getElementById("status"),
  statusBody: document.getElementById("status-body"),
};

let uiMode = null;           // null | "dialogue" | "menu" | "status"
let typeTimer = null;
let dlg = null;              // { pages, page, typing, onDone }
let menuState = null;        // { items, index, onClose }

const uiOpen = () => uiMode !== null;

// The DOM keydown handler and KAPLAY both see the same keypress. Without a
// grace period, Esc closing a window would immediately reopen the status
// screen (and Z closing a dialogue would immediately re-trigger the zone).
let justClosedAt = 0;
const justClosed = () => performance.now() - justClosedAt < 150;

function showWindow(el) {
  ui.root.hidden = false;
  el.hidden = false;
  el.setAttribute("tabindex", "-1");
  el.focus({ preventScroll: true });
}

function hideAll() {
  if (uiMode !== null) justClosedAt = performance.now();
  for (const el of [ui.dialogue, ui.menu, ui.status]) el.hidden = true;
  ui.root.hidden = true;
  uiMode = null;
  dlg = null;
  menuState = null;
  if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
  document.getElementById("game").focus?.({ preventScroll: true });
}

// --- dialogue: pages are { text, html? } — text is typed, html (links etc.)
// --- appears once the text finishes.
function openDialogue({ tab, tabClass, pages, onDone }) {
  hideAll();
  uiMode = "dialogue";
  dlg = { pages, page: -1, typing: false, onDone };
  ui.dialogueTitle.textContent = tab;
  ui.dialogueTitle.className = "ff-tab" + (tabClass ? " " + tabClass : "");
  showWindow(ui.dialogue);
  nextPage();
}

function nextPage() {
  if (!dlg) return;
  dlg.page += 1;
  if (dlg.page >= dlg.pages.length) {
    const done = dlg.onDone;
    hideAll();
    if (done) done();
    return;
  }
  const page = dlg.pages[dlg.page];
  ui.dialogueText.textContent = "";
  ui.dialogueAdvance.hidden = true;
  if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
  if (reducedMotion || !page.text) {
    finishPage(page);
  } else {
    dlg.typing = true;
    let i = 0;
    const textNode = document.createTextNode("");
    ui.dialogueText.appendChild(textNode);
    typeTimer = setInterval(() => {
      i += 2;
      textNode.data = page.text.slice(0, i);
      if (i >= page.text.length) {
        clearInterval(typeTimer);
        typeTimer = null;
        finishPage(page, textNode);
      }
    }, 16);
  }
}

function finishPage(page, textNode) {
  if (textNode) textNode.data = page.text;
  else if (page.text) ui.dialogueText.textContent = page.text;
  if (page.html) {
    const div = document.createElement("div");
    div.innerHTML = page.html;
    ui.dialogueText.appendChild(div);
  }
  if (dlg) dlg.typing = false;
  ui.dialogueAdvance.hidden = false;
}

function advanceDialogue() {
  if (!dlg) return;
  const page = dlg.pages[dlg.page];
  if (dlg.typing) {
    if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
    ui.dialogueText.textContent = "";
    finishPage(page);
  } else {
    nextPage();
  }
}

// --- menu: items are { label, sub?, onSelect } ------------------------------
function openMenu({ tab, tabClass, items, onClose }) {
  hideAll();
  uiMode = "menu";
  menuState = { items, index: 0, onClose };
  ui.menuTitle.textContent = tab;
  ui.menuTitle.className = "ff-tab" + (tabClass ? " " + tabClass : "");
  ui.menuList.innerHTML = "";
  items.forEach((item, i) => {
    const li = document.createElement("li");
    li.setAttribute("role", "menuitem");
    li.textContent = item.label;
    if (item.sub) {
      const sub = document.createElement("span");
      sub.className = "sub";
      sub.textContent = item.sub;
      li.appendChild(sub);
    }
    li.addEventListener("click", () => selectMenuItem(i));
    ui.menuList.appendChild(li);
  });
  highlightMenu(0);
  showWindow(ui.menu);
}

function highlightMenu(i) {
  if (!menuState) return;
  menuState.index = i;
  [...ui.menuList.children].forEach((li, j) => {
    li.setAttribute("aria-current", j === i ? "true" : "false");
  });
  ui.menuList.children[i]?.scrollIntoView({ block: "nearest" });
}

function selectMenuItem(i) {
  const item = menuState?.items[i];
  if (item) item.onSelect();
}

// --- status ----------------------------------------------------------------
function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function openStatus() {
  hideAll();
  uiMode = "status";
  const hl = DATA.headline;
  const statRow = (label, value, note) =>
    `<div class="stat-row"><span class="label">${label}</span>` +
    `<span>${value}</span><span class="note">${note}</span></div>`;
  let html = "";
  html += `<p style="margin:0 0 2px">MICHÈLE</p>`;
  html += `<p style="margin:0;font-size:9px;opacity:.8">Class: Environmental Physiologist<br>` +
    `Job: Research Fellow · NUS Medicine</p>`;
  html += `<hr style="border:1px solid rgba(255,255,255,.25);margin:10px 0">`;
  html += statRow("LV", hl.publications ?? "?", "peer-reviewed publications");
  html += statRow("EXP", (hl.personNights ?? 0).toLocaleString("en"), "person-nights of sleep data");
  html += statRow("PARTY", hl.participants ?? "?", "participants recruited");
  html += statRow("WAVES", hl.fieldWaves ?? "?", "field waves completed");
  html += statRow("GUILDS", hl.programmes ?? "?", "national research programmes");
  html += statRow("QUESTS", hl.reviewsInProgress ?? "?", "systematic reviews in progress");
  html += `<h3>ABILITIES</h3>`;
  DATA.skills.forEach((s) => {
    const more = s.total > s.items.length ? ` (+${s.total - s.items.length} more)` : "";
    html += `<div class="ability">▸ ${esc(s.name)}` +
      `<span class="items">${esc(s.items.join(" · "))}${more}</span></div>`;
  });
  html += `<p style="font-size:9px;margin-top:12px">Full record: ` +
    `<a href="../cv.html">curriculum vitae</a> · <a href="../publications.html">publications</a></p>`;
  ui.statusBody.innerHTML = html;
  showWindow(ui.status);
}

// --- shared key handling for the DOM layer ---------------------------------
document.addEventListener("keydown", (e) => {
  if (!uiOpen()) return;
  const key = e.key;
  if (uiMode === "dialogue") {
    if (["z", "Z", "Enter", " "].includes(key)) { e.preventDefault(); advanceDialogue(); }
    else if (key === "Escape") { e.preventDefault(); hideAll(); }
  } else if (uiMode === "menu") {
    if (key === "ArrowUp") { e.preventDefault(); highlightMenu((menuState.index + menuState.items.length - 1) % menuState.items.length); }
    else if (key === "ArrowDown") { e.preventDefault(); highlightMenu((menuState.index + 1) % menuState.items.length); }
    else if (["z", "Z", "Enter", " "].includes(key)) { e.preventDefault(); selectMenuItem(menuState.index); }
    else if (key === "Escape") {
      e.preventDefault();
      const close = menuState.onClose;
      hideAll();
      if (close) close();
    }
  } else if (uiMode === "status") {
    if (["Escape", "z", "Z", "Enter", " ", "m", "M"].includes(key)) { e.preventDefault(); hideAll(); }
  }
}, true);

ui.dialogue.addEventListener("click", (e) => {
  if (e.target.closest("a")) return;
  advanceDialogue();
});
ui.status.addEventListener("click", (e) => {
  if (e.target.closest("a")) return;
  hideAll();
});

// ============================== CONTENT ====================================

const SITE = "..";

const link = (href, label) =>
  `<a href="${href}" target="_blank" rel="noopener">${label}</a>`;
const localLink = (href, label) => `<a href="${href}">${label}</a>`;

function labMenu() {
  openMenu({
    tab: "Research Lab",
    items: [
      {
        label: "Project HEATS",
        sub: "heat and sleep in Singapore homes",
        onSelect: () => openDialogue({
          tab: "Project HEATS",
          pages: [
            { text: "How do hot bedrooms shape sleep? 122 participants, 10,303 person-nights of wearable and sensor data across three field waves in Singapore homes and dormitories." },
            { text: "Michèle leads the statistical analysis — from nighttime bedroom temperature to sleep continuity, and randomised cooling interventions.",
              html: `<p>${localLink(SITE + "/research.html", "▸ Read about the research")}</p>` },
          ],
          onDone: labMenu,
        }),
      },
      {
        label: "Cooling Singapore 2.0",
        sub: "heat vulnerability and advisories",
        onSelect: () => openDialogue({
          tab: "Cooling Singapore 2.0",
          pages: [
            { text: "Evidence synthesis behind Singapore's Exertional Heat Vulnerability Index, and a review of how heat-health advisories are designed — and whether they work." },
            { text: "Findings feed directly into national heat-health policy.",
              html: `<p>${localLink(SITE + "/research.html", "▸ Read about the research")}</p>` },
          ],
          onDone: labMenu,
        }),
      },
      {
        label: "eHVI programme",
        sub: "protocol lead and review guarantor",
        onSelect: () => openDialogue({
          tab: "eHVI",
          pages: [
            { text: "Michèle leads the evidence-synthesis workstream for the exertional Heat Vulnerability Index programme (NRF/NEA award CISR-2024-2R-04) as protocol lead and review guarantor." },
          ],
          onDone: labMenu,
        }),
      },
      {
        label: "Systematic reviews",
        sub: "four PROSPERO-registered quests",
        onSelect: () => openDialogue({
          tab: "Active quests",
          pages: [
            { text: "Four PROSPERO-registered systematic reviews in progress: heat-health advisories, vulnerability indices, warm-night thresholds, and cooling strategies." },
          ],
          onDone: labMenu,
        }),
      },
      { label: "Leave", sub: "", onSelect: hideAll },
    ],
  });
}

function libraryMenu() {
  const items = DATA.publications.map((p) => ({
    label: `${p.year} — ${p.title.length > 44 ? p.title.slice(0, 44) + "…" : p.title}`,
    onSelect: () => openDialogue({
      tab: `Tome of ${p.year}`,
      pages: [{
        text: `${p.authorsShort} (${p.year}). ${p.title}. ${p.journal}.`,
        html: p.doi ? `<p>${link("https://doi.org/" + p.doi, "▸ doi.org/" + p.doi)}</p>` : "",
      }],
      onDone: libraryMenu,
    }),
  }));
  items.push({ label: "Leave", onSelect: hideAll });
  openMenu({
    tab: `Library — tomes learned: ${DATA.publications.length}`,
    tabClass: "night",
    items,
  });
}

function innDialogue() {
  openDialogue({
    tab: "The Ember & Night Inn",
    tabClass: "night",
    pages: [
      { text: "Welcome, traveller! Rooms are 28°C — we're working on it." },
      { text: "Your host is Michèle Renard: environmental physiologist and quantitative researcher, working on how heat shapes sleep, physiological strain and health in real-world populations." },
      { text: "He works where field measurement meets statistical modelling, alongside early career researchers across two national programmes." },
      { text: "Care to leave a message?",
        html: `<p>${link("mailto:mrenard@nus.edu.sg", "✉ mrenard@nus.edu.sg")}<br>` +
          `${link("https://www.linkedin.com/in/michelerenard/", "▸ LinkedIn")} · ` +
          `${link("https://orcid.org/0000-0003-4517-1316", "▸ ORCID")}<br>` +
          `${localLink(SITE + "/collaborate.html", "▸ Working with Michèle")}</p>` },
    ],
  });
}

function shopMenu() {
  openMenu({
    tab: "Item Shop",
    items: [
      {
        label: "CLIF test chooser",
        sub: "which statistical test, and why?",
        onSelect: () => openDialogue({
          tab: "Rare item!",
          pages: [{
            text: "An open-access chooser that walks you from research question to statistical test. No login, works offline, free forever.",
            html: `<p>${link("https://michelerenard.github.io/clif-chooser/", "▸ Open the CLIF chooser")}</p>`,
          }],
          onDone: shopMenu,
        }),
      },
      {
        label: "heatsviz",
        sub: "visualisation package (party members only)",
        onSelect: () => openDialogue({
          tab: "heatsviz",
          pages: [{
            text: "A visualisation package keeping every Project HEATS figure on-brand. Internal for now — ask at the counter.",
            html: `<p>${localLink(SITE + "/tools.html", "▸ Tools & resources")}</p>`,
          }],
          onDone: shopMenu,
        }),
      },
      {
        label: "Teaching material",
        sub: "workshops and stats sessions",
        onSelect: () => openDialogue({
          tab: "Teaching",
          pages: [{
            text: "Workshop materials and statistics teaching, including the CLIF foundational workshop series.",
            html: `<p>${localLink(SITE + "/tools.html", "▸ Tools & resources")}</p>`,
          }],
          onDone: shopMenu,
        }),
      },
      { label: "Leave", sub: "", onSelect: hideAll },
    ],
  });
}

function crierDialogue() {
  openDialogue({
    tab: "Town crier",
    pages: [
      { text: "Hear ye, hear ye! What's the temperature in the bedroom in Singapore? A muggy 28°C, says a new study!" },
      { text: "Project HEATS findings were covered in The Straits Times and Lianhe Zaobao, and cited by the Chairman of the National Research Foundation.",
        html: `<p>${link("https://www.straitstimes.com/singapore/environment/whats-the-temperature-in-the-bedroom-in-spore-a-muggy-28-deg-c-says-new-study-on-residents", "▸ The Straits Times")} · ` +
          `${link("https://www.zaobao.com.sg/news/singapore/story20260625-9260617", "▸ Lianhe Zaobao")}</p>` },
    ],
  });
}

function signDialogue() {
  openDialogue({
    tab: "Signpost",
    pages: [
      { text: "EMBERREST — pop. 1 researcher, 122 study participants, 1 cat." },
      { text: "Move: arrow keys / WASD, or tap where you want to go. Interact: Z, Enter, or tap. Status screen: M. Close windows: Esc." },
    ],
  });
}

function fountainDialogue() {
  openDialogue({
    tab: "Fountain",
    pages: [
      { text: "The Fountain of Replication. The effect is stable across all three waves. You feel reassured." },
    ],
  });
}

function catDialogue() {
  openDialogue({
    tab: "Cat",
    pages: [
      { text: "Meow. (The cat has no comment on your p-values.)" },
    ],
  });
}

function gateMenu() {
  openMenu({
    tab: "South gate",
    items: [
      { label: "Leave for the overworld", sub: "michelerenard.github.io", onSelect: () => { window.location.href = "../"; } },
      { label: "Stay in the village", sub: "", onSelect: hideAll },
    ],
  });
}

// Interact zones: rect + action. Player interacts when its feet are within
// `range` px of the zone (or taps it while close).
const ZONES = [
  { name: "lab", x: 76, y: 72, w: 24, h: 26, action: labMenu },
  { name: "library", x: 228, y: 72, w: 24, h: 26, action: libraryMenu },
  { name: "guild", x: 324, y: 72, w: 24, h: 26, action: openStatus },
  { name: "inn", x: 40, y: 168, w: 24, h: 26, action: innDialogue },
  { name: "shop", x: 324, y: 168, w: 24, h: 26, action: shopMenu },
  { name: "fountain", x: 172, y: 96, w: 56, h: 48, action: fountainDialogue },
  { name: "sign", x: 156, y: 236, w: 24, h: 24, action: signDialogue },
  { name: "crier", x: 148, y: 116, w: 24, h: 30, action: crierDialogue },
  { name: "cat", x: 84, y: 146, w: 24, h: 24, action: catDialogue },
];

const GATE = { x: 184, y: 276, w: 32, h: 12 };

// ============================== SCENE ======================================

k.scene("village", () => {
  k.addLevel(GROUND, {
    tileWidth: TILE,
    tileHeight: TILE,
    tiles: groundTiles,
  });

  for (const b of BUILDINGS) {
    k.add([
      k.sprite(b.spr),
      k.pos(b.x, b.y),
      k.area({ shape: new k.Rect(k.vec2(0, b.h - b.solid), b.w, b.solid) }),
      k.body({ isStatic: true }),
      k.z(b.y + b.h),
    ]);
  }

  k.add([k.sprite("sign"), k.pos(160, 232), k.area(), k.body({ isStatic: true }), k.z(248)]);
  const crier = k.add([k.sprite("crier"), k.pos(152, 108), k.area(), k.body({ isStatic: true }), k.z(132)]);
  crier.play("bob");
  const cat = k.add([k.sprite("cat"), k.pos(88, 146), k.area(), k.body({ isStatic: true }), k.z(162)]);
  cat.play("flick");

  const player = k.add([
    k.sprite("michele"),
    k.pos(192, 240),
    k.area({ shape: new k.Rect(k.vec2(3, 14), 10, 9) }),
    k.body(),
    k.anchor("topleft"),
    k.z(264),
    "player",
  ]);
  player.play("idle-up");
  window.__rpg.player = player;

  const SPEED = 72;
  let facing = "up";
  let moving = false;
  let target = null;          // tap-to-move destination (vec2)
  let stuckTime = 0;
  let yFirst = false;         // leading axis for tap-walking
  let swappedAxis = false;    // one axis swap allowed per target
  const virtualKeys = { up: false, down: false, left: false, right: false };

  const keyDown = (dir) => {
    const maps = {
      up: ["up", "w"], down: ["down", "s"], left: ["left", "a"], right: ["right", "d"],
    };
    return maps[dir].some((key) => k.isKeyDown(key)) || virtualKeys[dir];
  };

  function feet() {
    return k.vec2(player.pos.x + 8, player.pos.y + 20);
  }

  function setAnim(dir, isMoving) {
    const want = (isMoving ? "walk-" : "idle-") + dir;
    const cur = player.getCurAnim ? player.getCurAnim()?.name : player.curAnim();
    if (cur !== want) player.play(want);
    facing = dir;
    moving = isMoving;
  }

  function zoneNear(pt, range) {
    for (const z of ZONES) {
      if (pt.x > z.x - range && pt.x < z.x + z.w + range &&
          pt.y > z.y - range && pt.y < z.y + z.h + range) return z;
    }
    return null;
  }

  function tryInteract() {
    if (uiOpen() || justClosed()) return;
    const z = zoneNear(feet(), 8);
    if (z) z.action();
  }

  k.onKeyPress(["z", "enter", "space"], () => tryInteract());
  k.onKeyPress(["m", "escape"], () => { if (!uiOpen() && !justClosed()) openStatus(); });

  k.onMousePress(() => {
    if (uiOpen()) return;
    const m = k.mousePos();
    // tapping an interactable while standing near it interacts; otherwise walk
    const z = zoneNear(m, 2);
    if (z && zoneNear(feet(), 10) === z) {
      z.action();
      return;
    }
    target = m.clone();
    yFirst = false;
    swappedAxis = false;
    stuckTime = 0;
  });

  document.querySelectorAll("#dpad button").forEach((btn) => {
    const dir = btn.dataset.dir;
    const on = (e) => { e.preventDefault(); virtualKeys[dir] = true; target = null; };
    const off = (e) => { e.preventDefault(); virtualKeys[dir] = false; };
    btn.addEventListener("pointerdown", on);
    btn.addEventListener("pointerup", off);
    btn.addEventListener("pointerleave", off);
    btn.addEventListener("pointercancel", off);
  });
  document.getElementById("btn-a").addEventListener("pointerdown", (e) => {
    e.preventDefault();
    tryInteract();
  });

  k.onUpdate(() => {
    if (uiOpen()) {
      if (moving) setAnim(facing, false);
      return;
    }

    let v = k.vec2(0, 0);
    if (keyDown("left")) v.x = -1;
    else if (keyDown("right")) v.x = 1;
    if (keyDown("up")) v.y = -1;
    else if (keyDown("down")) v.y = 1;

    if (v.x !== 0 || v.y !== 0) {
      target = null;
    } else if (target) {
      // axis-by-axis toward the tap target; when a wall blocks the leading
      // axis, swap to the other one before giving up (gets around signposts
      // and building corners without real pathfinding)
      const dx = target.x - (player.pos.x + 8);
      const dy = target.y - (player.pos.y + 12);
      const axes = yFirst
        ? [[Math.abs(dy) > 3 && Math.sign(dy), "y"], [Math.abs(dx) > 3 && Math.sign(dx), "x"]]
        : [[Math.abs(dx) > 3 && Math.sign(dx), "x"], [Math.abs(dy) > 3 && Math.sign(dy), "y"]];
      const [firstMove, firstAxis] = axes[0];
      const [secondMove] = axes[1];
      if (firstMove) {
        if (firstAxis === "x") v.x = firstMove; else v.y = firstMove;
      } else if (secondMove) {
        if (firstAxis === "x") v.y = secondMove; else v.x = secondMove;
      } else {
        target = null;
      }
    }

    if (v.x !== 0 || v.y !== 0) {
      const before = player.pos.clone();
      player.move(v.scale(SPEED));
      const dir = v.x < 0 ? "left" : v.x > 0 ? "right" : v.y < 0 ? "up" : "down";
      setAnim(dir, true);
      if (target) {
        stuckTime = player.pos.sub(before).len() < 0.01 ? stuckTime + k.dt() : 0;
        if (stuckTime > 0.25) {
          stuckTime = 0;
          if (!swappedAxis) {
            yFirst = !yFirst;      // blocked: try approaching on the other axis
            swappedAxis = true;
          } else {
            target = null;         // blocked both ways: give up
          }
        }
      }
    } else if (moving) {
      setAnim(facing, false);
    }

    player.z = player.pos.y + 24;

    // south gate
    const f = feet();
    if (f.x > GATE.x && f.x < GATE.x + GATE.w && f.y > GATE.y) {
      player.pos.y -= 4;
      gateMenu();
    }
  });
});

k.go("village");

// ============================== AUDIO ======================================

(() => {
  const btn = document.getElementById("audio-toggle");
  const audio = new Audio();
  audio.loop = true;
  audio.volume = 0.55;
  let available = false;
  audio.addEventListener("canplaythrough", () => { available = true; });
  audio.addEventListener("error", () => { btn.hidden = true; });
  audio.src = "assets/audio/theme.m4a";

  let on = false;
  btn.addEventListener("click", () => {
    if (!available) return;
    on = !on;
    if (on) audio.play().catch(() => { on = false; });
    else audio.pause();
    btn.textContent = on ? "♪ on" : "♪ off";
    btn.setAttribute("aria-pressed", String(on));
    btn.title = on ? "Music (on)" : "Music (off)";
    try { localStorage.setItem("rpg-audio", on ? "1" : "0"); } catch (e) { /* private mode */ }
  });
})();

document.getElementById("status-button").addEventListener("click", () => {
  if (uiOpen()) hideAll();
  openStatus();
});
