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


LOGO_SVG = ('<svg viewBox="0 0 34 38" aria-hidden="true"><path d="M17 1.5 31.5 6.5V18c0 9.5-6.5 15.5-14.5 18.5C9 33.5 2.5 27.5 2.5 18V6.5Z" fill="#1F5EFF"/>'
            '<path d="M10.5 19.2l4.6 4.6 8.4-10" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="27.5" cy="8.5" r="2.6" fill="#FF7A1A"/></svg>')


def logo(href="/"):
    return f'<a class="logo" href="{href}" aria-label="StimaVeloce, pagina iniziale">{LOGO_SVG}<b>StimaVeloce<i>.</i></b></a>'


MENU = [("/aiuto/incidenti-stradali/", "car", "Auto e Moto", "Incidenti, carrozzeria, moto e veicoli commerciali"),
        ("/casa/", "house", "Casa e Fabbricati", "Acqua, infiltrazioni, incendio, eventi atmosferici"),
        ("/aiuto/attivita-commerciali/", "store", "Aziende", "Locali, impianti, attrezzature, fermo attività"),
        ("/servizi/sinistri-nautici/", "sailboat", "Nautica", "Imbarcazioni, ormeggio, mareggiate"),
        ("/aiuto/infortuni-persona/", "heart-pulse", "Infortuni e Lesioni", "Documentazione e calcoli orientativi"),
        ("/aiuto/analisi-polizze/", "file-search", "Analisi Polizze", "Garanzie, esclusioni, franchigie, limiti"),
        ("/aiuto/perizie-stime/", "clipboard-check", "Perizie e Consulenze", "Stime, perizie di parte, contestazioni")]
STIME = [("/stima/", "sparkles", "Stima senza firma", "stima"), ("/stima/?tipo=auto", "car", "Perizia auto/moto", "perizia"),
         ("/contatti/?motivo=consulenza", "house", "Danni alla casa", None), ("/contatti/?motivo=consulenza", "stethoscope", "Lesioni alla persona", None)]
GRATIS = [("/offerta/", "scale", "Controlla l'offerta della compagnia"), (APP + "#checklist", "list-checks", "Check-list sinistro (PDF)"),
          (APP + "#incidente", "clipboard-list", "Modulo CAI guidato"), ("/simulatore/", "car", "Simulatore di dinamica"), ("/sei-in-tempo/", "hourglass", "Sei ancora in tempo?")]
NAV2 = [("/perche-noi/", "Perché noi"), ("/novita/", "Novità"), ("/guide/", "Guide"), ("/strumenti/", "Strumenti"), ("/chi-siamo/", "Chi siamo"), ("/contatti/", "Contatti")]


def _price(i):
    return prezzo_label(PV[i])


def header(cur):
    col1 = "<h5>Stime e perizie</h5>" + "".join(f'<a href="{h}">{ic(i)}<div><b>{t}<span class="price">{_price(k) if k else "Consulenza gratuita"}</span></b></div></a>' for h, i, t, k in STIME)
    col1 += "<h5>Gratis</h5>" + "".join(f'<a href="{h}">{ic(i)}<div><b>{t}</b></div></a>' for h, i, t in GRATIS)
    col2 = ('<h5>In primo piano</h5>'
            f'<a href="/polizza-catastrofale/">{ic("shield-check")}<div><b>Polizza catastrofale imprese</b><span>Controlla se ti copre davvero</span></div></a>'
            '<h5>Gestione sinistro</h5>'
            f'<a href="/gestione-sinistro/">{ic("handshake")}<div><b>Affida la pratica a noi</b><span>Seguiamo il sinistro per te</span></div></a>'
            f'<a href="/gestione-sinistro/#accessori">{ic("package")}<div><b>Accessori per la pratica<span class="tbd">PREZZI DA DEFINIRE</span></b></div></a>'
            '<h5>Per avvocati e professionisti</h5>'
            f'<a href="/professionisti/">{ic("gavel")}<div><b>Supporto peritale<span class="tbd">PREZZI DA DEFINIRE</span></b></div></a>'
            f'<a href="/partner/">{ic("handshake")}<div><b>Diventa partner</b><span>Carrozzerie, amministratori, soccorso</span></div></a>'
            '<h5>Novità e curiosità</h5>'
            f'<a href="/novita/">{ic("sparkles")}<div><b>Leggi aggiornate e «Lo sapevi?»</b></div></a>'
            '<h5>Accessi</h5>'
            f'<a href="{APP}#area">{ic("user")}<div><b>Area clienti</b></div></a><a href="/periti/">{ic("hard-hat")}<div><b>Area periti</b><span>Accesso e registrazione</span></div></a>'
            f'<a href="{APP}#area">{ic("search")}<div><b>Segui la tua pratica</b></div></a><a href="/contatti/">{ic("mail")}<div><b>Contatti</b></div></a>')
    col3 = "<h5>Per tipo di danno</h5>" + "".join(f'<a href="{h}">{ic(i)}<div><b>{t}</b><span>{d}</span></div></a>' for h, i, t, d in MENU)
    col3 += f'<a href="/servizi/">{ic("arrow-right")}<div><b>Tutti i servizi e i prezzi</b></div></a>'
    mega = f'<div class="col">{col1}</div><div class="col">{col2}</div><div class="col">{col3}</div>'
    links = "".join(f'<a href="{h}"{" aria-current=page" if cur == h else ""}>{t}</a>' for h, t in NAV2)
    mobile = mega.replace('class="col"', 'class="col" style="display:block"')
    srch = f'<div class="srch">{ic("search")}<input class="srch-in" type="search" placeholder="Cerca: infiltrazione, franchigia, perizia auto…" aria-label="Cerca nel sito" data-srch><ul class="srch-res" data-srch-res></ul></div>'
    tab = [("/", "house", "Home"), ("/stima/", "sparkles", "Stima"), ("/simulatore/", "car", "Simulatore"), (APP + "#area", "search", "Pratica")]
    tabbar = "".join(f'<a href="{h}"{" aria-current=page" if cur == h else ""}{" class=cta" if h == "/stima/" else ""}>{ic(i)}{t}</a>' for h, i, t in tab)
    tabbar += f'<a href="#menu" data-open-menu>{ic("menu")}Menu</a>'
    return f'''<a class="skip" href="#main">Vai al contenuto</a>
<header class="hd"><div class="wrap">{logo()}
<nav class="nav" aria-label="Principale"><details class="dd"><summary{" aria-current=page" if cur == "/servizi/" else ""}>Servizi{ic("chevron-down")}</summary><div class="mega">{mega}</div></details>{links}</nav>
<div class="hd-r"><button class="sbtn hide-m" type="button" data-open-srch aria-label="Cerca nel sito">{ic("search")}</button><a class="btn btn-g btn-sm hide-m" href="{APP}#area">{ic("user")}Area clienti</a><a class="btn btn-p btn-sm" href="/stima/">Quanto vale il tuo danno?</a>
<details class="mnav" id="menu"><summary aria-label="Apri il menu">{ic("menu")}</summary><div class="panel">{srch}<div class="mega" style="position:static;width:auto;box-shadow:none;display:block;padding:0">{mobile}</div><a href="/novita/">{ic("sparkles")}Novità</a><a href="/guide/">{ic("book-open")}Guide e risorse</a><a href="/strumenti/">{ic("calculator")}Strumenti gratuiti</a><a href="/chi-siamo/">{ic("users")}Chi siamo</a></div></details>
</div></div></header>
<nav class="tabbar" aria-label="Navigazione rapida">{tabbar}</nav>
<dialog class="sdlg" data-srch-dlg><form method="dialog" style="display:flex;justify-content:flex-end;margin:0 0 8px"><button class="sbtn" aria-label="Chiudi">{ic("x")}</button></form>{srch}</dialog>'''


WA_TOPICS = [("stima", "Vorrei una stima del danno"), ("perizia", "Vorrei una perizia"), ("pratica", "Stato della mia pratica"),
             ("offerta", "Ho ricevuto un'offerta dalla compagnia"), ("avvocati", "Sono un avvocato o un professionista"), ("altro", "Altro")]


def wa_widget():
    num = re.sub(r"\D", "", SITE["whatsapp"])
    if num:
        links = "".join(f'<a href="https://wa.me/{num}?text={e(t.replace(" ", "%20"))}" target="_blank" rel="noopener">{e(t)}{ic("chevron-right")}</a>' for k, t in WA_TOPICS)
        note = ""
    else:
        links = "".join(f'<a href="/contatti/?motivo={k}">{e(t)}{ic("chevron-right")}</a>' for k, t in WA_TOPICS)
        note = '<p class="small muted" style="margin:0">Il numero WhatsApp di StimaVeloce è in attivazione: per ora scegli l\'argomento e ti rispondiamo dal modulo contatti.</p>'
    wa = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>'
    return (f'<button class="wa-fab" type="button" data-open-wa aria-label="Scrivici su WhatsApp">{wa}</button>'
            f'<dialog class="wa" data-wa><form method="dialog" style="float:right;margin:0"><button class="sbtn" aria-label="Chiudi">{ic("x")}</button></form>'
            f'<h3>Come possiamo aiutarti?</h3><p class="muted small" style="margin:0">Scegli un argomento: il messaggio è già pronto.</p><div class="topics">{links}</div>{note}</dialog>')


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
<div>{logo()}<p style="margin-top:18px;max-width:340px">Stime e perizie sui sinistri, online in tutta Italia. Consulenza tecnica: non vendiamo polizze.</p><h4 style="margin-top:26px">Contatti</h4><ul>{"".join(contatti)}</ul></div>
<div><h4>Servizi</h4><ul>{serv}<li><a href="/servizi/">Tutti i servizi</a></li><li><a href="/prezzi/">Prezzi</a></li></ul></div>
<div><h4>Guide</h4><ul>{guide}<li><a href="/guide/">Tutte le guide</a></li><li><a href="/strumenti/">Strumenti gratuiti</a></li></ul></div>
<div><h4>StimaVeloce</h4><ul><li><a href="/chi-siamo/">Chi siamo</a></li><li><a href="/come-funziona/">Come funziona</a></li><li><a href="/faq/">Domande frequenti</a></li><li><a href="{APP}#area">Area personale</a></li><li><a href="/privacy/">Privacy Policy</a></li><li><a href="/cookie/">Cookie Policy</a></li><li><a href="/condizioni/">Condizioni generali</a></li></ul></div>
</div><div class="legal"><span>© 2026 StimaVeloce · {e(tit)} · Sede legale: {e(SITE["sede_legale"])}{piva} · Regime forfettario</span><span>Le informazioni del sito hanno carattere generale e non sostituiscono una valutazione professionale del caso.</span></div></div></footer>'''


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
<meta name="theme-color" content="#1F5EFF"><link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="StimaVeloce"><meta property="og:url" content="{canon}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{U}/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
{lds}{extra_head}</head><body>{header(cur)}<main id="main">{body}</main>{footer()}{wa_widget()}<script src="/assets/site.js?v={CSSV}" defer></script>{scripts}</body></html>'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    PAGES.append((path, index))
    TITLES[path] = (title.split(" | ")[0], desc)


ORG = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": U + "/#studio", "name": "StimaVeloce",
       "url": U + "/", "logo": U + "/icon-512.png", "image": U + "/og-image.jpg", "email": SITE["email"],
       "vatID": "IT" + SITE["piva"], "legalName": SITE["ragione_sociale"], "address": {"@type": "PostalAddress", "streetAddress": "Contrada Piano delle Donne", "postalCode": "87021", "addressLocality": "Belvedere Marittimo", "addressRegion": "CS", "addressCountry": "IT"}, "areaServed": {"@type": "Country", "name": "Italia"}}
if SITE["telefono"]:
    ORG["telephone"] = SITE["telefono"]


def faq_html(items, ld=True):
    h = "".join(f'<details><summary>{e(q)}{ic("chevron-down")}</summary><div class="a">{e(a)}</div></details>' for q, a in items)
    j = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<div class="faq">{h}</div>', j


def band(title="Raccontaci cosa è successo", text="Bastano pochi minuti. Ti diciamo quale servizio è più adatto, prima di qualsiasi pagamento.", btn="Scopri quanto vale il tuo danno"):
    return f'<section class="sec"><div class="wrap"><div class="band"><div><h2>{e(title)}</h2><p>{e(text)}</p></div><a class="btn btn-p btn-lg" href="/stima/">{e(btn)}{ic("arrow-right")}</a></div></div></section>'


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


CONS = "/contatti/?motivo=consulenza"


def price_box(ids):
    out = []
    for i in ids:
        p = PV[i]
        if p.get("vendibile") is False:
            out.append(f'<div class="card price-box"><div class="muted small">{e(p["nome"])}</div><div class="p" style="font-size:22px">Consulenza gratuita</div><p class="small muted">Valutiamo il caso insieme prima di proporti un servizio.</p><a class="btn btn-s" style="width:100%" href="{CONS}">Chiedi una consulenza gratuita</a></div>')
            continue
        out.append(f'<div class="card price-box"><div class="muted small">{e(p["nome"])}</div><div class="p">{prezzo_label(p)}</div><p class="small muted">{e(p["tempi"])}.</p>'
                   f'<a class="btn {"btn-p" if p["prezzo"] else "btn-s"}" style="width:100%" href="{APP}#prefattibilita">{"Inizia" if p["prezzo"] else "Chiedi un preventivo"}</a></div>')
    return "".join(out)


# ------------------------------------------------------------------ HOME
def build_home():
    import illus
    cards = []
    for k, kind, url, desc in [("stima", "perito", "/stima/", "Prima valutazione da foto e documenti, senza firma. Ideale per capire se vale la pena andare avanti."),
                               ("perizia", "auto", "/stima/?tipo=auto", "Relazione firmata sui danni a auto e moto, con verifica di ricambi, manodopera e valore del mezzo."),
                               ("fabbricati", "casa", CONS, "Infiltrazioni, crepe, eventi atmosferici: valutiamo il caso insieme e ti diciamo come procedere."),
                               ("medico", "medico", CONS, "Hai subito lesioni? Ti spieghiamo gratis quali documenti servono e quali sono i passi.")]:
        p = PV[k]
        if p.get("vendibile") is False:
            cards.append(f'<a class="card rv" href="{url}">{illus.mini(kind)}<h3 style="margin-top:16px">{e("Danni alla casa" if k == "fabbricati" else "Lesioni alla persona")}</h3><div class="pr" style="font-size:20px">Consulenza gratuita</div><p class="muted small">{e(desc)}</p><span class="btn btn-s btn-sm" style="width:100%">Chiedi una consulenza gratuita</span></a>')
            continue
        cards.append(f'<a class="card rv" href="{url}">{illus.mini(kind)}<h3 style="margin-top:16px">{e(p["nome"])}</h3><div class="pr">{p["prezzo"]} €</div><p class="muted small">{e(desc)}</p><span class="btn btn-s btn-sm" style="width:100%">Inizia</span></a>')
    gratis = "".join(f'<a class="card tool-card rv" href="{h}"><div class="ibox">{ic(i)}</div><div><h3>{e(t)}</h3><p>Gratis, senza registrazione</p></div></a>' for h, i, t in GRATIS)
    steps = [("Raccontaci cosa è successo", "Poche domande a tocchi, anche dal telefono. Bastano 2 minuti."),
             ("Carica le foto", "Danno, documenti, preventivi: ti diciamo noi cosa serve."),
             ("Ricevi la valutazione", "Un tecnico esamina il caso e ti propone il servizio giusto."),
             ("Segui la pratica", "Stato, documenti e messaggi nella tua area clienti.")]
    steps_h = "".join(f'<div class="step rv rv-d{i % 4}"><div class="n">{i + 1}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(steps))
    sapevi = [("Con il modulo CAI firmato da entrambi i conducenti, la compagnia ha 30 giorni invece di 60 per fare l'offerta sui danni alle cose.", "Art. 148 Codice delle assicurazioni"),
              ("Il diritto al risarcimento dei danni da circolazione di veicoli si prescrive in due anni.", "Art. 2947 Codice civile"),
              ("Se la polizza non dice diversamente, il sinistro va comunicato alla propria compagnia entro tre giorni.", "Art. 1913 Codice civile")]
    sapevi_h = "".join(f'<div class="card"><div class="ibox">{ic("sparkles")}</div><h3 style="font-size:19px">Lo sapevi?</h3><p>{e(t)}</p><p class="small muted" style="margin:0">{e(f)}</p></div>' for t, f in sapevi)
    sim = ('<svg class="ill" viewBox="0 0 560 300" role="img" aria-label="Anteprima del simulatore: due veicoli su un incrocio visti dall\'alto">'
           '<rect width="560" height="300" rx="24" fill="#EEF3FF"/><rect x="0" y="110" width="560" height="80" fill="#C9D3EA"/><rect x="230" y="0" width="100" height="300" fill="#C9D3EA"/>'
           '<path d="M0 150 H200 M360 150 H560 M280 0 V90 M280 210 V300" stroke="#fff" stroke-width="4" stroke-dasharray="16 12"/>'
           '<g transform="translate(120 126)"><rect width="84" height="40" rx="10" fill="#1F5EFF"/><rect x="54" y="6" width="18" height="28" rx="4" fill="#DDE7FF"/></g>'
           '<g transform="translate(262 196) rotate(-90)"><rect width="76" height="36" rx="10" fill="#FF7A1A"/><rect x="48" y="5" width="16" height="26" rx="4" fill="#FFE2CC"/></g>'
           '<circle cx="262" cy="150" r="14" fill="none" stroke="#FF7A1A" stroke-width="4"/><path d="M256 144l12 12M268 144l-12 12" stroke="#FF7A1A" stroke-width="4" stroke-linecap="round"/>'
           '<text x="120" y="112" font-family="Inter,sans-serif" font-size="14" font-weight="700" fill="#0B1B3A">A · 40 km/h</text><text x="296" y="262" font-family="Inter,sans-serif" font-size="14" font-weight="700" fill="#0B1B3A">B · 30 km/h</text></svg>')
    fq, fqld = faq_html(HOME_FAQ)
    body = f'''<section class="hero"><div class="wrap"><div>
<div class="eyebrow">Perizie e stime online · in tutta Italia</div>
<h1>Hai avuto un <span>sinistro?</span></h1>
<p class="lead">Ti aiutiamo a capire quanto vale davvero il tuo danno, con calma e senza burocrazia. Perizie e stime online, seguite da tecnici veri.</p>
<div class="cta-row"><a class="btn btn-p btn-lg" href="/stima/">Scopri quanto vale il tuo danno{ic("arrow-right")}</a><a class="btn btn-s btn-lg" href="/offerta/">Ho già un'offerta</a></div>
<div class="doors"><a href="/sei-in-tempo/">{ic("hourglass")}<span><b>Sinistro di mesi fa?</b>Scopri se sei ancora in tempo</span></a><a href="/polizza-catastrofale/">{ic("shield-check")}<span><b>Hai un'azienda?</b>Controlla la polizza catastrofale</span></a></div>
<p class="trust">{ic("shield-check")}Nessuna promessa di risarcimento: una valutazione tecnica chiara, con prezzi pubblicati.</p>
</div><div>{illus.hero_scene()}</div></div></section>
<section class="sec" id="come-funziona"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Come funziona</div><h2>Quattro passi, tutto online</h2></div><div class="steps">{steps_h}</div></div></section>
<section class="sec sec-w" id="servizi"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Stime e perizie</div><h2>Scegli il servizio, il prezzo è chiaro</h2><p class="lead">Prezzi finali pubblicati, senza IVA: StimaVeloce è in regime forfettario. Prima di pagare puoi sempre descrivere il caso gratis.</p></div><div class="svc4">{"".join(cards)}</div>
<p style="margin-top:22px"><a class="more" href="/prezzi/">Cosa comprende ogni servizio{ic("arrow-right")}</a></p></div></section>
<section class="sec"><div class="wrap"><div class="fixband rv"><div><div class="eyebrow">Perché noi</div><h2>Stime e perizie a prezzo fisso.</h2><p class="lead">Niente percentuali sulla valutazione: sai quanto spendi prima di iniziare, e ogni numero è spiegato.</p></div><div class="cta-row"><a class="btn btn-p btn-lg" href="/perche-noi/#risparmio">Fai il conto con i tuoi numeri</a><a class="btn btn-s btn-lg" href="/sei-in-tempo/">Sei ancora in tempo?</a></div></div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Gratis</div><h2>Strumenti gratuiti, subito</h2></div><div class="grid g2">{gratis}</div></div></section>
<section class="sec sec-w"><div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:40px;align-items:center"><div class="rv">{sim}</div><div class="rv"><div class="eyebrow">Simulatore di dinamica</div><h2>Disegna l'incidente in un minuto</h2><p class="lead">Trascina auto e moto sulla strada, segna i punti d'urto, le distanze e le velocità. Poi salva l'immagine o stampala.</p><p class="small muted">Schema indicativo, non è una perizia.</p><a class="btn btn-p" href="/simulatore/">Apri il simulatore{ic("arrow-right")}</a></div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h rv"><div class="eyebrow">Novità e curiosità</div><h2>Lo sapevi?</h2></div><div class="scroller">{sapevi_h}</div><p><a class="more" href="/novita/">Altre curiosità e leggi aggiornate{ic("arrow-right")}</a></p></div></section>
<section class="sec sec-w" id="segui"><div class="wrap narrow"><div class="card rv" style="padding:36px"><div class="eyebrow">Segui la tua pratica</div><h2 style="font-size:32px">Dov'è arrivata la mia pratica?</h2><p class="muted">Accedi con la tua email: trovi lo stato, i documenti e i messaggi del perito.</p><a class="btn btn-p" href="{APP}#area">Accedi all'area clienti{ic("arrow-right")}</a></div></div></section>
<section class="sec" id="chi-siamo"><div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:40px;align-items:center"><div class="rv"><div class="eyebrow">Chi siamo</div><h2>Tecnici veri, ovunque tu sia</h2><p class="lead">StimaVeloce è un servizio online di stime e perizie sui sinistri. Lavoriamo su foto e documenti, quindi possiamo seguirti in tutta Italia, dal telefono.</p><a class="btn btn-s" href="/chi-siamo/">Chi siamo</a></div><div class="rv"><svg class="ill" viewBox="0 0 300 200" aria-hidden="true"><rect width="300" height="200" rx="24" fill="#EEF3FF"/>{illus.perito(110, 10, .95)}</svg></div></div></section>
<section class="sec sec-w"><div class="wrap narrow"><div class="sec-h rv"><div class="eyebrow">Domande frequenti</div><h2>Le risposte più comuni</h2></div>{fq}<p style="margin-top:24px"><a class="more" href="/faq/">Tutte le domande{ic("arrow-right")}</a></p></div></section>
{band("Hai avuto un sinistro?", "Raccontaci cosa è successo: ti diciamo come possiamo aiutarti, prima di qualsiasi pagamento.", "Scopri quanto vale il tuo danno").replace(APP + "#prefattibilita", "/stima/")}
<script>(function(){{var h=location.hash;if(/^#[a-z][a-z0-9-]*$/.test(h)&&!document.getElementById(h.slice(1)))location.replace("{APP}"+h);}})();</script>'''
    lb = dict(ORG)
    lb.update({"@type": "ProfessionalService", "description": "Perizie e stime danni online in tutta Italia: auto, moto, casa, attività. Stima senza firma 30 €, perizia auto/moto 60 €.", "areaServed": {"@type": "Country", "name": "Italia"}, "priceRange": "30–60 €"})
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "StimaVeloce", "url": U + "/", "inLanguage": "it-IT"}
    page("/", "Perizia danni online in tutta Italia | StimaVeloce",
         "Stime e perizie danni online, in tutta Italia: stima senza firma 30 €, perizia auto/moto 60 €. Consulenza gratuita per casa e lesioni. Strumenti gratuiti.",
         body, cur="/", ld=[lb, web, fqld])


# ------------------------------------------------------------------ SERVIZI
def build_servizi():
    for s in SERVIZI:
        a = next(x for x in AMBITI if x["slug"] == s["ambito"])
        head, bld = ph([("/", "Home"), ("/servizi/", "Servizi"), ("", s["h1"])], s["h1"], s["desc"], a["nome"])
        fq, fqld = faq_html(s["faq"])
        rel_t = "".join(tool_card(TV[t]) for t in s["tools"])
        rel_g = "".join(f'<li><a href="/guide/{g}/">{e(GV[g]["h1"])}</a></li>' for g in s["guides"])
        rel_s = "".join(f'<li><a href="/servizi/{x}/">{e(SV[x]["h1"])}</a></li>' for x in s["correlati"])
        fp = os.path.join(ROOT, "assets/foto", f'svc-{s["slug"]}.webp')
        fig = f'<figure class="svc-ph"><img src="/assets/foto/svc-{s["slug"]}.webp" alt="{e(s["h1"])}: immagine illustrativa" width="1600" height="900" fetchpriority="high" decoding="async"></figure>' if os.path.exists(fp) else ""
        body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><article class="prose">{fig}
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
<div class="calc" data-calc="{t["slug"]}" data-cats="{t.get("cats", "edili,idraulici,elettrici")}"><form class="card form" novalidate onsubmit="return false">{t["form"]}</form>
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
    scan = (f'<a class="card tool-card" href="/strumenti/scanner-foto/" style="border:1.5px dashed #1F5EFF"><div class="ibox">{ic("camera")}</div><div><h3>Scanner foto danni <span class="tbd-chip" style="background:#FFF1E6;color:#E8650A">In arrivo</span></h3>'
            '<p>Fotografi il danno e ricevi un primo elenco delle parti coinvolte. Lascia l\'email: ti avvisiamo quando è pronto.</p></div></a>')
    body = f'{head}<section class="sec" style="padding-top:48px"><div class="wrap"><div class="grid g2">{scan}{"".join(tool_card(t) for t in STRUMENTI)}</div></div></section>{band()}'
    h2, b2 = ph([("/", "Home"), ("/strumenti/", "Strumenti"), ("", "Scanner foto danni")], "Scanner foto danni", "Fotografi il danno e ricevi un primo elenco delle parti coinvolte e delle foto che mancano. Lo stiamo preparando.", "In arrivo")
    page("/strumenti/scanner-foto/", "Scanner foto danni: in arrivo | StimaVeloce", "Lo scanner foto danni di StimaVeloce è in arrivo. Lascia la tua email e ti avvisiamo quando è pronto.",
         h2 + f'''<section class="sec" style="padding-top:40px"><div class="wrap narrow"><form class="card form" name="avvisami" method="POST" action="/strumenti/scanner-foto/grazie/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="avvisami"><input type="hidden" name="strumento" value="scanner-foto"><p class="sr"><label>Non compilare <input name="bot-field"></label></p>
<h2 style="font-size:26px;margin:0">Avvisami quando è pronto</h2><div class="fld"><label for="av-e">La tua email</label><input class="in" id="av-e" name="email" type="email" required autocomplete="email" placeholder="nome@esempio.it"></div>
<label class="chk"><input type="checkbox" name="privacy" value="si" required><span>Acconsento a ricevere una sola email quando lo strumento sarà disponibile (<a href="/privacy/">informativa</a>).</span></label>
<button class="btn btn-p btn-lg" type="submit">Avvisami</button></form><p class="small muted" style="margin-top:14px">Nel frattempo puoi <a href="/stima/">iniziare dalla stima</a> o usare gli <a href="/strumenti/">altri strumenti gratuiti</a>.</p></div></section>''', ld=[b2])
    h3, _ = ph([("/", "Home"), ("/strumenti/", "Strumenti"), ("", "Fatto")], "Ti avviseremo", "Grazie: riceverai un'email appena lo scanner foto danni sarà disponibile.")
    page("/strumenti/scanner-foto/grazie/", "Ti avviseremo | StimaVeloce", "Iscrizione ricevuta.", h3, index=False)
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
<h2>3. Ricevi una valutazione professionale</h2><p>Un tecnico di StimaVeloce esamina la richiesta e ti indica il servizio più adatto con il suo prezzo. Nessun pagamento prima di sapere cosa riceverai.</p>
<h2>4. Segui la pratica dalla tua area personale</h2><p>Ogni pratica ha un codice univoco. Nell'area personale vedi lo stato, carichi altri documenti, scarichi la relazione e ricevi le comunicazioni.</p>
<div class="box"><h3 style="margin-top:0">Gli stati della pratica</h3><ol class="olist">{"".join(f"<li>{e(s)}</li>" for s in stati)}</ol></div>
<h2>Cosa non facciamo</h2><p>Non vendiamo polizze, non garantiamo risarcimenti e non diamo pareri legali. Ci occupiamo della parte tecnica: documentare e quantificare il danno e leggere la polizza.</p>
</div><aside class="aside"><div class="card"><h3>Pronto a iniziare?</h3><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div></aside></div></section>'''
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "Come richiedere una valutazione del danno su StimaVeloce",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(["Racconta cosa è successo", "Carica fotografie e documenti", "Ricevi una valutazione professionale", "Segui la pratica dall'area personale"])]}
    page("/come-funziona/", "Come funziona: valutazione del danno online in 4 passaggi | StimaVeloce", "Racconti il sinistro, carichi foto e documenti, ricevi una valutazione professionale e segui la pratica online. Ecco come funziona StimaVeloce.", body, cur="/come-funziona/", ld=[bld, howto])
    # chi siamo
    head, bld = ph([("/", "Home"), ("", "Chi siamo")], "Chi siamo", "StimaVeloce porta online stime e perizie sui sinistri: tecnici veri, prezzi chiari, in tutta Italia.", "Chi siamo")
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap layout"><div class="prose">
<h2>Cosa facciamo</h2><p>StimaVeloce si occupa di consulenza tecnica sui sinistri: stime dei danni, perizie di parte, analisi di polizze e preventivi. Lavoriamo online, su foto e documenti, per rendere tutto più rapido, più trasparente e accessibile a chiunque, in tutta Italia.</p>
<h2>Il nostro metodo</h2><ul class="ticks"><li>Valutazioni tecniche documentate, in cui ogni numero è spiegato</li><li>Riferimento puntuale a clausole, pagine e voci di danno</li><li>Prezzi pubblicati e preventivi scritti prima di ogni attività aggiuntiva</li><li>Nessuna promessa di risultato: la decisione sull'indennizzo spetta alla compagnia</li></ul>
<h2>Tecnologia al servizio del professionista</h2><p>Usiamo strumenti digitali per organizzare documenti e foto e per velocizzare il lavoro ripetitivo. Le valutazioni restano sempre di un tecnico, che le verifica e le firma.</p>
<h2>Chi firma le perizie</h2><div class="card" style="display:flex;gap:18px;align-items:center;margin:0 0 24px"><div class="ibox" style="width:72px;height:72px;flex:none">{ic("user")}</div><div><b>[DA INSERIRE: nome e titolo del tecnico]</b><p class="small muted" style="margin:4px 0 0">Iscrizione all'albo o al ruolo periti IVASS: [DA INSERIRE] · Foto: [DA INSERIRE]</p></div></div><p>Ogni perizia riporta nome, qualifica e firma del professionista che l'ha redatta.</p>
<h2>Indipendenza</h2><p>Non vendiamo polizze e non lavoriamo per conto delle compagnie nei casi che seguiamo per i nostri clienti.</p>
</div><aside class="aside"><div class="card"><h3>Contatti</h3><p class="small"><a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a><br>{e(SITE["city"])}</p><a class="btn btn-s" style="width:100%" href="/contatti/">Scrivici</a></div></aside></div></section>{band()}'''
    page("/chi-siamo/", "Chi siamo | StimaVeloce", "StimaVeloce: consulenza tecnica sui sinistri, stime e perizie di parte online, in tutta Italia.", body, cur="/chi-siamo/", ld=[bld, ORG])
    # prezzi
    head, bld = ph([("/", "Home"), ("", "Prezzi")], "Servizi e prezzi", "Prezzi chiari prima di iniziare. Per le attività su preventivo ricevi l'importo per iscritto prima di qualsiasi lavoro.", "Prezzi")
    cards = ""
    for p in [x for x in PREZZI if x.get("vendibile") is not False]:
        cards += f'''<div class="card pcard{" feat-p" if p["id"] == "perizia" else ""}"><h3>{e(p["nome"])}</h3><p class="muted small" style="margin:0">{e(p["breve"])}</p><div class="p">{prezzo_label(p)}</div>
<h4>Comprende</h4><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in p["comprende"])}</ul><h4>Non comprende</h4><ul class="ticks x">{"".join(f"<li>{e(x)}</li>" for x in p["esclude"])}</ul>
<h4>Dettagli</h4><p class="dl"><b>Documenti:</b> {e(", ".join(p["documenti"]))}</p><p class="dl"><b>Tempi indicativi:</b> {e(p["tempi"])}</p><p class="dl"><b>Consegna:</b> {e(p["formato"])}</p><p class="dl" style="margin-bottom:20px"><b>Costi aggiuntivi:</b> {e(p["extra"])}</p>
<a class="btn {"btn-p" if p["prezzo"] else "btn-s"}" href="{APP}#prefattibilita">{"Inizia" if p["prezzo"] else "Chiedi un preventivo"}</a></div>'''
    body = f'''{head}<section class="sec" style="padding-top:48px"><div class="wrap"><div class="prices">{cards}</div>
<div class="card" style="margin-top:32px;display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between"><div><h3 style="margin:0">Danni alla casa o lesioni alla persona?</h3><p class="muted" style="margin:6px 0 0">Per ora li seguiamo con una consulenza gratuita: valutiamo il caso insieme e ti diciamo come procedere.</p></div><a class="btn btn-s" href="{CONS}">Chiedi una consulenza gratuita</a></div>
<div class="card" style="margin-top:20px"><h3>Pagamento e cancellazione</h3><p class="muted" style="margin:0">{e(CONDIZIONI_PAGAMENTO)}</p></div>
<p class="small muted" style="margin-top:16px">Prima di pagare puoi sempre descrivere il caso gratuitamente: ti indichiamo il servizio adatto. <a href="/condizioni/">Condizioni generali</a>.</p></div></section>{band()}'''
    offers = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Servizi StimaVeloce", "itemListElement": [
        {"@type": "Offer", "name": p["nome"], "price": p["prezzo"], "priceCurrency": "EUR"} for p in PREZZI if p["prezzo"] and p.get("vendibile") is not False]}
    page("/prezzi/", "Prezzi: stima 30 €, perizia auto/moto 60 € | StimaVeloce", "Prezzi dei servizi StimaVeloce: stima senza firma 30 €, perizia auto/moto 60 €. Consulenza gratuita per danni alla casa e lesioni. Cosa comprendono e condizioni.", body, ld=[bld, offers])
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
<div class="row2"><div class="fld"><label for="c-tel">Telefono <span class="muted">(facoltativo)</span></label><input class="in" id="c-tel" name="telefono" type="tel" autocomplete="tel"></div><div class="fld"><label for="c-mot">Argomento</label><select class="in" id="c-mot" name="motivo"><option value="consulenza">Consulenza gratuita (casa, lesioni, altro)</option><option value="stima">Vorrei una stima del danno</option><option value="perizia">Vorrei una perizia</option><option value="pratica">Stato della mia pratica</option><option value="offerta">Ho ricevuto un'offerta dalla compagnia</option><option value="avvocati">Sono un avvocato o un professionista</option><option value="altro">Altro</option></select></div></div>
<div class="fld"><label for="c-msg">Messaggio</label><textarea class="in" id="c-msg" name="messaggio" required></textarea></div>
<label class="chk"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l'<a href="/privacy/">informativa privacy</a> e acconsento al trattamento dei dati per ricevere risposta.</span></label>
<button class="btn btn-p btn-lg" type="submit">Invia messaggio</button></form>
<aside class="aside"><div class="card"><h3>Vuoi aprire una pratica?</h3><p class="muted small">Il percorso guidato raccoglie già tutte le informazioni utili.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Analizza il tuo sinistro</a></div>
<div class="card"><h3 style="font-size:17px">Recapiti</h3><p>{ic("mail")} <a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a></p>{tel}<p style="margin:0">{ic("map-pin")} {e(SITE["indirizzo"] or SITE["city"])}</p></div></aside></div></section>'''
    page("/contatti/", "Contatti | StimaVeloce", "Scrivici per informazioni sui servizi, preventivi e pratiche già aperte.", body, ld=[bld, ORG])
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


# ------------------------------------------------------------------ NUOVE SEZIONI (stima, simulatore, novità, periti, gestione, professionisti)
def build_stima():
    head, bld = ph([("/", "Home"), ("", "Quanto vale il tuo danno?")], "Quanto vale il tuo danno?", "Quattro tocchi per capire cosa valuta il perito nel tuo caso. Gratis, senza registrazione.", "Stima")
    body = head + f'''<section class="sec" style="padding-top:36px"><div class="wrap narrow">
<div class="card" id="quiz" style="padding:28px" data-app="{APP}">
<div class="mock-st" style="margin:0 0 22px" aria-hidden="true"><i class="on" data-qbar="0"></i><i data-qbar="1"></i><i data-qbar="2"></i><i data-qbar="3"></i></div>
<div data-q="0"><h2 style="font-size:28px">Che tipo di danno hai subito?</h2><div class="qopts" data-k="tipo">
<button type="button" data-v="auto">{ic("car")}Auto</button><button type="button" data-v="moto">{ic("bike")}Moto o scooter</button><button type="button" data-v="casa">{ic("house")}Casa o condominio</button>
<button type="button" data-v="attivita">{ic("store")}Attività o negozio</button><button type="button" data-v="persona">{ic("heart-pulse")}Lesioni alla persona</button><button type="button" data-v="sisma">{ic("triangle-alert")}Lesioni da sisma</button><button type="button" data-v="altro">{ic("circle-help")}Altro</button></div><p style="margin:18px 0 0"><a class="more" href="/offerta/">Hai già un'offerta della compagnia? Controllala{ic("arrow-right")}</a></p></div>
<div data-q="1" hidden><h2 style="font-size:28px" data-q1t>Cosa è stato danneggiato?</h2><div class="qopts" data-k="ogg"></div></div>
<div data-q="2" hidden><h2 style="font-size:28px">Quanto ti sembra grave?</h2><div class="qopts" data-k="grav">
<button type="button" data-v="lieve">{ic("info")}Lieve<small>Graffi, macchie, piccoli danni</small></button><button type="button" data-v="medio">{ic("triangle-alert")}Medio<small>Parti da sostituire o rifare</small></button><button type="button" data-v="grave">{ic("flame")}Grave<small>Danni estesi o non so valutare</small></button></div></div>
<div data-q="3" hidden><h2 style="font-size:28px">Hai delle foto del danno?</h2><div class="qopts" data-k="foto">
<button type="button" data-v="si">{ic("camera")}Sì, le ho</button><button type="button" data-v="poche">{ic("image")}Poche o non chiare</button><button type="button" data-v="no">{ic("x")}Non ancora</button></div></div>
<div data-q="4" hidden id="anteprima"></div>
<div style="display:flex;justify-content:space-between;margin-top:18px" class="no-print"><button type="button" class="btn btn-g btn-sm" data-qback hidden>{ic("arrow-left")}Indietro</button><span></span></div>
</div>
<p class="small muted" style="margin-top:16px">L'anteprima è qualitativa: non indica cifre. Il valore del danno arriva con la stima, eseguita da un tecnico sulla base delle tue foto e dei documenti.</p>
</div></section>'''
    page("/stima/", "Quanto vale il tuo danno? Stima in 4 tocchi | StimaVeloce", "Rispondi a 4 domande e scopri cosa valuta il perito nel tuo caso: auto, moto, casa, attività o lesioni. Poi ottieni la stima senza firma a 30 €.", body, cur="/stima/", ld=[bld], scripts=f'<script src="/assets/quiz.js?v={CSSV}" defer></script>')


def build_simulatore():
    head, bld = ph([("/", "Home"), ("", "Simulatore di dinamica")], "Simulatore di dinamica 2.0",
                   "Disegna il percorso col dito, premi play e guarda l'incidente accadere: il simulatore trova il punto di contatto, calcola velocità e spazi di frenata e scrive il racconto per te.", "Gratis · nuovo")
    pres = [("precedenza", "Precedenza all'incrocio"), ("tamponamento", "Tamponamento"), ("svolta", "Svolta a sinistra"), ("corsia", "Cambio corsia"),
            ("rotatoria", "Rotatoria"), ("parcheggio", "Uscita da parcheggio"), ("pedone", "Pedone sulle strisce")]
    chips = "".join(f'<button type="button" class="chip" data-preset="{k}">{e(t)}</button>' for k, t in pres)
    adds = "".join(f'<button type="button" class="btn btn-s btn-sm" data-add-v="{k}">{ic("plus")}{t}</button>' for k, t in
                   [("auto", "Auto"), ("moto", "Moto"), ("camion", "Furgone"), ("bici", "Bici"), ("pedone", "Pedone"), ("urto", "Segno d'urto")])
    body = head + f'''<section class="sec" style="padding-top:24px"><div class="wrap">
<div class="sim2">
<div class="sim-stage">
<div class="sim-wrap"><svg id="sim" viewBox="0 0 800 560" role="img" aria-label="Schema animato della dinamica dell'incidente"></svg><button type="button" class="sim-fab no-print" data-fab hidden>✍️ Disegna il percorso</button><button type="button" class="sim-fab sim-fab-x no-print" data-fab-x hidden>✕ Annulla disegno</button><div class="sim-banner no-print" data-banner hidden>✍️ Trascina il dito sulla strada, partendo dal veicolo</div></div>
<div class="sim-player no-print"><button type="button" class="btn btn-p" data-play>▶ Guarda l'incidente</button>
<input type="range" min="0" max="1000" value="0" data-time aria-label="Tempo"><span class="sim-t" data-tlabel>0,0 s</span>
<select class="in sim-speed" data-speed aria-label="Velocità di riproduzione"><option value="1">1×</option><option value="0.5">Lento ½</option><option value="0.25">Moviola ¼</option></select>
<label class="sim-ck"><input type="checkbox" data-strobe checked> Scia</label></div>
<p class="small muted sim-hint no-print" data-hint></p>
</div>
<div class="sim-panel no-print">
<div class="sp"><div class="sp-h"><span>1</span>Scegli una situazione</div><div class="chips">{chips}</div></div>
<div class="sp"><div class="sp-h"><span>2</span>Dove è successo</div>
<div class="row2"><select class="in" id="sim-road" aria-label="Tipo di strada"><option value="incrocio">Incrocio</option><option value="dritta">Rettilineo</option><option value="rotonda">Rotatoria</option><option value="parcheggio">Parcheggio</option><option value="mappa">🗺 Mappa reale</option></select>
<select class="in" id="sim-surf" aria-label="Fondo stradale"><option value="asciutto">Asfalto asciutto</option><option value="bagnato">Asfalto bagnato</option><option value="ghiaccio">Ghiaccio o neve</option></select></div>
<div class="sim-map" hidden><div class="row2" style="grid-template-columns:1fr auto"><input class="in" id="sim-addr" placeholder="Via e comune, es. Via Roma 1, Bologna" autocomplete="street-address"><button type="button" class="btn btn-s btn-sm" data-find>Cerca</button></div>
<div class="sim-add"><button type="button" class="btn btn-g btn-sm" data-gps>{ic("map-pin")}Usa la mia posizione</button><button type="button" class="btn btn-g btn-sm" data-zoom="1.5" aria-label="Avvicina">{ic("plus")}</button><button type="button" class="btn btn-g btn-sm" data-zoom="0.6667" aria-label="Allontana">{ic("minus")}</button></div>
<p class="small muted" data-map-msg>La mappa è in scala reale.</p></div></div>
<div class="sp"><div class="sp-h"><span>3</span>Chi era coinvolto</div><div class="sim-add">{adds}</div>
<div class="sim-sel card" hidden><div class="lbl" data-sel-name>Veicolo</div>
<div class="sim-mv"><div class="row2" style="grid-template-columns:1fr 96px"><div class="fld"><label class="small" for="sim-kmhr">Velocità</label><input type="range" id="sim-kmhr" min="0" max="130" step="5"></div><div class="fld"><label class="small" for="sim-kmh">km/h</label><input class="in" id="sim-kmh" type="number" min="0" max="200" inputmode="numeric"></div></div>
<label class="sim-ck"><input type="checkbox" id="sim-brake"> Ha frenato (reazione 1 s)</label>
<div class="sim-add"><button type="button" class="btn btn-p btn-sm" data-draw>{ic("square-pen")}Disegna il percorso</button><button type="button" class="btn btn-g btn-sm" data-clear-path>Dritto</button></div>
<div class="fld"><label class="small" for="sim-lab">Nome</label><input class="in" id="sim-lab" maxlength="14"></div></div>
<div class="sim-add"><button type="button" class="btn btn-g btn-sm sim-mv" data-rot="-15">↺</button><button type="button" class="btn btn-g btn-sm sim-mv" data-rot="15">↻</button><button type="button" class="btn btn-g btn-sm" data-del-v>{ic("x")}Elimina</button></div></div></div>
<div class="sim-add"><button type="button" class="btn btn-g btn-sm" data-undo>↶ Annulla</button><button type="button" class="btn btn-g btn-sm" data-reset>Ricomincia</button></div>
</div>
</div>
<div class="card sim-report" style="margin-top:20px;padding:24px"><div class="eyebrow">4 · Il racconto della dinamica</div><h2 style="font-size:26px;margin:6px 0 12px">Ecco cosa è successo</h2>
<div data-story></div>
<div class="sim-add no-print" style="margin-top:14px"><button type="button" class="btn btn-p btn-sm" data-copy>Copia il racconto</button><button type="button" class="btn btn-s btn-sm" data-export>{ic("download")}Salva immagine</button><button type="button" class="btn btn-s btn-sm" data-print>{ic("printer")}Stampa</button><button type="button" class="btn btn-s btn-sm" data-share>Condividi link</button><a class="btn btn-g btn-sm" href="/stima/?tipo=auto">Fai valutare il danno</a></div></div>
<div class="note" style="margin-top:16px">{ic("info")}<div><b>Schema indicativo, non è una perizia.</b> Velocità, tempi e spazi sono calcoli teorici (tempo di reazione 1 s, aderenza standard del fondo): servono a spiegare la dinamica, non ad attribuire responsabilità. La ricostruzione vera la fa un tecnico.</div></div>
</div></section>'''
    css = ('<style>.sim2{display:grid;grid-template-columns:1fr 360px;gap:20px;align-items:start}.sim-stage svg{width:100%;height:auto;border-radius:22px;background:#EEF3FF;touch-action:none;user-select:none;-webkit-user-select:none;box-shadow:0 10px 30px rgba(11,27,58,.08)}'
           '.sim-player{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px}.sim-player input[type=range]{flex:1;min-width:120px;accent-color:#FF7A1A;height:44px}.sim-t{font-weight:800;font-variant-numeric:tabular-nums;min-width:52px}.sim-player .sim-speed{width:auto;flex:none;min-height:44px}'
           '.sim-ck{display:flex;align-items:center;gap:8px;font-size:15px;min-height:44px}.sim-ck input{width:20px;height:20px;accent-color:#FF7A1A}.sim-hint{margin:8px 2px 0;min-height:1.4em}'
           '.sim-panel{display:grid;gap:14px}.sp{background:#fff;border:1px solid #E3E7F0;border-radius:20px;padding:16px;display:grid;gap:10px}.sp-h{font-weight:800;color:#0B1B3A;display:flex;align-items:center;gap:10px}.sp-h span{width:26px;height:26px;border-radius:50%;background:#1F5EFF;color:#fff;display:grid;place-items:center;font-size:14px}'
           '.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{min-height:44px;padding:8px 14px;border-radius:999px;border:1px solid #D3DAE8;background:#F7F8FB;font:inherit;font-size:14px;font-weight:600;color:#0B1B3A;cursor:pointer;transition:.15s}.chip:hover{background:#EEF3FF;border-color:#1F5EFF}'
           '.sim-add{display:flex;flex-wrap:wrap;gap:8px}.sim-add .btn{min-height:44px}.row2{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sim-sel{display:grid;gap:10px;padding:14px;border-color:#1F5EFF}.sim-sel input[type=range]{width:100%;accent-color:#1F5EFF;height:36px}'
           '.sim-text{line-height:1.7;font-size:16px}.sim-wrap{position:relative}.sim-fab{position:absolute;left:10px;top:10px;min-height:44px;padding:8px 16px;border-radius:999px;border:0;background:#0B1B3A;color:#fff;font:inherit;font-weight:700;font-size:15px;box-shadow:0 6px 18px rgba(11,27,58,.25);cursor:pointer}.sim-fab-x{background:#fff;color:#0B1B3A;border:1px solid #D3DAE8}.sim-banner{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);background:#1F5EFF;color:#fff;font-weight:700;padding:10px 16px;border-radius:999px;font-size:14px;white-space:nowrap;pointer-events:none;animation:svpulse 1.4s infinite}@keyframes svpulse{50%{opacity:.75}}.shake{animation:svshake .45s}.sim-boom{transform-box:fill-box;transform-origin:center;animation:svboom .5s ease-out}'
           '@keyframes svshake{0%,100%{transform:none}20%{transform:translate(-6px,2px)}40%{transform:translate(5px,-3px)}60%{transform:translate(-3px,2px)}80%{transform:translate(2px,-1px)}}@keyframes svboom{from{transform:scale(.2);opacity:0}to{transform:scale(1);opacity:1}}'
           '@media(prefers-reduced-motion:reduce){.shake,.sim-boom{animation:none}}'
           '@media(max-width:980px){.sim2{grid-template-columns:1fr}}'
           '@media print{.sim2{display:block}.sim-stage{position:static}.sim-stage svg{border:1px solid #ccc;box-shadow:none}.sim-report{break-inside:avoid;border:0}}</style>')
    page("/simulatore/", "Simulatore incidente stradale animato, gratis | StimaVeloce",
         "Ricostruisci l'incidente in un minuto: disegna i percorsi col dito, guarda l'animazione, trova il punto d'urto, calcola spazi di frenata. Anche su mappa reale. Gratis.",
         body, cur="/simulatore/", ld=[bld], extra_head=css, scripts=f'<script src="/assets/sim.js?v={CSSV}" defer></script>')


NOVITA = [
    ("2026-04-08", "Constatazione amichevole anche digitale", "Dall'8 aprile 2026 le compagnie devono permettere di compilare il CAI da smartphone o computer. Perizia e liquidazione restano invariate: per questo conta presentare il danno in modo chiaro.", "Regolamento IVASS sulla constatazione amichevole digitale", "/simulatore/"),
    ("2026-10-13", "Campi Flegrei: piano straordinario per le case danneggiate", "Contributo fino a 30.000 € per i danni lievi delle abitazioni principali sgomberate a Bacoli, Napoli, Pozzuoli e Monte di Procida. Domande entro il 31 dicembre 2026.", "Consiglio dei ministri, 13 ottobre 2026", "/campi-flegrei/"),
    ("2026-03-31", "Polizza catastrofale: obbligo esteso a tutte le imprese", "Con la scadenza del 31 marzo 2026 per turismo, ristorazione e pesca, l'obbligo vale ormai per quasi tutte le imprese. Franchigia massima 15%.", "L. 213/2023 e D.L. 200/2025", "/polizza-catastrofale/"),
    ("2026-04-01", "Danno biologico lieve: aggiornati gli importi", "Dal mese di aprile 2026 il primo punto di invalidità per le lesioni di lieve entità vale 988,45 € e l'inabilità temporanea assoluta 57,64 € al giorno (+2,6%).", "Art. 139 Codice delle assicurazioni, decreto MIMIT 2026", "/strumenti/danno-biologico/"),
    ("2026-01-29", "Nuovo prezzario dei lavori pubblici in Campania", "La Regione Campania ha approvato il prezzario 2026 (DGR n. 14 del 29 gennaio 2026): è il riferimento che usiamo nei calcolatori di stima dei lavori.", "BURC n. 6 del 2 febbraio 2026", "/strumenti/stime-ripristino/"),
    ("2025-03-05", "In vigore la Tabella unica nazionale per le lesioni gravi", "Per i sinistri stradali e sanitari dal 5 marzo 2025, le lesioni da 10 a 100 punti si liquidano con la Tabella unica nazionale.", "DPR 13 gennaio 2025, n. 12", "/guide/risarcimento-danni-auto/"),
]
SAPEVI = [
    ("Con il CAI firmato da entrambi, l'offerta arriva prima", "La compagnia ha 30 giorni invece di 60 per l'offerta sui danni alle cose.", "Art. 148 Codice delle assicurazioni"),
    ("Due anni per chiedere il risarcimento", "Il diritto al risarcimento dei danni da circolazione si prescrive in due anni.", "Art. 2947 Codice civile"),
    ("Tre giorni per avvisare la compagnia", "Se la polizza non prevede un termine diverso, il sinistro va comunicato entro tre giorni.", "Art. 1913 Codice civile"),
    ("Devi limitare il danno", "Chi è assicurato deve fare il possibile per evitare o ridurre il danno: le spese fatte per questo sono a carico dell'assicuratore nei limiti di legge.", "Art. 1914 Codice civile"),
    ("Sottoassicurato? L'indennizzo si riduce", "Se la somma assicurata è inferiore al valore del bene, l'indennizzo è proporzionale, salvo patto contrario.", "Art. 1907 Codice civile"),
    ("Il passeggero chiede al proprio veicolo", "Il terzo trasportato chiede il risarcimento alla compagnia del veicolo su cui viaggiava, chiunque abbia la colpa.", "Art. 141 Codice delle assicurazioni"),
]


def build_novita():
    head, bld = ph([("/", "Home"), ("", "Novità e curiosità")], "Novità e curiosità", "Leggi e regole aggiornate che cambiano qualcosa per chi ha un sinistro, e le curiosità che pochi conoscono.", "Novità")
    nov = "".join(f'<article class="card rv"><span class="tag">{d[8:10]}/{d[5:7]}/{d[:4]}</span><h3 style="margin-top:12px">{e(t)}</h3><p class="muted">{e(x)}</p><p class="small muted">Fonte: {e(f)}</p><a class="more" href="{u}">Approfondisci{ic("arrow-right")}</a></article>' for d, t, x, f, u in NOVITA)
    sap = "".join(f'<div class="card rv"><div class="ibox">{ic("sparkles")}</div><h3 style="font-size:19px">{e(t)}</h3><p class="muted">{e(x)}</p><p class="small muted" style="margin:0">{e(f)}</p></div>' for t, x, f in SAPEVI)
    body = head + f'<section class="sec" style="padding-top:40px"><div class="wrap"><h2>Leggi aggiornate</h2><div class="grid g3" style="margin-bottom:56px">{nov}</div><h2>Lo sapevi?</h2><div class="grid g3">{sap}</div><p class="small muted" style="margin-top:24px">Informazioni generali, non costituiscono consulenza legale.</p></div></section>' + band()
    page("/novita/", "Novità su sinistri e assicurazioni, curiosità | StimaVeloce", "Leggi aggiornate su risarcimenti, danno biologico, prezzari e tabelle, più le curiosità sui sinistri che pochi conoscono.", body, cur="/novita/", ld=[bld])


def build_periti():
    head, bld = ph([("/", "Home"), ("", "Area periti")], "Area periti", "Accedi alla tua scrivania o candidati per collaborare con StimaVeloce.", "Periti e collaboratori")
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><form class="card form" name="candidatura-perito" method="POST" action="/periti/grazie/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="candidatura-perito"><p class="sr"><label>Non compilare <input name="bot-field"></label></p>
<h2 style="font-size:28px;margin:0">Candidati come collaboratore</h2><p class="muted" style="margin:0">Ogni candidatura viene verificata da StimaVeloce prima dell'attivazione.</p>
<div class="row2"><div class="fld"><label for="p-nome">Nome e cognome</label><input class="in" id="p-nome" name="nome" required autocomplete="name"></div><div class="fld"><label for="p-email">Email</label><input class="in" id="p-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row2"><div class="fld"><label for="p-tel">Telefono</label><input class="in" id="p-tel" name="telefono" type="tel" autocomplete="tel"></div><div class="fld"><label for="p-q">Qualifica</label><select class="in" id="p-q" name="qualifica"><option>Perito assicurativo</option><option>Ingegnere</option><option>Architetto</option><option>Geometra</option><option>Medico legale</option><option>Altro</option></select></div></div>
<div class="row2"><div class="fld"><label for="p-ivass">Iscrizione al ruolo periti IVASS (se presente)</label><input class="in" id="p-ivass" name="ruolo_ivass" placeholder="Numero di iscrizione"></div><div class="fld"><label for="p-zone">Zone operative</label><input class="in" id="p-zone" name="zone" placeholder="Es. province o regioni"></div></div>
<div class="fld"><label for="p-spec">Specializzazioni ed esperienza</label><textarea class="in" id="p-spec" name="specializzazioni"></textarea></div>
<label class="chk"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l'<a href="/privacy/">informativa privacy</a> e acconsento al trattamento dei dati per la valutazione della candidatura.</span></label>
<button class="btn btn-p btn-lg" type="submit">Invia candidatura</button></form>
<aside class="aside"><div class="card"><h3>Sei già collaboratore?</h3><p class="muted small">Accedi alla scrivania del perito per vedere gli incarichi.</p><a class="btn btn-p" style="width:100%" href="{APP}#scrivania">Accedi alla scrivania</a></div></aside></div></section>'''
    page("/periti/", "Area periti: accesso e candidatura | StimaVeloce", "Accesso alla scrivania dei periti e candidatura per collaborare con StimaVeloce: periti assicurativi, tecnici e medici legali.", body, ld=[bld])
    h2, _ = ph([("/", "Home"), ("/periti/", "Area periti"), ("", "Candidatura inviata")], "Candidatura inviata", "Grazie: StimaVeloce valuterà la candidatura e ti contatterà via email.")
    page("/periti/grazie/", "Candidatura inviata | StimaVeloce", "Candidatura inviata.", h2, index=False)


def build_gestione():
    head, bld = ph([("/", "Home"), ("", "Gestione sinistro")], "Affida la pratica a noi", "Seguiamo la parte tecnica del tuo sinistro dall'inizio alla fine, così tu non devi rincorrere nessuno.", "Gestione sinistro")
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><div class="prose">
<h2>Cosa facciamo per te</h2><ul class="ticks"><li>Raccogliamo e ordiniamo foto e documenti</li><li>Valutiamo il danno e prepariamo la documentazione tecnica</li><li>Ti teniamo aggiornato sullo stato della pratica nell'area clienti</li><li>Verifichiamo le offerte della compagnia dal punto di vista tecnico</li></ul>
<h2>Cosa non facciamo</h2><p>Non diamo consulenza legale né medica. Gli atti a contenuto legale (messe in mora, contestazioni, accordi) vengono curati da un avvocato; le valutazioni sulle lesioni da un medico legale.</p>
<h2>Condizioni</h2><p><span class="tbd-chip">[DA DEFINIRE]</span> Le condizioni economiche dell'affidamento vengono comunicate per iscritto prima di iniziare.</p>
<h2 id="accessori">Accessori per la pratica</h2><p>Servizi aggiuntivi su richiesta. <span class="tbd-chip">PREZZI DA DEFINIRE</span></p>
</div><aside class="aside"><div class="card"><h3>Vuoi affidarci la pratica?</h3><p class="muted small">Raccontaci il caso: ti rispondiamo con una proposta scritta.</p><a class="btn btn-p" style="width:100%" href="{APP}#prefattibilita">Racconta il sinistro</a><a class="btn btn-g" style="width:100%;margin-top:6px" href="/contatti/?motivo=pratica">Fai una domanda</a></div></aside></div></section>'''
    page("/gestione-sinistro/", "Affida la gestione del sinistro a StimaVeloce | StimaVeloce", "Affida a StimaVeloce la parte tecnica del sinistro: documentazione, valutazione del danno, verifica delle offerte, aggiornamenti costanti.", body, ld=[bld])


def build_professionisti():
    head, bld = ph([("/", "Home"), ("", "Per avvocati e professionisti")], "Supporto peritale per avvocati e professionisti", "Perizie tecniche, quantificazioni e relazioni per studi legali, patrocinatori e professionisti.", "Professionisti")
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><div class="prose">
<h2>Cosa offriamo</h2><ul class="ticks"><li>Perizie di parte su veicoli e fabbricati</li><li>Computi e quantificazioni con prezzari di riferimento</li><li>Analisi di polizze, perizie della compagnia e preventivi</li><li>Relazioni tecniche a supporto della trattativa</li></ul>
<h2>Prezzi</h2><p><span class="tbd-chip">PREZZI DA DEFINIRE</span> Per ora ogni incarico viene quotato con un preventivo scritto.</p>
</div><aside class="aside"><div class="card"><h3>Richiedi un preventivo</h3><a class="btn btn-p" style="width:100%" href="/contatti/?motivo=avvocati">Contattaci</a></div></aside></div></section>'''
    page("/professionisti/", "Supporto peritale per avvocati e professionisti | StimaVeloce", "Perizie di parte, quantificazioni e relazioni tecniche per avvocati, patrocinatori e professionisti: preventivo su richiesta.", body, ld=[bld])


def build_seo():
    urls = [p for p, idx in PAGES if idx]
    def pri(p):
        return "1.0" if p == "/" else "0.8" if p.startswith("/servizi/") or p in ("/prezzi/", "/strumenti/") else "0.6"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'<url><loc>{U}{p}</loc><lastmod>{SITE["updated_iso"]}</lastmod><priority>{pri(p)}</priority></url>\n' for p in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\nDisallow: /contatti/grazie/\n\nSitemap: {U}/sitemap.xml\n")
    print(f"pagine: {len(PAGES)} · in sitemap: {len(urls)}")



# ------------------------------------------------------------------ IN PRIMO PIANO (Campi Flegrei, polizza catastrofale, offerta)
def _src(items):
    return '<h2>Fonti ufficiali</h2><ul class="small">' + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{e(t)}</a></li>' for t, u in items) + "</ul>"


def build_flegrei():
    head, bld = ph([("/", "Home"), ("", "Danni da sisma e bradisismo")], "Lesioni da sisma o bradisismo ai Campi Flegrei",
                   "Crepe, distacchi, infissi che non chiudono: documentiamo i danni della tua casa in modo ordinato, con foto, rilievo e computo dei lavori.", "In primo piano · Campi Flegrei")
    faq = [("StimaVeloce presenta la domanda di contributo per me?", "No. La domanda va presentata secondo le modalità indicate dall'amministrazione competente. Noi prepariamo la documentazione tecnica del danno che ti serve per farlo, o che serve al tecnico che sceglierai."),
           ("Mi garantite il contributo?", "No. Il contributo dipende dai requisiti fissati dalle norme e dalle verifiche degli enti. Ti diamo una fotografia tecnica chiara del danno e del costo di ripristino."),
           ("Abito fuori dai Comuni interessati: posso farmi seguire?", "Sì, per la parte tecnica (rilievo, foto, computo) e per eventuali richieste alla tua assicurazione, se la polizza copre il terremoto."),
           ("Quanto costa?", "La prima consulenza è gratuita. Per la stima senza firma (30 €) o per un sopralluogo ti diciamo prima il costo per iscritto.")]
    fq, fqld = faq_html(faq)
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><div class="prose">
<div class="note-box" style="background:#FFF4EB;border:1px solid #FFD5B5;border-radius:18px;padding:18px 20px;margin-bottom:28px"><b>Scadenza da tenere d'occhio.</b> Il Piano straordinario per i Campi Flegrei (decreto-legge approvato dal Consiglio dei ministri il 13 ottobre 2026) prevede un contributo fino a 30.000 € per riparare i danni lievi delle abitazioni principali sgomberate a Bacoli, Napoli, Pozzuoli e Monte di Procida, con domande entro il 31 dicembre 2026. Requisiti e modalità possono cambiare: verifica sempre sui siti della Protezione civile e del tuo Comune.</div>
<h2>Cosa facciamo per te</h2><ul class="ticks"><li>Fascicolo fotografico ordinato di ogni lesione, stanza per stanza</li><li>Rilievo e misure delle parti danneggiate</li><li>Computo dei lavori di ripristino con il Prezzario Regione Campania 2026</li><li>Perizia firmata da usare con la tua assicurazione, se la polizza copre il terremoto</li><li>Un elenco chiaro dei documenti da conservare</li></ul>
<h2>Cosa preparare</h2><ul class="ticks"><li>Eventuale ordinanza di sgombero e esito delle verifiche (scheda AeDES o CARTIS, se ricevuta)</li><li>Foto delle lesioni con la data, meglio con un metro o un oggetto di riferimento</li><li>Titolo di proprietà o contratto, dati catastali</li><li>Pratiche edilizie e eventuali domande di condono o sanatoria</li><li>Polizza casa o condominio, se c'è</li></ul>
<h2>Cosa non facciamo</h2><p>Non presentiamo le domande al posto tuo, non diamo consulenza legale e non promettiamo contributi o indennizzi. Le verifiche di agibilità sono compito degli enti e dei tecnici incaricati.</p>
<h2>Domande frequenti</h2>{fq}
{_src([("Protezione civile – Campi Flegrei", "https://rischi.protezionecivile.gov.it/it/vulcanico/vulcani-italia/campi-flegrei/"), ("Governo – Comunicati del Consiglio dei ministri", "https://www.governo.it/it/comunicati-stampa")])}
<p class="small muted">Ultimo aggiornamento: {e(SITE["updated"])}. Informazioni generali, non costituiscono consulenza legale.</p>
</div><aside class="aside"><div class="card"><h3>Hai lesioni in casa?</h3><p class="muted small">Inizia con 4 tocchi, poi carica le foto.</p><a class="btn btn-p" style="width:100%" href="/stima/?tipo=sisma">Inizia la stima</a><a class="btn btn-g" style="width:100%;margin-top:6px" href="/contatti/?motivo=perizia">Chiedi un sopralluogo</a></div></aside></div></section>'''
    page("/campi-flegrei/", "Danni da sisma e bradisismo Campi Flegrei: perizia e computo | StimaVeloce",
         "Lesioni in casa dopo il sisma ai Campi Flegrei? Fascicolo fotografico, rilievo e computo con Prezzario Campania 2026. Contributo fino a 30.000 €: domande entro il 31/12/2026.",
         body, ld=[bld, fqld])


def build_catnat():
    head, bld = ph([("/", "Home"), ("", "Polizza catastrofale imprese")], "Polizza catastrofale: la tua copre davvero?",
                   "È obbligatoria per quasi tutte le imprese. Leggiamo la tua polizza e ti diciamo in parole semplici cosa copre e cosa no.", "In primo piano · Aziende")
    faq = [("Chi deve averla?", "Le imprese con sede in Italia, o con stabile organizzazione in Italia, iscritte al Registro delle imprese, per i beni aziendali: terreni, fabbricati, impianti e macchinari, attrezzature. Sono escluse le imprese agricole, che hanno regole proprie."),
           ("Cosa deve coprire?", "Danni da terremoto, alluvione, frana, inondazione ed esondazione. La franchigia o lo scoperto non possono superare il 15% del danno."),
           ("Cosa rischia chi non la ha?", "La legge collega l'obbligo all'accesso a contributi, sovvenzioni e agevolazioni pubbliche. Per i dettagli sul tuo caso rivolgiti al tuo commercialista o al tuo intermediario."),
           ("Voi vendete polizze?", "No. Non siamo intermediari: facciamo solo l'analisi tecnica della polizza che hai già o del preventivo che ti hanno proposto.")]
    fq, fqld = faq_html(faq)
    rows = [("Grandi imprese (oltre 250 dipendenti)", "31 marzo 2025"), ("Medie imprese (50–250 dipendenti)", "1° ottobre 2025"), ("Micro e piccole imprese", "1° gennaio 2026"), ("Micro e piccole di turismo, ristorazione e pesca", "31 marzo 2026")]
    tab = "".join(f"<tr><td>{e(a)}</td><td><b>{e(b)}</b></td></tr>" for a, b in rows)
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><div class="prose">
<h2>Le scadenze</h2><div class="tbl-w"><table class="tbl"><thead><tr><th>Impresa</th><th>Obbligo dal</th></tr></thead><tbody>{tab}</tbody></table></div>
<p>Le scadenze sono ormai passate per tutti: oggi conta che la polizza sia <b>adeguata</b>.</p>
<h2>Cosa controlliamo</h2><ul class="ticks"><li>Che ci siano tutti e cinque gli eventi richiesti</li><li>Franchigie e scoperti, entro il 15%</li><li>Somme assicurate rispetto al valore reale dei beni (regola proporzionale)</li><li>Beni inclusi ed esclusi: fabbricato, impianti, macchinari, attrezzature</li><li>Limiti di indennizzo e condizioni particolari</li></ul>
<h2>Cosa ricevi</h2><p>Una scheda chiara, da girare al tuo intermediario, con i punti da sistemare. <span class="tbd-chip">PREZZO DA DEFINIRE</span> Fino ad allora ti facciamo un preventivo scritto.</p>
<h2>Domande frequenti</h2>{fq}
{_src([("MIMIT – Polizze per rischi catastrofali", "https://www.mimit.gov.it/it/mercato-e-consumatori/tutela-del-consumatore/assicurazioni/polizze-per-rischi-catastrofali"), ("Legge 30 dicembre 2023, n. 213, art. 1, commi 101-111", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2023-12-30;213")])}
<p class="small muted">Ultimo aggiornamento: {e(SITE["updated"])}. Informazioni generali, non costituiscono consulenza legale o fiscale.</p>
</div><aside class="aside"><div class="card"><h3>Fai controllare la polizza</h3><p class="muted small">Inviaci il PDF della polizza o del preventivo.</p><a class="btn btn-p" style="width:100%" href="/contatti/?motivo=offerta">Richiedi il controllo</a><a class="btn btn-g" style="width:100%;margin-top:6px" href="/aiuto/analisi-polizze/">Altre analisi polizze</a></div></aside></div></section>'''
    page("/polizza-catastrofale/", "Polizza catastrofale imprese: controllo copertura | StimaVeloce",
         "Polizza catastrofale obbligatoria per le imprese: scadenze, cosa deve coprire, franchigia max 15%. Analizziamo la tua polizza e ti diciamo cosa manca.",
         body, ld=[bld, fqld])


def build_offerta():
    head, bld = ph([("/", "Home"), ("", "Controlla l'offerta")], "Ti hanno fatto un'offerta? Controllala gratis",
                   "Prima di firmare, verifica che l'offerta della compagnia copra tutto quello che ti spetta dal punto di vista tecnico.", "Gratis")
    chk = ["Ci sono tutte le parti danneggiate che vedi?", "Ricambi e ore di manodopera sono coerenti con il danno?", "È considerato il fermo del mezzo o il noleggio, se documentati?",
           "Per la casa: sono incluse tutte le lavorazioni, anche quelle nascoste?", "Franchigie e scoperti sono applicati come dice la polizza?", "La firma vale come quietanza a saldo? Leggi bene prima di firmare."]
    li = "".join(f"<li>{e(c)}</li>" for c in chk)
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><div class="prose">
<h2>Sei domande da farti prima di firmare</h2><ul class="ticks">{li}</ul>
<h2>Come funziona il controllo</h2><ol><li>Inserisci l'importo offerto e cosa riguarda</li><li>Lo strumento ti mostra i punti da verificare</li><li>Se qualcosa non torna, puoi chiedere una stima a 30 € o una perizia firmata</li></ol>
<p class="small muted">Il confronto è tecnico: non diamo consulenza legale e non promettiamo importi diversi. Ogni anno i sinistri costano di più per ricambi e manodopera: per questo vale la pena controllare i numeri.</p>
</div><aside class="aside"><div class="card"><h3>Controlla ora</h3><p class="muted small">Gratis, senza registrazione.</p><a class="btn btn-p" style="width:100%" href="{APP}#confronto">Apri il controllo offerta</a><a class="btn btn-g" style="width:100%;margin-top:6px" href="/stima/">Ottieni una stima</a></div></aside></div></section>'''
    page("/offerta/", "Offerta dell'assicurazione: controllala prima di firmare | StimaVeloce",
         "Hai ricevuto un'offerta di risarcimento dalla compagnia? Sei domande da farti prima di firmare e un controllo gratuito online.",
         body, ld=[bld])


# ------------------------------------------------------------------ DIFFERENZIAZIONE (perché noi, sei in tempo, partner)
def build_perche():
    head, bld = ph([("/", "Home"), ("", "Perché StimaVeloce")], "Stime e perizie a prezzo fisso.",
                   "Molti servizi per i sinistri si pagano con una percentuale su quello che ottieni. Le nostre stime e perizie no: paghi un prezzo pubblicato, deciso prima.", "Perché noi")
    rows = [("Come paghi", "Prezzo fisso pubblicato: 30 € la stima, 60 € la perizia", "Spesso una percentuale di quanto ottieni"),
            ("Quando sai quanto spendi", "Prima di iniziare", "Solo alla fine, quando conosci l'importo"),
            ("Chi vede la valutazione", "Tu: ogni voce è spiegata", "Non sempre ti viene mostrata nel dettaglio"),
            ("Strumenti per capire da solo", "Quiz, simulatore animato, calcolatori, controllo offerta: gratis", "Di solito una chiamata o un modulo"),
            ("Dove", "Online, dal telefono, quando vuoi", "Spesso in ufficio, negli orari d'apertura")]
    tr = "".join(f"<tr><td><b>{e(a)}</b></td><td class=\"ok\">{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in rows)
    calc = '''<div class="card" id="risparmio" style="padding:26px"><h2 style="font-size:26px;margin-top:0">Fai il conto con i tuoi numeri</h2>
<p class="muted small">Inserisci l'importo che ti hanno prospettato e la percentuale che ti hanno chiesto. Il calcolo usa solo i tuoi numeri.</p>
<div class="row2"><div class="fld"><label for="rs-imp">Importo del risarcimento (€)</label><input class="in" id="rs-imp" type="number" min="0" step="100" inputmode="numeric" placeholder="es. 5000"></div>
<div class="fld"><label for="rs-pct">Percentuale richiesta (%)</label><input class="in" id="rs-pct" type="number" min="0" max="60" step="1" inputmode="numeric" placeholder="es. 20"></div></div>
<div class="fld"><label for="rs-srv">Nostro servizio</label><select class="in" id="rs-srv"><option value="30">Stima senza firma · 30 €</option><option value="60" selected>Perizia auto/moto · 60 €</option></select></div>
<div class="rs-out" aria-live="polite"></div>
<p class="small muted" style="margin:10px 0 0">Il confronto riguarda solo il costo del servizio tecnico. Non promettiamo un importo di risarcimento: lo decide la compagnia o, se serve, un giudice.</p></div>
<script>(function(){var i=document.getElementById("rs-imp"),p=document.getElementById("rs-pct"),s=document.getElementById("rs-srv"),o=document.querySelector(".rs-out");
function f(n){return n.toLocaleString("it-IT",{minimumFractionDigits:2,maximumFractionDigits:2})+" €";}
function go(){var a=+i.value||0,b=+p.value||0,c=+s.value;if(!a||!b){o.innerHTML="";return;}var perc=a*b/100,d=perc-c;
o.innerHTML='<div class="rs-grid"><div><span>Con la percentuale</span><b>'+f(perc)+'</b></div><div><span>Con StimaVeloce</span><b>'+f(c)+'</b></div><div class="rs-hl"><span>'+(d>0?"Ti restano in più":"Differenza")+'</span><b>'+f(Math.abs(d))+'</b></div></div>';}
[i,p,s].forEach(function(x){x.addEventListener("input",go);});})();</script>'''
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap">
<div class="tbl-w card" style="padding:8px 8px 0"><table class="tbl cmp"><thead><tr><th></th><th>StimaVeloce</th><th>Servizi a percentuale</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="small muted" style="margin-top:10px">Confronto con il modello di compenso a percentuale in generale, non con un'azienda specifica. Le condizioni dei singoli operatori possono essere diverse.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px;margin-top:40px;align-items:start">{calc}
<div class="prose"><h2>I nostri impegni</h2><ul class="ticks"><li>Prezzi pubblicati, uguali per tutti</li><li>Ogni numero della valutazione è spiegato</li><li>Nessuna promessa di risarcimento: solo tecnica, chiara</li><li>Atti legali solo con avvocati, lesioni solo con medici legali</li><li>I tuoi dati restano tuoi: niente vendita a terzi</li></ul><p class="small muted">Se poi scegli di affidarci anche la gestione della pratica, le condizioni ti vengono indicate per iscritto prima di firmare.</p>
<a class="btn btn-p btn-lg" href="/stima/">Scopri quanto vale il tuo danno{ic("arrow-right")}</a></div></div>
</div></section>'''
    css = '<style>.cmp td.ok{color:#0B1B3A;font-weight:600;background:#EEF3FF}.cmp th:nth-child(2){color:#1F5EFF}.rs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}.rs-grid div{background:#F7F8FB;border-radius:16px;padding:14px}.rs-grid span{display:block;font-size:13px;color:#4A5672}.rs-grid b{font-size:20px;color:#0B1B3A}.rs-grid .rs-hl{background:#FFF1E6}.rs-grid .rs-hl b{color:#E8650A}@media(max-width:560px){.rs-grid{grid-template-columns:1fr}}</style>'
    page("/perche-noi/", "Stime e perizie a prezzo fisso, niente percentuali | StimaVeloce",
         "Perizie e stime a prezzo fisso pubblicato, senza percentuali sul tuo risarcimento. Confronta i costi con i tuoi numeri.", body, ld=[bld], extra_head=css)


def build_intempo():
    head, bld = ph([("/", "Home"), ("/strumenti/", "Strumenti"), ("", "Sei ancora in tempo?")], "Sei ancora in tempo per chiedere il risarcimento?",
                   "Molti danni non vengono mai chiesti perché si pensa che sia troppo tardi. Inserisci la data e scopri le scadenze indicative.", "Gratis")
    tool = '''<div class="card" style="padding:26px"><div class="row2"><div class="fld"><label for="it-d">Quando è successo?</label><input class="in" id="it-d" type="date"></div>
<div class="fld"><label for="it-t">Che tipo di danno?</label><select class="in" id="it-t"><option value="rca">Incidente stradale (verso l'assicurazione di chi ha causato il danno)</option><option value="pol">Danno coperto dalla mia polizza (casa, infortuni, kasko…)</option><option value="civ">Danno causato da altri, non stradale (es. infiltrazione dal vicino)</option></select></div></div>
<div class="it-out" aria-live="polite"></div></div>
<script>(function(){var d=document.getElementById("it-d"),t=document.getElementById("it-t"),o=document.querySelector(".it-out");
var R={rca:[2,"Art. 2947, comma 2, Codice civile: i danni da circolazione dei veicoli si prescrivono in due anni. Se il fatto è anche un reato, il termine può essere più lungo."],
pol:[2,"Art. 2952 Codice civile: i diritti che derivano dal contratto di assicurazione si prescrivono in due anni. Ricorda anche l'avviso alla compagnia: entro 3 giorni, se la polizza non dice diversamente (art. 1913)."],
civ:[5,"Art. 2947, comma 1, Codice civile: il risarcimento del danno da fatto illecito si prescrive in cinque anni."]};
function go(){if(!d.value){o.innerHTML="";return;}var s=new Date(d.value+"T12:00:00"),r=R[t.value],e=new Date(s);e.setFullYear(e.getFullYear()+r[0]);
var now=new Date(),left=Math.ceil((e-now)/864e5),fmt=e.toLocaleDateString("it-IT",{day:"numeric",month:"long",year:"numeric"});
var cls=left<0?"late":left<90?"soon":"ok",msg=left<0?"Il termine indicativo è scaduto il "+fmt+". Non arrenderti subito: una richiesta scritta inviata prima può averlo interrotto. Fai verificare il caso.":left<90?"Attenzione: mancano "+left+" giorni. Il termine indicativo scade il "+fmt+".":"Sei in tempo: il termine indicativo scade il "+fmt+" (tra "+left+" giorni).";
o.innerHTML='<div class="it-res '+cls+'"><b>'+msg+'</b><p>'+r[1]+'</p><p class="small">Una richiesta scritta di risarcimento interrompe la prescrizione e il termine riparte da capo (art. 2943 c.c.). Calcolo indicativo: non è consulenza legale.</p></div><div class="sim-add" style="margin-top:12px"><a class="btn btn-p" href="/stima/">Valuta il tuo danno</a><a class="btn btn-g" href="/contatti/?motivo=stima">Fai una domanda</a></div>';}
d.max=new Date().toISOString().slice(0,10);[d,t].forEach(function(x){x.addEventListener("input",go);x.addEventListener("change",go);});})();</script>'''
    body = head + f'''<section class="sec" style="padding-top:36px"><div class="wrap narrow">{tool}
<div class="prose" style="margin-top:32px"><h2>Perché conta</h2><p>Dopo un sinistro si pensa subito alla riparazione e la richiesta di risarcimento resta indietro. I termini però corrono dal giorno del fatto. Una richiesta scritta, anche semplice, li interrompe.</p>
<h2>Fonti</h2><ul class="small"><li>Codice civile, artt. 1913, 2943, 2947, 2952</li></ul></div></div></section>'''
    css = '<style>.it-res{margin-top:16px;border-radius:18px;padding:18px;border:1px solid}.it-res p{margin:8px 0 0}.it-res.ok{background:#EEF8F1;border-color:#BFE3CA}.it-res.soon{background:#FFF4EB;border-color:#FFD5B5}.it-res.late{background:#FDEEF0;border-color:#F4C2CA}</style>'
    page("/sei-in-tempo/", "Prescrizione risarcimento danni: sei ancora in tempo? | StimaVeloce",
         "Calcola subito la scadenza indicativa per chiedere il risarcimento: incidente stradale 2 anni, polizza 2 anni, altri danni 5 anni. Gratis.", body, ld=[bld], extra_head=css)


def build_partner():
    head, bld = ph([("/", "Home"), ("", "Diventa partner")], "Diventa partner di StimaVeloce",
                   "Carrozzerie, amministratori di condominio, soccorso stradale, studi legali: quando un tuo cliente ha un danno, dagli una valutazione tecnica chiara in poche ore di lavoro tuo in meno.", "Partner")
    tipi = ["Carrozzeria o officina", "Amministratore di condominio", "Soccorso stradale", "Studio legale", "Agenzia immobiliare", "Altro"]
    opts = "".join(f"<option>{e(t)}</option>" for t in tipi)
    body = head + f'''<section class="sec" style="padding-top:40px"><div class="wrap layout"><form class="card form" name="partner" method="POST" action="/partner/grazie/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="partner"><p class="sr"><label>Non compilare <input name="bot-field"></label></p>
<h2 style="font-size:28px;margin:0">Richiedi di diventare partner</h2>
<div class="row2"><div class="fld"><label for="pa-n">Nome e cognome</label><input class="in" id="pa-n" name="nome" required autocomplete="name"></div><div class="fld"><label for="pa-a">Attività</label><input class="in" id="pa-a" name="attivita" required autocomplete="organization"></div></div>
<div class="row2"><div class="fld"><label for="pa-e">Email</label><input class="in" id="pa-e" name="email" type="email" required autocomplete="email"></div><div class="fld"><label for="pa-t">Telefono</label><input class="in" id="pa-t" name="telefono" type="tel" autocomplete="tel"></div></div>
<div class="row2"><div class="fld"><label for="pa-k">Tipo di attività</label><select class="in" id="pa-k" name="tipo">{opts}</select></div><div class="fld"><label for="pa-z">Zona</label><input class="in" id="pa-z" name="zona" placeholder="Es. provincia o regione"></div></div>
<label class="chk"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l'<a href="/privacy/">informativa privacy</a> e acconsento a essere ricontattato.</span></label>
<button class="btn btn-p btn-lg" type="submit">Invia la richiesta</button></form>
<aside class="aside"><div class="card"><h3>Cosa ottieni</h3><ul class="ticks small"><li>Un link e un QR code dedicati per i tuoi clienti</li><li>Clienti seguiti fino alla fine, senza lavoro in più per te</li><li>Materiali pronti: locandina, biglietti, testo per WhatsApp</li></ul><p class="small muted">Condizioni della collaborazione: <span class="tbd-chip">[DA DEFINIRE]</span></p></div></aside></div></section>'''
    page("/partner/", "Diventa partner: carrozzerie, amministratori, soccorso | StimaVeloce",
         "Programma partner StimaVeloce per carrozzerie, amministratori di condominio, soccorso stradale e studi legali in tutta Italia.", body, ld=[bld])
    h2, _ = ph([("/", "Home"), ("/partner/", "Partner"), ("", "Richiesta inviata")], "Richiesta inviata", "Grazie: StimaVeloce ti contatterà per definire la collaborazione.")
    page("/partner/grazie/", "Richiesta inviata | StimaVeloce", "Richiesta inviata.", h2, index=False)

if __name__ == "__main__":
    build_home(); build_servizi(); build_casa(); build_strumenti(); build_guide(); build_istituzionali(); build_stima(); build_simulatore(); build_novita(); build_periti(); build_gestione(); build_professionisti(); build_flegrei(); build_catnat(); build_offerta(); build_perche(); build_intempo(); build_partner(); build_seo(); build_search()
