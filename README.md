# StimaVeloce

Sito pubblicato su Netlify da questo repository (ramo `main`, cartella principale).

## Struttura
- `tools/` – generatore delle pagine pubbliche. Testi e prezzi si modificano qui:
  - `data_base.py` – contatti, dati societari, **prezzi** e condizioni di pagamento
  - `data_servizi.py` – 15 pagine servizi e 6 ambiti ("In cosa possiamo aiutarti")
  - `data_strumenti.py` – calcolatori (testi, formule, avvertenze)
  - `data_guide.py` – guide; `verificato=False` = pagina non indicizzata finché lo Studio non approva il testo
  - `data_pagine.py` – FAQ, privacy, cookie, condizioni generali
  - Dopo una modifica: `python3 tools/build.py`
- `assets/` – stile (`site.css`), calcolatori (`calc.js`), font Inter e Manrope
- `app/` – percorso guidato, area cliente e gestionale (applicazione dimostrativa: pagamenti simulati)
- `sitemap.xml`, `robots.txt`, `404.html` – generati dallo script

Icone: Lucide (licenza ISC).
