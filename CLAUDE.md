# Notes for Claude

- Source of truth: `src/ledger-up.html`. Never edit `docs/` by hand; run `python3 build.py`.
- After changing the source, do BOTH: push to `main` (the Cloudflare Worker `ledger-up` proxies raw.githubusercontent.com/sunihard-bit/ledger-up/main/docs at poa.tidyassistant.com; GitHub's raw cache can take ~5 minutes) and republish the Claude artifact https://claude.ai/artifact/EzS165YpcEkoRDhXs5LRMm from the same file (capabilities: sample with images, db, user).
- Keep `CLAIM_KEY`, `APP_URL` and `ONLINE_URL` consistent between the two, or Coach points stop transferring.
- The owner (Sunil, Trinidad) is non-technical; explain any step he must take in plain words.
- DNS for tidyassistant.com is on Cloudflare. poa.tidyassistant.com is a Workers custom domain for the `ledger-up` Worker. The repo must stay public for the Worker to read it.
