/* StimaVeloce – calcolatori. Ogni risultato mostra i passaggi. */
(function () {
  "use strict";
  var EUR = new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR" });
  var PCT = new Intl.NumberFormat("it-IT", { maximumFractionDigits: 2 });
  function eur(x) { return EUR.format(isFinite(x) ? x : 0); }
  function n(v) { if (v == null || v === "") return NaN; return parseFloat(String(v).replace(/\./g, "").replace(",", ".")) ; }
  function num(form, k, def) { var el = form.elements[k]; if (!el) return def; var v = el.type === "number" || el.type === "date" ? el.value : el.value; var x = el.type === "number" ? parseFloat(v) : n(v); return isNaN(x) ? def : x; }
  function val(form, k) { var el = form.elements[k]; return el ? el.value : ""; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function table(rows) { return rows.map(function (r) { return "<tr" + (r[2] ? ' class="tot"' : "") + "><td>" + r[0] + "</td><td>" + r[1] + "</td></tr>"; }).join(""); }

  var PRZ = null, PRZ_META = null;
  var FREE = { code: "", n: "Voce libera (prezzo da preventivo)", u: "corpo", p: null };
  function voci(box) {
    var cats = (box.getAttribute("data-cats") || "edili,idraulici,elettrici").split(",");
    return (PRZ || []).filter(function (v) { return cats.indexOf(v.cat) > -1; }).concat([FREE]);
  }
  function addLine(box, d, list) {
    d = d || {};
    var i = box.children.length, L = list || voci(box.closest("[data-calc]"));
    var opts = L.map(function (v, k) { return '<option value="' + k + '"' + ((d.code && v.code === d.code) || (!d.code && !v.code && d.free) ? " selected" : "") + ">" + esc(v.n) + "</option>"; }).join("");
    var cur = L.filter(function (v) { return d.code ? v.code === d.code : !v.code; })[0] || L[0];
    var el = document.createElement("div");
    el.className = "line";
    el.innerHTML = '<div class="fld wide"><label class="small" for="ld' + i + '">Lavorazione</label><select class="in" id="ld' + i + '" data-l="desc">' + opts + '</select><span class="hint" data-l="code">' + esc(cur.code ? cur.code.replace("CAM26_", "Prezzario Campania 2026 · ") : "Inserisci il prezzo del tuo preventivo") + "</span></div>" +
      '<div class="fld"><label class="small" for="lu' + i + '">Unità</label><input class="in" id="lu' + i + '" data-l="u" value="' + esc(cur.u) + '"></div>' +
      '<div class="fld"><label class="small" for="lq' + i + '">Quantità</label><input class="in" id="lq' + i + '" data-l="q" type="number" min="0" step="any" inputmode="decimal" value="' + (d.q == null ? "" : d.q) + '"></div>' +
      '<div class="fld"><label class="small" for="lp' + i + '">Prezzo unit. €</label><input class="in" id="lp' + i + '" data-l="p" type="number" min="0" step="any" inputmode="decimal" placeholder="es. 25" value="' + (cur.p == null ? (d.p == null ? "" : d.p) : cur.p) + '"></div>' +
      '<button type="button" aria-label="Rimuovi voce" data-del>×</button>';
    el._list = L;
    box.appendChild(el);
  }
  function lines(form) {
    var out = [];
    form.querySelectorAll(".line").forEach(function (l) {
      if (!l.querySelector('[data-l="desc"]')) return;
      var q = parseFloat(l.querySelector('[data-l="q"]').value), p = parseFloat(l.querySelector('[data-l="p"]').value), v = (l._list || [])[+l.querySelector('[data-l="desc"]').value] || {};
      var official = v.code && v.p != null && Math.abs(p - v.p) < 0.005;
      out.push({ desc: v.n || l.querySelector('[data-l="desc"]').selectedOptions[0].text, code: official ? v.code : "", u: l.querySelector('[data-l="u"]').value, q: isNaN(q) ? 0 : q, p: isNaN(p) ? 0 : p });
    });
    return out;
  }
  function linesRows(ls) {
    return ls.filter(function (l) { return l.q && l.p; }).map(function (l) { return [esc(l.desc) + ' <span class="muted">' + PCT.format(l.q) + " " + esc(l.u) + " × " + eur(l.p) + (l.code ? " · " + esc(l.code.replace("CAM26_", "")) : " · prezzo inserito") + "</span>", eur(l.q * l.p)]; });
  }
  var TPL = {
    "danni-fabbricato": [{ code: "CAM26_R02.040.010.A", q: 18 }, { code: "CAM26_E16.020.030.A", q: 18 }, { code: "CAM26_E21.020.030.A", q: 64 }],
    "preventivo-lavori": [{ code: "CAM26_R02.060.040.A", q: 20 }, { code: "CAM26_E07.010.010.A", q: 20 }, { code: "CAM26_E13.030.020.A", q: 20 }, { code: "CAM26_E15.080.050.A", q: 18 }],
    "stime-edili": [{ code: "CAM26_R02.040.010.A", q: 12 }, { code: "CAM26_E16.020.030.A", q: 12 }, { code: "CAM26_E16.020.080.A", q: 30 }, { code: "CAM26_E21.020.030.A", q: 60 }],
    "stime-idrauliche": [{ code: "CAM26_R02.050.010.A", q: 1 }, { code: "CAM26_I01.010.010.A", q: 2 }, { free: 1, q: 1 }],
    "stime-elettriche": [{ code: "CAM26_L01.010.010.A", q: 3 }, { code: "CAM26_L01.010.090.A", q: 6 }],
    "stime-ripristino": [{ code: "CAM26_R02.040.010.A", q: 18 }, { code: "CAM26_E16.020.030.A", q: 18 }, { code: "CAM26_E21.020.030.B", q: 64 }, { code: "CAM26_R02.060.040.A", q: 12 }, { code: "CAM26_E07.010.010.A", q: 12 }, { code: "CAM26_E13.030.020.A", q: 12 }, { code: "CAM26_E15.080.050.A", q: 14 }]
  };

  var C = {};

  C["danni-fabbricato"] = function (f) {
    var ls = lines(f), imp = ls.reduce(function (s, l) { return s + l.q * l.p; }, 0);
    var acc = imp * num(f, "acc", 0) / 100, ivaP = num(f, "iva", 0), iva = (imp + acc) * ivaP / 100, tot = imp + acc + iva;
    var vet = Math.min(Math.max(num(f, "vet", 0), 0), 100), dopo = tot * (1 - vet / 100), fr = num(f, "fr", 0), ind = Math.max(0, dopo - fr);
    var rows = linesRows(ls);
    rows.push(["Imponibile lavorazioni", eur(imp)], ["Costi accessori (" + PCT.format(num(f, "acc", 0)) + "%)", eur(acc)], ["IVA " + ivaP + "%", eur(iva)], ["Totale lavori", eur(tot), 1]);
    if (vet) rows.push(["Deprezzamento vetustà (" + PCT.format(vet) + "%)", "− " + eur(tot - dopo)]);
    if (fr) rows.push(["Franchigia", "− " + eur(Math.min(fr, dopo))]);
    rows.push(["Importo orientativo indennizzabile", eur(ind), 1]);
    var sup = num(f, "sup", 0);
    return { big: eur(ind), sub: "Totale lavori " + eur(tot) + (sup ? " · " + eur(tot / sup) + "/m² sulla superficie indicata" : ""), rows: rows };
  };

  C["preventivo-lavori"] = function (f) {
    var ls = lines(f), lav = ls.reduce(function (s, l) { return s + l.q * l.p; }, 0);
    var sic = lav * num(f, "sic", 0) / 100, tec = lav * num(f, "tec", 0) / 100, imp = lav * num(f, "imp", 0) / 100;
    var base = lav + sic + tec + imp, ivaP = num(f, "iva", 0), iva = base * ivaP / 100;
    var rows = linesRows(ls);
    rows.push(["Totale lavori", eur(lav), 1], ["Oneri sicurezza", eur(sic)], ["Spese tecniche", eur(tec)], ["Imprevisti", eur(imp)], ["Imponibile", eur(base), 1], ["IVA " + ivaP + "%", eur(iva)], ["Totale preventivo", eur(base + iva), 1]);
    return { big: eur(base + iva), sub: "Imponibile " + eur(base), rows: rows };
  };

  ["stime-edili", "stime-idrauliche", "stime-elettriche", "stime-ripristino"].forEach(function (k) { C[k] = function (f) { return C["preventivo-lavori"](f); }; });

  C["franchigia-scoperto"] = function (f) {
    var d = num(f, "danno", 0), fr = num(f, "fr", 0), sc = num(f, "sc", 0), mn = num(f, "scmin", 0), mx = num(f, "scmax", NaN), lim = num(f, "lim", NaN);
    var ord = val(f, "ord"), comb = val(f, "comb"), rows = [["Danno", eur(d)]];
    var base = d;
    if (ord === "prima" && !isNaN(lim) && lim > 0 && d > lim) { base = lim; rows.push(["Danno ridotto al limite di indennizzo", eur(base)]); }
    var s = 0;
    if (sc > 0) {
      s = base * sc / 100; var note = PCT.format(sc) + "% di " + eur(base) + " = " + eur(s);
      if (mn && s < mn) { s = mn; note += " → minimo " + eur(mn); }
      if (!isNaN(mx) && mx > 0 && s > mx) { s = mx; note += " → massimo " + eur(mx); }
      rows.push(["Scoperto <span class='muted'>" + note + "</span>", eur(s)]);
    }
    if (fr) rows.push(["Franchigia", eur(fr)]);
    var car = comb === "somma" ? fr + s : Math.max(fr, s);
    if (fr && s) rows.push([comb === "somma" ? "A tuo carico (franchigia + scoperto)" : "A tuo carico (il maggiore dei due)", eur(car)]);
    car = Math.min(car, base);
    var ind = Math.max(0, base - car);
    if (ord !== "prima" && !isNaN(lim) && lim > 0 && ind > lim) { rows.push(["Prima del limite", eur(ind)]); ind = lim; rows.push(["Applicato limite di indennizzo", eur(lim)]); }
    rows.push(["Indennizzo", eur(ind), 1], ["Resta a tuo carico", eur(d - ind)]);
    return { big: eur(ind), sub: d ? "Resta a tuo carico " + eur(d - ind) + " (" + PCT.format((d - ind) / d * 100) + "% del danno)" : "", rows: rows };
  };

  C["sottoassicurazione"] = function (f) {
    var v = num(f, "val", 0), s = num(f, "som", 0), d = num(f, "danno", 0), tol = num(f, "tol", 0), forma = val(f, "forma");
    var rows = [["Valore assicurabile", eur(v)], ["Somma assicurata", eur(s)], ["Danno", eur(d)]], ind, sub;
    if (forma === "primo") { ind = Math.min(d, s); rows.push(["Primo rischio assoluto: nessuna proporzione", ""]); sub = "La regola proporzionale non si applica"; }
    else if (!v || s >= v) { ind = Math.min(d, s); sub = "Somma assicurata adeguata: nessuna riduzione"; rows.push(["Rapporto somma/valore", PCT.format(v ? s / v * 100 : 100) + "%"]); }
    else if (s >= v * (1 - tol / 100)) { ind = Math.min(d, s); sub = "Sottoassicurazione entro la tolleranza del " + PCT.format(tol) + "%: nessuna riduzione"; rows.push(["Rapporto somma/valore", PCT.format(s / v * 100) + "%"]); }
    else { var r = s / v; ind = Math.min(d * r, s); rows.push(["Rapporto somma/valore", PCT.format(r * 100) + "%"], ["Danno × " + PCT.format(r * 100) + "%", eur(d * r)]); sub = "Riduzione per sottoassicurazione: " + eur(d - ind); }
    rows.push(["Indennizzo teorico (prima di franchigie e scoperti)", eur(ind), 1]);
    return { big: eur(ind), sub: sub, rows: rows };
  };

  C["vetusta"] = function (f) {
    var vita = val(f, "bene") === "custom" ? num(f, "vita", 0) : parseFloat(val(f, "bene"));
    var anno = num(f, "anno", new Date().getFullYear()), nuovo = num(f, "nuovo", 0), k = parseFloat(val(f, "stato")) || 1;
    var resid = Math.min(Math.max(num(f, "res", 0), 0), 100) / 100, lim = num(f, "lim", 100) / 100, crit = val(f, "crit"), merc = num(f, "merc", NaN);
    var eta = Math.max(0, new Date().getFullYear() - anno);
    if (!vita) return { big: "—", sub: "Indica la vita utile del bene", rows: [] };
    var vet = Math.min(eta / vita * k, 1 - resid), uso = nuovo * (1 - vet), ind, nota;
    if (crit === "nuovo") { ind = nuovo; nota = "Valore a nuovo: nessun deprezzamento (spesso la differenza è pagata dopo il rimpiazzo)"; }
    else if (crit === "uso") { ind = uso; nota = "Stato d'uso: si applica la vetustà"; }
    else { ind = vet > lim ? uso : nuovo; nota = vet > lim ? "Vetustà oltre il limite del " + PCT.format(lim * 100) + "%: si indennizza a stato d'uso" : "Vetustà entro il limite: si indennizza a valore a nuovo"; }
    var rows = [["Età del bene", eta + " anni su " + PCT.format(vita) + " di vita utile"], ["Vetustà tecnica", PCT.format(vet * 100) + "%"], ["Valore a nuovo", eur(nuovo)], ["Valore a stato d'uso", eur(uso)]];
    if (!isNaN(merc)) rows.push(["Valore di mercato indicato (dato distinto)", eur(merc)]);
    rows.push(["Indennizzo secondo il criterio di polizza", eur(ind), 1]);
    return { big: eur(ind), sub: nota, rows: rows };
  };

  C["danno-biologico"] = function (f) {
    var rif = val(f, "rif");
    if (rif !== "139") return { big: "Non calcolato", sub: rif === "tun" ? "Le lesioni da 10 a 100 punti nei sinistri stradali e sanitari dal 5 marzo 2025 seguono la Tabella unica nazionale (DPR 12/2025), con valori per ogni punto ed età: richiedi una valutazione." : "Le Tabelle del Tribunale di Milano richiedono parametri e criteri del caso concreto: richiedi una valutazione.", rows: [] };
    var d = val(f, "data"), eta = Math.round(num(f, "eta", 0)), p = Math.round(num(f, "punti", 0));
    var T = d >= "2026-04-01" ? { pt: 988.45, gg: 57.64, ref: "DM 2026 (da aprile 2026)" } : d >= "2025-04-01" ? { pt: 963.40, gg: 56.18, ref: "DM 18 luglio 2025 (da aprile 2025)" } : null;
    if (!d || !T) return { big: "—", sub: "Indica una data del sinistro dal 1° aprile 2025. Per date precedenti si applicano gli importi dei decreti di quegli anni.", rows: [] };
    if (p < 1 || p > 9) return { big: "—", sub: "L'art. 139 riguarda invalidità da 1 a 9 punti. Da 10 punti si applica la Tabella unica nazionale.", rows: [] };
    var COEF = [0, 1, 1.1, 1.2, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3];
    var red = eta > 10 ? Math.max(0, 1 - 0.005 * (eta - 10)) : 1;
    var perm = p * T.pt * COEF[p] * red;
    var g100 = num(f, "itt", 0), g75 = num(f, "itp75", 0), g50 = num(f, "itp50", 0), g25 = num(f, "itp25", 0);
    var temp = T.gg * (g100 + g75 * 0.75 + g50 * 0.5 + g25 * 0.25);
    var pers = Math.min(Math.max(num(f, "pers", 0), 0), 20), base = perm + temp, tot = base * (1 + pers / 100);
    var rows = [["Importi applicati", T.ref], ["Primo punto", eur(T.pt)], [p + " punti × " + eur(T.pt) + " × " + PCT.format(COEF[p]) + (red < 1 ? " × " + PCT.format(red * 100) + "% (età)" : ""), eur(perm)],
      ["Inabilità temporanea <span class='muted'>(" + g100 + " gg 100%, " + g75 + " gg 75%, " + g50 + " gg 50%, " + g25 + " gg 25% · " + eur(T.gg) + "/gg)</span>", eur(temp)]];
    if (pers) rows.push(["Personalizzazione " + PCT.format(pers) + "%", eur(base * pers / 100)]);
    rows.push(["Totale orientativo", eur(tot), 1]);
    return { big: eur(tot), sub: "Permanente " + eur(perm) + " · temporanea " + eur(temp), rows: rows };
  };


  C["massimale"] = function (f) {
    var d = num(f, "danno", 0), m = num(f, "mass", NaN), so = num(f, "sotto", NaN), an = num(f, "annuo", NaN), us = num(f, "usato", 0);
    var lims = [], rows = [["Danno indennizzabile", eur(d)]];
    if (!isNaN(m) && m > 0) { lims.push(m); rows.push(["Massimale per sinistro", eur(m)]); }
    if (!isNaN(so) && so > 0) { lims.push(so); rows.push(["Sottolimite della garanzia", eur(so)]); }
    if (!isNaN(an) && an > 0) { var res = Math.max(0, an - us); lims.push(res); rows.push(["Massimale annuo residuo (" + eur(an) + " − " + eur(us) + ")", eur(res)]); }
    var lim = lims.length ? Math.min.apply(null, lims) : Infinity, ind = Math.min(d, lim);
    if (lims.length) rows.push(["Limite applicabile (il più basso)", eur(lim)]);
    rows.push(["Importo nei limiti", eur(ind), 1], ["Resta scoperto", eur(Math.max(0, d - ind))]);
    return { big: eur(ind), sub: d > ind ? "Oltre il limite restano scoperti " + eur(d - ind) : "Il danno rientra nei limiti indicati", rows: rows };
  };

  C["iva"] = function (f) {
    var x = num(f, "imp", 0), a = parseFloat(val(f, "aliq")) / 100, det = Math.min(Math.max(num(f, "detr", 0), 0), 100) / 100;
    var netto = val(f, "modo") === "lordo" ? x / (1 + a) : x, iva = netto * a, lordo = netto + iva, ivaInd = iva * (1 - det);
    var rows = [["Imponibile", eur(netto)], ["IVA " + PCT.format(a * 100) + "%", eur(iva)], ["Totale con IVA", eur(lordo), 1], ["IVA detraibile (" + PCT.format(det * 100) + "%)", eur(iva * det)], ["IVA indennizzabile", eur(ivaInd), 1], ["Importo indennizzabile (imponibile + IVA indennizzabile)", eur(netto + ivaInd), 1]];
    return { big: eur(lordo), sub: "Indennizzabile: " + eur(netto + ivaInd), rows: rows };
  };

  function addRoom(box, d) {
    d = d || {}; var i = box.children.length, el = document.createElement("div"); el.className = "line"; el.style.gridTemplateColumns = "1.4fr 1fr 1fr 1fr .8fr .8fr 40px";
    function fld(k, lab, v, wide) { return '<div class="fld' + (wide ? ' wide' : '') + '"><label class="small" for="r' + k + i + '">' + lab + '</label><input class="in" id="r' + k + i + '" data-r="' + k + '" ' + (k === "n" ? "" : 'type="number" min="0" step="any" inputmode="decimal" ') + 'value="' + (v == null ? "" : v) + '"></div>'; }
    el.innerHTML = fld("n", "Stanza", d.n || ("Stanza " + (i + 1)), 1) + fld("l", "Lungh. m", d.l) + fld("w", "Largh. m", d.w) + fld("h", "Altezza m", d.h) + fld("p", "Porte", d.p) + fld("f", "Finestre", d.f) + '<button type="button" aria-label="Rimuovi stanza" data-del>×</button>';
    box.appendChild(el);
  }
  C["superfici"] = function (f) {
    var sp = num(f, "porta", 0), sf = num(f, "fin", 0), T = { pav: 0, per: 0, lorde: 0, nette: 0 }, rows = [];
    f.querySelectorAll("[data-rooms] .line").forEach(function (r) {
      function g(k) { var v = parseFloat(r.querySelector('[data-r="' + k + '"]').value); return isNaN(v) ? 0 : v; }
      var n = r.querySelector('[data-r="n"]').value || "Stanza", l = g("l"), w = g("w"), h = g("h"), pav = l * w, per = 2 * (l + w), lor = per * h, net = Math.max(0, lor - g("p") * sp - g("f") * sf);
      T.pav += pav; T.per += per; T.lorde += lor; T.nette += net;
      rows.push([esc(n) + ' <span class="muted">pavimento ' + PCT.format(pav) + " m² · pareti nette " + PCT.format(net) + " m²</span>", PCT.format(per) + " m"]);
    });
    rows.push(["Pavimento totale (= soffitto)", PCT.format(T.pav) + " m²", 1], ["Pareti lorde", PCT.format(T.lorde) + " m²"], ["Pareti nette", PCT.format(T.nette) + " m²", 1], ["Perimetro totale (battiscopa)", PCT.format(T.per) + " m"]);
    return { big: PCT.format(T.nette) + " m²", sub: "Pavimento " + PCT.format(T.pav) + " m² · perimetro " + PCT.format(T.per) + " m", rows: rows };
  };

  C["quantita"] = function (f) {
    var pa = num(f, "pareti", 0), so = num(f, "soff", 0), pv = num(f, "pav", 0), pe = num(f, "perim", 0), sp = num(f, "spess", 0), sfr = num(f, "sfrido", 0), mani = Math.max(1, Math.round(num(f, "mani", 1))), it = num(f, "intonaco", 0), resa = num(f, "resa", 0);
    var tint = pa + so, litri = resa > 0 ? tint * mani / resa : 0, mc = pv * sp / 100;
    var rows = [["Tinteggiatura (pareti + soffitti)", PCT.format(tint) + " m²"], ["Pittura necessaria (" + mani + " mani)", resa > 0 ? PCT.format(Math.ceil(litri)) + " l" : "—"], ["Intonaco da rifare", PCT.format(it) + " m²"], ["Massetto (" + PCT.format(sp) + " cm)", PCT.format(Math.round(mc * 100) / 100) + " m³"], ["Pavimento da posare", PCT.format(pv) + " m²"], ["Pavimento da acquistare (+" + PCT.format(sfr) + "%)", PCT.format(Math.ceil(pv * (1 + sfr / 100))) + " m²"], ["Battiscopa", PCT.format(pe) + " m"]];
    return { big: PCT.format(tint) + " m²", sub: "da tinteggiare · massetto " + PCT.format(Math.round(mc * 100) / 100) + " m³", rows: rows };
  };

  function run(box) {
    var f = box.querySelector("form"), fn = C[box.getAttribute("data-calc")];
    if (!fn) return;
    var r;
    try { r = fn(f); } catch (err) { r = { big: "—", sub: "Controlla i valori inseriti", rows: [] }; }
    box.querySelector('[data-out="big"]').textContent = r.big;
    box.querySelector('[data-out="sub"]').textContent = r.sub || "";
    box.querySelector('[data-out="tab"]').innerHTML = table(r.rows || []);
  }

  document.querySelectorAll("[data-calc]").forEach(function (box) {
    var lb = box.querySelector("[data-lines]");
    if (lb) {
      var start = function () {
        (TPL[box.getAttribute("data-calc")] || [{ free: 1 }]).forEach(function (d) { addLine(lb, d); });
        run(box);
      };
      fetch("/assets/prezzario-campania-2026.json").then(function (r) { return r.json(); }).then(function (j) { PRZ = j.voci; PRZ_META = j.meta; start(); }).catch(function () { PRZ = []; start(); });
      box.querySelector("[data-add]").addEventListener("click", function () { addLine(lb, { free: 0 }); run(box); });
      lb.addEventListener("click", function (ev) { if (ev.target.hasAttribute("data-del")) { ev.target.parentNode.remove(); run(box); } });
      lb.addEventListener("change", function (ev) {
        if (ev.target.getAttribute("data-l") !== "desc") return;
        var line = ev.target.closest(".line"), v = line._list[+ev.target.value];
        line.querySelector('[data-l="u"]').value = v.u;
        line.querySelector('[data-l="p"]').value = v.p == null ? "" : v.p;
        line.querySelector('[data-l="code"]').textContent = v.code ? v.code.replace("CAM26_", "Prezzario Campania 2026 \u00b7 ") : "Inserisci il prezzo del tuo preventivo";
      });
    }
    var rb = box.querySelector("[data-rooms]");
    if (rb) {
      addRoom(rb, { n: "Soggiorno", l: 5, w: 4, h: 2.7, p: 1, f: 1 }); addRoom(rb, { n: "Corridoio", l: 4, w: 1.2, h: 2.7, p: 3, f: 0 });
      box.querySelector("[data-add-room]").addEventListener("click", function () { addRoom(rb, { h: 2.7, p: 1, f: 1 }); run(box); });
      rb.addEventListener("click", function (ev) { if (ev.target.hasAttribute("data-del")) { ev.target.parentNode.remove(); run(box); } });
    }
    box.addEventListener("input", function () { run(box); });
    box.addEventListener("change", function () { run(box); });
    run(box);
  });
})();
