# AVEN Property — Brand Book

Static brand book, served via GitHub Pages (branch `main`, root). Public but unlisted (`noindex`).

- `index.html` — the book (single page, chapter rail)
- `kit/` — the operator kit: tokens, voice rules, outlined logos — consumed by the website build and AI agents
- `assets/fonts/` — self-hosted web fonts (OFL)
- `src/` — editable logo masters + build/publish scripts (`python src/build.py all`, `python src/publish.py`)

Never add `.github/workflows/` (token lacks workflow scope). Relative paths only — the site lives under `/aven-brand/`.
