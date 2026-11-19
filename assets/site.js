/* StimaVeloce – navigazione, ricerca, animazioni leggere */
(function () {
  "use strict";
  var IDX = null;
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function load(cb) { if (IDX) return cb(IDX); fetch("/assets/search.json").then(function (r) { return r.json(); }).then(function (d) { IDX = d; cb(d); }).catch(function () { cb([]); }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function search(input) {
    var out = input.parentNode.querySelector("[data-srch-res]"), q = norm(input.value.trim());
    if (q.length < 2) { out.innerHTML = ""; return; }
    load(function (idx) {
      var words = q.split(/\s+/).map(function (w) { return w.length > 5 ? w.slice(0, -1) : w; });
      var res = idx.map(function (p) { var t = norm(p.t), d = norm(p.d), sc = 0;
        words.forEach(function (w) { if (t.indexOf(w) > -1) sc += 3; else if (d.indexOf(w) > -1) sc += 1; else sc -= 5; });
        return { p: p, s: sc }; }).filter(function (x) { return x.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
      out.innerHTML = res.length ? res.map(function (x) { return '<li><a href="' + esc(x.p.u) + '">' + esc(x.p.t) + "<small>" + esc(x.p.d) + "</small></a></li>"; }).join("")
        : '<li style="padding:10px 4px;color:#5C646D">Nessun risultato. Prova con altre parole o <a href="/app/#prefattibilita">descrivi il tuo caso</a>.</li>';
    });
  }
  document.addEventListener("input", function (e) { if (e.target.hasAttribute && e.target.hasAttribute("data-srch")) search(e.target); });
  var dlg = document.querySelector("[data-srch-dlg]");
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-open-srch]");
    if (b && dlg && dlg.showModal) { dlg.showModal(); var i = dlg.querySelector("[data-srch]"); if (i) i.focus(); return; }
    document.querySelectorAll("details.dd[open]").forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute("open"); });
    var a = e.target.closest && e.target.closest(".mnav .panel a");
    if (a) { var m = a.closest(".mnav"); if (m) m.removeAttribute("open"); }
  });
  document.addEventListener("keydown", function (e) {
    if ((e.key === "/" && !/input|textarea|select/i.test((document.activeElement || {}).tagName)) || (e.key === "k" && (e.ctrlKey || e.metaKey))) {
      if (dlg && dlg.showModal) { e.preventDefault(); dlg.showModal(); var i = dlg.querySelector("[data-srch]"); if (i) i.focus(); }
    }
    if (e.key === "Escape") document.querySelectorAll("details.dd[open],details.mnav[open]").forEach(function (d) { d.removeAttribute("open"); });
  });
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var rv = document.querySelectorAll(".rv");
  if (!("IntersectionObserver" in window) || reduce) { rv.forEach(function (el) { el.classList.add("is-in"); }); }
  else {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("is-in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  }
  var steps = document.querySelectorAll(".story-step"), items = document.querySelectorAll(".story-nav li");
  if (steps.length && "IntersectionObserver" in window) {
    var so = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { var n = x.target.getAttribute("data-step"); items.forEach(function (li) { li.classList.toggle("on", li.getAttribute("data-step") === n); }); } }); }, { rootMargin: "-40% 0px -50% 0px" });
    steps.forEach(function (s) { so.observe(s); });
  }
})();
(function () {
  "use strict";
  document.addEventListener("click", function (e) {
    var m = e.target.closest && e.target.closest("[data-open-menu]");
    if (m) { e.preventDefault(); var d = document.getElementById("menu"); if (d) { d.setAttribute("open", ""); window.scrollTo({ top: 0 }); } return; }
    var w = e.target.closest && e.target.closest("[data-open-wa]");
    if (w) { var dl = document.querySelector("[data-wa]"); if (dl && dl.showModal) dl.showModal(); }
  });
  var mot = new URLSearchParams(location.search).get("motivo"), sel = document.getElementById("c-mot");
  if (mot && sel) { for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === mot) sel.selectedIndex = i; }
})();
