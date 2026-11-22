# -*- coding: utf-8 -*-
"""Dati generali del sito StimaVeloce. Modifica qui prezzi, contatti e dati societari:
lo script build.py rigenera tutte le pagine."""

SITE = {
    "url": "https://stimaveloce.it",
    "name": "StimaVeloce",
    "studio": "StimaVeloce",
    "city": "Online in tutta Italia",
    "email": "studiotecnicodellavecchia@gmail.com",
    # Da completare: lasciare vuoto finché non disponibile (non viene mostrato)
    "telefono": "",
    "whatsapp": "",
    "indirizzo": "",
    "piva": "04034390783",
    "ragione_sociale": "Della Vecchia Vincenzo",
    "sede_legale": "C.da Piano delle Donne, 87021 Belvedere Marittimo (CS)",
    "google_reviews_url": "https://www.google.com/search?q=Studio+Tecnico+Legale+Della+Vecchia+Casoria",
    "ga4_id": "",           # es. G-XXXXXXX: si attiva solo dopo consenso cookie
    "gsc_verification": "", # codice di verifica Google Search Console
    "updated": "19 novembre 2026",
    "updated_iso": "2026-11-19",
}

APP = "/app/"  # percorso guidato, area cliente e gestionale

# Prezzi: un solo punto da cui li leggono tutte le pagine.
PREZZI = [
    {
        "id": "stima", "nome": "Stima senza firma", "prezzo": 30, "da": False,
        "breve": "Una prima valutazione tecnica del danno, da foto e documenti, senza firma del perito.",
        "comprende": [
            "Esame delle foto e dei documenti che carichi",
            "Valutazione orientativa del danno con indicazione delle voci considerate",
            "Indicazione dei documenti mancanti e dei passi successivi consigliati",
            "Risposta scritta nella tua area personale",
        ],
        "esclude": [
            "Sopralluogo sul posto",
            "Relazione peritale firmata da utilizzare verso terzi",
            "Trattativa con la compagnia",
        ],
        "documenti": ["Foto del danno", "Eventuale polizza o offerta ricevuta", "Breve descrizione dell'accaduto"],
        "tempi": "Di norma entro 3 giorni lavorativi dalla documentazione completa",
        "formato": "Documento PDF nella tua area personale",
        "extra": "Nessuno. Se serve un sopralluogo o una perizia ti viene proposto prima un preventivo.",
    },
    {
        "id": "perizia", "nome": "Perizia auto/moto", "prezzo": 60, "da": False,
        "breve": "Relazione tecnica firmata sui danni al veicolo, con quantificazione motivata.",
        "comprende": [
            "Analisi tecnica di foto, documenti e preventivi",
            "Quantificazione motivata delle voci di danno",
            "Relazione tecnica firmata in PDF",
            "Indicazione della documentazione da presentare alla compagnia",
        ],
        "esclude": [
            "Sopralluogo sul posto (preventivo a parte)",
            "Assistenza legale e attività giudiziale",
            "Spese per accertamenti di terzi (analisi di laboratorio, ditte specializzate)",
        ],
        "documenti": ["Foto del danno", "Polizza (condizioni generali e particolari)", "Preventivi o fatture", "Comunicazioni con la compagnia"],
        "tempi": "Di norma 5–7 giorni lavorativi dalla documentazione completa",
        "formato": "Relazione tecnica in PDF firmata",
        "extra": "Il sopralluogo, se necessario, viene quotato prima e solo con il tuo consenso.",
    },
    {
        "id": "fabbricati", "nome": "Perizia fabbricati", "prezzo": 130, "da": False, "vendibile": False,
        "breve": "Relazione tecnica firmata sui danni a casa, condominio o locali, con computo delle lavorazioni.",
        "comprende": ["Analisi di foto, misure, polizza e preventivi", "Computo delle lavorazioni con prezzi di riferimento", "Applicazione delle clausole di polizza", "Relazione tecnica firmata in PDF"],
        "esclude": ["Sopralluogo (preventivo a parte)", "Indagini strumentali (ricerca perdite, termografia)", "Assistenza legale"],
        "documenti": ["Foto e misure degli ambienti", "Polizza", "Preventivi", "Comunicazioni con la compagnia o il condominio"],
        "tempi": "Di norma 7–10 giorni lavorativi dalla documentazione completa",
        "formato": "Relazione tecnica in PDF firmata",
        "extra": "Il sopralluogo, se necessario, viene quotato prima e solo con il tuo consenso.",
    },
    {
        "id": "medico", "nome": "Valutazione medico-legale", "prezzo": 250, "da": False, "vendibile": False,
        "breve": "Valutazione delle lesioni a cura di un medico legale, per sinistri con danni alla persona.",
        "comprende": ["Esame della documentazione sanitaria da parte di un medico legale", "Valutazione dei postumi e dell'inabilit\u00e0 temporanea", "Relazione medico-legale firmata dal medico"],
        "esclude": ["Visite specialistiche ed esami strumentali", "Spese mediche", "Assistenza legale"],
        "documenti": ["Referti e certificati medici", "Verbale di pronto soccorso", "Documentazione del sinistro"],
        "tempi": "Concordati dopo l'esame della documentazione; pu\u00f2 servire una visita",
        "formato": "Relazione medico-legale in PDF",
        "extra": "Eventuale visita medico-legale secondo preventivo. I dati sanitari sono trattati solo con il tuo consenso esplicito.",
    },
    {
        "id": "analisi", "nome": "Analisi documentale personalizzata", "prezzo": None, "da": False,
        "breve": "Lettura della polizza e dei documenti del sinistro, con sintesi delle clausole rilevanti.",
        "comprende": [
            "Lettura di condizioni generali e particolari",
            "Sintesi di garanzie, esclusioni, franchigie, scoperti e limiti, con rimando a pagina e articolo",
            "Indicazione dei punti da approfondire",
        ],
        "esclude": ["Pareri legali", "Quantificazione del danno (disponibile con la perizia)"],
        "documenti": ["Polizza completa", "Documenti del sinistro"],
        "tempi": "Concordati in base al numero e alla lunghezza dei documenti",
        "formato": "Sintesi in PDF",
        "extra": "Prezzo comunicato prima di iniziare, in base ai documenti.",
    },
    {
        "id": "consulenza", "nome": "Consulenza specialistica", "prezzo": None, "da": False,
        "breve": "Supporto tecnico per sinistri complessi, contestazioni e casi con più parti.",
        "comprende": ["Esame preliminare del caso", "Preventivo scritto prima di qualsiasi attività"],
        "esclude": ["Attività non indicate nel preventivo accettato"],
        "documenti": ["Tutta la documentazione disponibile"],
        "tempi": "Indicati nel preventivo",
        "formato": "Secondo l'incarico",
        "extra": "Solo quelli indicati nel preventivo che accetti.",
    },
]

CONDIZIONI_PAGAMENTO = (
    "I prezzi indicati sono finali: StimaVeloce applica il regime forfettario, quindi non viene addebitata l'IVA "
    "(art. 1, commi 54-89, legge 190/2014). Il pagamento avviene online al momento dell'ordine. Il lavoro inizia quando la documentazione è completa. "
    "Come consumatore hai 14 giorni per recedere (art. 52 Codice del consumo). Se chiedi di iniziare subito, "
    "il recesso non è più possibile una volta che il servizio è stato completamente eseguito con il tuo consenso "
    "(art. 59, lett. a, Codice del consumo); se recedi prima, viene trattenuta solo la parte già svolta."
)


ACCESSORI = [
    ("Accessori per la pratica", "Servizi aggiuntivi alla gestione del sinistro"),
    ("Supporto peritale per avvocati e professionisti", "Perizie e consulenze tecniche per studi legali e professionisti"),
]


def prezzo_label(p):
    if p["prezzo"] is None:
        return "Su preventivo"
    return ("da " if p["da"] else "") + f"{p['prezzo']} €"
