// Avvisi di Stripe: conferma la pratica anche se il cliente chiude la pagina prima di tornare sul sito
import crypto from "node:crypto";
import { json, conferma } from "../lib/pay.mjs";

const secret = () => (globalThis.Netlify ? Netlify.env.get("STRIPE_WEBHOOK_SECRET") : process.env.STRIPE_WEBHOOK_SECRET) || "";

export default async (req) => {
  if (req.method !== "POST") return json({ errore: "Metodo non consentito" }, 405);
  if (!secret()) return json({ errore: "Webhook non configurato" }, 503);
  const body = await req.text();
  const sig = req.headers.get("stripe-signature") || "";
  const parts = Object.fromEntries(sig.split(",").map((x) => x.split("=")).filter((x) => x.length === 2 && x[0] !== "v1"));
  const v1 = sig.split(",").filter((x) => x.startsWith("v1=")).map((x) => x.slice(3));
  const atteso = crypto.createHmac("sha256", secret()).update(parts.t + "." + body).digest("hex");
  const ok = v1.some((v) => v.length === atteso.length && crypto.timingSafeEqual(Buffer.from(v), Buffer.from(atteso)));
  if (!ok || Math.abs(Date.now() / 1000 - Number(parts.t)) > 600) return json({ errore: "Firma non valida" }, 400);
  const ev = JSON.parse(body);
  try {
    if (ev.type === "checkout.session.completed" || ev.type === "checkout.session.async_payment_succeeded") await conferma(ev.data.object);
    return json({ ricevuto: true });
  } catch (e) {
    console.error(e);
    return json({ errore: "Elaborazione non riuscita" }, 500);
  }
};
