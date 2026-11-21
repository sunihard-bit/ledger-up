// Cloudflare Worker "ledger-up" (poa.tidyassistant.com).
// 1) Serves the app from the public GitHub repo's docs/ folder.
// 2) /api/sync/<id>: tiny progress store for the "sync code" feature (D1 database ledger-up-sync, binding DB).
//    <id> is a SHA-256 of the sync code made on the device, so codes themselves are never stored.
// Deploy: upload this file as the module worker.js with a D1 binding named DB (see CLAUDE.md).
const ORIGIN = "https://raw.githubusercontent.com/sunihard-bit/ledger-up/main/docs";
const TYPES = { html: "text/html; charset=utf-8", js: "text/javascript; charset=utf-8", webmanifest: "application/manifest+json", png: "image/png", json: "application/json" };
const MAX = 400000;
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

async function sync(request, env, id) {
  if (!/^[a-f0-9]{64}$/.test(id)) return json({ error: "bad id" }, 400);
  const row = () => env.DB.prepare("SELECT v, data FROM sync WHERE id = ?").bind(id).first();
  if (request.method === "GET") {
    const r = await row();
    return r ? json({ v: r.v, data: r.data }) : json({ v: 0, data: null });
  }
  if (request.method === "PUT") {
    const body = await request.text();
    if (body.length > MAX) return json({ error: "too big" }, 413);
    let b; try { b = JSON.parse(body); } catch (e) { return json({ error: "bad json" }, 400); }
    const ifV = Number(b.ifV) || 0, data = String(b.data || "");
    if (!data || data.length > MAX) return json({ error: "bad data" }, 400);
    const now = Date.now();
    const res = ifV === 0
      ? await env.DB.prepare("INSERT INTO sync (id, v, data, at) VALUES (?, 1, ?, ?) ON CONFLICT(id) DO NOTHING").bind(id, data, now).run()
      : await env.DB.prepare("UPDATE sync SET v = v + 1, data = ?, at = ? WHERE id = ? AND v = ?").bind(data, now, id, ifV).run();
    if (res.meta.changes === 1) return json({ v: ifV + 1 });
    const r = await row();
    return json({ conflict: true, v: r ? r.v : 0, data: r ? r.data : null }, 409);
  }
  return json({ error: "method" }, 405);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/sync/")) {
      try { return await sync(request, env, url.pathname.slice(10)); } catch (e) { return json({ error: "server" }, 500); }
    }
    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405 });
    let path = url.pathname;
    if (path === "/" || !/\.[a-z0-9]+$/i.test(path)) path = "/index.html";
    if (path.includes("..")) return new Response("Not found", { status: 404 });
    const ext = path.split(".").pop().toLowerCase();
    if (!TYPES[ext]) return new Response("Not found", { status: 404 });
    const r = await fetch(ORIGIN + path, { cf: { cacheTtl: 60, cacheEverything: true } });
    if (!r.ok) return new Response("Not found", { status: 404 });
    const img = ext === "png";
    return new Response(r.body, { headers: { "content-type": TYPES[ext], "cache-control": img ? "public, max-age=86400" : "no-cache", "x-content-type-options": "nosniff", "referrer-policy": "strict-origin-when-cross-origin" } });
  }
};
