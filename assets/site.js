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

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) {
    document.querySelectorAll("video[data-autoplay]").forEach(function (v) {
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    });
  }
})();
