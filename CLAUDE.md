# Notes for Claude

- Source of truth: `src/ledger-up.html`. Never edit `docs/` by hand; run `python3 build.py`.
- After changing the source, do BOTH: push to `main` (GitHub Pages serves `docs/` at poa.tidyassistant.com) and republish the Claude artifact https://claude.ai/artifact/EzS165YpcEkoRDhXs5LRMm from the same file (capabilities: sample with images, db, user).
- Keep `CLAIM_KEY`, `APP_URL` and `ONLINE_URL` consistent between the two, or Coach points stop transferring.
- The owner (Sunil, Trinidad) is non-technical; explain any step he must take in plain words.
- DNS for tidyassistant.com is on Cloudflare. `poa` is a CNAME to sunihard-bit.github.io (DNS only, not proxied).
