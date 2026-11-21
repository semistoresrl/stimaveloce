/* StimaVeloce – Simulatore di dinamica 2.0
   Ricostruzione cinematica indicativa: percorsi disegnati col dito, animazione in tempo reale,
   frenata con tempo di reazione, rilevamento automatico del contatto, racconto generato,
   mappa reale in scala, link condivisibile. Schema indicativo, non è una perizia. */
(function () {
  "use strict";
  var svg = document.getElementById("sim"); if (!svg) return;
  var W = 800, H = 560, LANE = 56, G = 9.81, TR = 1.0, MAXT = 12, DT = 0.02;
  var COL = ["#1F5EFF", "#FF7A1A", "#14794A", "#8B5CF6", "#0B1B3A", "#D9304F"];
  var SIZE = { auto: [4.4, 1.8], moto: [2.1, 0.8], camion: [6.2, 2.3], bici: [1.8, 0.6], pedone: [0.6, 0.6] };
  var NOME = { auto: "auto", moto: "moto", camion: "furgone", bici: "bicicletta", pedone: "pedone" };
  var MU = { asciutto: 0.7, bagnato: 0.4, ghiaccio: 0.1 };
  var ROADN = { dritta: "rettilineo a due corsie", incrocio: "incrocio", rotonda: "rotatoria", parcheggio: "parcheggio", mappa: "mappa reale" };
  var S, sel = null, mode = "move", T = 0, playing = false, R = null, undo = [];
  var $ = function (q) { return document.querySelector(q); }, $$ = function (q) { return document.querySelectorAll(q); };
  function fresh() { return { road: "incrocio", surf: "asciutto", pxm: 16, map: null, items: [], seq: 0 }; }
  function snap() { undo.push(JSON.stringify(S)); if (undo.length > 40) undo.shift(); }
  function f1(n) { return (Math.round(n * 10) / 10).toFixed(1).replace(".", ","); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function byId(id) { for (var i = 0; i < S.items.length; i++) if (S.items[i].id === id) return S.items[i]; return null; }
  function movers() { return S.items.filter(function (i) { return i.t !== "urto"; }); }

  /* ---------- cinematica ---------- */
  function acc() { return (MU[S.surf] || .7) * G; }
  function sAt(it, t) {
    var v0 = (+it.kmh || 0) / 3.6; if (!v0) return 0;
    if (!it.brake || t <= TR) return v0 * t;
    var a = acc(), tb = t - TR, ts = v0 / a;
    return tb >= ts ? v0 * TR + v0 * v0 / (2 * a) : v0 * TR + v0 * tb - a * tb * tb / 2;
  }
  function vAt(it, t) {
    var v0 = (+it.kmh || 0) / 3.6; if (!it.brake || t <= TR) return v0;
    return Math.max(0, v0 - acc() * (t - TR));
  }
  function pathOf(it) {
    if (it.path && it.path.length > 1) return it.path;
    var a = it.r * Math.PI / 180; return [[it.x, it.y], [it.x + Math.cos(a) * 3000, it.y + Math.sin(a) * 3000]];
  }
  function pose(it, t) {
    if (it.t === "urto" || !t || !(+it.kmh)) return { x: it.x, y: it.y, a: it.r };
    var d = sAt(it, t) * S.pxm, p = pathOf(it);
    for (var i = 1; i < p.length; i++) {
      var dx = p[i][0] - p[i - 1][0], dy = p[i][1] - p[i - 1][1], L = Math.hypot(dx, dy);
      var ang = Math.atan2(dy, dx) * 180 / Math.PI;
      if (d <= L || i === p.length - 1) { var k = L ? Math.min(1, d / L) : 0; return { x: p[i - 1][0] + dx * k, y: p[i - 1][1] + dy * k, a: ang, end: d > L }; }
      d -= L;
    }
    return { x: it.x, y: it.y, a: it.r };
  }
  function half(it) { var s = SIZE[it.t] || SIZE.auto; return [s[0] * S.pxm / 2, s[1] * S.pxm / 2]; }
  function corners(it, p) {
    var h = half(it), a = p.a * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(function (k) { var x = k[0] * h[0], y = k[1] * h[1]; return [p.x + x * c - y * s, p.y + x * s + y * c]; });
  }
  function overlap(A, B) {
    var ax = [A, B];
    for (var q = 0; q < 2; q++) for (var i = 0; i < 2; i++) {
      var P = ax[q], nx = -(P[i + 1][1] - P[i][1]), ny = P[i + 1][0] - P[i][0];
      var pa = A.map(function (c) { return c[0] * nx + c[1] * ny; }), pb = B.map(function (c) { return c[0] * nx + c[1] * ny; });
      if (Math.max.apply(0, pa) < Math.min.apply(0, pb) || Math.max.apply(0, pb) < Math.min.apply(0, pa)) return false;
    }
    return true;
  }
  function inside(pt, C) {
    var s = null; for (var i = 0; i < 4; i++) { var a = C[i], b = C[(i + 1) % 4], cr = (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0]); if (s === null) s = cr > 0; else if ((cr > 0) !== s) return false; } return true;
  }
  function simulate() {
    var V = movers(), skip = {}, i, j;
    for (i = 0; i < V.length; i++) for (j = i + 1; j < V.length; j++) if (overlap(corners(V[i], pose(V[i], 0)), corners(V[j], pose(V[j], 0)))) skip[i + "_" + j] = 1;
    var res = { tc: null, end: MAXT };
    for (var t = DT; t <= MAXT; t += DT) {
      var P = V.map(function (it) { return pose(it, t); }), C = V.map(function (it, k) { return corners(it, P[k]); });
      for (i = 0; i < V.length; i++) for (j = i + 1; j < V.length; j++) {
        if (skip[i + "_" + j] || (!(+V[i].kmh) && !(+V[j].kmh))) continue;
        if (overlap(C[i], C[j])) {
          var pt = null; C[i].forEach(function (c) { if (!pt && inside(c, C[j])) pt = c; }); C[j].forEach(function (c) { if (!pt && inside(c, C[i])) pt = c; });
          if (!pt) pt = [(P[i].x + P[j].x) / 2, (P[i].y + P[j].y) / 2];
          res = { tc: t, end: t, a: V[i], b: V[j], pa: P[i], pb: P[j], pt: pt }; return res;
        }
      }
      var done = V.every(function (it, k) { return !(+it.kmh) || vAt(it, t) === 0 || P[k].end || P[k].x < -150 || P[k].x > W + 150 || P[k].y < -150 || P[k].y > H + 150; });
      if (done) { res.end = t; return res; }
    }
    return res;
  }

  /* ---------- disegno ---------- */
  function tilesSVG() {
    var m = S.map, n = Math.pow(2, m.z), lat = m.lat * Math.PI / 180;
    var gx = (m.lon + 180) / 360 * 256 * n, gy = (1 - Math.log(Math.tan(lat) + 1 / Math.cos(lat)) / Math.PI) / 2 * 256 * n;
    var k = m.k, x0 = gx - W / 2 / k, y0 = gy - H / 2 / k, out = "";
    for (var tx = Math.floor(x0 / 256); tx <= Math.floor((gx + W / 2 / k) / 256); tx++)
      for (var ty = Math.floor(y0 / 256); ty <= Math.floor((gy + H / 2 / k) / 256); ty++)
        out += '<image href="https://tile.openstreetmap.org/' + m.z + "/" + tx + "/" + ty + '.png" x="' + ((tx * 256 - x0) * k).toFixed(1) + '" y="' + ((ty * 256 - y0) * k).toFixed(1) + '" width="' + (256 * k + .5) + '" height="' + (256 * k + .5) + '" preserveAspectRatio="none"/>';
    return '<rect width="800" height="560" fill="#E9EEF5"/>' + out + '<rect x="0" y="536" width="250" height="24" fill="rgba(255,255,255,.85)"/><text x="8" y="553" font-size="12" fill="#333" font-family="Inter,sans-serif">© OpenStreetMap contributors</text>';
  }
  function roadSVG() {
    var A = "#C9D3EA", L = 'stroke="#fff" stroke-width="4" stroke-dasharray="18 14" fill="none"', o = '<rect width="800" height="560" fill="#E7F0E4"/>';
    if (S.road === "mappa" && S.map) return tilesSVG();
    if (S.road === "dritta") {
      o += '<rect x="0" y="' + (H / 2 - LANE) + '" width="800" height="' + LANE * 2 + '" fill="' + A + '"/><path d="M0 280H800" ' + L + '/>';
      o += '<rect x="0" y="216" width="800" height="8" fill="#B9C3D9"/><rect x="0" y="336" width="800" height="8" fill="#B9C3D9"/>';
      for (var z = 0; z < 7; z++) o += '<rect x="560" y="' + (228 + z * 16) + '" width="44" height="9" fill="#fff" opacity=".9"/>';
    } else if (S.road === "incrocio") {
      o += '<rect x="0" y="224" width="800" height="112" fill="' + A + '"/><rect x="344" y="0" width="112" height="560" fill="' + A + '"/>';
      o += '<path d="M0 280H330M470 280H800M400 0V210M400 350V560" ' + L + '/><path d="M340 224V336M460 224V336M344 220H456M344 340H456" stroke="#fff" stroke-width="3" opacity=".7"/>';
    } else if (S.road === "rotonda") {
      o += '<rect x="0" y="224" width="800" height="112" fill="' + A + '"/><rect x="344" y="0" width="112" height="560" fill="' + A + '"/><circle cx="400" cy="280" r="190" fill="' + A + '"/><circle cx="400" cy="280" r="80" fill="#BFDDB6" stroke="#fff" stroke-width="4"/><circle cx="400" cy="280" r="135" fill="none" ' + L + '/>';
    } else if (S.road === "parcheggio") {
      o += '<rect width="800" height="560" fill="' + A + '"/>';
      for (var i = 0; i < 10; i++) o += '<path d="M' + (20 + i * 84) + ' 0V150M' + (20 + i * 84) + ' 560V410" stroke="#fff" stroke-width="4"/>';
      o += '<path d="M0 280H800" ' + L + '/>';
    }
    return o;
  }
  function vehSVG(it, p, ghost) {
    var h = half(it), L = h[0] * 2, Wd = h[1] * 2, c = it.c, g = '<g transform="translate(' + p.x.toFixed(1) + " " + p.y.toFixed(1) + ") rotate(" + p.a.toFixed(1) + ')"' + (ghost ? ' opacity=".16"' : ' data-id="' + it.id + '" style="cursor:grab"') + ">";
    var hit = ghost ? "" : '<rect x="' + (-L / 2 - 8) + '" y="' + (-Wd / 2 - 8) + '" width="' + (L + 16) + '" height="' + (Wd + 16) + '" fill="transparent"/>';
    if (it.t === "urto") return '<g transform="translate(' + it.x + " " + it.y + ')" data-id="' + it.id + '" style="cursor:grab"><circle r="18" fill="rgba(255,122,26,.18)" stroke="#FF7A1A" stroke-width="4"/><path d="M-7 -7L7 7M7 -7L-7 7" stroke="#FF7A1A" stroke-width="4" stroke-linecap="round"/></g>';
    var s = sel === it.id && !ghost ? ' stroke="#0B1B3A" stroke-width="3"' : "";
    if (it.t === "pedone") return g + hit + '<ellipse rx="' + Wd * .45 + '" ry="' + Wd * .75 + '" fill="' + c + '"' + s + '/><circle r="' + Wd * .32 + '" fill="#F2C9A0"/></g>';
    if (it.t === "bici" || it.t === "moto") {
      var w = it.t === "moto" ? "#1b2333" : "#555";
      return g + hit + '<rect x="' + (-L / 2) + '" y="-2" width="' + (L * .28) + '" height="4" rx="2" fill="' + w + '"/><rect x="' + (L / 2 - L * .28) + '" y="-2" width="' + (L * .28) + '" height="4" rx="2" fill="' + w + '"/>' +
        '<rect x="' + (-L * .32) + '" y="' + (-Wd / 2) + '" width="' + (L * .64) + '" height="' + Wd + '" rx="' + Wd / 2 + '" fill="' + c + '"' + s + '/><path d="M' + (L * .22) + " " + (-Wd * .9) + "V" + (Wd * .9) + '" stroke="#1b2333" stroke-width="3" stroke-linecap="round"/><circle cx="' + (-L * .05) + '" r="' + Wd * .38 + '" fill="#0B1B3A"/></g>';
    }
    var o = g + hit + '<rect x="' + (-L / 2 + 3) + '" y="' + (-Wd / 2 - 2) + '" width="' + (L * .22) + '" height="' + (Wd + 4) + '" rx="3" fill="#1b2333"/><rect x="' + (L / 2 - 3 - L * .22) + '" y="' + (-Wd / 2 - 2) + '" width="' + (L * .22) + '" height="' + (Wd + 4) + '" rx="3" fill="#1b2333"/>';
    o += '<rect x="' + (-L / 2) + '" y="' + (-Wd / 2) + '" width="' + L + '" height="' + Wd + '" rx="' + Math.min(10, Wd * .3) + '" fill="' + c + '"' + s + "/>";
    if (it.t === "camion") o += '<rect x="' + (L / 2 - L * .26) + '" y="' + (-Wd / 2 + 3) + '" width="' + (L * .2) + '" height="' + (Wd - 6) + '" rx="3" fill="rgba(255,255,255,.8)"/><path d="M' + (L / 2 - L * .3) + " " + (-Wd / 2) + "V" + (Wd / 2) + '" stroke="rgba(0,0,0,.25)" stroke-width="2"/>';
    else o += '<path d="M' + (L * .16) + " " + (-Wd / 2 + 3) + "L" + (L * .3) + " " + (-Wd / 2 + 5) + "V" + (Wd / 2 - 5) + "L" + (L * .16) + " " + (Wd / 2 - 3) + 'Z" fill="rgba(255,255,255,.85)"/><path d="M' + (-L * .3) + " " + (-Wd / 2 + 4) + "L" + (-L * .38) + " " + (-Wd / 2 + 6) + "V" + (Wd / 2 - 6) + "L" + (-L * .3) + " " + (Wd / 2 - 4) + 'Z" fill="rgba(255,255,255,.7)"/>';
    o += '<circle cx="' + (L / 2 - 2) + '" cy="' + (-Wd / 2 + 4) + '" r="2.4" fill="#FFF7C2"/><circle cx="' + (L / 2 - 2) + '" cy="' + (Wd / 2 - 4) + '" r="2.4" fill="#FFF7C2"/>';
    return o + "</g>";
  }
  function fs(n) { var w = svg.clientWidth || 800; return Math.round(Math.max(n, Math.min(n * 1.9, 11 * W / w))); }
  function label(it, p, t) {
    if (it.t === "urto") return "";
    var v = t ? vAt(it, t) * 3.6 : +it.kmh || 0, txt = it.lab + (v ? " · " + Math.round(v) + " km/h" : it.t === "pedone" ? "" : " · fermo");
    return '<text x="' + p.x.toFixed(1) + '" y="' + (p.y - half(it)[0] - 12).toFixed(1) + '" text-anchor="middle" font-family="Inter,sans-serif" font-size="' + fs(15) + '" font-weight="800" fill="#0B1B3A" paint-order="stroke" stroke="#fff" stroke-width="5" pointer-events="none">' + esc(txt) + "</text>";
  }
  function pathSVG(it) {
    if (it.t === "urto" || !(+it.kmh) && !(it.path && it.path.length > 1)) return "";
    var p = it.path && it.path.length > 1 ? it.path : null, last, prev;
    if (!p) { var a = it.r * Math.PI / 180, len = Math.min(220, 40 + (+it.kmh) * 3); p = [[it.x, it.y], [it.x + Math.cos(a) * len, it.y + Math.sin(a) * len]]; }
    last = p[p.length - 1]; prev = p[p.length - 2];
    var an = Math.atan2(last[1] - prev[1], last[0] - prev[0]), ah = function (d) { return (last[0] + Math.cos(an + d) * 14).toFixed(1) + "," + (last[1] + Math.sin(an + d) * 14).toFixed(1); };
    return '<polyline points="' + p.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" ") + '" fill="none" stroke="' + it.c + '" stroke-width="4" stroke-dasharray="10 8" stroke-linecap="round" stroke-linejoin="round" opacity=".75" pointer-events="none"/>' +
      '<polygon points="' + last[0].toFixed(1) + "," + last[1].toFixed(1) + " " + ah(Math.PI - .45) + " " + ah(Math.PI + .45) + '" fill="' + it.c + '" opacity=".85" pointer-events="none"/>';
  }
  function stopAtT() { return R.tc != null ? R.tc : R.end; }
  function draw() {
    var o = roadSVG(), stopAt = stopAtT();
    S.items.forEach(function (it) { o += pathSVG(it); });
    if ($("[data-strobe]").checked) movers().forEach(function (it) { if (+it.kmh) for (var k = .5; k < stopAt - .05; k += .5) o += vehSVG(it, pose(it, k), true); });
    var P = {}; S.items.forEach(function (it) { P[it.id] = pose(it, T); o += vehSVG(it, P[it.id]); });
    if (R.tc != null && T >= R.tc - 1e-6) {
      var x = R.pt[0], y = R.pt[1], st = "";
      for (var i = 0; i < 16; i++) { var r = i % 2 ? 11 : 28, a = i * Math.PI / 8; st += (x + Math.cos(a) * r).toFixed(1) + "," + (y + Math.sin(a) * r).toFixed(1) + " "; }
      o += '<polygon class="sim-boom" points="' + st + '" fill="#FFD23F" stroke="#FF7A1A" stroke-width="3" pointer-events="none"/><text x="' + x.toFixed(1) + '" y="' + (y + 48).toFixed(1) + '" text-anchor="middle" font-family="Inter,sans-serif" font-size="' + fs(14) + '" font-weight="800" fill="#D9304F" paint-order="stroke" stroke="#fff" stroke-width="5" pointer-events="none">Contatto a ' + f1(R.tc) + " s</text>";
    }
    S.items.forEach(function (it) { o += label(it, P[it.id], T); });
    var s = sel && byId(sel);
    if (s && s.t !== "urto" && !T && mode === "move") {
      var p = P[s.id], an = p.a * Math.PI / 180, d = half(s)[0] + 26, hx = p.x + Math.cos(an) * d, hy = p.y + Math.sin(an) * d;
      o += '<line x1="' + p.x + '" y1="' + p.y + '" x2="' + hx + '" y2="' + hy + '" stroke="#0B1B3A" stroke-width="2" opacity=".4" pointer-events="none"/><g data-rot-h style="cursor:alias"><circle cx="' + hx + '" cy="' + hy + '" r="16" fill="#fff" stroke="#0B1B3A" stroke-width="2"/><path d="M' + (hx - 6) + " " + (hy + 2) + 'a6 6 0 1 1 6 6" fill="none" stroke="#0B1B3A" stroke-width="2"/></g>';
    }
    var bar = 10 * S.pxm, by = S.road === "mappa" ? 500 : 520;
    o += '<g font-family="Inter,sans-serif" font-size="12" font-weight="700" fill="#0B1B3A" pointer-events="none"><rect x="14" y="' + by + '" width="' + (bar + 46) + '" height="24" rx="8" fill="rgba(255,255,255,.88)"/><path d="M22 ' + (by + 12) + "h" + bar + '" stroke="#0B1B3A" stroke-width="3"/><text x="' + (28 + bar) + '" y="' + (by + 16) + '">10 m</text>' +
      '<g transform="translate(766 34)"><circle r="18" fill="rgba(255,255,255,.88)"/><path d="M0 -12L6 6L0 2L-6 6Z" fill="#0B1B3A"/></g>' +
      '<text x="786" y="' + (by + 30) + '" text-anchor="end" font-weight="500" fill="#4A5672" paint-order="stroke" stroke="#fff" stroke-width="4">Schema indicativo, non è una perizia · StimaVeloce</text></g>';
    if (mode === "path") o += '<rect width="800" height="560" fill="rgba(31,94,255,.07)" pointer-events="none"/>';
    svg.innerHTML = o;
    $("[data-tlabel]").textContent = f1(T) + " s";
    $("[data-time]").value = Math.round(T / (stopAt || 1) * 1000);
  }

  /* ---------- racconto ---------- */
  var DIR = ["est", "sud-est", "sud", "sud-ovest", "ovest", "nord-ovest", "nord", "nord-est"];
  function dir(a) { return DIR[((Math.round(a / 45) % 8) + 8) % 8]; }
  function stopDist(it) { var v = (+it.kmh || 0) / 3.6, r = v * TR, b = v * v / (2 * acc()); return [r, b, r + b]; }
  function story() {
    var V = movers(), out = [], h = "", box = $("[data-story]");
    if (!V.length) { box.innerHTML = '<p class="muted small">Aggiungi i veicoli per ottenere il racconto della dinamica.</p>'; box.setAttribute("data-text", ""); return; }
    var luogo = S.road === "mappa" && S.map ? "mappa reale" + (S.map.label ? " – " + S.map.label : "") : ROADN[S.road];
    out.push("Luogo: " + luogo + ". Fondo stradale: " + S.surf + ".");
    V.forEach(function (it) {
      var a0 = it.path && it.path.length > 1 ? Math.atan2(it.path[1][1] - it.path[0][1], it.path[1][0] - it.path[0][0]) * 180 / Math.PI : it.r;
      var turn = "";
      if (it.path && it.path.length > 2) { var n = it.path.length, a1 = Math.atan2(it.path[n - 1][1] - it.path[n - 2][1], it.path[n - 1][0] - it.path[n - 2][0]) * 180 / Math.PI, dd = ((a1 - a0) % 360 + 540) % 360 - 180; turn = Math.abs(dd) < 25 ? (Math.abs(dd) > 3 ? ", spostandosi di lato" : "") : dd > 0 ? ", poi svoltando a destra" : ", poi svoltando a sinistra"; }
      if (!(+it.kmh)) out.push(it.lab + " (" + NOME[it.t] + ") era fermo.");
      else out.push(it.lab + " (" + NOME[it.t] + ") procedeva verso " + dir(a0) + " a " + it.kmh + " km/h" + turn + (it.brake ? ", frenando dopo un tempo di reazione di 1 secondo." : ", senza frenare."));
    });
    if (R.tc != null) {
      var da = Math.abs(((R.pa.a - R.pb.a) % 360 + 540) % 360 - 180);
      var tipo = da > 150 ? "urto frontale" : da < 30 ? "tamponamento o strisciamento" : "urto laterale (angolo di circa " + Math.round(da) + "°)";
      out.push("Dopo " + f1(R.tc) + " secondi " + R.a.lab + " e " + R.b.lab + " entrano in contatto: " + tipo + ".");
      [R.a, R.b].forEach(function (it) { if (+it.kmh) out.push("Al contatto " + it.lab + " viaggiava a circa " + Math.round(vAt(it, R.tc) * 3.6) + " km/h e aveva percorso " + f1(sAt(it, R.tc)) + " m."); });
    } else out.push("Nella simulazione i veicoli non entrano in contatto.");
    var rows = V.filter(function (it) { return +it.kmh && it.t !== "pedone"; }).map(function (it) {
      var d = stopDist(it); return "<tr><td><b>" + esc(it.lab) + "</b> a " + it.kmh + " km/h</td><td>" + f1(d[0]) + " m</td><td>" + f1(d[1]) + " m</td><td><b>" + f1(d[2]) + " m</b></td></tr>";
    }).join("");
    h = '<p class="sim-text">' + out.map(esc).join("<br>") + "</p>";
    if (rows) h += '<div class="tbl-w"><table class="tbl"><thead><tr><th>Spazio di arresto</th><th>Reazione</th><th>Frenata</th><th>Totale</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
    h += '<p class="small muted">Calcolo indicativo: tempo di reazione 1 s, aderenza ' + String(MU[S.surf]).replace(".", ",") + " (fondo " + S.surf + "). Schema indicativo, non è una perizia.</p>";
    box.innerHTML = h;
    box.setAttribute("data-text", out.join("\n") + "\n(Schema indicativo realizzato con il simulatore StimaVeloce, non è una perizia.)");
  }

  /* ---------- aggiornamento ---------- */
  function update(keepT) {
    R = simulate(); if (!keepT) T = 0;
    var s = sel && byId(sel), box = $(".sim-sel");
    box.hidden = !s;
    if (s) {
      $("[data-sel-name]").textContent = s.t === "urto" ? "Punto d'urto" : NOME[s.t].charAt(0).toUpperCase() + NOME[s.t].slice(1) + " " + s.lab;
      $("#sim-lab").value = s.lab || ""; $("#sim-kmh").value = s.kmh || 0; $("#sim-kmhr").value = s.kmh || 0; $("#sim-brake").checked = !!s.brake;
      $$(".sim-mv").forEach(function (e) { e.hidden = s.t === "urto"; });
    }
    $("#sim-road").value = S.road; $("#sim-surf").value = S.surf;
    $(".sim-map").hidden = S.road !== "mappa";
    hint(); draw(); story(); save();
  }
  function hint() {
    var it = byId(sel);
    var h = mode === "path" ? "Ora trascina il dito sulla strada partendo da " + (it ? it.lab : "il veicolo") + ": disegna dove andava." :
      !S.items.length ? "Scegli una situazione oppure aggiungi i veicoli." :
      sel ? "Trascina per spostare, usa il pallino per girare. Poi premi «Guarda l'incidente»." : "Tocca un veicolo per modificarlo. Premi «Guarda l'incidente» per vedere la dinamica.";
    $("[data-hint]").textContent = h;
  }
  function save() { try { localStorage.setItem("sv_sim2", JSON.stringify(S)); } catch (e) {} }

  /* ---------- animazione ---------- */
  var last = 0;
  function frame(ts) {
    if (!playing) return;
    var stopAt = stopAtT(), dt = last ? Math.min(.1, (ts - last) / 1000) : 0; last = ts;
    T = Math.min(stopAt, T + dt * +$("[data-speed]").value);
    draw();
    if (T >= stopAt) { stop(); if (R.tc != null) { svg.classList.remove("shake"); void svg.getBoundingClientRect(); svg.classList.add("shake"); if (navigator.vibrate) try { navigator.vibrate(120); } catch (e) {} } return; }
    requestAnimationFrame(frame);
  }
  function play() {
    if (!movers().some(function (i) { return +i.kmh; })) { $("[data-hint]").textContent = "Imposta la velocità di almeno un veicolo."; return; }
    if (T >= stopAtT() - 1e-6) T = 0;
    playing = true; last = 0; mode = "move"; $("[data-play]").textContent = "❚❚ Pausa"; requestAnimationFrame(frame);
  }
  function stop() { playing = false; $("[data-play]").textContent = "▶ Guarda l'incidente"; }

  /* ---------- elementi ---------- */
  function add(t, x, y, r, kmh, path, brake) {
    var n = movers().length;
    var it = { id: "v" + (++S.seq), t: t, x: x != null ? x : 160 + (S.items.length * 90) % 480, y: y != null ? y : (n % 2 ? 252 : 308), r: r || 0, c: COL[n % COL.length], lab: t === "urto" ? "" : String.fromCharCode(65 + n), kmh: t === "urto" ? 0 : kmh != null ? kmh : t === "pedone" ? 5 : t === "bici" ? 15 : 40, path: path || null, brake: !!brake };
    S.items.push(it); return it;
  }
  function ring(t0, t1, step) { var o = []; for (var t = t0; step > 0 ? t <= t1 : t >= t1; t += step) o.push([400 + Math.cos(t * Math.PI / 180) * 135, 280 + Math.sin(t * Math.PI / 180) * 135]); return o; }
  var PRESET = {
    tamponamento: function () { S.road = "dritta"; add("auto", 110, 308, 0, 50, null, true); add("auto", 400, 308, 0, 10); },
    precedenza: function () { S.road = "incrocio"; add("auto", 90, 308, 0, 40); add("auto", 428, 540, 270, 30); },
    svolta: function () { S.road = "incrocio"; add("auto", 150, 308, 0, 30, [[150, 308], [330, 308], [372, 298], [408, 270], [426, 230], [428, 30]]); add("auto", 780, 252, 180, 45); },
    corsia: function () { S.road = "dritta"; add("auto", 150, 308, 0, 60, [[150, 308], [300, 306], [380, 280], [440, 254], [800, 252]]); add("auto", 40, 252, 0, 75, null, true); },
    rotatoria: function () { S.road = "rotonda"; add("auto", 60, 308, 0, 25, [[60, 308], [200, 306], [267, 303]].concat(ring(165, 95, -5))); var b = ring(290, 120, -5); add("auto", b[0][0], b[0][1], 200, 30, b); },
    parcheggio: function () { S.road = "dritta"; add("auto", 320, 372, 330, 8, [[320, 372], [350, 345], [395, 318], [460, 309], [800, 308]]); add("auto", 40, 308, 0, 40, null, true); },
    pedone: function () { S.road = "dritta"; var p = add("pedone", 582, 372, 270, 5); p.lab = "Pedone"; add("auto", 110, 308, 0, 50, null, true).lab = "A"; }
  };
  function preset(k) { snap(); stop(); S.items = []; S.seq = 0; S.map = null; S.pxm = 16; PRESET[k](); sel = null; mode = "move"; update(); svg.scrollIntoView({ behavior: "smooth", block: "center" }); setTimeout(play, 450); }

  /* ---------- puntatore ---------- */
  function pt(ev) { var r = svg.getBoundingClientRect(); return [(ev.clientX - r.left) * W / r.width, (ev.clientY - r.top) * H / r.height]; }
  var drag = null;
  svg.addEventListener("pointerdown", function (ev) {
    var p = pt(ev); if (playing) stop();
    if (mode === "path") { var it0 = byId(sel); if (!it0) { mode = "move"; return; } snap(); T = 0; it0.path = [[it0.x, it0.y]]; drag = { k: "path", it: it0 }; svg.setPointerCapture(ev.pointerId); return; }
    if (ev.target.closest("[data-rot-h]")) { snap(); drag = { k: "rot", it: byId(sel) }; svg.setPointerCapture(ev.pointerId); return; }
    var g = ev.target.closest("[data-id]");
    if (g) { snap(); T = 0; var v = byId(g.getAttribute("data-id")); sel = v.id; drag = { k: "move", it: v, dx: p[0] - v.x, dy: p[1] - v.y }; svg.setPointerCapture(ev.pointerId); update(); return; }
    if (S.road === "mappa" && S.map) { snap(); drag = { k: "pan", x: p[0], y: p[1] }; svg.setPointerCapture(ev.pointerId); return; }
    if (T > 0) { T = 0; draw(); return; }
    if (sel) { sel = null; update(true); }
  });
  svg.addEventListener("pointermove", function (ev) {
    if (!drag) return; var p = pt(ev), it = drag.it;
    if (drag.k === "move") {
      var nx = Math.max(6, Math.min(W - 6, p[0] - drag.dx)), ny = Math.max(6, Math.min(H - 6, p[1] - drag.dy)), dx = nx - it.x, dy = ny - it.y;
      it.x = nx; it.y = ny; if (it.path) it.path = it.path.map(function (q) { return [q[0] + dx, q[1] + dy]; });
    } else if (drag.k === "rot") {
      it.r = Math.round(Math.atan2(p[1] - it.y, p[0] - it.x) * 180 / Math.PI / 5) * 5; it.path = null;
    } else if (drag.k === "path") {
      var l = it.path[it.path.length - 1]; if (Math.hypot(p[0] - l[0], p[1] - l[1]) > 7) it.path.push([Math.round(p[0]), Math.round(p[1])]);
      if (it.path.length === 3) it.r = Math.atan2(it.path[2][1] - it.path[0][1], it.path[2][0] - it.path[0][0]) * 180 / Math.PI;
    } else if (drag.k === "pan") {
      var ddx = p[0] - drag.x, ddy = p[1] - drag.y; drag.x = p[0]; drag.y = p[1]; panMap(ddx, ddy);
    }
    draw();
  });
  function end() {
    if (!drag) return;
    if (drag.k === "path") { var it = drag.it; if (it.path.length < 3) it.path = null; else if (!(+it.kmh)) it.kmh = it.t === "pedone" ? 5 : 30; mode = "move"; }
    drag = null; update();
  }
  svg.addEventListener("pointerup", end); svg.addEventListener("pointercancel", end);

  /* ---------- mappa reale ---------- */
  function setPxm() { var m = S.map; S.pxm = m.k / (156543.03392 * Math.cos(m.lat * Math.PI / 180) / Math.pow(2, m.z)); }
  function panMap(dx, dy) {
    var m = S.map, n = Math.pow(2, m.z), lat = m.lat * Math.PI / 180;
    var gx = (m.lon + 180) / 360 * 256 * n - dx / m.k, gy = (1 - Math.log(Math.tan(lat) + 1 / Math.cos(lat)) / Math.PI) / 2 * 256 * n - dy / m.k;
    m.lon = gx / (256 * n) * 360 - 180; m.lat = Math.atan(Math.sinh(Math.PI * (1 - 2 * gy / (256 * n)))) * 180 / Math.PI;
    S.items.forEach(function (it) { it.x += dx; it.y += dy; if (it.path) it.path = it.path.map(function (q) { return [q[0] + dx, q[1] + dy]; }); });
  }
  function zoom(f) {
    var m = S.map; if (!m) return; var k2 = Math.max(1, Math.min(4, m.k * f)), r = k2 / m.k; if (r === 1) return; snap();
    S.items.forEach(function (it) { it.x = 400 + (it.x - 400) * r; it.y = 280 + (it.y - 280) * r; if (it.path) it.path = it.path.map(function (q) { return [400 + (q[0] - 400) * r, 280 + (q[1] - 280) * r]; }); });
    m.k = k2; setPxm(); update();
  }
  function goMap(lat, lon, lab) {
    snap(); S.road = "mappa"; S.map = { lat: lat, lon: lon, z: 19, k: 2, label: lab || "" }; setPxm();
    S.items = []; S.seq = 0; sel = null; update();
    $("[data-map-msg]").textContent = (lab ? "Trovato: " + lab + ". " : "") + "Trascina la mappa per centrarla, poi aggiungi i veicoli.";
  }
  $("[data-find]").addEventListener("click", function () {
    var q = $("#sim-addr").value.trim(); if (!q) return; var msg = $("[data-map-msg]"); msg.textContent = "Cerco…";
    fetch("https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=it&accept-language=it&q=" + encodeURIComponent(q))
      .then(function (r) { return r.json(); }).then(function (j) { if (!j.length) { msg.textContent = "Indirizzo non trovato: prova ad aggiungere il comune."; return; } goMap(+j[0].lat, +j[0].lon, j[0].display_name.split(",").slice(0, 3).join(",")); })
      .catch(function () { msg.textContent = "Ricerca non disponibile in questo momento."; });
  });
  $("#sim-addr").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); $("[data-find]").click(); } });
  $("[data-gps]").addEventListener("click", function () {
    var msg = $("[data-map-msg]"); if (!navigator.geolocation) { msg.textContent = "Posizione non disponibile su questo dispositivo."; return; }
    msg.textContent = "Rilevo la posizione…";
    navigator.geolocation.getCurrentPosition(function (p) { goMap(p.coords.latitude, p.coords.longitude, "posizione attuale"); }, function () { msg.textContent = "Non è stato possibile rilevare la posizione."; }, { enableHighAccuracy: true, timeout: 10000 });
  });
  $$("[data-zoom]").forEach(function (b) { b.addEventListener("click", function () { zoom(+b.getAttribute("data-zoom")); }); });

  /* ---------- comandi ---------- */
  $$("[data-preset]").forEach(function (b) { b.addEventListener("click", function () { preset(b.getAttribute("data-preset")); }); });
  $$("[data-add-v]").forEach(function (b) { b.addEventListener("click", function () {
    snap(); stop(); var t = b.getAttribute("data-add-v"), it = add(t);
    if (t === "urto") { it.x = 400; it.y = 280; } if (t === "pedone") { it.r = 270; it.y = 372; }
    sel = it.id; update(); svg.scrollIntoView({ behavior: "smooth", block: "center" });
  }); });
  $("#sim-road").addEventListener("change", function (e) {
    snap(); S.road = e.target.value; if (S.road !== "mappa") { S.map = null; S.pxm = 16; } update();
    if (S.road === "mappa" && !S.map) { $("[data-map-msg]").textContent = "Cerca l'indirizzo o usa la tua posizione."; $("#sim-addr").focus(); }
  });
  $("#sim-surf").addEventListener("change", function (e) { snap(); S.surf = e.target.value; update(); });
  function setSel(fn) { var it = byId(sel); if (!it) return; fn(it); update(); }
  $("#sim-lab").addEventListener("change", function (e) { snap(); setSel(function (it) { it.lab = e.target.value.slice(0, 14) || it.lab; }); });
  function setK(v) { setSel(function (it) { it.kmh = Math.max(0, Math.min(200, Math.round(+v || 0))); }); }
  $("#sim-kmh").addEventListener("change", function (e) { snap(); setK(e.target.value); });
  $("#sim-kmhr").addEventListener("input", function (e) { setK(e.target.value); });
  $("#sim-kmhr").addEventListener("pointerdown", snap);
  $("#sim-brake").addEventListener("change", function (e) { snap(); setSel(function (it) { it.brake = e.target.checked; }); });
  $$("[data-rot]").forEach(function (b) { b.addEventListener("click", function () { snap(); setSel(function (it) { it.r = (it.r + (+b.getAttribute("data-rot"))) % 360; it.path = null; }); }); });
  $("[data-draw]").addEventListener("click", function () { if (!sel) return; stop(); T = 0; mode = "path"; hint(); draw(); svg.scrollIntoView({ behavior: "smooth", block: "center" }); });
  $("[data-clear-path]").addEventListener("click", function () { snap(); setSel(function (it) { it.path = null; }); });
  $("[data-del-v]").addEventListener("click", function () { snap(); S.items = S.items.filter(function (i) { return i.id !== sel; }); sel = null; update(); });
  $("[data-play]").addEventListener("click", function () { playing ? stop() : play(); });
  $("[data-time]").addEventListener("input", function (e) { stop(); T = (+e.target.value / 1000) * stopAtT(); draw(); });
  $("[data-strobe]").addEventListener("change", draw);
  $("[data-undo]").addEventListener("click", function () { if (!undo.length) return; stop(); S = JSON.parse(undo.pop()); if (sel && !byId(sel)) sel = null; mode = "move"; update(); });
  $("[data-reset]").addEventListener("click", function () { snap(); stop(); S = fresh(); sel = null; mode = "move"; if (location.hash) history.replaceState(null, "", location.pathname); update(); });
  $("[data-copy]").addEventListener("click", function (e) {
    var t = $("[data-story]").getAttribute("data-text") || "", b = e.currentTarget;
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { b.textContent = "Copiato ✓"; setTimeout(function () { b.textContent = "Copia il racconto"; }, 1800); }, function () { window.prompt("Copia il testo:", t); });
  });
  $("[data-share]").addEventListener("click", function (e) {
    var b = e.currentTarget, url = location.origin + location.pathname + "#s=" + btoa(unescape(encodeURIComponent(JSON.stringify(S))));
    if (navigator.share) navigator.share({ title: "Dinamica dell'incidente – StimaVeloce", text: "Ecco lo schema della dinamica (indicativo):", url: url }).catch(function () {});
    else (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { b.textContent = "Link copiato ✓"; setTimeout(function () { b.textContent = "Condividi link"; }, 1800); }, function () { window.prompt("Copia il link:", url); });
  });
  $("[data-export]").addEventListener("click", function () {
    var prevT = T; if (R.tc != null) T = R.tc; var pm = mode, ps = sel; mode = "move"; sel = null; draw();
    var clone = svg.cloneNode(true); T = prevT; mode = pm; sel = ps; draw();
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg"); clone.setAttribute("width", 1600); clone.setAttribute("height", 1120);
    var imgs = Array.prototype.slice.call(clone.querySelectorAll("image"));
    Promise.all(imgs.map(function (im) {
      return fetch(im.getAttribute("href")).then(function (r) { return r.blob(); }).then(function (b) { return new Promise(function (ok) { var fr = new FileReader(); fr.onload = function () { im.setAttribute("href", fr.result); ok(); }; fr.readAsDataURL(b); }); }).catch(function () { im.remove(); });
    })).then(function () {
      var img = new Image(); img.onload = function () {
        var c = document.createElement("canvas"); c.width = 1600; c.height = 1120; var x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, 1600, 1120); x.drawImage(img, 0, 0, 1600, 1120);
        c.toBlob(function (b) { var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = "dinamica-incidente-stimaveloce.png"; document.body.appendChild(a); a.click(); a.remove(); });
      };
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(new XMLSerializer().serializeToString(clone));
    });
  });
  $("[data-print]").addEventListener("click", function () { window.print(); });
  var tBefore = 0;
  window.addEventListener("beforeprint", function () { tBefore = T; stop(); if (R.tc != null) T = R.tc; draw(); });
  window.addEventListener("afterprint", function () { T = tBefore; draw(); });

  /* ---------- avvio ---------- */
  S = fresh();
  try {
    var m = /#s=([^&]+)/.exec(location.hash);
    var loaded = m ? JSON.parse(decodeURIComponent(escape(atob(m[1])))) : JSON.parse(localStorage.getItem("sv_sim2") || "null");
    if (loaded && loaded.items) { S = Object.assign(fresh(), loaded); S.items = S.items.filter(function (i) { return SIZE[i.t] || i.t === "urto"; }); }
  } catch (e) { S = fresh(); }
  if (S.road === "mappa" && S.map) setPxm();
  if (!S.items.length && S.road !== "mappa") PRESET.precedenza();
  window.addEventListener("resize", function () { if (!playing) draw(); });
  update();
  window.__sim = { get: function () { return { S: S, R: R, T: T }; }, preset: preset };
})();
