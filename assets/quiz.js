/* StimaVeloce – quiz "Quanto vale il tuo danno?" (anteprima qualitativa, nessuna cifra) */
(function () {
  "use strict";
  var box = document.getElementById("quiz"); if (!box) return;
  var APP = box.getAttribute("data-app") || "/app/";
  var A = {}, step = 0;
  var OGG = {
    auto: ["Carrozzeria", "Paraurti o fanali", "Cristalli", "Meccanica o motore", "Non cammina più"],
    moto: ["Carenature", "Forcella o telaio", "Cerchi o freni", "Casco e abbigliamento", "Non cammina più"],
    casa: ["Soffitto o pareti", "Pavimenti", "Impianti", "Infissi o tetto", "Mobili e contenuto"],
    attivita: ["Locali", "Impianti", "Attrezzature", "Merci", "Fermo dell'attività"],
    persona: ["Colpo di frusta o collo", "Fratture", "Contusioni", "Altro"],
    sisma: ["Crepe nei muri", "Distacchi di intonaco", "Infissi che non chiudono", "Pavimenti o scale", "Casa sgomberata"],
    altro: ["Barca o natante", "Bene personale", "Non lo so"]
  };
  var Q1T = { auto: "Cosa si è danneggiato dell'auto?", moto: "Cosa si è danneggiato della moto?", casa: "Dove si vede il danno?", attivita: "Cosa è stato colpito?", persona: "Che tipo di lesione?", sisma: "Cosa noti in casa?", altro: "Di cosa si tratta?" };
  var _SERV_OLD = { auto: ["perizia", "Perizia auto/moto", 60], moto: ["perizia", "Perizia auto/moto", 60], casa: ["fabbricati", "Perizia fabbricati", 130], attivita: ["fabbricati", "Perizia fabbricati", 130], persona: ["medico", "Valutazione medico-legale", 250], sisma: ["fabbricati", "Perizia fabbricati", 130], altro: ["stima", "Stima senza firma", 30] };
  var VALUTA = {
    auto: ["Ricambi necessari: originali o equivalenti", "Ore di manodopera e verniciatura", "Valore commerciale del veicolo prima del sinistro", "Fermo tecnico, noleggio e traino se documentati"],
    moto: ["Componenti di sicurezza: telaio, forcella, freni", "Ricambi e manodopera", "Casco e abbigliamento protettivo", "Valore del mezzo prima del sinistro"],
    casa: ["Lavorazioni di ripristino con quantità e prezzi", "Origine del danno e possibili danni nascosti", "Garanzie, franchigie e limiti della polizza", "Vetustà dei beni se la polizza paga a stato d'uso"],
    attivita: ["Danni a locali, impianti e attrezzature", "Merci danneggiate e loro valore", "Fermo dell'attività se coperto dalla polizza", "Somme assicurate e regola proporzionale"],
    persona: ["Documentazione sanitaria completa", "Giorni di inabilità temporanea", "Eventuali postumi permanenti (valutati dal medico legale)", "Spese mediche documentate"],
    sisma: ["Tipo, ampiezza e posizione delle lesioni", "Rilievo e misure delle parti danneggiate", "Computo dei lavori con i prezzari regionali di riferimento", "Documenti per contributi o polizza (verifiche, sgombero, pratiche)"],
    altro: ["Che tipo di bene e quale polizza lo copre", "Documentazione disponibile", "Valore del bene prima del danno"]
  };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function show(n) {
    step = n;
    box.querySelectorAll("[data-q]").forEach(function (q) { q.hidden = +q.getAttribute("data-q") !== n; });
    box.querySelectorAll("[data-qbar]").forEach(function (b) { b.classList.toggle("on", +b.getAttribute("data-qbar") <= n); });
    box.querySelector("[data-qback]").hidden = n === 0;
    var h = box.querySelector('[data-q="' + n + '"] h2'); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  }
  function fillOgg() {
    var w = box.querySelector('[data-k="ogg"]');
    w.innerHTML = (OGG[A.tipo] || OGG.altro).map(function (o) { return '<button type="button" data-v="' + esc(o) + '">' + esc(o) + "</button>"; }).join("");
    box.querySelector("[data-q1t]").textContent = Q1T[A.tipo] || "Cosa è stato danneggiato?";
  }
  var CONS = "/contatti/?motivo=consulenza";
  function card(kind) {
    if (kind === "stima") return '<div class="cmp-card"><div class="cmp-tag">Stima</div><div class="cmp-p">30 €</div><p>Valutazione tecnica del danno su foto e documenti, senza firma del perito. Serve per capire quanto vale il danno e come impostare la trattativa.</p><a class="btn btn-p" href="' + APP + '#acquista-stima">Scegli la stima</a></div>';
    if (kind === "perizia") return '<div class="cmp-card cmp-feat"><div class="cmp-tag">Perizia</div><div class="cmp-p">60 €</div><p>Documento firmato dal perito, da presentare come perizia di parte e per contestare la valutazione della compagnia.</p><a class="btn btn-p" href="' + APP + '#acquista-perizia">Scegli la perizia</a></div>';
    return '<div class="cmp-card"><div class="cmp-tag">' + (A.tipo === "persona" ? "Lesioni alla persona" : "Consulenza") + '</div><div class="cmp-p">Gratis</div><p>' + (A.tipo === "persona" ? "Le lesioni le valuta un medico legale. Ti spieghiamo gratis quali documenti servono e come procedere." : "Valutiamo il caso insieme e ti diciamo se serve una perizia e come procedere.") + '</p><a class="btn btn-s" href="' + CONS + '">Chiedi una consulenza gratuita</a></div>';
  }
  function scelta() {
    var t = A.tipo, ks = t === "auto" || t === "moto" ? ["stima", "perizia"] : t === "persona" ? ["cons"] : ["stima", "cons"];
    return '<div class="cmp2' + (ks.length === 1 ? " cmp1" : "") + '">' + ks.map(card).join("") + "</div>" +
      (ks.indexOf("perizia") > -1 ? '<p class="cmp-hint">Non sai quale scegliere? Parti dalla stima: se poi serve la perizia, il costo della stima viene scalato.</p>' : "");
  }
  function preview() {
    var list = (VALUTA[A.tipo] || VALUTA.altro).slice();
    if (A.grav === "grave" && (A.tipo === "auto" || A.tipo === "moto")) list.unshift("Con un danno esteso serve una documentazione accurata: valuta subito la perizia firmata");
    var foto = A.foto === "si" ? "Bene: le foto sono il punto di partenza. Ti chiederemo anche una foto d'insieme e una da vicino per ogni danno."
      : A.foto === "poche" ? "Ti indicheremo quali foto aggiungere: una d'insieme, una da vicino per ogni danno e, se possibile, un riferimento per le misure."
      : "Nessun problema: ti diciamo noi quali foto scattare e come.";
    var out = '<div class="eyebrow">La tua anteprima</div><h2 style="font-size:30px">Ecco cosa valuta il perito</h2>' +
      '<p class="muted">' + esc(A.ogg || "") + (A.grav ? " · danno " + esc(A.grav) : "") + '</p><ul class="ticks" style="margin:14px 0 18px">' + list.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" +
      '<div class="note" style="margin-bottom:18px"><div><b>Le foto.</b> ' + esc(foto) + "</div></div>" +
      '<p>Per sapere <b>quanto vale</b> il tuo danno serve la valutazione di un tecnico: non diamo cifre inventate. Scegli come andare avanti:</p>' + scelta() +
      '<p class="small no-print" style="margin-top:14px"><a href="' + APP + '#prefattibilita">Oppure racconta i dettagli gratis</a> · <button type="button" class="btn btn-g btn-sm" onclick="window.print()" style="display:inline-flex">Stampa</button></p>';
    var el = document.getElementById("anteprima"); el.innerHTML = out;
    try { localStorage.setItem("sv_quiz", JSON.stringify(A)); } catch (e) {}
  }
  box.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-v]");
    if (b) {
      var k = b.parentNode.getAttribute("data-k"); A[k] = b.getAttribute("data-v");
      if (k === "tipo") { fillOgg(); show(1); } else if (k === "ogg") show(2); else if (k === "grav") show(3); else if (k === "foto") { preview(); show(4); }
      return;
    }
    if (e.target.closest("[data-qback]")) show(Math.max(0, step - 1));
  });
  var t = new URLSearchParams(location.search).get("tipo");
  if (t && OGG[t]) { A.tipo = t; fillOgg(); show(1); }
})();
