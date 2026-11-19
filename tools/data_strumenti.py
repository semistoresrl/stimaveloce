# -*- coding: utf-8 -*-
"""Calcolatori. Il calcolo è in /assets/calc.js (stessi slug)."""
from data_guide import CC, CDA

def f(name, label, val="", hint="", typ="number", step="any", unit=""):
    u = f' <span class="muted">({unit})</span>' if unit else ""
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<div class="fld"><label for="f-{name}">{label}{u}</label><input class="in" id="f-{name}" name="{name}" type="{typ}" inputmode="decimal" step="{step}" min="0" value="{val}">{h}</div>'

def sel(name, label, opts, hint=""):
    o = "".join(f'<option value="{v}">{t}</option>' for v, t in opts)
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<div class="fld"><label for="f-{name}">{label}</label><select class="in" id="f-{name}" name="{name}">{o}</select>{h}</div>'

def row(*x): return '<div class="row2">' + "".join(x) + "</div>"
def row3(*x): return '<div class="row3">' + "".join(x) + "</div>"

LINES = ('<div class="lbl">Lavorazioni</div><div class="lines" data-lines></div>'
         '<button class="btn btn-s btn-sm" type="button" data-add style="justify-self:start">+ Aggiungi lavorazione</button>')

STRUMENTI = [
 dict(slug="danni-fabbricato", icon="building-2", nome="Calcolatore danni al fabbricato",
  h1="Calcolatore danni al fabbricato", breve="Lavorazioni, quantità e prezzi, con IVA, vetustà e franchigia.",
  title="Calcolatore danni al fabbricato: stima lavorazioni e indennizzo | StimaVeloce",
  desc="Calcola un importo orientativo del danno al fabbricato: lavorazioni, quantità, prezzi unitari, costi accessori, IVA, vetustà e franchigia di polizza.",
  intro="Inserisci le lavorazioni necessarie per il ripristino con quantità e prezzo unitario. Il calcolatore applica costi accessori, IVA, eventuale vetustà e franchigia.",
  res_label="Importo orientativo indennizzabile",
  form=row(sel("tipo", "Tipologia immobile", [("abitazione","Abitazione"),("condominio","Parti comuni condominiali"),("commerciale","Locale commerciale"),("altro","Altro")]), f("sup", "Superficie interessata", "", "", unit="m²")) + LINES +
       row(f("acc", "Costi accessori", "5", "Oneri sicurezza, smaltimento, spese tecniche", unit="%"), sel("iva", "IVA applicabile", [("10","10% (manutenzione su abitazioni)"),("22","22%"),("0","Non applicabile o recuperabile")])) +
       row(f("vet", "Deprezzamento per vetustà", "0", "Solo se la polizza indennizza a stato d'uso", unit="%"), f("fr", "Franchigia", "0", "", unit="€")),
  formula="<p><code>Imponibile = Σ (quantità × prezzo unitario)</code><br><code>Costi accessori = Imponibile × %accessori</code><br><code>Totale lavori = (Imponibile + accessori) × (1 + IVA)</code><br><code>Dopo vetustà = Totale lavori × (1 − %vetustà)</code><br><code>Indennizzo orientativo = max(0, Dopo vetustà − franchigia)</code></p>",
  spiegazione="<p>Il <b>totale lavori</b> è il costo stimato del ripristino. L'<b>importo indennizzabile</b> tiene conto di come la polizza tratta il danno: deprezzamento se l'indennizzo è a stato d'uso e franchigia. Scoperti, limiti di indennizzo e regola proporzionale si calcolano con gli strumenti dedicati.</p><p>L'IVA è indennizzabile quando resta effettivamente a carico dell'assicurato; in genere non lo è per chi può detrarla.</p>",
  avvertenze="I prezzi proposti sono quelli del Prezzario regionale dei Lavori Pubblici della Campania 2026 (IVA esclusa, comprensivi di spese generali e utile d'impresa); puoi sostituirli con quelli del tuo preventivo. Il risultato è orientativo e non sostituisce un computo metrico redatto da un tecnico né considera tutte le clausole della polizza.",
  fonti=[CC]),
 dict(slug="franchigia-scoperto", icon="percent", nome="Calcolatore franchigia e scoperto",
  h1="Calcolatore franchigia e scoperto", breve="Applica franchigia, scoperto con minimo e massimo e limite di indennizzo.",
  title="Calcolatore franchigia e scoperto con minimo, massimo e limite | StimaVeloce",
  desc="Calcola l'indennizzo applicando franchigia fissa, scoperto percentuale con minimo e massimo e limite di indennizzo. Calcolo passo per passo.",
  intro="Inserisci il danno e le clausole della tua polizza. Vedi passo per passo quanto resta a tuo carico e quanto è indennizzabile.",
  res_label="Indennizzo calcolato",
  form=f("danno", "Importo del danno", "5000", unit="€") + row(f("fr", "Franchigia fissa", "250", unit="€"), f("sc", "Scoperto", "10", unit="%")) +
       row(f("scmin", "Minimo di scoperto", "500", unit="€"), f("scmax", "Massimo di scoperto", "", "Lascia vuoto se non previsto", unit="€")) +
       f("lim", "Limite di indennizzo", "", "Lascia vuoto se non previsto", unit="€") +
       sel("comb", "Se sono previsti sia franchigia sia scoperto", [("max","Si applica il maggiore dei due (più frequente)"),("somma","Si applicano entrambi")], "Controlla la formulazione della tua polizza") +
       sel("ord", "Ordine di applicazione del limite", [("dopo","Il limite si applica dopo le detrazioni (più frequente)"),("prima","Le detrazioni si applicano al danno ridotto al limite")]),
  formula="<p><code>Scoperto = danno × % (non meno del minimo, non oltre il massimo)</code><br><code>A tuo carico = max(franchigia, scoperto)</code> oppure <code>franchigia + scoperto</code><br><code>Indennizzo = min(danno − a tuo carico, limite)</code> — oppure, se il limite si applica prima: <code>min(danno, limite) − a tuo carico</code></p>",
  spiegazione="<p>La <b>franchigia</b> è un importo fisso a tuo carico; lo <b>scoperto</b> è una percentuale del danno, spesso con un minimo in euro. Il <b>limite di indennizzo</b> è l'importo massimo che la compagnia paga per quel tipo di danno. L'ordine con cui si applicano cambia il risultato: per questo puoi sceglierlo.</p>",
  avvertenze="Le polizze possono prevedere combinazioni diverse da quelle proposte. Verifica sempre il testo della clausola. Il risultato non tiene conto della regola proporzionale: usa il calcolatore sottoassicurazione.",
  fonti=[CC]),
 dict(slug="sottoassicurazione", icon="scale", nome="Calcolatore sottoassicurazione",
  h1="Calcolatore sottoassicurazione (regola proporzionale)", breve="Indennizzo teorico secondo l'art. 1907 c.c., con tolleranza o primo rischio.",
  title="Calcolatore regola proporzionale e sottoassicurazione (art. 1907 c.c.) | StimaVeloce",
  desc="Calcola l'indennizzo teorico quando la somma assicurata è inferiore al valore del bene: regola proporzionale dell'art. 1907 c.c., tolleranza e primo rischio assoluto.",
  intro="Se la somma assicurata è inferiore al valore del bene, l'indennizzo si riduce in proporzione, salvo patto contrario. Inserisci i valori per vedere l'effetto.",
  res_label="Indennizzo teorico",
  form=row(f("val", "Valore assicurabile al momento del sinistro", "300000", unit="€"), f("som", "Somma assicurata", "200000", unit="€")) + f("danno", "Importo del danno", "30000", unit="€") +
       sel("forma", "Forma di assicurazione", [("intero","Valore intero (si applica l'art. 1907)"),("primo","Primo rischio assoluto (nessuna proporzione)")]) +
       f("tol", "Tolleranza prevista in polizza (deroga)", "0", "Es. 10 o 20: entro questo scarto la regola non si applica", unit="%"),
  formula="<p><code>Se somma assicurata ≥ valore × (1 − tolleranza) → nessuna riduzione</code><br><code>Altrimenti: indennizzo = danno × somma assicurata ÷ valore</code><br><code>In ogni caso l'indennizzo non supera la somma assicurata</code></p><p class='small muted'>Art. 1907 c.c.: «Se l'assicurazione copre solo una parte del valore che la cosa assicurata aveva nel tempo del sinistro, l'assicuratore risponde dei danni in proporzione della parte suddetta, a meno che non sia diversamente convenuto».</p>",
  spiegazione="<p>Il rapporto <b>somma assicurata ÷ valore</b> indica quanta parte del bene è assicurata. Con la forma a <b>primo rischio assoluto</b> la compagnia risponde fino alla somma assicurata senza considerare il valore totale. La tolleranza è una deroga contrattuale: alcune polizze, superata la tolleranza, calcolano la proporzione in modo diverso.</p>",
  avvertenze="Il calcolo è teorico. Franchigie, scoperti e limiti si applicano in aggiunta, secondo l'ordine previsto dalla polizza. La stima del valore assicurabile richiede una valutazione tecnica.",
  fonti=[CC]),
 dict(slug="vetusta", icon="hourglass", nome="Calcolatore vetustà e svalutazione",
  h1="Calcolatore vetustà e svalutazione", breve="Distingue vetustà tecnica, valore di mercato e criterio di polizza.",
  title="Calcolatore vetustà e deprezzamento: valore a nuovo o stato d'uso | StimaVeloce",
  desc="Calcola il deprezzamento per vetustà di un bene e confrontalo con il criterio di indennizzo della polizza: valore a nuovo, stato d'uso, limite di deprezzamento.",
  intro="Tre cose diverse spesso confuse: la vetustà tecnica (quanto il bene si è consumato), il valore commerciale (quanto varrebbe sul mercato) e il criterio della polizza (come viene indennizzato).",
  res_label="Indennizzo secondo il criterio scelto",
  form=row(sel("bene", "Tipologia del bene", [("10","Elettrodomestici ed elettronica (vita utile 10 anni)"),("15","Mobili e arredi (15 anni)"),("20","Impianti e serramenti interni (20 anni)"),("30","Pavimenti, rivestimenti, infissi esterni (30 anni)"),("40","Strutture e coperture (40 anni)"),("custom","Altro: indico la vita utile")]), f("vita", "Vita utile (se «Altro»)", "", unit="anni")) +
       row(f("anno", "Anno di acquisto o installazione", "2016", typ="number", step="1"), f("nuovo", "Valore a nuovo (costo di rimpiazzo)", "1200", unit="€")) +
       row(sel("stato", "Stato di conservazione", [("1","Normale"),("0.85","Buono (deprezzamento ridotto)"),("1.2","Scarso (deprezzamento aumentato)")]), f("res", "Valore residuo minimo", "20", "Il bene in uso conserva comunque un valore", unit="%")) +
       row(sel("crit", "Criterio della polizza", [("nuovo","Valore a nuovo"),("uso","Stato d'uso"),("limite","Valore a nuovo con limite di deprezzamento")]), f("lim", "Limite di deprezzamento (se previsto)", "50", "Oltre questo deprezzamento si indennizza a stato d'uso", unit="%")) +
       f("merc", "Valore di mercato noto (facoltativo)", "", "Es. quotazione dell'usato: è un dato diverso dalla vetustà", unit="€"),
  formula="<p><code>Età = anno corrente − anno di acquisto</code><br><code>Vetustà tecnica = min(età ÷ vita utile × coefficiente di stato, 1 − residuo minimo)</code><br><code>Valore a stato d'uso = valore a nuovo × (1 − vetustà)</code><br><code>Valore a nuovo con limite: se vetustà > limite → stato d'uso, altrimenti valore a nuovo</code></p>",
  spiegazione="<p>La <b>vetustà tecnica</b> è calcolata in modo lineare sulla vita utile del bene, corretta per lo stato di conservazione. Il <b>valore di mercato</b> dipende da domanda e offerta e non coincide con la vetustà: se lo conosci viene mostrato a confronto. Il <b>criterio di polizza</b> decide quale valore conta: con il valore a nuovo la differenza rispetto allo stato d'uso viene spesso pagata solo dopo il rimpiazzo o la riparazione.</p>",
  avvertenze="Le vite utili proposte sono valori di riferimento indicativi, non tabelle contrattuali: se la polizza o la prassi del settore prevedono criteri diversi, prevalgono quelli. Per i veicoli il valore commerciale si determina con le quotazioni di mercato.",
  fonti=[CC]),
 dict(slug="danno-biologico", icon="heart-pulse", nome="Calcolatore danno biologico orientativo",
  h1="Calcolatore danno biologico orientativo (lesioni lievi, art. 139)", breve="Micropermanenti da 1 a 9 punti e invalidità temporanea, valori aggiornati.",
  title="Calcolatore danno biologico lieve entità art. 139 – valori 2026 | StimaVeloce",
  desc="Calcolo orientativo del danno biologico per lesioni di lieve entità (1–9 punti) da sinistri stradali secondo l'art. 139 del Codice delle assicurazioni, con importi aggiornati al DM 2026.",
  intro="Per sinistri stradali e nautici con lesioni di lieve entità (invalidità permanente fino a 9 punti) il risarcimento segue gli importi dell'art. 139 del Codice delle assicurazioni, aggiornati ogni anno.",
  res_label="Importo orientativo",
  form=sel("rif", "Riferimento normativo o tabellare", [("139","Art. 139 Codice assicurazioni – lesioni lievi (1–9 punti), circolazione veicoli e natanti"),("tun","Tabella unica nazionale – lesioni non lievi (10–100 punti)"),("milano","Tabelle del Tribunale di Milano – altri ambiti")]) +
       row(f("data", "Data del sinistro", "2026-05-15", typ="date"), f("eta", "Età del danneggiato alla data del sinistro", "35", typ="number", step="1", unit="anni")) +
       f("punti", "Invalidità permanente stimata dal medico legale", "3", typ="number", step="1", unit="punti, da 1 a 9") +
       row3(f("itt", "Giorni di inabilità al 100%", "10", typ="number", step="1"), f("itp75", "Giorni al 75%", "0", typ="number", step="1"), f("itp50", "Giorni al 50%", "15", typ="number", step="1")) +
       row(f("itp25", "Giorni al 25%", "20", typ="number", step="1"), f("pers", "Personalizzazione (fino al 20%)", "0", "Solo se riconosciuta per specifiche ripercussioni dinamico-relazionali", unit="%")),
  formula="<p><code>Valore permanente = punti × valore del primo punto × coefficiente per punti × riduzione per età</code><br>Coefficienti: 1 punto ×1,0 · 2 ×1,1 · 3 ×1,2 · 4 ×1,3 · 5 ×1,5 · 6 ×1,7 · 7 ×1,9 · 8 ×2,1 · 9 ×2,3<br>Riduzione per età: −0,5% per ogni anno a partire dall'11° (<code>1 − 0,005 × (età − 10)</code>)<br><code>Temporanea = giorni × importo giornaliero × percentuale di inabilità</code><br><code>Totale = (permanente + temporanea) × (1 + personalizzazione)</code></p><p>Importi in vigore: dal 1° aprile 2025 primo punto 963,40 € e inabilità assoluta 56,18 €/giorno (DM 18 luglio 2025); dal 1° aprile 2026 primo punto 988,45 € e 57,64 €/giorno (DM 2026, +2,6%).</p>",
  spiegazione="<p>Il calcolatore traduce in euro una percentuale di invalidità <b>già stimata da un medico legale</b>. La personalizzazione fino al 20% è prevista dall'art. 139, comma 3, solo per lesioni che incidono in modo rilevante su specifici aspetti dinamico-relazionali documentati.</p><p>Le lesioni da 10 a 100 punti seguono la <b>Tabella unica nazionale</b> (DPR 13 gennaio 2025, n. 12) per i sinistri stradali e sanitari avvenuti dal 5 marzo 2025, mentre in altri ambiti si fa normalmente riferimento alle <b>Tabelle del Tribunale di Milano</b>: queste tabelle non sono calcolate qui.</p>",
  avvertenze="Risultato orientativo, non è una liquidazione. Non comprende spese mediche, danno patrimoniale, interessi e rivalutazione. Le tabelle diverse non vanno confuse: ogni riferimento si applica solo al proprio ambito e periodo. Per sinistri anteriori ad aprile 2025 o per verificare aggiornamenti successivi consulta il decreto in vigore alla data del sinistro.",
  aggiornato="19 novembre 2026 (importi DM 2026, decorrenza aprile 2026)",
  fonti=[CDA, ("DM MIMIT 18 luglio 2025 – aggiornamento importi art. 139 (PDF)", "https://www.mimit.gov.it/images/stories/normativa/DM_microlesioni_2025_firmato.pdf"),
         ("Aggiornamento importi danno biologico 2026 (PDF, ACI Rivista giuridica)", "https://rivistagiuridica.aci.it/fileadmin/Documenti/2026/Normativa/Decreti_Ministeriali/aggiornamento_importi_danno_biologico_2026.pdf"),
         ("DPR 13 gennaio 2025, n. 12 – Tabella unica nazionale (Gazzetta Ufficiale)", "https://www.gazzettaufficiale.it/eli/id/2025/02/18/25G00019/sg")]),
 dict(slug="preventivo-lavori", icon="receipt", nome="Calcolatore preventivo lavori",
  h1="Calcolatore preventivo lavori", breve="Componi un preventivo con voci, oneri, spese tecniche e IVA.",
  title="Calcolatore preventivo lavori di ripristino con IVA e oneri | StimaVeloce",
  desc="Componi un preventivo dei lavori di ripristino: voci, quantità, prezzi unitari, oneri per la sicurezza, spese tecniche, imprevisti e IVA. Stampabile.",
  intro="Utile per confrontare preventivi o prepararne uno dettagliato da presentare alla compagnia. Ogni voce mostra quantità e prezzo unitario.",
  res_label="Totale preventivo",
  form=LINES + row3(f("sic", "Oneri per la sicurezza", "3", unit="%"), f("tec", "Spese tecniche", "0", unit="%"), f("imp", "Imprevisti", "0", unit="%")) +
       sel("iva", "IVA", [("10","10%"),("22","22%"),("0","Esente o non applicabile")]),
  formula="<p><code>Lavori = Σ (quantità × prezzo unitario)</code><br><code>Oneri sicurezza, spese tecniche e imprevisti = Lavori × rispettive %</code><br><code>Imponibile = Lavori + oneri + spese + imprevisti</code><br><code>Totale = Imponibile × (1 + IVA)</code></p>",
  spiegazione="<p>Un preventivo verificabile indica per ogni voce unità di misura, quantità e prezzo unitario. Le percentuali di oneri e spese tecniche variano da caso a caso: inseriscile solo se effettivamente previste.</p>",
  avvertenze="L'aliquota IVA dipende dal tipo di intervento e di immobile: verifica con l'impresa o il consulente fiscale. I prezzi proposti vengono dal Prezzario regionale della Campania 2026 e sono già comprensivi di spese generali e utile d'impresa: non aggiungere altre percentuali per le stesse voci.",
  fonti=[]),
]

STRUMENTI += [
 dict(slug="massimale", icon="shield-check", nome="Calcolatore massimale e sottolimiti",
  h1="Calcolatore massimale e sottolimiti", breve="Quanto resta coperto tra massimale per sinistro, annuo e sottolimiti.",
  title="Calcolatore massimale, sottolimite e massimale annuo | StimaVeloce",
  desc="Verifica quanto può essere indennizzato rispetto al massimale per sinistro, al sottolimite della garanzia e al massimale annuo già in parte utilizzato.",
  intro="Il massimale è l'importo massimo che la compagnia paga. Spesso ci sono anche un sottolimite per la singola garanzia e un massimale per anno assicurativo.",
  res_label="Importo nei limiti di polizza",
  form=f("danno", "Danno indennizzabile dopo franchigie e scoperti", "60000", unit="€") + row(f("mass", "Massimale per sinistro", "50000", unit="€"), f("sotto", "Sottolimite della garanzia", "", "Lascia vuoto se non previsto", unit="€")) +
       row(f("annuo", "Massimale per anno assicurativo", "", "Lascia vuoto se non previsto", unit="€"), f("usato", "Già liquidato nello stesso anno", "0", unit="€")),
  formula="<p><code>Limite applicabile = il più basso tra massimale per sinistro, sottolimite e (massimale annuo − già liquidato)</code><br><code>Importo = min(danno, limite applicabile)</code><br><code>Scoperto di massimale = danno − importo</code></p>",
  spiegazione="<p>Il <b>sottolimite</b> vale per una specifica garanzia o tipo di danno ed è più basso del massimale generale. Il <b>massimale annuo</b> si consuma con i sinistri liquidati nello stesso anno assicurativo. La parte di danno che supera il limite resta scoperta.</p>",
  avvertenze="Il danno da inserire è quello già ridotto da franchigie, scoperti ed eventuale regola proporzionale, secondo l'ordine previsto dalla polizza: usa prima gli altri calcolatori.",
  fonti=[CC]),
 dict(slug="iva", icon="percent", nome="Calcolatore IVA sull'indennizzo",
  h1="Calcolatore IVA: scorporo, aggiunta e IVA indennizzabile", breve="Scorpora o aggiunge l'IVA e indica quanta è indennizzabile.",
  title="Calcolatore IVA: scorporo, aggiunta e IVA indennizzabile | StimaVeloce",
  desc="Scorpora o aggiungi l'IVA a un preventivo e calcola quanta IVA è indennizzabile in base alla detraibilità: utile per privati, professionisti e aziende.",
  intro="L'IVA su una riparazione è un costo per chi non può detrarla. Chi la detrae, come molte aziende e professionisti, di norma non ne ottiene il rimborso nell'indennizzo.",
  res_label="Totale con IVA",
  form=row(f("imp", "Importo", "1000", unit="€"), sel("modo", "L'importo è", [("netto","Senza IVA (imponibile)"),("lordo","Con IVA compresa")])) +
       row(sel("aliq", "Aliquota", [("22","22% ordinaria"),("10","10% (es. manutenzione su abitazioni)"),("4","4%"),("0","0% / esente")]), f("detr", "Quota di IVA detraibile da chi riceve l'indennizzo", "0", "0 per un privato; 100 per chi detrae tutta l'IVA", unit="%")),
  formula="<p><code>Da netto: IVA = imponibile × aliquota; totale = imponibile + IVA</code><br><code>Da lordo: imponibile = totale ÷ (1 + aliquota); IVA = totale − imponibile</code><br><code>IVA indennizzabile = IVA × (1 − quota detraibile)</code></p>",
  spiegazione="<p>Per un privato l'IVA pagata è un costo effettivo e rientra nel danno. Chi può detrarre l'IVA la recupera con la propria contabilità, quindi di norma resta fuori dall'indennizzo. La quota parziale serve per chi detrae solo una parte, ad esempio con il pro-rata.</p>",
  avvertenze="L'aliquota corretta dipende dal tipo di intervento e di immobile, e la detraibilità dalla posizione fiscale di chi riceve l'indennizzo: verifica con il tuo consulente fiscale. Molte polizze liquidano l'IVA solo dopo la presentazione della fattura.",
  fonti=[]),
 dict(slug="superfici", icon="ruler", nome="Calcolatore superfici",
  h1="Calcolatore superfici di stanze, pareti e soffitti", breve="Pavimento, soffitto, pareti nette e perimetro di ogni stanza.",
  title="Calcolatore superfici: pavimento, pareti nette, soffitto | StimaVeloce",
  desc="Calcola pavimento, soffitto, pareti al netto di porte e finestre e perimetro di una o più stanze, per stimare lavorazioni come intonaco, tinteggiatura e pavimenti.",
  intro="Misura lunghezza, larghezza e altezza di ogni stanza e indica porte e finestre: ottieni le superfici che servono per stimare le lavorazioni.",
  res_label="Pareti nette totali",
  form='<div class="lbl">Stanze</div><div class="lines" data-rooms></div><button class="btn btn-s btn-sm" type="button" data-add-room style="justify-self:start">+ Aggiungi stanza</button>' +
       row(f("porta", "Superficie media di una porta", "1.8", unit="m²"), f("fin", "Superficie media di una finestra", "1.5", unit="m²")),
  formula="<p><code>Pavimento = soffitto = lunghezza × larghezza</code><br><code>Perimetro = 2 × (lunghezza + larghezza)</code><br><code>Pareti lorde = perimetro × altezza</code><br><code>Pareti nette = pareti lorde − porte × sup. porta − finestre × sup. finestra</code></p>",
  spiegazione="<p>Le <b>pareti nette</b> servono per intonaci e tinteggiature, il <b>pavimento</b> per massetti e pavimentazioni, il <b>perimetro</b> per zoccolini e battiscopa. Per stanze non rettangolari scomponile in rettangoli e inseriscile come stanze separate.</p>",
  avvertenze="I capitolati e i prezzari possono prevedere regole di misurazione diverse, ad esempio sul conteggio dei vani inferiori a una certa superficie: in una stima formale si seguono quelle regole.",
  fonti=[]),
 dict(slug="quantita", icon="layers", nome="Calcolatore quantità lavorazioni",
  h1="Calcolatore quantità delle lavorazioni", breve="Dalle superfici alle quantità: mani di pittura, sfridi, massetti, smaltimento.",
  title="Calcolatore quantità lavorazioni: pittura, massetto, pavimento | StimaVeloce",
  desc="Trasforma le superfici in quantità di lavorazione: tinteggiatura, intonaco, massetto in metri cubi, pavimento con sfrido, battiscopa e materiale da smaltire.",
  intro="Parti dalle superfici misurate (anche con il calcolatore superfici) e ottieni le quantità tipiche delle lavorazioni di ripristino.",
  res_label="Riepilogo quantità",
  form=row(f("pareti", "Pareti da trattare", "60", unit="m²"), f("soff", "Soffitti da trattare", "20", unit="m²")) +
       row(f("pav", "Pavimento da rifare", "20", unit="m²"), f("perim", "Perimetro per battiscopa", "18", unit="m")) +
       row3(f("spess", "Spessore massetto", "5", unit="cm"), f("sfrido", "Sfrido pavimento", "10", unit="%"), f("mani", "Mani di pittura", "2", typ="number", step="1")) +
       row(f("intonaco", "Intonaco da rifare (porzione danneggiata)", "15", unit="m²"), f("resa", "Resa della pittura", "10", "Metri quadrati per litro per mano, dalla scheda del prodotto", unit="m²/l")),
  formula="<p><code>Tinteggiatura = (pareti + soffitti) m²</code>; <code>pittura = superficie × mani ÷ resa</code> litri<br><code>Massetto = pavimento × spessore ÷ 100</code> m³<br><code>Pavimento da acquistare = pavimento × (1 + sfrido)</code><br><code>Battiscopa = perimetro</code> m</p>",
  spiegazione="<p>Le quantità di lavorazione (m², m, m³) sono quelle da moltiplicare per i prezzi unitari. I litri di pittura e il materiale con sfrido servono a chi esegue i lavori e non si sommano ai prezzi unitari, che di norma comprendono già il materiale.</p>",
  avvertenze="Le rese reali dipendono dal prodotto e dal supporto; lo sfrido cambia con il formato delle piastrelle e la forma della stanza.",
  fonti=[]),
]

PRZ_SRC = ("Prezzario regionale dei Lavori Pubblici della Campania 2026 – DGR n. 14 del 29/01/2026, BURC n. 6 del 02/02/2026", "https://burc.regione.campania.it/")
_PRZ_FORM = LINES + row3(f("sic", "Oneri per la sicurezza", "3", unit="%"), f("tec", "Spese tecniche", "0", unit="%"), f("imp", "Imprevisti", "0", unit="%")) + sel("iva", "IVA", [("10","10%"),("22","22%"),("0","Esente o non applicabile")])
_PRZ_FORMULA = "<p><code>Lavori = \u03a3 (quantit\u00e0 \u00d7 prezzo unitario del prezzario)</code><br><code>Imponibile = lavori + oneri per la sicurezza + spese tecniche + imprevisti</code><br><code>Totale = imponibile \u00d7 (1 + IVA)</code></p><p>I prezzi unitari sono quelli del <b>Prezzario regionale dei Lavori Pubblici della Campania, anno 2026</b> (DGR n. 14 del 29 gennaio 2026): al netto dell'IVA e gi\u00e0 comprensivi del 17% di spese generali e del 10% di utile d'impresa. Ogni voce mostra il suo codice ufficiale.</p>"
_PRZ_SPIEG = "<p>Il risultato \u00e8 una stima a prezzi pubblici di riferimento, utile per confrontare un preventivo o un'offerta. I prezzi di mercato possono essere diversi: se cambi un prezzo, la voce viene segnata come \u00abprezzo inserito\u00bb.</p>"
_PRZ_AVV = "I prezzi pubblici sono un riferimento per opere pubbliche: per interventi piccoli, urgenti o in condizioni particolari i costi reali possono essere maggiori. Le quantit\u00e0 vanno misurate sul posto. La stima non sostituisce un computo metrico firmato da un tecnico."

def _prz(slug, icon, nome, h1, breve, desc, intro, cats):
    return dict(slug=slug, icon=icon, nome=nome, h1=h1, breve=breve, title=h1 + " con prezzario Campania 2026 | StimaVeloce", desc=desc, intro=intro,
                res_label="Totale stimato", form=_PRZ_FORM, formula=_PRZ_FORMULA, spiegazione=_PRZ_SPIEG, avvertenze=_PRZ_AVV, cats=cats, fonti=[PRZ_SRC])

STRUMENTI += [
 _prz("stime-edili", "hammer", "Stime edili", "Stima lavori edili", "Intonaci, rasature, tinteggiature, pavimenti a prezzi ufficiali.",
      "Stima i lavori edili di ripristino (intonaci, rasature, tinteggiature, massetti, pavimenti, controsoffitti) con i prezzi del Prezzario Campania 2026.",
      "Scegli le lavorazioni e inserisci le quantit\u00e0: i prezzi unitari arrivano dal prezzario regionale ufficiale, con il codice di ogni voce.", "edili"),
 _prz("stime-idrauliche", "droplets", "Stime idrauliche", "Stima lavori idraulici", "Allacci e rimozioni di sanitari, con le opere edili collegate.",
      "Stima lavori idraulici dopo un danno da acqua: rimozione e allaccio di apparecchi sanitari e opere edili collegate, con prezzi del Prezzario Campania 2026.",
      "Per la ricerca e la riparazione del guasto il prezzario non ha voci specifiche: inseriscile come voce libera con il prezzo dell'idraulico.", "idraulici,edili"),
 _prz("stime-elettriche", "plug", "Stime elettriche", "Stima lavori elettrici", "Punti luce e prese con le opere murarie comprese.",
      "Stima il ripristino dell'impianto elettrico per punti luce e punti presa, opere murarie comprese, con i prezzi del Prezzario Campania 2026.",
      "Le voci del prezzario per punti luce e prese comprendono conduttori, scatole, frutto, placca e apertura delle tracce.", "elettrici,edili"),
 _prz("stime-ripristino", "wrench", "Stime di ripristino", "Stima completa di ripristino", "Esempio pronto: soffitto, pareti e pavimento dopo un danno da acqua.",
      "Stima completa del ripristino di un ambiente dopo un danno: rimozioni, intonaci, tinteggiature, massetto, pavimento e battiscopa con prezzi del Prezzario Campania 2026.",
      "Parte da un esempio di ripristino dopo un danno da acqua: modifica quantit\u00e0 e voci in base al tuo caso.", "edili,idraulici,elettrici"),
]
