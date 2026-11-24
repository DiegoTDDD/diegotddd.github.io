// Start the demo videos muted, unless the visitor prefers reduced motion; they keep their controls.
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;
  document.querySelectorAll("video[data-autoplay]").forEach(function (v) {
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
  });
})();
