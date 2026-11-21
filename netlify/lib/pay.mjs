// StimaVeloce – logica pagamenti condivisa (Stripe Checkout + Supabase)
export const SUPABASE_URL = "https://byebnunoygoktyegbofv.supabase.co";
// Prezzi decisi dal server: il browser non può cambiarli (centesimi di euro)
export const LISTINO = {
  stima: { n: "Stima senza firma", c: 3000 },
  perizia: { n: "Perizia auto/moto", c: 6000 },
  video: { n: "Video-perizia in diretta", c: 2900 },
};
const env = (k) => (globalThis.Netlify ? Netlify.env.get(k) : process.env[k]) || "";
export const stripeKey = () => env("STRIPE_SECRET_KEY");
const sbKey = () => env("SUPABASE_SERVICE_ROLE_KEY");
export const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export async function stripe(path, params, method = "POST") {
  const body = params ? new URLSearchParams(params).toString() : undefined;
  const r = await fetch("https://api.stripe.com/v1/" + path, {
    method, body, headers: { authorization: "Bearer " + stripeKey(), "content-type": "application/x-www-form-urlencoded" },
  });
  const j = await r.json();
  if (!r.ok) throw new Error((j.error && j.error.message) || "Errore Stripe");
  return j;
}
export async function sb(path, opt = {}) {
  const r = await fetch(SUPABASE_URL + "/rest/v1/" + path, {
    ...opt,
    headers: { apikey: sbKey(), ...(sbKey().startsWith("sb_") ? {} : { authorization: "Bearer " + sbKey() }), "content-type": "application/json", prefer: opt.prefer || "return=representation", ...(opt.headers || {}) },
  });
  const t = await r.text();
  if (!r.ok) throw new Error("Supabase " + r.status + ": " + t.slice(0, 200));
  return t ? JSON.parse(t) : null;
}
export const ready = () => !!stripeKey() && !!sbKey();
export const mode = () => (stripeKey().startsWith("sk_live_") || stripeKey().startsWith("rk_live_") ? "live" : "test");

const oggi = () => new Date().toLocaleDateString("it-IT", { timeZone: "Europe/Rome", day: "2-digit", month: "2-digit", year: "numeric" });

// Segna come pagata la pratica legata alla sessione Stripe (idempotente)
export async function conferma(session) {
  if (session.payment_status !== "paid") return null;
  const id = session.metadata && session.metadata.pratica_id;
  if (!id) return null;
  const rows = await sb("pratiche?id=eq." + encodeURIComponent(id) + "&select=dati,stato");
  if (!rows || !rows.length) return null;
  const d = rows[0].dati || {};
  if (!d.pagato) {
    const items = String(session.metadata.servizi || "").split(",").filter((k) => LISTINO[k]);
    d.pagato = true;
    d.stato = "ricevuta";
    const sconto = Number(session.metadata.sconto_cent || 0);
    d.pagamenti = items.map((k) => ({ d: LISTINO[k].n, v: LISTINO[k].c / 100, at: oggi() }));
    if (sconto) d.pagamenti.push({ d: "Stima già pagata, scalata", v: -sconto / 100, at: oggi() });
    d.notifiche = [{ t: "Pagamento confermato: pratica ricevuta", at: oggi() }].concat(d.notifiche || []);
    d.stripe = { sessione: session.id, modalita: session.livemode ? "live" : "test" };
    await sb("pratiche?id=eq." + encodeURIComponent(id), { method: "PATCH", body: JSON.stringify({ dati: d, stato: "ricevuta" }), prefer: "return=minimal" });
  }
  const sid = session.metadata.stima_id;
  if (sid) {
    const st = await sb("pratiche?id=eq." + encodeURIComponent(sid) + "&select=dati");
    if (st && st.length && st[0].dati && !st[0].dati.scalata) {
      const sd = st[0].dati; sd.scalata = id;
      await sb("pratiche?id=eq." + encodeURIComponent(sid), { method: "PATCH", body: JSON.stringify({ dati: sd }), prefer: "return=minimal" });
    }
  }
  await sb("pagamenti?on_conflict=stripe_session", {
    method: "POST", prefer: "resolution=ignore-duplicates,return=minimal",
    body: JSON.stringify({ pratica_id: id, email: (session.customer_details && session.customer_details.email) || session.customer_email || d.email, servizi: session.metadata.servizi, importo_cent: session.amount_total, stripe_session: session.id, stato: "pagato" }),
  });
  return d;
}
