# Reconnaissance Report (Gate 0A)

Date: 2026-10-12
Branch: portfolio/oct17 (cut from main)

## 1. Git Status & History

- **Current branch:** `portfolio/oct17`
- **Tracked files:** Clean working tree with Step -1 relocation committed.
- **Untracked files:**
  - `assets/` (protected original artwork)
  - `blog/` (protected draft content)
  - `reports/` (local test & visual reports)
  - `.env` (protected environment file - never touched)

## 2. Codebase Architecture & Tree

```
├── main.py                     # Entry point & FastAPI app definition
├── pyproject.toml              # Dependencies & project metadata
├── uv.lock                     # Lockfile (Python 3.13)
├── justfile                    # Task runner (check, test, dev, freeze, preview, deploy)
├── docs/ai/                    # Canonical agent artifact home
│   ├── master-context.md       # New canonical master context
│   ├── orchestrator-prompt.md  # Orchestrator instructions
│   ├── CONTRACT.md             # File ownership matrix
│   ├── RECON.md                # This report
│   ├── STATE.md                # Task ledger
│   ├── archive/                # Historical docs (master-context.old.md, OLD-VS-NEW.md)
│   └── inputs/                 # Original doodle artwork
├── src/
│   ├── api/
│   │   ├── config/             # Environment, settings, and YAML loader
│   │   ├── models/             # Pydantic models (Settings, Content schemas)
│   │   ├── static/             # Static assets mounted at /static/
│   │   │   ├── assets/fonts/   # Self-hosted Fredoka, Nunito, JetBrains Mono
│   │   │   ├── assets/images/  # Doodle art, QR code, meta OG cards
│   │   │   ├── scripts/        # whisker.js, fx.js
│   │   │   └── stylesheets/    # tokens.css, base.css, section styles
│   │   └── templates/          # Jinja2 templates (base.html, index.html, sections)
├── tests/                      # Playwright and pytest accessibility suite
└── dist/                       # Static export target for Cloudflare Pages
```

## 3. Current Functionality & Execution Status

- `uv sync` and `uv run` succeed cleanly.
- `just check` passes 100%:
  - WCAG 2.1 AA contrast matrix verified (`scripts/check_contrast.py`)
  - 0 broken facts, 39 tracked `TODO(lyra)` items (`scripts/check_todos.py`)
  - Ruff lint clean (`ruff check .`)
  - 10 automated test suites passing (`pytest tests`)
  - Static freeze pipeline verifies into `dist/` with zero runtime network calls.

## 4. `blog/` Inventory

- **Entry:** `blog/00015 The World Has Gone Mad, And So HAve I.md`
- **Format:** Markdown without standard YAML frontmatter; contains disclaimer, article heading, signature opening `"Nyahallo! Your favorite kittygirl hacker here :3"`, missing image reference `![](Pasted%20image%2020260211013024.png)`, and draft placeholders `[TODO: citation]`, `[TODO: Bridge]`.
- **Classification:** Needs front matter + draft flag (`draft: true`) + image asset resolution (`TODO(lyra)`).
- **Handling:** Original in `blog/` is strictly read-only. Imported copy created in `content/blog/` with added YAML frontmatter and `draft: true`.

## 5. Area Decisions: Reuse / Refactor / Replace

| Area | Decision | Reason |
|---|---|---|
| `main.py` | **Refactor** | Mount generic collection router for `/projects`, `/writing`, `/blog`, `/resume`, `/cv`, `/contacts`, `/talks`; enforce auto-hide rule when collections are empty; maintain `/code/{code}` status handlers. |
| `src/api/models/` | **Enhance** | Implement Pydantic models: `Site`, `Project`, `Resume` (`visibility: private` default), `Talk`, and shared `Post` model for blog, poems, and song analyses. |
| `src/api/config/content.py` | **Refactor** | Multi-file loader that reads `content/` (`site.yaml`, `projects.yaml`, `resume.yaml`, `talks.yaml`, and Markdown collections), validates with Pydantic, and raises human-readable errors naming file, field, and fix. |
| `content/` | **Create** | Seed placeholder YAML and Markdown files with clear README; auto-hide empty collections in production freeze. |
| `scripts/freeze.py` | **Enhance** | Enumerate all dynamic routes + collection slugs, render `/cv` canonical to `/resume`, generate sitemap and RSS feed. |
| `docs/ai/MOTION.md` | **Create** | Document motion budget rules (reduced-motion static, rAF loop, lite mode) and testable invariants. |
| `docs/ai/CONTRACT.md` | **Update** | Update file ownership and route boundaries for all Wave 1 tasks and content engine models. |
| `docs/ai/STATE.md` | **Update** | Maintain authoritative task ledger for full multi-route build. |

## 6. Deviations & Conflicts

1. **Tagline:** Previous code and templates used `"Software developer, cyberdeck builder, and FOSS advocate! ✧"`. New master context locks tagline to `"neko dev. weird hardware. FOSS or bust."`. All templates, meta tags, and `site.yaml` must use the locked tagline.
2. **Hero Structure:** Wave 1 previously implemented 1-page landing sections. New master context expands hero to full 10 layers with "Heroine + Sidekick" positioning and adds separate pages for projects, writing, resume, contacts, and talks.
3. **Python Worker:** FastAPI Python Worker on `api.lyra-on.top` must be deployed to Cloudflare early for health verification (`GET /health`), separate from the static Pages site.
