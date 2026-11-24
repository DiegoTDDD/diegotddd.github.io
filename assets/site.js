// Theme toggle (remembered per visitor), project filters, and muted autoplay of demo videos.
(function () {
  var root = document.documentElement;
  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  var toggle = document.querySelector(".theme");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store("theme", next);
    });
  }

  // Remember the language a visitor picks, so the Portuguese pages stop redirecting them.
  var langLink = document.querySelector("a.lang[data-lang]");
  if (langLink) {
    langLink.addEventListener("click", function () { store("lang", langLink.getAttribute("data-lang")); });
  }

  var chips = document.querySelectorAll(".chip");
  var rows = document.querySelectorAll(".row[data-tags]");
  var groups = document.querySelectorAll(".group");
  var empty = document.querySelector(".empty");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      var shown = 0;
      rows.forEach(function (r) {
        var on = f === "all" || r.getAttribute("data-tags").split(" ").indexOf(f) >= 0;
        r.hidden = !on;
        if (on) shown++;
      });
      groups.forEach(function (g) { g.hidden = !g.querySelector(".row:not([hidden])"); });
      if (empty) empty.hidden = shown > 0;
    });
  });

  // Case pages: technical or manager view, remembered across pages.
  var caseEl = document.querySelector(".case[data-view]");
  var viewButtons = document.querySelectorAll(".view button");
  function setView(v) {
    if (!caseEl) return;
    caseEl.setAttribute("data-view", v);
    viewButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-view") === v)); });
  }
  try { var savedView = localStorage.getItem("view"); if (savedView === "manager") setView("manager"); } catch (e) {}
  viewButtons.forEach(function (b) {
    b.addEventListener("click", function () { var v = b.getAttribute("data-view"); setView(v); store("view", v); });
  });

  // Books page: SQL / Power BI / Python tabs, with arrow-key navigation.
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function selectTab(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute("aria-controls"));
      if (panel) { if (on) panel.removeAttribute("data-off"); else panel.setAttribute("data-off", ""); }
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (ev) {
      var j = ev.key === "ArrowRight" ? i + 1 : ev.key === "ArrowLeft" ? i - 1 : null;
      if (j === null) return;
      var next = tabs[(j + tabs.length) % tabs.length];
      selectTab(next); next.focus(); ev.preventDefault();
    });
  });

  // Impact calculators. Measured rates come from the page; the rest are the visitor's assumptions.
  document.querySelectorAll("form.calc").forEach(function (form) {
    var cfg = JSON.parse(form.getAttribute("data-calc"));
    var locale = cfg.lang === "pt" ? "pt-BR" : "en-US";
    function fmt(n, d) { return Number(n).toLocaleString(locale, { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); }
    function val(name) { var x = parseFloat(form.elements[name].value); return isFinite(x) && x > 0 ? x : 0; }
    function out(name, text) { var o = form.querySelector('[data-out="' + name + '"]'); if (o) o.textContent = text; }
    function run() {
      var d = cfg.data;
      if (cfg.kind === "fraud") {
        var tp = d.recall * d.frauds;
        var fpr = tp * (1 - d.precision) / d.precision / (d.rows - d.frauds);
        var tx = val("tx"), rate = val("rate") / 100;
        var frauds = tx * rate, caught = frauds * d.recall, fals = tx * (1 - rate) * fpr;
        var saved = caught * val("ticket");
        out("caught", fmt(caught));
        out("saved", fmt(saved));
        out("false", fmt(fals));
        out("prec", caught + fals > 0 ? fmt(100 * caught / (caught + fals), 1) + "%" : "–");
        out("net", fmt(saved - (caught + fals) * val("review")));
      } else if (cfg.kind === "supply") {
        var n = val("orders") * d.share, fix = val("fix") / 100, late = val("late_cost"), act = val("act_cost");
        var reachModel = n * d.top, reachRandom = n * d.base;
        out("model", fmt(reachModel));
        out("random", fmt(reachRandom));
        out("net", fmt(reachModel * fix * late - n * act));
        out("net_random", fmt(reachRandom * fix * late - n * act));
      } else if (cfg.kind === "finetune") {
        var req = val("req");
        var vms = Math.max(1, Math.ceil(req / d.capacity));
        var rows = [[cfg.text.own + " (" + vms + " " + (vms === 1 ? cfg.text.vm : cfg.text.vms) + ")", vms * d.vm_month]];
        d.apis.forEach(function (a) { rows.push([a[0], req / 1e6 * a[1]]); });
        var best = Math.min.apply(null, rows.map(function (r) { return r[1]; }));
        var body = form.querySelector('[data-out="table"]');
        body.textContent = "";
        rows.forEach(function (r) {
          var tr = document.createElement("tr");
          if (r[1] === best) tr.className = "best";
          var a = document.createElement("td"); a.textContent = r[0];
          if (r[1] === best) { var s = document.createElement("span"); s.className = "tag"; s.textContent = cfg.text.cheapest; a.appendChild(s); }
          var b = document.createElement("td"); b.textContent = (cfg.lang === "pt" ? "US$ " : "$") + fmt(r[1]) + " " + cfg.text.month;
          tr.appendChild(a); tr.appendChild(b); body.appendChild(tr);
        });
      }
    }
    form.addEventListener("input", run);
    run();
  });

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Browsers defer autoplay in background tabs, so start again whenever the page becomes visible.
  function playAll() {
    if (reduce || document.visibilityState !== "visible") return;
    document.querySelectorAll("video[data-autoplay]").forEach(function (v) {
      if (!v.paused) return;
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    });
  }
  playAll();
  document.addEventListener("visibilitychange", playAll);
})();
