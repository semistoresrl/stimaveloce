// POST: crea la pratica in attesa di pagamento e apre il pagamento Stripe. GET: dice se i pagamenti veri sono attivi.
import { LISTINO, json, ready, mode, stripe, sb } from "../lib/pay.mjs";

export default async (req) => {
  if (req.method === "GET") return json({ attivo: ready(), modalita: ready() ? mode() : null });
  if (req.method !== "POST") return json({ errore: "Metodo non consentito" }, 405);
  if (!ready()) return json({ errore: "Pagamenti non ancora attivi" }, 503);
  let b;
  try { b = await req.json(); } catch { return json({ errore: "Richiesta non valida" }, 400); }
  const items = [...new Set((b.servizi || []).filter((k) => LISTINO[k]))];
  const email = String(b.email || "").trim().toLowerCase();
  if (!items.length) return json({ errore: "Nessun servizio selezionato" }, 400);
  if (!/^\S+@\S+\.\S+$/.test(email) || email.length > 200) return json({ errore: "Email non valida" }, 400);
  const dati = b.pratica && typeof b.pratica === "object" ? b.pratica : {};
  const raw = JSON.stringify(dati);
  if (raw.length > 60000) return json({ errore: "Dati della pratica troppo grandi" }, 413);
  const id = /^[A-Za-z0-9-]{4,30}$/.test(dati.id || "") ? dati.id : "SV-" + Date.now().toString(36).toUpperCase();
  Object.assign(dati, { id, email, pagato: false, stato: "attesa_pagamento", pagamenti: [] });
  try {
    const esiste = await sb("pratiche?id=eq." + encodeURIComponent(id) + "&select=id,dati");
    if (esiste.length && esiste[0].dati && esiste[0].dati.pagato) return json({ errore: "Pratica già pagata" }, 409);
    await sb("pratiche?on_conflict=id", { method: "POST", prefer: "resolution=merge-duplicates,return=minimal", body: JSON.stringify({ id, email, stato: "attesa_pagamento", dati }) });
    const origin = new URL(req.url).origin;
    const p = {
      mode: "payment", locale: "it", customer_email: email, client_reference_id: id,
      success_url: origin + "/app/?pagato={CHECKOUT_SESSION_ID}#area", cancel_url: origin + "/app/#checkout",
      "metadata[pratica_id]": id, "metadata[servizi]": items.join(","),
      "payment_intent_data[description]": "StimaVeloce – pratica " + id,
      "payment_intent_data[metadata][pratica_id]": id,
    };
    items.forEach((k, i) => {
      p[`line_items[${i}][quantity]`] = "1";
      p[`line_items[${i}][price_data][currency]`] = "eur";
      p[`line_items[${i}][price_data][unit_amount]`] = String(LISTINO[k].c);
      p[`line_items[${i}][price_data][product_data][name]`] = LISTINO[k].n;
    });
    const s = await stripe("checkout/sessions", p);
    return json({ url: s.url, id });
  } catch (e) {
    console.error(e);
    return json({ errore: "Non è stato possibile avviare il pagamento. Riprova tra poco." }, 502);
  }
};
