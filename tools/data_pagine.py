# -*- coding: utf-8 -*-
from data_base import SITE

HOME_FAQ = [
 ("Quanto costa?", "Descrivere il caso è gratuito. La stima senza firma costa 30 €, la perizia auto/moto 60 €, mentre per danni alla casa e lesioni la prima consulenza è gratuita. Analisi documentali e consulenze specialistiche sono su preventivo, comunicato prima di iniziare."),
 ("Mi garantite il risarcimento?", "No. Nessuno può garantirlo onestamente: la decisione spetta alla compagnia e, in caso di disaccordo, alle procedure previste. Ti diamo una valutazione tecnica seria e documentata da usare nel confronto."),
 ("Devo venire in studio?", "No, nella maggior parte dei casi basta caricare foto e documenti online. Se serve un sopralluogo te lo diciamo prima, con il relativo costo."),
 ("Quali documenti servono?", "Dipende dal caso: di solito foto del danno, polizza, preventivi e comunicazioni della compagnia. Il percorso guidato ti indica cosa caricare e ti segnaliamo noi eventuali mancanze."),
 ("Vendete polizze?", "No. Ci occupiamo solo della parte tecnica del sinistro: documentare, quantificare e leggere la polizza."),
]

FAQ_ALL = [
 ("Servizi e costi", HOME_FAQ[:2] + [
   ("Che differenza c'è tra stima e perizia?", "La stima senza firma è una prima valutazione orientativa basata su foto e documenti. La perizia è una relazione completa, con quantificazione motivata di ogni voce, firmata dal tecnico."),
   ("Come pago?", "Online, al momento dell'ordine. Ricevi conferma via email e trovi l'ordine nella tua area personale."),
   ("Posso annullare?", "Sì, come consumatore hai 14 giorni per recedere. Se chiedi di iniziare subito e il servizio viene completato prima, il recesso non è più possibile; se recedi durante il lavoro paghi solo la parte svolta."),
 ]),
 ("Documenti e tempi", [HOME_FAQ[3],
   ("Quanto tempo ci vuole?", "La stima senza firma di norma entro 3 giorni lavorativi, la perizia auto/moto entro 5–7  dalla documentazione completa. Per casi complessi i tempi sono indicati nel preventivo."),
   ("Posso caricare documenti in un secondo momento?", "Sì, dalla tua area personale puoi aggiungere documenti in qualsiasi momento finché la pratica è aperta."),
   ("Entro quando devo avvisare la mia compagnia?", "Il Codice civile prevede l'avviso entro tre giorni da quando ne sei venuto a conoscenza, salvo termini diversi in polizza (art. 1913 c.c.). Non aspettare la nostra valutazione per farlo."),
 ]),
 ("StimaVeloce e la piattaforma", [HOME_FAQ[2], HOME_FAQ[4],
   ("Chi esegue le valutazioni?", "I tecnici di StimaVeloce. Gli strumenti digitali aiutano a organizzare i documenti, ma ogni valutazione è verificata e firmata da un professionista."),
   ("I miei dati sono al sicuro?", "Trattiamo i dati solo per gestire la tua richiesta, come descritto nell'informativa privacy. Ogni cliente vede solo le proprie pratiche."),
 ]),
]

_tit = SITE["ragione_sociale"] or SITE["studio"]
_mail = f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'

LEGALI = {
 "privacy": ("Privacy Policy", [
  ("Titolare del trattamento", [f"{_tit}, P.IVA {SITE['piva']}, sede legale {SITE['sede_legale']}. Contatto: {_mail}."]),
  ("Quali dati trattiamo", ["Dati che ci fornisci compilando il percorso guidato, il modulo contatti o un ordine: nome, email, telefono, descrizione del sinistro, foto e documenti caricati. Possono essere presenti dati relativi alla salute, se li inserisci tu (ad esempio referti in caso di lesioni): li trattiamo solo per gestire la tua richiesta.",
                            "Dati tecnici di navigazione strettamente necessari al funzionamento del sito."]),
  ("Perché li trattiamo", ["Per rispondere alle tue richieste e fornire i servizi richiesti (esecuzione di misure precontrattuali e del contratto, art. 6.1.b GDPR); per adempiere a obblighi di legge, ad esempio fiscali (art. 6.1.c); i dati relativi alla salute solo con il tuo consenso esplicito (art. 9.2.a)."]),
  ("Con chi li condividiamo", ["Con i fornitori tecnici che ci permettono di erogare il servizio, nominati responsabili del trattamento: hosting e gestione dei moduli (Netlify, Inc., con trasferimento verso gli Stati Uniti sulla base delle garanzie previste dal GDPR) e, quando attivati, i fornitori di pagamento ed email. Non vendiamo i tuoi dati."]),
  ("Per quanto tempo", ["Per il tempo necessario a gestire la richiesta e, per le pratiche e gli ordini, per i tempi previsti dalla legge (in genere 10 anni per la documentazione contabile). Le richieste che non diventano incarico vengono cancellate entro 24 mesi."]),
  ("I tuoi diritti", [f"Puoi chiedere accesso, rettifica, cancellazione, limitazione, portabilità e opporti al trattamento scrivendo a {_mail}. Puoi revocare il consenso in qualsiasi momento e proporre reclamo al Garante per la protezione dei dati personali (garanteprivacy.it)."]),
 ]),
 "cookie": ("Cookie Policy", [
  ("Cosa usiamo", ["Il sito usa solo strumenti tecnici necessari al funzionamento: la memoria del browser (localStorage) per ricordare le compilazioni in corso e l'accesso all'area personale. Non usiamo cookie di profilazione.",
                   "Se in futuro attiveremo strumenti di misurazione (ad esempio Google Analytics 4) o marketing, verranno caricati solo dopo il tuo consenso, richiesto con un apposito banner, e questa pagina verrà aggiornata."]),
  ("Come gestirli", ["Puoi cancellare i dati memorizzati dal browser dalle impostazioni del tuo browser. Così facendo verranno perse le compilazioni non inviate."]),
 ]),
 "condizioni": ("Condizioni generali", [
  ("Chi fornisce il servizio", [f"I servizi di StimaVeloce sono forniti da {_tit}, P.IVA {SITE['piva']}, sede legale {SITE['sede_legale']} ({_mail})."]),
  ("Oggetto", ["StimaVeloce offre servizi di consulenza tecnica sui sinistri: stime, perizie di parte, analisi documentali e consulenze. Non offre consulenza legale, non intermedia polizze e non garantisce l'esito di richieste di indennizzo o risarcimento."]),
  ("Ordine e pagamento", ["Il contratto si conclude con la conferma dell'ordine. Il prezzo è quello indicato al momento dell'ordine. Le attività aggiuntive (sopralluoghi, accertamenti) vengono svolte solo dopo l'accettazione di un preventivo scritto."]),
  ("Esecuzione", ["Il servizio inizia quando la documentazione necessaria è completa. I tempi indicati sono indicativi e decorrono da quel momento. Il cliente è responsabile della veridicità e completezza delle informazioni fornite."]),
  ("Recesso", ["Il consumatore può recedere entro 14 giorni dalla conclusione del contratto (art. 52 Codice del consumo), scrivendo a " + _mail + ". Se chiede espressamente che il servizio inizi durante il periodo di recesso, perde il diritto di recesso una volta che il servizio è stato completamente eseguito (art. 59, lett. a); in caso di recesso durante l'esecuzione è dovuto l'importo proporzionale a quanto già fornito (art. 57, comma 3)."]),
  ("Reclami", [f"Per reclami scrivi a {_mail}. Ti risponderemo entro 30 giorni."]),
  ("Legge applicabile", ["Si applica la legge italiana. Per i consumatori è competente il foro del luogo di residenza o domicilio del consumatore."]),
 ]),
}
