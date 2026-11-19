# -*- coding: utf-8 -*-
"""Genera il sito statico StimaVeloce.  Uso:  python3 tools/build.py
Le pagine vengono scritte nella cartella principale del repository (pubblicata da Netlify)."""
import json, os, html, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from data_base import SITE, APP, PREZZI, CONDIZIONI_PAGAMENTO, prezzo_label
from data_servizi import SERVIZI, AMBITI
from data_guide import GUIDE, AUTORE
from data_strumenti import STRUMENTI
from data_pagine import HOME_FAQ, FAQ_ALL, LEGALI

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))
U = SITE["url"]
SV = {s["slug"]: s for s in SERVIZI}
GV = {g["slug"]: g for g in GUIDE}
TV = {t["slug"]: t for t in STRUMENTI}
PV = {p["id"]: p for p in PREZZI}
PAGES = []  # (path, indicizzabile)
TITLES = {}
CSSV = str(int(os.path.getmtime(os.path.join(ROOT, "assets/site.css"))))

e = lambda s: html.escape(str(s), quote=True)


def ic(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


LOGO_SVG = ('<svg viewBox="0 0 34 38" aria-hidden="true"><path d="M17 1.5 31.5 6.5V18c0 9.5-6.5 15.5-14.5 18.5C9 33.5 2.5 27.5 2.5 18V6.5Z" fill="#30363D"/>'
            '<path d="M10.5 19.2l4.6 4.6 8.4-10" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="27.5" cy="8.5" r="2.4" fill="#C7AD7C"/></svg>')


def logo(href="/"):
    return f'<a class="logo" href="{href}" aria-label="StimaVeloce, pagina iniziale">{LOGO_SVG}<b>StimaVeloce<i>.</i></b></a>'


MENU = [("/aiuto/incidenti-stradali/", "car", "Auto e Moto", "Incidenti, carrozzeria, moto e veicoli commerciali"),
        ("/casa/", "house", "Casa e Fabbricati", "Acqua, infiltrazioni, incendio, eventi atmosferici"),
        ("/aiuto/attivita-commerciali/", "store", "Aziende", "Locali, impianti, attrezzature, fermo attivit\u00e0"),
        ("/servizi/sinistri-nautici/", "sailboat", "Nautica", "Imbarcazioni, ormeggio, mareggiate"),
        ("/aiuto/infortuni-persona/", "heart-pulse", "Infortuni e Lesioni", "Documentazione e calcoli orientativi"),
        ("/aiuto/analisi-polizze/", "file-search", "Analisi Polizze", "Garanzie, esclusioni, franchigie, limiti"),
        ("/aiuto/perizie-stime/", "clipboard-check", "Perizie e Consulenze", "Stime, perizie di parte, contestazioni")]
NAV2 = [("/guide/", "Guide e risorse"), ("/strumenti/", "Strumenti"), ("/chi-siamo/", "Chi siamo")]


def header(cur):
    mega = "".join(f'<a href="{h}">{ic(i)}<div><b>{t}</b><span>{d}</span></div></a>' for h, i, t, d in MENU)
    mega += f'<a class="all" href="/servizi/">Tutti i servizi e i prezzi \u2192</a>'
    links = "".join(f'<a href="{h}"{" aria-current=page" if cur == h else ""}>{t}</a>' for h, t in NAV2)
    mlinks = "".join(f'<a href="{h}">{ic(i)}{t}</a>' for h, i, t, d in MENU)
    mlinks += f'<a href="/guide/">{ic("book-open")}Guide e risorse</a><a href="/strumenti/">{ic("calculator")}Strumenti gratuiti</a><a href="/prezzi/">{ic("badge-euro")}Prezzi</a><a href="/chi-siamo/">{ic("users")}Chi siamo</a><a href="/contatti/">{ic("mail")}Contatti</a><a href="{APP}#area">{ic("log-in")}Area Clienti</a>'
    srch = f'<div class="srch">{ic("search")}<input class="srch-in" type="search" placeholder="Cerca: infiltrazione, franchigia, perizia auto\u2026" aria-label="Cerca nel sito" data-srch><ul class="srch-res" data-srch-res></ul></div>'
    return f'''<a class="skip" href="#main">Vai al contenuto</a>
<header class="hd"><div class="wrap">{logo()}
<nav class="nav" aria-label="Principale"><details class="dd"><summary{" aria-current=page" if cur == "/servizi/" else ""}>Servizi{ic("chevron-down")}</summary><div class="mega">{mega}</div></details>{links}</nav>
<div class="hd-r"><button class="sbtn hide-m" type="button" data-open-srch aria-label="Cerca nel sito">{ic("search")}</button><a class="btn btn-g btn-sm hide-m" href="{APP}#area">{ic("user")}Area Clienti</a><a class="btn btn-p btn-sm" href="{APP}#prefattibilita">Analizza il tuo sinistro</a>
<details class="mnav"><summary aria-label="Apri il menu">{ic("menu")}</summary><div class="panel">{srch}{mlinks}<a class="btn btn-p" href="{APP}#prefattibilita" style="border:0;color:#fff;justify-content:center">Analizza il tuo sinistro</a></div></details>
</div></div></header>
<dialog class="sdlg" data-srch-dlg><form method="dialog" style="display:flex;justify-content:flex-end;margin:0 0 8px"><button class="sbtn" aria-label="Chiudi">{ic("x")}</button></form>{srch}</dialog>'''


def footer():
    contatti = [f'<li><a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a></li>']
    if SITE["telefono"]:
        contatti.append(f'<li><a href="tel:{SITE["telefono"].replace(" ", "")}">{e(SITE["telefono"])}</a></li>')
    if SITE["indirizzo"]:
        contatti.append(f'<li>{e(SITE["indirizzo"])}</li>')
    else:
        contatti.append(f'<li>{e(SITE["city"])}</li>')
    contatti.append('<li><a href="/contatti/">Scrivici</a></li>')
    serv = "".join(f'<li><a href="/servizi/{s["slug"]}/">{e(s["h1"])}</a></li>' for s in SERVIZI[:7])
    guide = "".join(f'<li><a href="/guide/{g["slug"]}/">{e(g["h1"].split(":")[0])}</a></li>' for g in GUIDE[:6])
    tit = SITE["ragione_sociale"] or SITE["studio"]
    piva = f' · P.IVA {e(SITE["piva"])}' if SITE["piva"] else ""
    return f'''<footer class="ft"><div class="wrap"><div class="cols">
<div>{logo()}<p style="margin-top:18px;max-width:340px">Analisi tecniche, stime e perizie assicurative a cura dello {e(SITE["studio"])}. Consulenza tecnica sui sinistri: non vendiamo polizze.</p><h4 style="margin-top:26px">Contatti</h4><ul>{"".join(contatti)}</ul></div>
<div><h4>Servizi</h4><ul>{serv}<li><a href="/servizi/">Tutti i servizi</a></li><li><a href="/prezzi/">Prezzi</a></li></ul></div>
<div><h4>Guide</h4><ul>{guide}<li><a href="/guide/">Tutte le guide</a></li><li><a href="/strumenti/">Strumenti gratuiti</a></li></ul></div>
<div><h4>Studio</h4><ul><li><a href="/chi-siamo/">Chi siamo</a></li><li><a href="/come-funziona/">Come funziona</a></li><li><a href="/faq/">Domande frequenti</a></li><li><a href="{APP}#area">Area personale</a></li><li><a href="/privacy/">Privacy Policy</a></li><li><a href="/cookie/">Cookie Policy</a></li><li><a href="/condizioni/">Condizioni generali</a></li></ul></div>
</div><div class="legal"><span>© 2026 {e(tit)}{piva} · Titolare del servizio: {e(tit)}, {e(SITE["city"])}</span><span>Le informazioni del sito hanno carattere generale e non sostituiscono una valutazione professionale del caso.</span></div></div></footer>'''


def breadcrumb(items):
    lis = "".join((f'<li><a href="{h}">{e(t)}</a></li>' if h else f'<li aria-current="page">{e(t)}</li>') for h, t in items)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": U + h} if h else {})} for i, (h, t) in enumerate(items)]}
    return f'<nav aria-label="Percorso"><ol class="bc">{lis}</ol></nav>', ld


FOTO_ALT = {}


def foto(m):
    k = m.group(1)
    for ext in ("avif", "webp", "jpg"):
        if os.path.exists(os.path.join(ROOT, "assets/foto", f"{k}.{ext}")):
            alt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            return f'<div class="ph-slot" data-foto="{k}"><img src="/assets/foto/{k}.{ext}" alt="{e(FOTO_ALT.get(k, alt))}" loading="lazy" decoding="async"></div>'
    return m.group(0)


def page(path, title, desc, body, cur="", index=True, ld=None, og_type="website", extra_head="", scripts=""):
    body = re.sub(r'<div class="ph-slot" data-foto="([a-z0-9-]+)">(.*?)</div>', foto, body)
    canon = U + path
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    robots = "" if index else '<meta name="robots" content="noindex,follow">'
    gsc = f'<meta name="google-site-verification" content="{e(SITE["gsc_verification"])}">' if SITE["gsc_verification"] and path == "/" else ""
    doc = f'''<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}{gsc}
<link rel="canonical" href="{canon}">
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add("js")</script><link rel="stylesheet" href="/assets/site.css?v={CSSV}">
<meta name="theme-color" content="#30363D"><link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="StimaVeloce"><meta property="og:url" content="{canon}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{U}/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
{lds}{extra_head}</head><body>{header(cur)}<main id="main">{body}</main>{footer()}<script src="/assets/site.js?v={CSSV}" defer></script>{scripts}</body></html>'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    PAGES.append((path, index))
    TITLES[path] = (title.split(" | ")[0], desc)


ORG = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": U + "/#studio", "name": "StimaVeloce – " + SITE["studio"],
       "url": U + "/", "logo": U + "/icon-512.png", "image": U + "/og-image.jpg", "email": SITE["email"],
       "address": {"@type": "PostalAddress", "addressLocality": "Casoria", "addressRegion": "NA", "addressCountry": "IT"}, "areaServed": "IT"}
if SITE["telefono"]:
    ORG["telephone"] = SITE["telefono"]


def faq_html(items, ld=True):
    h = "".join(f'<details><summary>{e(q)}{ic("chevron-down")}</summary><div class="a">{e(a)}</div></details>' for q, a in items)
    j = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<div class="faq">{h}</div>', j


def band(title="Raccontaci cosa è successo", text="Bastano pochi minuti. Ti diciamo quale servizio è più adatto, prima di qualsiasi pagamento.", btn="Analizza il tuo sinistro"):
    return f'<section class="sec"><div class="wrap"><div class="band"><div><h2>{e(title)}</h2><p>{e(text)}</p></div><a class="btn btn-p btn-lg" href="{APP}#prefattibilita">{e(btn)}{ic("arrow-right")}</a></div></div></section>'


def ph(crumbs, h1, lead="", eyebrow=""):
    bc, ld = breadcrumb(crumbs)
    eb = f'<div class="eyebrow">{e(eyebrow)}</div>' if eyebrow else ""
    return f'<section class="ph"><div class="wrap">{bc}{eb}<h1>{e(h1)}</h1>{f"<p class=lead>{e(lead)}</p>" if lead else ""}</div></section>', ld


def svc_card(s):
    return f'<a class="card" href="/servizi/{s["slug"]}/"><div class="ibox">{ic(s["icon"])}</div><h3>{e(s["h1"])}</h3><p class="muted small">{e(s["desc"].split(".")[0])}.</p><span class="more">Scopri il servizio{ic("arrow-right")}</span></a>'


def tool_card(t):
    return f'<a class="card tool-card" href="/strumenti/{t["slug"]}/"><div class="ibox">{ic(t["icon"])}</div><div><h3>{e(t["nome"])}</h3><p>{e(t["breve"])}</p></div></a>'


def guide_card(g):
    return f'<a class="card" href="/guide/{g["slug"]}/"><span class="tag">{e(g["cat"])}</span><h3 style="margin-top:14px">{e(g["h1"])}</h3><p class="muted small">{e(g["desc"])}</p><span class="more">Leggi la guida{ic("arrow-right")}</span></a>'


def price_box(ids):
    out = []
    for i in ids:
        p = PV[i]
        out.append(f'<div class="card price-box"><div class="muted small">{e(p["nome"])}</div><div class="p">{prezzo_label(p)}</div><p class="small muted">{e(p["tempi"])}.</p>'
                   f'<a class="btn {"btn-p" if p["prezzo"] else "btn-s"}" style="width:100%" href="{APP}#prefattibilita">{"Inizia" if p["prezzo"] else "Chiedi un preventivo"}</a></div>')
    return "".join(out)


# ------------------------------------------------------------------ HOME
def build_home():
    ambiti = "".join(
        f'<a class="card rv" href="{"/casa/" if a["slug"] == "danni-casa" else "/aiuto/" + a["slug"] + "/"}"><div class="ibox">{ic(a["icon"])}</div><h3>{e(a["nome"])}</h3><ul class="ticks">{"".join(f"<li>{e(v)}</li>" for v in a["voci"])}</ul><span class="more">Vai alla sezione{ic("arrow-right")}</span></a>'
        for a in AMBITI)
    steps = [("Raccontaci cosa è successo", "Rispondi a poche domande guidate, a tocchi. Nessuna competenza assicurativa richiesta."),
             ("Carica fotografie e documenti", "Foto, polizza, preventivi, lettere della compagnia: anche dal telefono."),
             ("Ricevi una valutazione professionale", "Un tecnico dello Studio esamina il caso e ti propone il servizio adatto."),
             ("Segui la pratica online", "Stato di avanzamento, documenti e relazione nella tua area personale.")]
    steps_h = "".join(f'<div class="step rv rv-d{i % 4}"><div class="n">{i + 1}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(steps))
    feats = [("file-search", "Analisi documentale", "Leggiamo polizze, perizie e preventivi e indichiamo la clausola o la voce a cui ci riferiamo."),
             ("award", "Professionisti qualificati", "Le valutazioni sono svolte e firmate dai tecnici dello Studio."),
             ("monitor", "Procedure digitali", "Apri la pratica e carica i documenti online, senza appuntamenti."),
             ("badge-euro", "Costi trasparenti", "Prezzi pubblicati e preventivo scritto prima di ogni attività aggiuntiva."),
             ("list-checks", "Pratiche tracciabili", "Ogni pratica ha un codice e uno stato aggiornato che puoi consultare."),
             ("message-square", "Supporto personalizzato", "Un riferimento che conosce il tuo caso, per domande e chiarimenti.")]
    feats_h = "".join(f'<div class="feat rv"><div class="ibox">{ic(i)}</div><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>' for i, t, d in feats)
    tools = "".join(tool_card(t) for t in STRUMENTI)
    fq, fqld = faq_html(HOME_FAQ)
    mock = f'''<div class="mock" role="img" aria-label="Esempio di relazione tecnica digitale con foto, voci di danno e stato della pratica">
<div class="mock-h"><div><b>Relazione tecnica</b><small>Pratica SV-2026-0142 · Danni da acqua condotta</small></div><span class="pill">{ic("circle-check")}Documenti completi</span></div>
<div class="mock-ph"><div>{ic("camera")}</div><div>{ic("image")}</div><div>{ic("file-text")}</div><div>{ic("receipt")}</div></div>
<div class="mock-row"><span>{ic("ruler")}Ripristino intonaci · 18 m²</span><b>€ ···</b></div>
<div class="mock-row"><span>{ic("paintbrush")}Tinteggiature · 64 m²</span><b>€ ···</b></div>
<div class="mock-row"><span>{ic("wrench")}Ricerca e riparazione guasto</span><b>€ ···</b></div>
<div class="mock-row"><span>{ic("percent")}Franchigia di polizza · art. 12</span><b>− € ···</b></div>
<div class="mock-tot"><span>Stima motivata</span><b>In verifica</b></div>
<div class="mock-st"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i></div>
<div class="mock-note">Stato: in verifica professionale · 5 di 8</div>
<div class="mock-badge">{ic("shield-check")}Ogni voce è verificabile</div></div>'''
    body = f'''<section class="hero"><div class="wrap"><div>
<div class="eyebrow">Consulenza tecnica assicurativa</div>
<h1>Il tuo sinistro. <span>La nostra competenza.</span></h1>
<p class="lead">Dalla valutazione del danno all'analisi della polizza. Un percorso semplice, professionale e digitale.</p>
<div class="cta-row"><a class="btn btn-p btn-lg" href="{APP}#prefattibilita">Analizza il tuo sinistro{ic("arrow-right")}</a><a class="btn btn-s btn-lg" href="#aiuto">Scopri come possiamo aiutarti</a></div>
<p class="trust">{ic("shield-check")}Competenza tecnica, trasparenza e supporto professionale in ogni fase.</p>
</div>{mock}</div></section>
<section class="sec" id="aiuto"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Scegli il tuo caso</div><h2>In cosa possiamo aiutarti?</h2><p class="lead">Seleziona l'ambito: trovi i servizi dedicati, gli strumenti utili e le guide.</p></div><div class="grid g3">{ambiti}</div></div></section>
<section class="sec sec-s" id="come-funziona"><div class="wrap"><div class="sec-h"><div class="eyebrow">Come funziona</div><h2>Richiedere una valutazione non è mai stato così semplice.</h2></div><div class="steps">{steps_h}</div><p style="margin-top:28px"><a class="btn btn-p" href="{APP}#prefattibilita">Inizia ora, è gratuito{ic("arrow-right")}</a> <a class="btn btn-g" href="/come-funziona/">Tutti i dettagli</a></p></div></section>
<section class="sec sec-w"><div class="wrap"><div class="sec-h"><div class="eyebrow">Perché StimaVeloce</div><h2>La competenza tecnica incontra la tecnologia.</h2><p class="lead">Non promettiamo risultati: ti diamo una valutazione tecnica seria, documentata e comprensibile.</p></div><div class="grid g3" style="gap:36px 32px">{feats_h}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div class="eyebrow">Strumenti gratuiti</div><h2>Strumenti intelligenti per capire meglio i tuoi danni.</h2><p class="lead">Calcolatori con formule visibili e spiegazione del risultato. Gratuiti e senza registrazione.</p></div><div class="grid g3">{tools}</div></div></section>
<section class="sec sec-s"><div class="wrap"><div class="sec-h"><div class="eyebrow">Recensioni</div><h2>Le opinioni dei clienti</h2><p class="lead">Pubblichiamo solo recensioni reali e verificabili, raccolte sul profilo Google dello Studio.</p></div>
<div class="rev-empty"><div><div class="stars">{ic("star")}{ic("star")}{ic("star")}{ic("star")}{ic("star")}</div><h3 style="margin:10px 0 4px">Sei già nostro cliente?</h3><p class="muted" style="margin:0">Raccontaci com'è andata: la tua opinione aiuta altre persone a scegliere.</p></div><a class="btn btn-s" href="{e(SITE["google_reviews_url"])}" rel="noopener" target="_blank">Recensioni su Google{ic("external-link")}</a></div></div></section>
<section class="sec"><div class="wrap narrow"><div class="sec-h"><div class="eyebrow">Domande frequenti</div><h2>Le risposte alle domande più comuni</h2></div>{fq}<p style="margin-top:24px"><a class="more" href="/faq/">Tutte le domande{ic("arrow-right")}</a></p></div></section>
{band()}
<script>(function(){{var h=location.hash;if(/^#[a-z][a-z0-9-]*$/.test(h)&&!document.getElementById(h.slice(1)))location.replace("{APP}"+h);}})();</script>'''
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "StimaVeloce", "url": U + "/", "inLanguage": "it-IT"}
    page("/", "StimaVeloce – Il tuo sinistro, la nostra competenza | Perizie online",
         "Hai subito un danno? Analisi tecniche, stime e perizie assicurative online per auto, casa, attività e infortuni. Stima tecnica da 45 €, perizia 69 €.",
         body, cur="/", ld=[ORG, web, fqld])


# ------------------------------------------------------------------ SERVIZI
def build_servizi():
    for s in SERVIZI:
        a = next(x for x in AMBITI if x["slug"] == s["ambito"])
        head, bld = ph([("/", "Home"), ("/servizi/", "Servizi"), ("", s["h1"])], s["h1"], s["desc"], a["nome"])
        fq, fqld = faq_html(s["faq"])
        rel_t = "".join(tool_card(TV[t]) for t in s["tools"])
        rel_g = "".join(f'<li><a href="/guide/{g}/">{e(GV[g]["h1"])}</a></li>' for g in s["guides"])
        rel_s = "".join(f'<li><a href="/servizi/{x}/">{e(SV[x]["h1"])}</a></li>' for x in s["correlati"])
        body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><article class="prose">
<h2>Il problema</h2><p>{e(s["problema"])}</p>
<h2>Come ti aiutiamo</h2><p>{e(s["servizio"])}</p><div class="box"><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in s["cosa"])}</ul></div>
<h2>Documenti necessari</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in s["documenti"])}</ul><p class="small muted">Se non hai tutto non preoccuparti: ti indichiamo noi cosa manca.</p>
<h2>Come si svolge</h2><ol class="olist">{"".join(f"<li>{e(x)}</li>" for x in s["passi"])}</ol>
<h2>Costi</h2><p>I prezzi sono pubblicati e il preventivo per eventuali attività aggiuntive ti viene comunicato prima. <a href="/prezzi/">Cosa comprende ogni servizio</a>.</p><div class="grid g2">{price_box(s["prezzi"])}</div>
<h2>Domande frequenti</h2>{fq}
<h2>Strumenti e approfondimenti</h2><div class="grid g2" style="margin-bottom:20px">{rel_t}</div><ul>{rel_g}</ul>
<div class="note" style="margin-top:28px">{ic("info")}<div>Le valutazioni sono tecniche e non costituiscono parere legale. Non garantiamo l'esito della richiesta di indennizzo: la decisione spetta alla compagnia e, in caso di disaccordo, alle procedure previste.</div></div>
</article><aside class="aside"><div class="card"><h3>Richiedi assistenza</h3><p class="muted small">Descrivi il caso: è gratuito e senza impegno. Ti proponiamo il servizio adatto.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a><a class="btn btn-g" style="width:100%;margin-top:6px" href="/contatti/">Fai una domanda</a></div>
<div class="card"><h3 style="font-size:17px">Servizi correlati</h3><ul class="small" style="padding-left:18px;margin:0">{rel_s}</ul></div></aside></div></section>{band()}'''
        svc = {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "description": s["desc"], "provider": {"@id": U + "/#studio"},
               "areaServed": "IT", "url": f'{U}/servizi/{s["slug"]}/'}
        prices = [PV[i] for i in s["prezzi"] if PV[i]["prezzo"]]
        if prices:
            svc["offers"] = [{"@type": "Offer", "name": p["nome"], "price": p["prezzo"], "priceCurrency": "EUR"} for p in prices]
        page(f'/servizi/{s["slug"]}/', s["title"], s["desc"], body, cur="/servizi/", ld=[bld, svc, fqld])
    # hub
    head, bld = ph([("/", "Home"), ("", "Servizi")], "I nostri servizi", "Perizie, stime e analisi documentali per incidenti stradali, danni alla casa, attività commerciali e infortuni.", "Servizi")
    blocks = ""
    for a in AMBITI:
        cards = "".join(svc_card(SV[x]) for x in a["servizi"] if SV[x]["ambito"] == a["slug"])
        if cards:
            blocks += f'<h2 style="margin-top:8px">{e(a["nome"])}</h2><p class="muted">{e(a["intro"])}</p><div class="grid g3" style="margin-bottom:48px">{cards}</div>'
    body = f'{head}<section class="sec" style="padding-top:48px"><div class="wrap">{blocks}<p><a class="btn btn-s" href="/prezzi/">Vedi prezzi e cosa comprendono</a></p></div></section>{band()}'
    page("/servizi/", "Servizi: perizie, stime e analisi polizze | StimaVeloce", "Tutti i servizi di StimaVeloce: perizie danni auto e moto, danni alla casa, incendio, furto, analisi delle polizze, contestazione delle perizie.", body, cur="/servizi/", ld=[bld])
    # ambiti
    for a in AMBITI:
        head, bld = ph([("/", "Home"), ("/servizi/", "Servizi"), ("", a["nome"])], a["nome"], a["intro"], "In cosa possiamo aiutarti")
        cards = "".join(svc_card(SV[x]) for x in a["servizi"])
        tl = []
        gl = []
        for x in a["servizi"]:
            for t in SV[x]["tools"]:
                if t not in tl: tl.append(t)
            for g in SV[x]["guides"]:
                if g not in gl: gl.append(g)
        body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap"><div class="card" style="margin-bottom:36px"><h3>Situazioni che seguiamo</h3><ul class="ticks" style="columns:2;column-gap:32px">{"".join(f"<li>{e(v)}</li>" for v in a["voci"])}</ul></div>
<h2>Servizi dedicati</h2><div class="grid g3" style="margin-bottom:48px">{cards}</div>
<h2>Strumenti utili</h2><div class="grid g3" style="margin-bottom:48px">{"".join(tool_card(TV[t]) for t in tl[:6])}</div>
<h2>Guide</h2><div class="grid g3">{"".join(guide_card(GV[g]) for g in gl[:6])}</div></div></section>{band()}'''
        page(f'/aiuto/{a["slug"]}/', f'{a["nome"]}: servizi, strumenti e guide | StimaVeloce', a["intro"] + " Servizi dedicati, calcolatori gratuiti e guide.", body, cur="/servizi/", ld=[bld])


# ------------------------------------------------------------------ STRUMENTI
def build_strumenti():
    for t in STRUMENTI:
        head, bld = ph([("/", "Home"), ("/strumenti/", "Strumenti gratuiti"), ("", t["nome"])], t["h1"], t["intro"], "Strumento gratuito")
        body = f'''{head}<section class="sec" style="padding-top:44px"><div class="wrap">
<div class="calc" data-calc="{t["slug"]}"><form class="card form" novalidate onsubmit="return false">{t["form"]}</form>
<div class="res" aria-live="polite"><div class="muted small">{e(t["res_label"])}</div><div class="big" data-out="big">—</div><div class="small muted" data-out="sub"></div><table data-out="tab"></table>
<div class="no-print" style="display:flex;gap:8px;margin-top:18px;flex-wrap:wrap"><button class="btn btn-s btn-sm" type="button" onclick="window.print()">{ic("printer")}Stampa</button><a class="btn btn-p btn-sm" href="{APP}#prefattibilita">Fallo verificare</a></div></div></div>
<div class="layout" style="margin-top:56px"><div class="prose"><h2>Formula e criteri utilizzati</h2><div class="formula">{t["formula"]}</div>
<h2>Come leggere il risultato</h2>{t["spiegazione"]}
<h2>Avvertenze</h2><div class="note">{ic("triangle-alert")}<div>{t["avvertenze"]}</div></div>
<p class="small muted" style="margin-top:16px">Ultimo aggiornamento dei criteri: {e(t.get("aggiornato", SITE["updated"]))}.</p>
{("<h2>Fonti</h2><ul class=sources>" + "".join(f'<li><a href="{f[1]}" rel="noopener" target="_blank">{e(f[0])}</a></li>' for f in t["fonti"]) + "</ul>") if t.get("fonti") else ""}
</div><aside class="aside"><div class="card"><h3>Vuoi una verifica professionale?</h3><p class="muted small">Il calcolatore dà un ordine di grandezza. Una stima tecnica considera la tua polizza e i tuoi documenti.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div>
<div class="card"><h3 style="font-size:17px">Altri strumenti</h3><ul class="small" style="padding-left:18px;margin:0">{"".join(f'<li><a href="/strumenti/{x["slug"]}/">{e(x["nome"])}</a></li>' for x in STRUMENTI if x["slug"] != t["slug"])}</ul></div></aside></div></div></section>'''
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["nome"], "applicationCategory": "FinanceApplication", "operatingSystem": "Web",
               "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}, "url": f'{U}/strumenti/{t["slug"]}/'}
        page(f'/strumenti/{t["slug"]}/', t["title"], t["desc"], body, cur="/strumenti/", ld=[bld, app], scripts=f'<script src="/assets/calc.js?v={CSSV}" defer></script>')
    head, bld = ph([("/", "Home"), ("", "Strumenti gratuiti")], "Strumenti gratuiti", "Calcolatori tecnici per farti un'idea del danno e di come la polizza lo tratta. Ogni strumento mostra formula, criteri e avvertenze.", "Strumenti")
    body = f'{head}<section class="sec" style="padding-top:48px"><div class="wrap"><div class="grid g2">{"".join(tool_card(t) for t in STRUMENTI)}</div></div></section>{band()}'
    page("/strumenti/", "Calcolatori gratuiti: franchigia, scoperto, vetustà, danni | StimaVeloce", "Calcolatori gratuiti con formule verificabili: danni al fabbricato, franchigia e scoperto, sottoassicurazione, vetustà, danno biologico orientativo, preventivo lavori.", body, cur="/strumenti/", ld=[bld])


# ------------------------------------------------------------------ GUIDE
def build_guide():
    for g in GUIDE:
        head, bld = ph([("/", "Home"), ("/guide/", "Guide"), ("", g["h1"])], g["h1"], g["intro"], g["cat"])
        meta = f'<div class="meta"><span>{ic("user")}{e(AUTORE)}</span><span>{ic("calendar-clock")}Pubblicata il {e(SITE["updated"])}</span><span>{ic("clock")}Aggiornata il {e(SITE["updated"])}</span></div>'
        head = head.replace("</div></section>", meta + "</div></section>", 1)
        secs = "".join(f'<h2>{e(t)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) for t, ps in g["sezioni"])
        fonti = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{e(n)}</a></li>' for n, u in g["fonti"])
        body = f'''{head}<section class="sec" style="padding-top:44px"><div class="wrap layout"><article class="prose">{secs}
<h2>Fonti consultate</h2><ul class="sources">{fonti}</ul>
<div class="note" style="margin-top:24px">{ic("info")}<div>Questa guida ha carattere informativo generale. Ogni polizza e ogni sinistro hanno caratteristiche proprie: per il tuo caso serve una valutazione specifica.</div></div>
</article><aside class="aside"><div class="card"><h3>Hai un caso simile?</h3><p class="muted small">Raccontaci cosa è successo: ti diciamo come possiamo aiutarti.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div>
<div class="card"><h3 style="font-size:17px">Servizi collegati</h3><ul class="small" style="padding-left:18px;margin:0">{"".join(f'<li><a href="/servizi/{x}/">{e(SV[x]["h1"])}</a></li>' for x in g["servizi"])}</ul><h3 style="font-size:17px;margin-top:18px">Strumenti</h3><ul class="small" style="padding-left:18px;margin:0">{"".join(f'<li><a href="/strumenti/{x}/">{e(TV[x]["nome"])}</a></li>' for x in g["tools"])}</ul></div></aside></div></section>'''
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": "it-IT",
               "author": {"@type": "Organization", "name": AUTORE}, "publisher": {"@id": U + "/#studio"},
               "datePublished": SITE["updated_iso"], "dateModified": SITE["updated_iso"], "mainEntityOfPage": f'{U}/guide/{g["slug"]}/', "image": U + "/og-image.jpg"}
        page(f'/guide/{g["slug"]}/', g["title"], g["desc"], body, cur="/guide/", index=g["verificato"], ld=[bld, art], og_type="article")
    head, bld = ph([("/", "Home"), ("", "Guide")], "Il mondo dei sinistri – Guide e approfondimenti", "Guide pratiche e verificate su polizze, perizie e risarcimenti, con le fonti normative consultate.", "Guide e risorse")
    cats = sorted({g["cat"] for g in GUIDE}, key=lambda c: ["RCA", "Rami elementari", "Polizze casa", "Danni ai fabbricati", "Perizie"].index(c) if c in ["RCA", "Rami elementari", "Polizze casa", "Danni ai fabbricati", "Perizie"] else 99)
    blocks = "".join(f'<h2>{e(c)}</h2><div class="grid g3" style="margin-bottom:44px">{"".join(guide_card(g) for g in GUIDE if g["cat"] == c)}</div>' for c in cats)
    body = f'{head}<section class="sec" style="padding-top:48px"><div class="wrap">{blocks}</div></section>{band()}'
    page("/guide/", "Guide sui sinistri: polizze, perizie, risarcimenti | StimaVeloce", "Il mondo dei sinistri: guide su risarcimento danni auto, franchigie, scoperti, regola proporzionale, polizze casa e perizie di parte.", body, cur="/guide/", ld=[bld])


# ------------------------------------------------------------------ PAGINE ISTITUZIONALI
def build_istituzionali():
    # come funziona
    head, bld = ph([("/", "Home"), ("", "Come funziona")], "Come funziona", "Dalla prima richiesta alla relazione finale: tutto online, con un tecnico che segue il tuo caso.", "Come funziona")
    stati = ["Richiesta ricevuta", "In attesa di documentazione", "Documentazione completa", "In lavorazione", "In verifica professionale", "Relazione pronta", "Consegnata", "Chiusa"]
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><div class="prose">
<h2>1. Raccontaci cosa è successo</h2><p>Il percorso guidato ti chiede che tipo di danno hai subito e poi solo le domande pertinenti al tuo caso. Si compila a tocchi, anche dal telefono, in pochi minuti. È gratuito e senza impegno.</p>
<h2>2. Carica fotografie e documenti</h2><p>Foto del danno, polizza, preventivi, lettere della compagnia. Se manca qualcosa te lo segnaliamo noi.</p>
<h2>3. Ricevi una valutazione professionale</h2><p>Un tecnico dello Studio esamina la richiesta e ti indica il servizio più adatto con il suo prezzo. Nessun pagamento prima di sapere cosa riceverai.</p>
<h2>4. Segui la pratica dalla tua area personale</h2><p>Ogni pratica ha un codice univoco. Nell'area personale vedi lo stato, carichi altri documenti, scarichi la relazione e ricevi le comunicazioni.</p>
<div class="box"><h3 style="margin-top:0">Gli stati della pratica</h3><ol class="olist">{"".join(f"<li>{e(s)}</li>" for s in stati)}</ol></div>
<h2>Cosa non facciamo</h2><p>Non vendiamo polizze, non garantiamo risarcimenti e non diamo pareri legali. Ci occupiamo della parte tecnica: documentare e quantificare il danno e leggere la polizza.</p>
</div><aside class="aside"><div class="card"><h3>Pronto a iniziare?</h3><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div></aside></div></section>'''
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "Come richiedere una valutazione del danno su StimaVeloce",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(["Racconta cosa è successo", "Carica fotografie e documenti", "Ricevi una valutazione professionale", "Segui la pratica dall'area personale"])]}
    page("/come-funziona/", "Come funziona: valutazione del danno online in 4 passaggi | StimaVeloce", "Racconti il sinistro, carichi foto e documenti, ricevi una valutazione professionale e segui la pratica online. Ecco come funziona StimaVeloce.", body, cur="/come-funziona/", ld=[bld, howto])
    # chi siamo
    head, bld = ph([("/", "Home"), ("", "Chi siamo")], "Chi siamo", f"StimaVeloce è il servizio digitale dello {SITE['studio']}, a {SITE['city']}.", "Lo Studio")
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><div class="prose">
<h2>Lo Studio</h2><p>Lo {e(SITE["studio"])} si occupa di consulenza tecnica sui sinistri: stime dei danni, perizie di parte, analisi di polizze e preventivi. StimaVeloce porta questo lavoro online, per renderlo più rapido, più trasparente e accessibile a chiunque.</p>
<h2>Il nostro metodo</h2><ul class="ticks"><li>Valutazioni tecniche documentate, in cui ogni numero è spiegato</li><li>Riferimento puntuale a clausole, pagine e voci di danno</li><li>Prezzi pubblicati e preventivi scritti prima di ogni attività aggiuntiva</li><li>Nessuna promessa di risultato: la decisione sull'indennizzo spetta alla compagnia</li></ul>
<h2>Tecnologia al servizio del professionista</h2><p>Usiamo strumenti digitali per organizzare documenti e foto e per velocizzare il lavoro ripetitivo. Le valutazioni restano sempre di un tecnico, che le verifica e le firma.</p>
<h2>Indipendenza</h2><p>Non vendiamo polizze e non lavoriamo per conto delle compagnie nei casi che seguiamo per i nostri clienti.</p>
</div><aside class="aside"><div class="card"><h3>Contatti</h3><p class="small"><a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a><br>{e(SITE["city"])}</p><a class="btn btn-s" style="width:100%" href="/contatti/">Scrivici</a></div></aside></div></section>{band()}'''
    page("/chi-siamo/", f"Chi siamo – {SITE['studio']} | StimaVeloce", f"StimaVeloce è il servizio online dello {SITE['studio']}: consulenza tecnica sui sinistri, stime e perizie di parte.", body, cur="/chi-siamo/", ld=[bld, ORG])
    # prezzi
    head, bld = ph([("/", "Home"), ("", "Prezzi")], "Servizi e prezzi", "Prezzi chiari prima di iniziare. Per le attività su preventivo ricevi l'importo per iscritto prima di qualsiasi lavoro.", "Prezzi")
    cards = ""
    for p in PREZZI:
        cards += f'''<div class="card pcard{" feat-p" if p["id"] == "perizia" else ""}"><h3>{e(p["nome"])}</h3><p class="muted small" style="margin:0">{e(p["breve"])}</p><div class="p">{prezzo_label(p)}</div>
<h4>Comprende</h4><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in p["comprende"])}</ul><h4>Non comprende</h4><ul class="ticks x">{"".join(f"<li>{e(x)}</li>" for x in p["esclude"])}</ul>
<h4>Dettagli</h4><p class="dl"><b>Documenti:</b> {e(", ".join(p["documenti"]))}</p><p class="dl"><b>Tempi indicativi:</b> {e(p["tempi"])}</p><p class="dl"><b>Consegna:</b> {e(p["formato"])}</p><p class="dl" style="margin-bottom:20px"><b>Costi aggiuntivi:</b> {e(p["extra"])}</p>
<a class="btn {"btn-p" if p["prezzo"] else "btn-s"}" href="{APP}#prefattibilita">{"Inizia" if p["prezzo"] else "Chiedi un preventivo"}</a></div>'''
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap"><div class="prices">{cards}</div>
<div class="card" style="margin-top:32px"><h3>Pagamento e cancellazione</h3><p class="muted" style="margin:0">{e(CONDIZIONI_PAGAMENTO)}</p></div>
<p class="small muted" style="margin-top:16px">Prima di pagare puoi sempre descrivere il caso gratuitamente: ti indichiamo il servizio adatto. <a href="/condizioni/">Condizioni generali</a>.</p></div></section>{band()}'''
    offers = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Servizi StimaVeloce", "itemListElement": [
        {"@type": "Offer", "name": p["nome"], "price": p["prezzo"], "priceCurrency": "EUR"} for p in PREZZI if p["prezzo"]]}
    page("/prezzi/", "Prezzi: stima tecnica 45 €, perizia 69 € | StimaVeloce", "Prezzi dei servizi StimaVeloce: stima tecnica online 45 €, perizia tecnica 69 €, analisi documentale e consulenze su preventivo. Cosa comprendono e condizioni.", body, ld=[bld, offers])
    # faq
    head, bld = ph([("/", "Home"), ("", "Domande frequenti")], "Domande frequenti", "Risposte brevi e chiare su servizi, costi, documenti e tempi.", "FAQ")
    blocks = ""
    allq = []
    for cat, items in FAQ_ALL:
        h, _ = faq_html(items)
        allq += items
        blocks += f'<h2 style="margin-top:36px">{e(cat)}</h2>{h}'
    _, fqld = faq_html(allq)
    body = f'{head}<section class="sec" style="padding-top:24px"><div class="wrap narrow">{blocks}</div></section>{band()}'
    page("/faq/", "Domande frequenti su stime, perizie e sinistri | StimaVeloce", "Quanto costa una stima, quali documenti servono, quanto tempo ci vuole, cosa succede dopo: le risposte alle domande più frequenti.", body, ld=[bld, fqld])
    # contatti
    head, bld = ph([("/", "Home"), ("", "Contatti")], "Contatti", "Per aprire una pratica usa il percorso guidato. Per domande generali scrivici qui.", "Contatti")
    tel = f'<p>{ic("phone")} <a href="tel:{SITE["telefono"]}">{e(SITE["telefono"])}</a></p>' if SITE["telefono"] else ""
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><form class="card form" name="contatto" method="POST" action="/contatti/grazie/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="contatto"><p class="sr"><label>Non compilare <input name="bot-field"></label></p>
<div class="row2"><div class="fld"><label for="c-nome">Nome e cognome</label><input class="in" id="c-nome" name="nome" required autocomplete="name"></div><div class="fld"><label for="c-email">Email</label><input class="in" id="c-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row2"><div class="fld"><label for="c-tel">Telefono <span class="muted">(facoltativo)</span></label><input class="in" id="c-tel" name="telefono" type="tel" autocomplete="tel"></div><div class="fld"><label for="c-mot">Argomento</label><select class="in" id="c-mot" name="motivo"><option>Informazioni su un servizio</option><option>Pratica già aperta</option><option>Preventivo per consulenza</option><option>Collaborazioni</option><option>Altro</option></select></div></div>
<div class="fld"><label for="c-msg">Messaggio</label><textarea class="in" id="c-msg" name="messaggio" required></textarea></div>
<label class="chk"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l'<a href="/privacy/">informativa privacy</a> e acconsento al trattamento dei dati per ricevere risposta.</span></label>
<button class="btn btn-p btn-lg" type="submit">Invia messaggio</button></form>
<aside class="aside"><div class="card"><h3>Vuoi aprire una pratica?</h3><p class="muted small">Il percorso guidato raccoglie già tutte le informazioni utili.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div>
<div class="card"><h3 style="font-size:17px">Recapiti</h3><p>{ic("mail")} <a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a></p>{tel}<p style="margin:0">{ic("map-pin")} {e(SITE["indirizzo"] or SITE["city"])}</p></div></aside></div></section>'''
    page("/contatti/", "Contatti | StimaVeloce – Studio Della Vecchia", "Scrivi allo Studio per informazioni sui servizi, preventivi e pratiche già aperte.", body, ld=[bld, ORG])
    head, bld = ph([("/", "Home"), ("/contatti/", "Contatti"), ("", "Messaggio inviato")], "Messaggio inviato", "Grazie, ti risponderemo il prima possibile all'indirizzo email indicato.")
    page("/contatti/grazie/", "Messaggio inviato | StimaVeloce", "Messaggio inviato.", head + f'<section class="sec"><div class="wrap"><a class="btn btn-p" href="/">Torna alla home</a></div></section>', index=False)
    # legali
    for slug, (h1, sezioni) in LEGALI.items():
        head, bld = ph([("/", "Home"), ("", h1)], h1, f"Ultimo aggiornamento: {SITE['updated']}")
        secs = "".join(f"<h2>{e(t)}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for t, ps in sezioni)
        page(f"/{slug}/", f"{h1} | StimaVeloce", f"{h1} del servizio StimaVeloce.", f'{head}<section class="sec" style="padding-top:44px"><div class="wrap narrow prose">{secs}</div></section>', ld=[bld])
    # 404
    body = f'<section class="ph"><div class="wrap"><div class="eyebrow">Errore 404</div><h1>Pagina non trovata</h1><p class="lead">L\'indirizzo potrebbe essere cambiato. Prova da qui:</p><div class="cta-row" style="margin-top:20px"><a class="btn btn-p" href="/">Home</a><a class="btn btn-s" href="/servizi/">Servizi</a><a class="btn btn-s" href="/guide/">Guide</a><a class="btn btn-s" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div></div></section>'
    page("/404.html", "Pagina non trovata | StimaVeloce", "Pagina non trovata.", body, index=False)
    PAGES.pop()


# ------------------------------------------------------------------ CASA
CASA_FOTO = [("infiltrazioni-soffitto", "droplet", "Infiltrazioni dal soffitto", "La macchia visibile è spesso solo la parte finale di un percorso dell'acqua più lungo."),
             ("umidita-pareti", "waves", "Umidità e danni alle pareti", "Intonaci che si gonfiano, muffe, pitture che si staccano: danni che cambiano nel tempo."),
             ("rottura-tubazioni", "wrench", "Rotture di tubazioni", "La ricerca del guasto e la riparazione sono voci diverse dal danno all'ambiente."),
             ("pavimenti", "layers", "Danni ai pavimenti", "Sotto un pavimento bagnato possono esserci massetto e isolanti da rifare."),
             ("incendio", "flame", "Danni da incendio", "Fumo e calore arrivano anche dove le fiamme non sono passate."),
             ("eventi-atmosferici", "cloud-lightning", "Eventi atmosferici", "Coperture, infissi e facciate: la garanzia ha spesso condizioni specifiche."),
             ("impianti", "plug", "Danni agli impianti", "Impianti elettrici e termici vanno verificati, non solo guardati."),
             ("strutture", "construction", "Elementi strutturali", "Lesioni e deformazioni richiedono sempre un approfondimento tecnico.")]
CASA_STEPS = [("Prima segnalazione", "Un proprietario segnala una macchia d'acqua sul soffitto del soggiorno e carica due fotografie dal telefono."),
              ("Prima quantificazione", "La prima stima riguarda il danno visibile: ripristino dell'intonaco e tinteggiatura di una porzione di soffitto."),
              ("Raccolta di ulteriori fotografie", "Il tecnico chiede foto della stanza intera, del bagno al piano di sopra e delle pareti vicine, con un riferimento metrico."),
              ("Approfondimento tecnico", "Le nuove foto mostrano umidità anche sulla parete adiacente: il danno è più esteso di quanto apparisse all'inizio."),
              ("Individuazione delle lavorazioni", "Si elencano le lavorazioni necessarie: rimozioni, rifacimenti, tinteggiature, ricerca e riparazione del guasto."),
              ("Verifica della documentazione", "Si leggono le condizioni di polizza: garanzia acqua condotta, franchigia, limiti per la ricerca del guasto."),
              ("Relazione tecnica finale", "La relazione descrive il danno, le lavorazioni con quantità e prezzi e le clausole applicabili. Ogni numero è spiegato.")]


def build_casa():
    bc, bld = breadcrumb([("/", "Home"), ("/servizi/", "Servizi"), ("", "Casa e Fabbricati")])
    gal = "".join(f'<figure class="rv"><div class="ph-slot" data-foto="{k}">{ic(i)}<span>{e(t)}</span></div><figcaption><b>{e(t)}.</b> {e(d)}</figcaption></figure>' for k, i, t, d in CASA_FOTO)
    nav = "".join(f'<li data-step="{n}">{e(t)}</li>' for n, (t, d) in enumerate(CASA_STEPS))
    steps = "".join(f'<div class="story-step" data-step="{n}"><div class="eyebrow">Passo {n + 1} di {len(CASA_STEPS)}</div><h3 style="font-size:26px">{e(t)}</h3><p class="lead">{e(d)}</p></div>' for n, (t, d) in enumerate(CASA_STEPS))
    serv = "".join(svc_card(SV[x]) for x in ["danni-acqua-condotta", "danni-infiltrazioni", "danni-incendio", "danni-eventi-atmosferici", "danni-da-furto", "danni-fabbricati"])
    ghost = 'style="background:transparent;color:#fff;border-color:rgba(255,255,255,.35)"'
    body = (
        f'<section class="casa-hero"><div class="wrap">{bc}<div class="eyebrow" style="margin-top:18px;color:var(--gold)">Casa e Fabbricati</div>'
        '<h1>Un danno alla casa non è soltanto una macchia sul muro.</h1>'
        '<p class="lead">Quello che si vede è spesso solo una parte del danno. Una valutazione tecnica corretta ricostruisce cosa è successo, quali lavorazioni servono e cosa prevede la polizza.</p>'
        f'<div class="cta-row" style="margin-top:28px"><a class="btn btn-p btn-lg" href="{APP}#prefattibilita">Analizza il danno alla tua casa{ic("arrow-right")}</a><a class="btn btn-s btn-lg" {ghost} href="#percorso">Guarda un caso esemplificativo</a></div></div></section>'
        f'<section class="sec"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Cosa può nascondere un danno</div><h2>Otto danni che vanno guardati da vicino</h2><p class="lead">Scorri le schede: ognuna spiega perché la prima impressione non basta.</p></div><div class="gal">{gal}</div></div></section>'
        '<section class="sec sec-s" id="percorso"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Caso esemplificativo, simulato</div><h2>Dalla prima segnalazione alla relazione finale</h2>'
        '<p class="lead">Un esempio costruito a scopo illustrativo, non un caso reale: mostra perché una prima quantificazione non sempre esaurisce tutti gli aspetti tecnici del danno.</p></div>'
        f'<div class="story"><nav class="story-nav" aria-label="Passi del caso"><ol>{nav}</ol></nav><div>{steps}</div></div></div></section>'
        '<section class="sec"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Prima e dopo</div><h2>Lo stesso ambiente, prima e dopo il ripristino</h2>'
        '<p class="lead">Il confronto aiuta a capire quali lavorazioni sono state necessarie. Pubblicheremo solo confronti reali autorizzati dai proprietari, con dati anonimizzati.</p></div>'
        f'<div class="ba"><figure class="rv" style="margin:0"><div class="ph-slot" data-foto="prima">{ic("camera")}<span>Prima del ripristino</span></div></figure>'
        f'<figure class="rv rv-d1" style="margin:0"><div class="ph-slot" data-foto="dopo">{ic("circle-check")}<span>Dopo il ripristino</span></div></figure></div></div></section>'
        f'<section class="sec sec-w"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Servizi per la casa</div><h2>Come possiamo aiutarti</h2></div><div class="grid g3">{serv}</div>'
        f'<p style="margin-top:28px"><a class="more" href="/strumenti/danni-fabbricato/">Prova il calcolatore danni al fabbricato{ic("arrow-right")}</a></p></div></section>'
        + band("Hai un danno in casa?", "Racconta cosa è successo e carica le foto: ti diciamo quale valutazione serve, prima di qualsiasi pagamento.")
    )
    page("/casa/", "Danni alla casa: infiltrazioni, acqua, incendio | StimaVeloce",
         "Un danno alla casa non è soltanto una macchia sul muro: infiltrazioni, tubazioni, incendio, eventi atmosferici. Come si valuta correttamente, passo per passo.",
         body, cur="/servizi/", ld=[bld])


def build_search():
    idx = [{"u": p, "t": TITLES[p][0], "d": TITLES[p][1]} for p, ok in PAGES if ok]
    idx.append({"u": APP + "#prefattibilita", "t": "Analizza il tuo sinistro", "d": "Percorso guidato gratuito"})
    idx.append({"u": APP + "#area", "t": "Area Clienti", "d": "Accedi alle tue pratiche"})
    json.dump(idx, open(os.path.join(ROOT, "assets/search.json"), "w"), ensure_ascii=False, separators=(",", ":"))


def build_seo():
    urls = [p for p, idx in PAGES if idx]
    def pri(p):
        return "1.0" if p == "/" else "0.8" if p.startswith("/servizi/") or p in ("/prezzi/", "/strumenti/") else "0.6"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'<url><loc>{U}{p}</loc><lastmod>{SITE["updated_iso"]}</lastmod><priority>{pri(p)}</priority></url>\n' for p in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\nDisallow: /contatti/grazie/\n\nSitemap: {U}/sitemap.xml\n")
    print(f"pagine: {len(PAGES)} · in sitemap: {len(urls)}")


if __name__ == "__main__":
    build_home(); build_servizi(); build_casa(); build_strumenti(); build_guide(); build_istituzionali(); build_seo(); build_search()
