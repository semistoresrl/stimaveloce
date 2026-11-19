/* StimaVeloce – simulatore di dinamica (schema indicativo, non è una perizia) */
(function () {
  "use strict";
  var svg = document.getElementById("sim"); if (!svg) return;
  var NS = "http://www.w3.org/2000/svg", W = 800, H = 560, LANE = 56; // 1 corsia = 56 px ≈ 3,5 m → 16 px/m
  var PXM = LANE / 3.5;
  var road = "incrocio", items = [], sel = null, seq = 0;
  var COL = ["#1F5EFF", "#FF7A1A", "#14794A", "#8B5CF6", "#0B1B3A"];
  var SIZE = { auto: [4.4, 1.8], moto: [2.1, 0.8], camion: [6.0, 2.2] };
  function el(n, a, p) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function roadSVG() {
    var g = el("g", { "data-road": "1" }), asphalt = "#C9D3EA", line = { stroke: "#fff", "stroke-width": 4, "stroke-dasharray": "18 14" };
    el("rect", { x: 0, y: 0, width: W, height: H, fill: "#E7F0E4" }, g);
    if (road === "dritta") { el("rect", { x: 0, y: H / 2 - LANE, width: W, height: LANE * 2, fill: asphalt }, g); el("path", Object.assign({ d: "M0 " + H / 2 + " H" + W }, line), g); }
    if (road === "incrocio") {
      el("rect", { x: 0, y: H / 2 - LANE, width: W, height: LANE * 2, fill: asphalt }, g); el("rect", { x: W / 2 - LANE, y: 0, width: LANE * 2, height: H, fill: asphalt }, g);
      el("path", Object.assign({ d: "M0 " + H / 2 + " H" + (W / 2 - LANE - 10) + " M" + (W / 2 + LANE + 10) + " " + H / 2 + " H" + W + " M" + W / 2 + " 0 V" + (H / 2 - LANE - 10) + " M" + W / 2 + " " + (H / 2 + LANE + 10) + " V" + H }, line), g);
    }
    if (road === "rotonda") {
      el("rect", { x: 0, y: H / 2 - LANE, width: W, height: LANE * 2, fill: asphalt }, g); el("rect", { x: W / 2 - LANE, y: 0, width: LANE * 2, height: H, fill: asphalt }, g);
      el("circle", { cx: W / 2, cy: H / 2, r: 190, fill: asphalt }, g); el("circle", { cx: W / 2, cy: H / 2, r: 80, fill: "#BFDDB6", stroke: "#fff", "stroke-width": 4 }, g);
    }
    if (road === "parcheggio") {
      el("rect", { x: 0, y: 0, width: W, height: H, fill: asphalt }, g);
      for (var i = 0; i < 9; i++) { el("path", { d: "M" + (40 + i * 84) + " 0 V150 M" + (40 + i * 84) + " " + H + " V" + (H - 150), stroke: "#fff", "stroke-width": 4 }, g); }
    }
    return g;
  }
  function vehicle(it) {
    var g = el("g", { "data-id": it.id, transform: "translate(" + it.x + " " + it.y + ") rotate(" + it.r + ")", style: "cursor:grab" });
    if (it.t === "urto") {
      el("circle", { r: 16, fill: "rgba(255,122,26,.18)", stroke: "#FF7A1A", "stroke-width": 4 }, g);
      el("path", { d: "M-7 -7 L7 7 M7 -7 L-7 7", stroke: "#FF7A1A", "stroke-width": 4, "stroke-linecap": "round" }, g);
    } else {
      var L = SIZE[it.t][0] * PXM, Wd = SIZE[it.t][1] * PXM;
      el("rect", { x: -L / 2, y: -Wd / 2, width: L, height: Wd, rx: it.t === "moto" ? Wd / 2 : 8, fill: it.c, stroke: sel === it.id ? "#0B1B3A" : "none", "stroke-width": 3 }, g);
      if (it.t !== "moto") el("rect", { x: L / 2 - L * .36, y: -Wd / 2 + 5, width: L * .18, height: Wd - 10, rx: 4, fill: "rgba(255,255,255,.75)" }, g);
      el("path", { d: "M" + (L / 2 + 6) + " 0 l12 0 m-6 -6 l6 6 l-6 6", stroke: it.c, "stroke-width": 3, fill: "none", "stroke-linecap": "round" }, g);
    }
    var lab = it.lab + (it.kmh ? " · " + it.kmh + " km/h" : "");
    if (lab) {
      var tg = el("g", { transform: "rotate(" + (-it.r) + ")" }, g);
      var tx = el("text", { x: 0, y: -26, "text-anchor": "middle", "font-family": "Inter,sans-serif", "font-size": 15, "font-weight": 700, fill: "#0B1B3A", "paint-order": "stroke", stroke: "#fff", "stroke-width": 4 }, tg);
      tx.textContent = lab;
    }
    return g;
  }
  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.appendChild(roadSVG());
    var vs = items.filter(function (i) { return i.t !== "urto"; });
    if (vs.length >= 2) {
      var a = vs[0], b = vs[1], d = Math.hypot(a.x - b.x, a.y - b.y) / PXM;
      el("path", { d: "M" + a.x + " " + a.y + " L" + b.x + " " + b.y, stroke: "#0B1B3A", "stroke-width": 2, "stroke-dasharray": "6 6", opacity: .5 }, svg);
      var t = el("text", { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 - 8, "text-anchor": "middle", "font-family": "Inter,sans-serif", "font-size": 13, "font-weight": 700, fill: "#0B1B3A", "paint-order": "stroke", stroke: "#fff", "stroke-width": 4 }, svg);
      t.textContent = "≈ " + d.toFixed(1).replace(".", ",") + " m";
      document.querySelector("[data-dist]").textContent = "Distanza tra " + a.lab + " e " + b.lab + ": circa " + d.toFixed(1).replace(".", ",") + " m (tra i centri dei veicoli).";
    } else document.querySelector("[data-dist]").textContent = "Aggiungi almeno due veicoli per vedere la distanza.";
    items.forEach(function (it) { svg.appendChild(vehicle(it)); });
    var nt = el("text", { x: W - 12, y: H - 12, "text-anchor": "end", "font-family": "Inter,sans-serif", "font-size": 13, fill: "#4A5672" }, svg);
    nt.textContent = "Schema indicativo, non è una perizia · StimaVeloce";
    var p = document.querySelector(".sim-sel"), it = items.filter(function (i) { return i.id === sel; })[0];
    p.hidden = !it;
    if (it) { document.querySelector("[data-sel-name]").textContent = it.t === "urto" ? "Punto d'urto" : "Veicolo " + it.lab; document.getElementById("sim-lab").value = it.lab; document.getElementById("sim-kmh").value = it.kmh || ""; document.getElementById("sim-kmh").disabled = it.t === "urto"; }
    try { localStorage.setItem("sv_sim", JSON.stringify({ road: road, items: items, seq: seq })); } catch (e) {}
  }
  function add(t) {
    var n = items.filter(function (i) { return i.t !== "urto"; }).length;
    var it = { id: "v" + (++seq), t: t, x: 200 + (items.length * 70) % 420, y: H / 2 - LANE / 2 + (n % 2) * LANE, r: 0, c: COL[n % COL.length], lab: t === "urto" ? "" : String.fromCharCode(65 + n), kmh: "" };
    if (t === "urto") { it.x = W / 2; it.y = H / 2; }
    items.push(it); sel = it.id; draw();
  }
  function pt(ev) { var r = svg.getBoundingClientRect(); return { x: (ev.clientX - r.left) * W / r.width, y: (ev.clientY - r.top) * H / r.height }; }
  var drag = null;
  svg.addEventListener("pointerdown", function (ev) {
    var g = ev.target.closest("[data-id]"); if (!g) { sel = null; draw(); return; }
    var it = items.filter(function (i) { return i.id === g.getAttribute("data-id"); })[0]; sel = it.id;
    var p = pt(ev); drag = { it: it, dx: p.x - it.x, dy: p.y - it.y }; svg.setPointerCapture(ev.pointerId); draw();
  });
  svg.addEventListener("pointermove", function (ev) { if (!drag) return; var p = pt(ev); drag.it.x = Math.max(10, Math.min(W - 10, p.x - drag.dx)); drag.it.y = Math.max(10, Math.min(H - 10, p.y - drag.dy)); draw(); });
  svg.addEventListener("pointerup", function () { drag = null; });
  document.querySelectorAll("[data-add-v]").forEach(function (b) { b.addEventListener("click", function () { add(b.getAttribute("data-add-v")); }); });
  document.querySelectorAll("[data-rot]").forEach(function (b) { b.addEventListener("click", function () { var it = items.filter(function (i) { return i.id === sel; })[0]; if (it) { it.r = (it.r + (+b.getAttribute("data-rot"))) % 360; draw(); } }); });
  document.querySelector("[data-del-v]").addEventListener("click", function () { items = items.filter(function (i) { return i.id !== sel; }); sel = null; draw(); });
  document.getElementById("sim-lab").addEventListener("input", function (e) { var it = items.filter(function (i) { return i.id === sel; })[0]; if (it) { it.lab = e.target.value; draw(); e.target.focus(); } });
  document.getElementById("sim-kmh").addEventListener("input", function (e) { var it = items.filter(function (i) { return i.id === sel; })[0]; if (it) { it.kmh = e.target.value; draw(); e.target.focus(); } });
  document.getElementById("sim-road").addEventListener("change", function (e) { road = e.target.value; draw(); });
  document.querySelector("[data-reset]").addEventListener("click", function () { items = []; sel = null; seq = 0; add("auto"); add("auto"); sel = null; draw(); });
  document.querySelector("[data-export]").addEventListener("click", function () {
    var xml = new XMLSerializer().serializeToString(svg).replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1120"');
    var img = new Image(); img.onload = function () {
      var c = document.createElement("canvas"); c.width = 1600; c.height = 1120; var x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, 1600, 1120); x.drawImage(img, 0, 0, 1600, 1120);
      c.toBlob(function (b) { var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = "schema-dinamica-stimaveloce.png"; document.body.appendChild(a); a.click(); a.remove(); });
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(xml);
  });
  try { var s = JSON.parse(localStorage.getItem("sv_sim") || "null"); if (s && s.items) { road = s.road; items = s.items; seq = s.seq || items.length; document.getElementById("sim-road").value = road; } } catch (e) {}
  document.getElementById("sim-road").value = road;
  if (!items.length) { add("auto"); items[0].x = 230; items[0].y = H / 2 + LANE / 2; add("auto"); items[1].x = W / 2 - LANE / 2; items[1].y = 120; items[1].r = 90; sel = null; }
  draw();
})();
