#!/usr/bin/env python3
"""Build the offline (PWA) version of Ledger Up from ledger-up.html.

Usage: python3 build.py
Reads src/ledger-up.html and writes the installable offline site to docs/
(served by GitHub Pages at https://poa.tidyassistant.com). The cache version
is a hash of the page, so every build makes phones fetch the new version.
"""
import base64, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "src" / "ledger-up.html").read_text()
OUT = ROOT / "docs"
VERSION = hashlib.sha1(SRC.encode()).hexdigest()[:10]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0A5246">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Ledger Up">
<meta name="description" content="CSEC Principles of Accounts study app">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
TAIL = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}));
}
</script>
</body>
</html>
"""

MANIFEST = {
  "name": "Ledger Up: CSEC Principles of Accounts",
  "short_name": "Ledger Up",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#EEF3F0",
  "theme_color": "#0A5246",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
  ],
}

SW = """const CACHE = "ledgerup-__V__";
const SHELL = ["/", "/manifest.webmanifest", "/icon-192.png", "/icon-512.png", "/apple-touch-icon.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Pages: try the network first so updates arrive, fall back to the saved copy offline.
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put("/", c)); return r; }).catch(() => caches.match("/")));
    return;
  }
  // Fonts and icons: use the saved copy, refresh it in the background.
  if (url.origin === location.origin || /fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname)) {
    e.respondWith(caches.match(req).then(hit => {
      const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); } return r; }).catch(() => hit);
      return hit || net;
    }));
  }
});
""".replace("__V__", VERSION)

page = HEAD + SRC + TAIL
(OUT / "index.html").write_text(page)
(OUT / "sw.js").write_text(SW)
(OUT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, indent=1))

(OUT / "CNAME").write_text("poa.tidyassistant.com\n")
(OUT / ".nojekyll").write_text("")
print("built", VERSION)
