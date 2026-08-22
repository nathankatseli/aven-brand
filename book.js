/* AVEN brand book — rail + decision capture + export. No dependencies, no network. */
(function () {
  "use strict";
  var KEY = "aven-brand:v1";
  var FONT_SERIF = {
    "source-serif-4": '"Cand Source Serif 4","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif',
    "crimson-pro": '"Cand Crimson Pro","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif',
    "eb-garamond": '"Cand EB Garamond","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif'
  };
  var FONT_SANS = {
    "nunito-sans": '"Cand Nunito Sans","Avenir Next","Avenir","Segoe UI",system-ui,sans-serif',
    "mulish": '"Cand Mulish","Avenir Next","Avenir","Segoe UI",system-ui,sans-serif',
    "inter": '"Cand Inter","Avenir Next","Avenir","Segoe UI",system-ui,sans-serif'
  };

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "null") || { v: 1, book: "aven-brand", calls: {} }; }
    catch (e) { return { v: 1, book: "aven-brand", calls: {} }; }
  }
  function save(state) {
    state.at = new Date().toISOString();
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }
  var state = load();

  function fieldsets() { return Array.prototype.slice.call(document.querySelectorAll("fieldset.call")); }

  function readCall(fs) {
    var id = fs.dataset.id, label = fs.dataset.label;
    var checked = fs.querySelectorAll("input:checked");
    var choices = Array.prototype.map.call(checked, function (i) { return { value: i.value, label: i.dataset.label || i.value }; });
    var note = (fs.querySelector("textarea[data-note]") || {}).value || "";
    return { id: id, label: label, choices: choices, note: note.trim() };
  }

  function serialise() {
    var calls = {};
    fieldsets().forEach(function (fs) {
      var c = readCall(fs);
      if (c.choices.length || c.note) calls[c.id] = { label: c.label, choice: c.choices.map(function (x) { return x.value; }).join(", "), choiceLabel: c.choices.map(function (x) { return x.label; }).join(", "), note: c.note };
    });
    state.calls = calls;
    save(state);
  }

  function hydrate() {
    fieldsets().forEach(function (fs) {
      var saved = state.calls[fs.dataset.id];
      if (!saved) return;
      var vals = saved.choice ? saved.choice.split(", ") : [];
      fs.querySelectorAll("input").forEach(function (i) { i.checked = vals.indexOf(i.value) >= 0; });
      var ta = fs.querySelector("textarea[data-note]"); if (ta) ta.value = saved.note || "";
    });
  }

  function paint() {
    var made = 0, total = fieldsets().length;
    fieldsets().forEach(function (fs) {
      var c = readCall(fs);
      var done = c.choices.length > 0;
      fs.classList.toggle("made", done);
      if (done) made++;
      var cp = fs.querySelector(".call-print");
      if (cp) cp.textContent = done ? ("Call: " + c.choices.map(function (x) { return x.label; }).join(", ") + (c.note ? " — " + c.note : "")) : "Call: not yet made";
      var lk = document.querySelector('.lock[data-for="' + fs.dataset.id + '"]');
      if (lk) { lk.classList.toggle("made", done); lk.classList.toggle("open", !done); var v = lk.querySelector(".s"); if (v && done) v.textContent = c.choices.map(function (x) { return x.label; }).join(", "); }
    });
    document.querySelectorAll("[data-counter]").forEach(function (el) { el.textContent = made + " of " + total + " calls made"; });
    applyFonts();
    renderDecisions();
  }

  function applyFonts() {
    var s = document.querySelector('fieldset.call[data-id="type-serif"] input:checked');
    var a = document.querySelector('fieldset.call[data-id="type-sans"] input:checked');
    var root = document.documentElement.style;
    if (s && FONT_SERIF[s.value]) root.setProperty("--font-serif", FONT_SERIF[s.value]); else root.removeProperty("--font-serif");
    if (a && FONT_SANS[a.value]) root.setProperty("--font-sans", FONT_SANS[a.value]); else root.removeProperty("--font-sans");
  }

  function rows() {
    return fieldsets().map(function (fs) {
      var c = readCall(fs);
      return { label: c.label, choice: c.choices.map(function (x) { return x.label; }).join(", "), note: c.note };
    });
  }

  function renderDecisions() {
    var tb = document.querySelector("table.dec tbody"); if (!tb) return;
    tb.innerHTML = "";
    rows().forEach(function (r) {
      var tr = document.createElement("tr");
      var td1 = document.createElement("td"); td1.textContent = r.label;
      var td2 = document.createElement("td"); td2.textContent = r.choice || "open"; td2.className = r.choice ? "c" : "o";
      var td3 = document.createElement("td"); td3.textContent = r.note || "";
      tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3); tb.appendChild(tr);
    });
  }

  function toMarkdown() {
    var d = new Date().toISOString().slice(0, 10);
    var out = ["# AVEN brand book — decisions (" + d + ")", "", "| Aspect | Call | Note |", "|---|---|---|"];
    rows().forEach(function (r) { out.push("| " + r.label + " | " + (r.choice || "open") + " | " + r.note.replace(/\|/g, "/").replace(/\n/g, " ") + " |"); });
    return out.join("\n");
  }

  function toast(msg) { var t = document.querySelector(".toast"); if (t) { t.textContent = msg; setTimeout(function () { t.textContent = ""; }, 3500); } }

  document.addEventListener("change", function (e) {
    if (!(e.target.closest && e.target.closest("fieldset.call"))) return;
    if (e.target.name === "mark-secondary" && e.target.checked) {
      var on = Array.prototype.filter.call(document.querySelectorAll('input[name="mark-secondary"]'), function (i) { return i.checked; });
      if (on.length > 2) { on[0] === e.target ? on[1].checked = false : on[0].checked = false; }
    }
    serialise(); paint();
  });
  document.addEventListener("input", function (e) { if (e.target.matches && e.target.matches("fieldset.call textarea")) { serialise(); paint(); } });

  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-act]"); if (!b) return;
    var act = b.dataset.act;
    if (act === "copy-md") {
      navigator.clipboard.writeText(toMarkdown()).then(function () { toast("Copied as Markdown — paste it into chat or Notion."); }, function () { toast("Copy failed — select the table and copy manually."); });
    } else if (act === "download-json") {
      var blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "aven-decisions-" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + ".json"; a.click();
      toast("Downloaded.");
    } else if (act === "reset") {
      if (confirm("Clear every call and note on this device?")) { state = { v: 1, book: "aven-brand", calls: {} }; save(state); fieldsets().forEach(function (fs) { fs.querySelectorAll("input").forEach(function (i) { i.checked = false; }); var ta = fs.querySelector("textarea"); if (ta) ta.value = ""; }); paint(); toast("Cleared."); }
    }
  });

  /* rail */
  var links = Array.prototype.slice.call(document.querySelectorAll(".rail a[href^='#']"));
  if ("IntersectionObserver" in window && links.length) {
    var map = {}; links.forEach(function (l) { map[l.getAttribute("href").slice(1)] = l; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { links.forEach(function (l) { l.classList.remove("is-active"); }); var l = map[en.target.id]; if (l) l.classList.add("is-active"); } });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll(".chapter[id]").forEach(function (s) { io.observe(s); });
  }

  /* debug: ?debug=1 prints font-load state in the footer */
  if (/[?&]debug=1/.test(location.search) && document.fonts) {
    document.fonts.ready.then(function () {
      var el = document.querySelector("footer .dbg"); if (!el) return;
      el.textContent = 'AVEN Serif loaded: ' + document.fonts.check('16px "AVEN Serif"') + ' · AVEN Sans loaded: ' + document.fonts.check('16px "AVEN Sans"') + ' · fonts: ' + document.fonts.size;
    });
  }

  /* topbar: chapter label, scroll progress, dark mode over ink sections; counter band; reveal */
  (function () {
    var tb = document.getElementById("topbar"), ch = document.getElementById("tb-ch"), prog = document.getElementById("tb-prog");
    var chapters = Array.prototype.slice.call(document.querySelectorAll(".chapter[id]"));
    var names = {}; document.querySelectorAll(".rail a[href^='#']").forEach(function (a) { names[a.getAttribute("href").slice(1)] = a.textContent; });
    function onScroll() {
      var y = window.scrollY || document.documentElement.scrollTop;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (prog) prog.style.width = (h > 0 ? Math.min(100, y / h * 100) : 0) + "%";
      var cover = document.querySelector("header.cover"), foot = document.querySelector("footer.ink");
      var dark = false;
      if (cover && y < cover.offsetHeight - 56) dark = true;
      if (foot && foot.getBoundingClientRect().top < 56) dark = true;
      if (tb) tb.classList.toggle("dark", dark);
      var rail = document.querySelector(".rail"); if (rail) rail.classList.toggle("onink", dark);
      var cur = null; chapters.forEach(function (c) { if (c.getBoundingClientRect().top <= 120) cur = c; });
      if (cur && ch) { var t = names[cur.id] || cur.id; var m = t.match(/^(\d\d)(.*)$/); ch.innerHTML = m ? '<span class="n">' + m[1] + '</span>' + m[2].trim() : t; }
    }
    window.addEventListener("scroll", onScroll, { passive: true }); window.addEventListener("resize", onScroll); onScroll();
    var made = document.querySelector("[data-made]");
    function syncMade() { var c = document.querySelector("[data-counter]"); if (!c || !made) return; var m = c.textContent.match(/^(\d+) of (\d+)/); if (m) { made.innerHTML = m[1] + "<small>/ " + m[2] + "</small>"; var tc = document.getElementById("tb-cnt"); if (tc) tc.classList.toggle("done", +m[1] === +m[2]); } }
    new MutationObserver(syncMade).observe(document.querySelector("[data-counter]"), { childList: true, characterData: true, subtree: true }); syncMade();
    if ("IntersectionObserver" in window) {
      var ro = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); ro.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
      document.querySelectorAll(".reveal").forEach(function (el) { ro.observe(el); });
    } else { document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); }); }
  })();

  hydrate();
  paint();
})();
