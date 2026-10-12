# Orchestration Task Ledger: STATE.md

Last updated: Gate 0 Extended & Multi-Route Architecture Complete (2026-10-12)
Target branch: `portfolio/oct17`

## Gate 0 Status (Complete)
- [x] Step -1: Relocation -> All agent docs in `docs/ai/`, archived old context (`aa75641`)
- [x] 0A: Reconnaissance -> `docs/ai/RECON.md` updated with `blog/` inventory
- [x] 0B: Design & Build Contract:
  - [x] Image-lock interaction rule in `base.css`
  - [x] Pydantic content models in `src/api/models/content.py`
  - [x] Content directory skeleton with `content/README.md`
  - [x] Unified content loader with human-readable errors in `src/api/config/content_loader.py`
  - [x] Content validation CLI & `just validate` recipe
  - [x] Generic collection router and templates (`/projects`, `/writing`, `/blog`, `/resume`, `/cv`, `/contacts`, `/talks`)
  - [x] Auto-hide rule enforced across nav, router, and static freeze
  - [x] Dynamic freeze pipeline with sitemap and `_redirects` in `scripts/freeze.py`
  - [x] Motion and performance budget invariants in `docs/ai/MOTION.md`
  - [x] Updated architectural contract in `docs/ai/CONTRACT.md`

---

## Task Ledger

| ID | Task | Owner | Branch | Status | Commit | Notes |
|---|---|---|---|---|---|---|
| **W1-HERO-A** | Hero variant A: maximalist sticker-sheet | worker | `task/w1-hero-a` | merged | `5246ff5` | Winner of Hero Race (Score 30/30). |
| **W1-HERO-B** | Hero variant B: terminal-in-cute | worker | `task/w1-hero-b` | closed | `1c57716` | Race evaluated (Score 26.5/30). |
| **W1-HERO-C** | Hero variant C: shoujo-manga panel layout | worker | `task/w1-hero-c` | closed | `baaa269` | Race evaluated (Score 28/30). |
| **W1-BRAND** | Logo system as SVG, wordmark, doodle asset | worker | `task/w1-brand` | complete | `aa75641` | Doodle in static assets; palette SVG wordmark ready. |
| **W1-SIDEKICK** | WhiskerFrame mascot inline SVG | worker | `task/w1-sidekick` | merged | `4f89363` | Inline SVG partial, 3 states, <8KB palette colors. |
| **W1-CURSOR** | Cat cursor + footer toggle | worker | `task/w1-cursor` | in_progress | - | CSS cursor with image-set() + fallbacks. |
| **W1-MOTION** | Aurora backdrop, marquee, floaters | worker | `task/w1-motion` | merged | `4bebbda` | Shared rAF loop, reduced-motion safe. |
| **W1-ENGINE-QA** | Content engine tests & fixtures | worker | `task/w1-engine-qa` | in_progress | - | Fixture tests in `tests/test_content.py`. |
| **W1-PROJECTS** | Projects grid & detail router/template | orchestrator | `portfolio/oct17` | complete | `gate0` | Tag/status filter, featured-first, renders from YAML. |
| **W1-WRITING** | Writing hub, poems, song-analysis | orchestrator | `portfolio/oct17` | complete | `gate0` | Preserved whitespace for poems, lyric length guards. |
| **W1-BLOG** | Blog index, detail, RSS, signature styling | orchestrator | `portfolio/oct17` | complete | `gate0` | Styled intro/outro signatures; draft auto-hide active. |
| **W1-RESUME** | Resume & CV page (canonical /resume) | orchestrator | `portfolio/oct17` | complete | `gate0` | Public-only filter, deadname note verbatim, print CSS. |
| **W1-CONTACTS** | Obfuscated email & Discord | orchestrator | `portfolio/oct17` | complete | `gate0` | Scraper-obfuscated email, noscript fallback, copy tag. |
| **W1-TALKS** | Talks page & slides QR | orchestrator | `portfolio/oct17` | complete | `gate0` | Talks grid, SVG QR code via `segno`. |
| **W1-STORY** | WhiskerFrame story section | worker | `task/w1-story` | merged | `7f21034` | Confirmed facts only; no invented specs. |
| **W1-FOSS** | Loudest FOSS slogan banner | worker | `task/w1-foss` | merged | `c4d79a8` | Verbatim slogan, passes contrast matrix. |
| **W1-WINS** | Hackathon wins (CodeKada) | worker | `task/w1-wins` | merged | `697cbe9` | Known fields only; unknowns marked TODO(lyra). |
| **W1-NAV** | Nav bar, footer, skip link, 404 | orchestrator | `portfolio/oct17` | complete | `gate0` | Auto-hide aware nav, keyboard accessible. |
| **W1-META** | OG cards, manifest, robots | worker | `task/w1-meta` | merged | `b4a4d8d` | 1200x630 card, robots.txt, sitemap.xml. |
| **W1-A11Y** | Playwright test suite (axe, keyboard) | worker | `task/w1-a11y` | merged | `c77135d` | A11y and heading hierarchy tests passing. |
| **W1-PERFLAB** | Performance & motion budget tests | worker | `task/w1-perflab` | in_progress | - | Playwright CPU throttle & CLS tests. |
| **W1-DEPLOY** | Cloudflare Pages deployment | worker | `task/w1-deploy` | merged | `5e4e828` | Static dist/ export configuration. |
| **W1-WORKER** | Cloudflare Python Worker deployment | worker | `task/w1-worker` | scheduled | - | FastAPI on `api.lyra-on.top` (GET /health). |
| **W1-LEGACY** | Clean up unused legacy assets | worker | `task/w1-legacy` | merged | `4bc5cc9` | Retired unused assets; no dead links. |
