# -*- coding: utf-8 -*-
"""Guide «Il mondo dei sinistri». verificato=False => pagina in noindex finché lo Studio non approva il testo."""

CC = ("Codice civile, artt. 1882–1932 (Normattiva)", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:regio.decreto:1942-03-16;262")
CDA = ("D.Lgs. 7 settembre 2005, n. 209 – Codice delle assicurazioni private (Normattiva)", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-07;209")
IVASS = ("IVASS – Sezione consumatori", "https://www.ivass.it/consumatori/index.html")
CONSUMO = ("D.Lgs. 6 settembre 2005, n. 206 – Codice del consumo (Normattiva)", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206")

CATEGORIE = ["RCA", "Rami elementari", "Polizze casa", "Danni ai fabbricati", "Furti", "Incendi", "Infortuni", "Perizie", "Diritti dell'assicurato"]

AUTORE = "Redazione StimaVeloce"

GUIDE = [
 dict(
  slug="risarcimento-danni-auto", cat="RCA", icon="car", verificato=False,
  h1="Risarcimento danni auto: come funziona la richiesta",
  title="Risarcimento danni auto: procedura, termini e documenti | StimaVeloce",
  desc="Indennizzo diretto o richiesta alla compagnia del responsabile, termini per l'offerta, modulo CAI e prescrizione: la procedura di risarcimento dopo un incidente.",
  intro="Dopo un incidente stradale la richiesta di risarcimento segue regole precise stabilite dal Codice delle assicurazioni private. Conoscerle aiuta a non perdere tempo e a presentare una richiesta completa.",
  sezioni=[
   ("A chi chiedere il risarcimento", [
     "Se nell'incidente sono coinvolti due veicoli identificati e assicurati in Italia, e le eventuali lesioni del conducente non responsabile sono di lieve entità, si applica di norma l'indennizzo diretto: chiedi il risarcimento alla tua compagnia (art. 149 del Codice delle assicurazioni).",
     "Negli altri casi la richiesta va presentata alla compagnia del veicolo responsabile (art. 148). Il terzo trasportato chiede il risarcimento alla compagnia del veicolo su cui viaggiava, indipendentemente da chi abbia la colpa (art. 141).",
   ]),
   ("Cosa deve contenere la richiesta", [
     "La richiesta deve indicare le generalità di chi chiede il risarcimento, il luogo, il giorno e l'ora del sinistro, una descrizione dei fatti, i dati dei veicoli coinvolti e il luogo e gli orari in cui il veicolo è disponibile per l'ispezione da parte del perito. In caso di lesioni servono anche i dati relativi all'età, all'attività e al reddito e la documentazione medica.",
     "Il modulo di constatazione amichevole (CAI) firmato da entrambi i conducenti accelera la procedura e fa presumere che il sinistro si sia svolto come descritto.",
   ]),
   ("Entro quanto arriva l'offerta", [
     "La compagnia deve formulare un'offerta motivata, oppure comunicare i motivi per cui non la fa, entro 60 giorni dalla richiesta completa per i danni a veicoli e cose. Il termine si riduce a 30 giorni se il modulo CAI è firmato da entrambi i conducenti e sale a 90 giorni se ci sono lesioni (art. 148).",
     "Se l'offerta non arriva o non ti convince puoi chiedere chiarimenti, far verificare la valutazione da un perito di parte, presentare un reclamo alla compagnia e, se non sei soddisfatto della risposta, all'IVASS.",
   ]),
   ("Attenzione ai tempi", [
     "Il diritto al risarcimento del danno da circolazione di veicoli si prescrive in due anni (art. 2947, secondo comma, c.c.). Conserva copia di tutte le comunicazioni e delle ricevute di invio.",
   ]),
  ],
  fonti=[CDA, CC, IVASS],
  servizi=["perizia-danni-auto","contestazione-perizia-assicurativa"], tools=["vetusta"],
 ),
 dict(
  slug="perizia-assicurativa-di-parte", cat="Perizie", icon="clipboard-check", verificato=False,
  h1="Perizia assicurativa di parte: cos'è e quando serve",
  title="Perizia di parte assicurativa: cos'è, quando serve, come si usa | StimaVeloce",
  desc="La differenza tra il perito della compagnia e il perito di parte, quando conviene una perizia di parte e cosa deve contenere per essere utile.",
  intro="Dopo un sinistro la compagnia incarica un proprio perito per stimare il danno. Il perito di parte è invece un tecnico scelto da te, che valuta lo stesso danno nel tuo interesse.",
  sezioni=[
   ("Perito della compagnia e perito di parte", [
     "Il perito della compagnia accerta il danno e ne propone una quantificazione all'assicuratore. Il perito di parte esamina lo stesso danno per conto dell'assicurato o del danneggiato e ne verifica la valutazione.",
     "Per i danni a veicoli e cose derivanti dalla circolazione l'accertamento e la stima professionale sono riservati ai periti iscritti nel ruolo tenuto dall'IVASS (art. 157 del Codice delle assicurazioni).",
   ]),
   ("Quando conviene", [
     "Quando l'offerta ti sembra bassa e non capisci come è stata calcolata.",
     "Quando il danno è esteso o tecnico, ad esempio danni strutturali, impianti, incendi o attività commerciali.",
     "Quando la compagnia applica clausole come la regola proporzionale, scoperti o deprezzamenti che cambiano molto l'importo.",
   ]),
   ("Cosa deve contenere", [
     "Una perizia utile descrive il danno, indica le lavorazioni o i ricambi necessari con quantità e prezzi, spiega i criteri adottati e richiama le clausole di polizza pertinenti. Deve essere verificabile: chi la legge deve poter ricostruire ogni numero.",
   ]),
   ("Perizia contrattuale", [
     "Molte polizze danni prevedono che, in caso di disaccordo sull'ammontare, il danno sia quantificato da due periti nominati dalle parti ed eventualmente da un terzo. Le regole e la ripartizione delle spese sono scritte nelle condizioni di polizza.",
   ]),
  ],
  fonti=[CDA, CC, IVASS],
  servizi=["contestazione-perizia-assicurativa","perizia-danni-auto"], tools=["franchigia-scoperto"],
 ),
 dict(
  slug="franchigia-come-funziona", cat="Rami elementari", icon="percent", verificato=False,
  h1="Franchigia assicurativa: come funziona",
  title="Franchigia assicurazione: cos'è, come si calcola, esempi | StimaVeloce",
  desc="La franchigia è l'importo del danno che resta a tuo carico. Differenza tra franchigia assoluta e relativa, esempi di calcolo e interazione con i limiti di indennizzo.",
  intro="La franchigia è una parte del danno, espressa in euro, che resta a carico dell'assicurato. Serve a escludere i piccoli danni e a ridurre il premio.",
  sezioni=[
   ("Franchigia assoluta", [
     "È la forma più comune: l'importo indicato viene sempre sottratto dal danno indennizzabile. Esempio: danno 2.000 €, franchigia 250 € → indennizzo 1.750 €. Se il danno è inferiore alla franchigia non si riceve nulla.",
   ]),
   ("Franchigia relativa", [
     "Se il danno supera la franchigia viene indennizzato per intero; se è inferiore non viene pagato. È meno diffusa: verifica nella polizza quale forma è prevista.",
   ]),
   ("Franchigia e limiti di indennizzo", [
     "Quando la polizza prevede anche un limite di indennizzo, conta l'ordine con cui le clausole si applicano: di solito si sottrae prima la franchigia e poi si applica il limite, ma alcune polizze dispongono diversamente. Il calcolatore gratuito mostra il calcolo passo per passo.",
   ]),
   ("Dove trovarla", [
     "Le franchigie sono indicate nelle condizioni particolari o in una tabella riepilogativa, spesso diversa per ogni garanzia.",
   ]),
  ],
  fonti=[CC],
  servizi=["analisi-franchigie-scoperti","analisi-condizioni-generali"], tools=["franchigia-scoperto"],
 ),
 dict(
  slug="scoperto-assicurativo", cat="Rami elementari", icon="percent", verificato=False,
  h1="Scoperto assicurativo: cosa significa",
  title="Scoperto assicurativo: significato, minimo e massimo, esempi | StimaVeloce",
  desc="Lo scoperto è una percentuale del danno a carico dell'assicurato, spesso con un minimo e un massimo in euro. Come si calcola, con esempi.",
  intro="Lo scoperto è una quota percentuale del danno che resta a tuo carico. A differenza della franchigia cresce con l'importo del danno.",
  sezioni=[
   ("Come si calcola", [
     "Esempio: danno 8.000 €, scoperto 10% → restano a tuo carico 800 € e l'indennizzo è 7.200 €.",
   ]),
   ("Minimo e massimo", [
     "Spesso lo scoperto ha un minimo in euro: «scoperto 10% con il minimo di 500 €». Con un danno di 3.000 € il 10% sarebbe 300 €, ma si applica il minimo di 500 € e l'indennizzo è 2.500 €. Alcune polizze prevedono anche un massimo, oltre il quale la quota a tuo carico non cresce più.",
   ]),
   ("Scoperto e franchigia insieme", [
     "Possono essere previsti entrambi, oppure lo scoperto può sostituire la franchigia in situazioni particolari, ad esempio nel furto quando mancano alcuni mezzi di protezione. Leggi con attenzione le tabelle della polizza.",
   ]),
  ],
  fonti=[CC],
  servizi=["analisi-franchigie-scoperti","danni-da-furto"], tools=["franchigia-scoperto"],
 ),
 dict(
  slug="regola-proporzionale", cat="Rami elementari", icon="scale", verificato=False,
  h1="Regola proporzionale: cos'è la sottoassicurazione",
  title="Regola proporzionale (art. 1907 c.c.) e sottoassicurazione | StimaVeloce",
  desc="Se la somma assicurata è inferiore al valore del bene, l'indennizzo si riduce in proporzione. Come funziona l'art. 1907 c.c., le deroghe e un esempio di calcolo.",
  intro="Se assicuri un bene per una somma inferiore al suo valore effettivo, la compagnia risponde del danno solo in proporzione: è la regola proporzionale prevista dall'art. 1907 del Codice civile.",
  sezioni=[
   ("Il calcolo", [
     "Indennizzo = danno × somma assicurata ÷ valore del bene al momento del sinistro.",
     "Esempio: abitazione con valore di ricostruzione 300.000 €, assicurata per 200.000 €, danno 30.000 € → indennizzo 30.000 × 200.000 ÷ 300.000 = 20.000 €, prima di franchigie e scoperti.",
   ]),
   ("Le deroghe", [
     "L'art. 1907 consente di pattuire diversamente. Molte polizze prevedono una tolleranza (ad esempio il 10% o il 20%) entro la quale la regola non si applica, oppure la forma «a primo rischio assoluto», con cui si risponde fino alla somma assicurata senza considerare il valore totale.",
   ]),
   ("Come evitarla", [
     "Aggiorna periodicamente le somme assicurate, soprattutto dopo ristrutturazioni o acquisti importanti, e verifica se la polizza prevede l'adeguamento automatico all'indice dei prezzi.",
   ]),
  ],
  fonti=[CC],
  servizi=["danni-incendio","analisi-condizioni-generali"], tools=["sottoassicurazione"],
 ),
 dict(
  slug="come-leggere-polizza-casa", cat="Polizze casa", icon="house", verificato=False,
  h1="Come leggere una polizza casa",
  title="Come leggere una polizza casa: garanzie, esclusioni, limiti | StimaVeloce",
  desc="La struttura di una polizza casa e cosa controllare: definizioni, garanzie, esclusioni, franchigie, forme di assicurazione e obblighi in caso di sinistro.",
  intro="Una polizza casa riunisce spesso più garanzie: incendio, acqua condotta, eventi atmosferici, furto, responsabilità civile. Ecco come orientarsi.",
  sezioni=[
   ("1. Le definizioni", [
     "All'inizio trovi il glossario: «fabbricato», «contenuto», «acqua condotta», «scoppio». Il significato di questi termini decide cosa è coperto, per questo vanno letti per primi.",
   ]),
   ("2. Le garanzie e le esclusioni", [
     "Per ogni garanzia controlla cosa è assicurato e cosa è escluso. Le esclusioni sono spesso in un articolo a parte, ad esempio umidità e stillicidio, gelo o usura.",
   ]),
   ("3. Franchigie, scoperti e limiti", [
     "Di solito sono riassunti in una tabella. Ogni garanzia può avere valori diversi.",
   ]),
   ("4. La forma di assicurazione", [
     "Valore intero, con possibile applicazione della regola proporzionale, oppure primo rischio assoluto. Valore a nuovo o stato d'uso.",
   ]),
   ("5. Cosa fare in caso di sinistro", [
     "La polizza indica i termini per la denuncia e i documenti da presentare. In mancanza di termini diversi, il Codice civile prevede l'avviso entro tre giorni (art. 1913) e l'obbligo di fare il possibile per limitare il danno (art. 1914).",
   ]),
  ],
  fonti=[CC, IVASS],
  servizi=["analisi-condizioni-generali","danni-acqua-condotta"], tools=["franchigia-scoperto","sottoassicurazione"],
 ),
 dict(
  slug="quanto-costa-una-perizia", cat="Perizie", icon="badge-euro", verificato=False,
  h1="Quanto costa una perizia assicurativa",
  title="Quanto costa una perizia assicurativa di parte | StimaVeloce",
  desc="Da cosa dipende il costo di una perizia di parte e quali sono i prezzi dei servizi StimaVeloce: stima senza firma 30 €, perizia auto/moto 60 €, perizia fabbricati 130 €.",
  intro="Il costo di una perizia di parte dipende soprattutto dalla complessità del danno e dal lavoro necessario per documentarlo.",
  sezioni=[
   ("Cosa incide sul prezzo", [
     "Tipo di danno ed estensione, necessità di un sopralluogo, numero di documenti da esaminare, livello di dettaglio richiesto (stima orientativa o relazione completa) ed eventuali accertamenti di terzi.",
   ]),
   ("I prezzi di StimaVeloce", [
     "Stima senza firma: 30 €. Perizia auto/moto: 60 €. Perizia fabbricati: 130 €. Valutazione medico-legale: 250 €. Analisi documentale e consulenze specialistiche: su preventivo comunicato prima di iniziare. Il dettaglio di cosa è incluso è nella pagina Prezzi.",
   ]),
   ("Prima di affidare l'incarico", [
     "Chiedi sempre cosa è incluso, i tempi, il formato del documento e gli eventuali costi aggiuntivi. Diffida di chi promette risultati certi o compensi legati a un risarcimento garantito.",
   ]),
  ],
  fonti=[CONSUMO],
  servizi=["contestazione-perizia-assicurativa","perizia-danni-auto"], tools=["preventivo-lavori"],
 ),
 dict(
  slug="come-valutare-danno-fabbricato", cat="Danni ai fabbricati", icon="building-2", verificato=False,
  h1="Come valutare un danno al fabbricato",
  title="Come valutare un danno al fabbricato: computo e prezzi | StimaVeloce",
  desc="Il metodo per stimare un danno a un edificio: elenco delle lavorazioni, quantità, prezzi unitari, IVA, vetustà e clausole di polizza.",
  intro="Stimare un danno al fabbricato significa descrivere cosa serve per riportarlo allo stato precedente, misurarlo e dargli un prezzo.",
  sezioni=[
   ("1. Elencare le lavorazioni", [
     "Per ogni ambiente: rimozioni e demolizioni, rifacimenti (intonaci, massetti, pavimenti), impianti, finiture e tinteggiature, smaltimento dei materiali.",
   ]),
   ("2. Misurare le quantità", [
     "Metri quadrati di superficie, metri lineari, numero di elementi. Foto con riferimenti metrici e una planimetria aiutano molto.",
   ]),
   ("3. Applicare prezzi unitari motivati", [
     "Come riferimento si possono usare i prezzari regionali dei lavori pubblici, ad esempio quello della Regione Campania, o preventivi di imprese con voci dettagliate.",
   ]),
   ("4. Aggiungere le voci accessorie", [
     "Oneri per la sicurezza, eventuali spese tecniche, IVA quando non è recuperabile.",
   ]),
   ("5. Applicare la polizza", [
     "Valore a nuovo o stato d'uso, franchigie, scoperti, limiti e regola proporzionale. Il calcolatore danni al fabbricato ti guida in questi passaggi.",
   ]),
  ],
  fonti=[CC],
  servizi=["danni-fabbricati","valutazione-preventivi"], tools=["danni-fabbricato","preventivo-lavori"],
 ),
 dict(
  slug="risarcimento-danni-allagamento", cat="Polizze casa", icon="droplets", verificato=False,
  h1="Risarcimento danni da allagamento",
  title="Danni da allagamento: cosa copre la polizza e cosa fare | StimaVeloce",
  desc="Allagamento da tubazioni, nubifragio o alluvione: garanzie diverse, cosa fare subito e come documentare i danni per la richiesta di indennizzo.",
  intro="«Allagamento» può voler dire cose molto diverse per una polizza: rottura di una tubazione, acqua piovana, esondazione o alluvione. Ognuna ricade in una garanzia diversa.",
  sezioni=[
   ("Quale garanzia si applica", [
     "Acqua condotta: rottura accidentale di impianti idrici o di riscaldamento. Eventi atmosferici: acqua piovana entrata a causa di danni provocati dall'evento al fabbricato. Alluvione e inondazione: rientrano tra le catastrofi naturali, spesso escluse dalle polizze ordinarie o assicurabili con garanzie specifiche. Per le imprese la legge 30 dicembre 2023, n. 213 ha introdotto l'obbligo di assicurarsi contro alcuni eventi catastrofali.",
   ]),
   ("Cosa fare subito", [
     "Metti in sicurezza persone e impianti, limita il danno (art. 1914 c.c.), fotografa e filma tutto prima di pulire e conserva i beni danneggiati finché la compagnia non li ha visti. Avvisa la compagnia nei termini della polizza.",
   ]),
   ("Come documentare", [
     "Foto d'insieme e di dettaglio con l'altezza raggiunta dall'acqua, elenco dei beni danneggiati con età e valore, fatture degli interventi urgenti, preventivi di ripristino.",
   ]),
  ],
  fonti=[CC, IVASS],
  servizi=["danni-acqua-condotta","danni-eventi-atmosferici"], tools=["danni-fabbricato","franchigia-scoperto"],
 ),
]
