# Ledger Up

A CSEC Principles of Accounts study app (exam: May/June 2028).

- **Main app (works offline):** https://poa.tidyassistant.com. Install it from the browser to the phone's home screen.
- **Coach (needs internet):** https://claude.ai/artifact/EzS165YpcEkoRDhXs5LRMm. The AI tutor runs inside Claude. Points earned there are sent back to the main app with the "Add XP to app" link.

## How it is built

`src/ledger-up.html` is the single source file. It runs in two modes:

| Where it runs | Mode | What it does |
|---|---|---|
| poa.tidyassistant.com (no `window.claude`) | `STANDALONE` | Full app: topics, visuals, quizzes from the built-in bank, game, flashcards, XP/streak/coins/rewards. Coach buttons link to the Claude page. |
| The Claude artifact | `COACH_MODE` | Coach, AI lessons, Paper 02 marking. XP is held as pending and sent to the main app via a signed `#claim-…` link. |

## Updating

1. Edit `src/ledger-up.html`.
2. Run `python3 build.py` (writes `docs/`).
3. Commit and push to `main`. GitHub Pages republishes `docs/` in about a minute.
4. Republish the Coach artifact from the same `src/ledger-up.html` (Claude's Artifact tool, same URL).
