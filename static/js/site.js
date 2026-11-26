// Scroll effects: reveal on scroll (both directions), progress bar, compact header,
// active nav link, hero parallax and a timeline that fills as you scroll.
(function () {
  var root = document.documentElement;
  if (!root.classList.contains("js")) return;   // reduced motion or no JS: show everything plainly
  window.__reveal = true;

  /* ---------- reveal on scroll ---------- */
  var SELECTORS = [
    ".hero .wrap > :not(.photo-wrap)", ".photo-wrap",
    ".section h2", ".section .sub", ".section .card", ".entry",
    ".icons a", ".contact .muted", ".detail > *"
  ].join(",");

  var items = Array.prototype.filter.call(document.querySelectorAll(SELECTORS), function (el) {
    return !(el.classList.contains("card") && el.closest(".entry"));
  });

  // stagger siblings a little
  var counts = new Map();
  items.forEach(function (el) {
    el.classList.add("reveal");
    var n = counts.get(el.parentNode) || 0;
    counts.set(el.parentNode, n + 1);
    el.dataset.delay = Math.min(n, 5) * 90;
    Array.prototype.forEach.call(el.querySelectorAll(".chips li"), function (li, i) {
      li.style.setProperty("--i", Math.min(i, 12));
    });
  });

  var timers = new Map();
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var el = entry.target;
      clearTimeout(timers.get(el));
      if (entry.isIntersecting) {
        el.style.transitionDelay = el.dataset.delay + "ms";
        el.classList.add("in");
        // drop the delay afterwards so hover effects respond instantly
        timers.set(el, setTimeout(function () { el.style.transitionDelay = ""; }, 1100));
      } else {
        // it left the screen: set it up to re-enter from the side it exited
        var above = entry.boundingClientRect.top < 0;
        el.style.transitionDelay = "";
        el.style.setProperty("--ry", above ? "-24px" : "24px");
        el.classList.remove("in");
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  items.forEach(function (el) { io.observe(el); });

  /* ---------- scroll-linked effects ---------- */
  var bar = document.querySelector(".progress");
  var nav = document.querySelector(".nav");
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav nav a[href*='#']"));
  var spy = links.map(function (a) {
    var id = a.getAttribute("href").split("#")[1];
    return { a: a, el: id ? document.getElementById(id) : null };
  }).filter(function (x) { return x.el; });
  var timeline = document.querySelector(".timeline");
  var ticking = false;

  function clamp(v) { return Math.max(0, Math.min(1, v)); }

  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    var max = root.scrollHeight - window.innerHeight;

    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? clamp(y / max) : 0) + ")";
    if (nav) nav.classList.toggle("scrolled", y > 40);
    root.style.setProperty("--p", Math.min(y, 900));

    // active nav link
    var current = null;
    spy.forEach(function (x) {
      if (x.el.getBoundingClientRect().top <= window.innerHeight * 0.35) current = x;
    });
    spy.forEach(function (x) { x.a.classList.toggle("active", x === current); });

    // timeline fill
    if (timeline) {
      var r = timeline.getBoundingClientRect();
      timeline.style.setProperty("--fill", clamp((window.innerHeight * 0.6 - r.top) / r.height).toFixed(3));
    }
  }

  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();
