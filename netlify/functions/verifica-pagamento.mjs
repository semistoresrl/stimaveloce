// GET ?s=<id sessione Stripe>: controlla il pagamento su Stripe e conferma la pratica
import { json, ready, stripe, conferma } from "../lib/pay.mjs";

export default async (req) => {
  if (!ready()) return json({ errore: "Pagamenti non attivi" }, 503);
  const s = new URL(req.url).searchParams.get("s") || "";
  if (!/^cs_(test|live)_[A-Za-z0-9]+$/.test(s)) return json({ errore: "Sessione non valida" }, 400);
  try {
    const session = await stripe("checkout/sessions/" + s, null, "GET");
    if (session.payment_status !== "paid") return json({ pagato: false });
    const dati = await conferma(session);
    return dati ? json({ pagato: true, pratica: dati }) : json({ errore: "Pratica non trovata" }, 404);
  } catch (e) {
    console.error(e);
    return json({ errore: "Verifica non riuscita" }, 502);
  }
};
