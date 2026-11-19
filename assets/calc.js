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

  var LAV = [["Demolizione/rimozione intonaco", "m²"], ["Rifacimento intonaco", "m²"], ["Tinteggiatura pareti e soffitti", "m²"], ["Rimozione pavimento", "m²"], ["Massetto", "m²"], ["Posa pavimento", "m²"], ["Rivestimenti", "m²"], ["Impianto elettrico (ripristino)", "corpo"], ["Impianto idraulico (ripristino)", "corpo"], ["Controsoffitto", "m²"], ["Infissi", "cad"], ["Smaltimento materiali", "corpo"], ["Altra lavorazione", "corpo"]];

  function addLine(box, d) {
    d = d || {};
    var i = box.children.length;
    var opts = LAV.map(function (l) { return '<option data-u="' + l[1] + '"' + (d.desc === l[0] ? " selected" : "") + ">" + l[0] + "</option>"; }).join("");
    var el = document.createElement("div");
    el.className = "line";
    el.innerHTML = '<div class="fld wide"><label class="small" for="ld' + i + '">Voce</label><select class="in" id="ld' + i + '" data-l="desc">' + opts + "</select></div>" +
      '<div class="fld"><label class="small" for="lu' + i + '">Unità</label><input class="in" id="lu' + i + '" data-l="u" value="' + esc(d.u || "m²") + '"></div>' +
      '<div class="fld"><label class="small" for="lq' + i + '">Quantità</label><input class="in" id="lq' + i + '" data-l="q" type="number" min="0" step="any" inputmode="decimal" value="' + (d.q == null ? "" : d.q) + '"></div>' +
      '<div class="fld"><label class="small" for="lp' + i + '">Prezzo unit. €</label><input class="in" id="lp' + i + '" data-l="p" type="number" min="0" step="any" inputmode="decimal" placeholder="es. 25" value="' + (d.p == null ? "" : d.p) + '"></div>' +
      '<button type="button" aria-label="Rimuovi voce" data-del>×</button>';
    box.appendChild(el);
  }
  function lines(form) {
    var out = [];
    form.querySelectorAll(".line").forEach(function (l) {
      var q = parseFloat(l.querySelector('[data-l="q"]').value), p = parseFloat(l.querySelector('[data-l="p"]').value);
      out.push({ desc: l.querySelector('[data-l="desc"]').value, u: l.querySelector('[data-l="u"]').value, q: isNaN(q) ? 0 : q, p: isNaN(p) ? 0 : p });
    });
    return out;
  }
  function linesRows(ls) {
    return ls.filter(function (l) { return l.q && l.p; }).map(function (l) { return [esc(l.desc) + ' <span class="muted">' + PCT.format(l.q) + " " + esc(l.u) + " × " + eur(l.p) + "</span>", eur(l.q * l.p)]; });
  }

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
      var demo = box.getAttribute("data-calc") === "danni-fabbricato"
        ? [{ desc: "Demolizione/rimozione intonaco", u: "m²", q: 18, p: null }, { desc: "Rifacimento intonaco", u: "m²", q: 18, p: null }, { desc: "Tinteggiatura pareti e soffitti", u: "m²", q: 64, p: null }]
        : [{ desc: "Rimozione pavimento", u: "m²", q: 20, p: null }, { desc: "Posa pavimento", u: "m²", q: 20, p: null }];
      demo.forEach(function (d) { addLine(lb, d); });
      box.querySelector("[data-add]").addEventListener("click", function () { addLine(lb, {}); run(box); });
      lb.addEventListener("click", function (ev) { if (ev.target.hasAttribute("data-del")) { ev.target.parentNode.remove(); run(box); } });
      lb.addEventListener("change", function (ev) { if (ev.target.getAttribute("data-l") === "desc") { var o = ev.target.selectedOptions[0]; var u = ev.target.closest(".line").querySelector('[data-l="u"]'); if (o && u) u.value = o.getAttribute("data-u"); } });
    }
    box.addEventListener("input", function () { run(box); });
    box.addEventListener("change", function () { run(box); });
    run(box);
  });
})();
