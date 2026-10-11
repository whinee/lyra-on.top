# Orchestration Task Ledger: STATE.md

Last updated: Gate 0B Locked (2026-10-12)
Target branch: `portfolio/oct17`

## Gate 0 Status
- [x] 0A: Reconnaissance -> `docs/RECON.md`
- [x] 0B: Design & Build Contract -> `gate0` tag committed
- [x] Contrast check: WCAG AA verified (`scripts/check_contrast.py`)
- [x] TODO tracker: Verified (`scripts/check_todos.py`)
- [x] Static freeze: Verified into `dist/` (`scripts/freeze.py`)
- [x] Test / task runner: Configured (`justfile`)

---

## Wave 1 Tasks Ledger

| ID | Task | Owner | Branch | Status | Commit | Notes |
|---|---|---|---|---|---|---|
| **W1-HERO-A** | Hero variant A: sticker-sheet / maximalist | worker | `task/w1-hero-a` | todo | - | Owns `templates/sections/hero_a.html`, `stylesheets/hero_a.css` |
| **W1-HERO-B** | Hero variant B: terminal-in-cute (boots/enters) | worker | `task/w1-hero-b` | todo | - | Owns `templates/sections/hero_b.html`, `stylesheets/hero_b.css` |
| **W1-HERO-C** | Hero variant C: shoujo-manga panel layout | worker | `task/w1-hero-c` | todo | - | Owns `templates/sections/hero_c.html`, `stylesheets/hero_c.css` |
| **W1-SIDEKICK** | WhiskerFrame mascot inline SVG + interactive states | worker | `task/w1-sidekick` | todo | - | Owns `templates/partials/whisker.html`, `static/scripts/whisker.js`, `stylesheets/whisker.css` |
| **W1-STORY** | WhiskerFrame story section | worker | `task/w1-story` | todo | - | Owns `templates/sections/story.html`, `stylesheets/story.css` |
| **W1-FOSS** | FOSS slogan banner (loudest element) | worker | `task/w1-foss` | todo | - | Owns `templates/sections/foss.html`, `stylesheets/foss.css` |
| **W1-WINS** | Hackathon wins (CodeKada) | worker | `task/w1-wins` | todo | - | Owns `templates/sections/wins.html`, `stylesheets/wins.css` |
| **W1-HIRE** | Hire-me / contact with clear CTA | worker | `task/w1-hire` | todo | - | Owns `templates/sections/hire.html`, `stylesheets/hire.css` |
| **W1-SLIDES** | Slides section + static SVG QR (`segno`) | worker | `task/w1-slides` | todo | - | Owns `templates/sections/slides.html`, `stylesheets/slides.css`, `scripts/make_qr.py` |
| **W1-FX** | Sparkles, floaters, dividers, scroll-pop (vanilla JS/CSS) | worker | `task/w1-fx` | todo | - | Owns `static/scripts/fx.js`, `stylesheets/fx.css` |
| **W1-META** | Favicon, OG card (1200x630), robots, sitemap | worker | `task/w1-meta` | todo | - | Owns `static/assets/images/meta/*`, head partial via `NEEDS.md` |
| **W1-A11Y** | Playwright test suite (axe, keyboard, responsive) | worker | `task/w1-a11y` | todo | - | Owns `tests/*` |
| **W1-DEPLOY** | Cloudflare Pages static deploy & docs | worker | `task/w1-deploy` | todo | - | Owns `docs/DEPLOY.md`, `wrangler.toml` |
| **W1-LEGACY** | Retire legacy Hielo template assets/styles | worker | `task/w1-legacy` | todo | - | Owns cleanups specified in `docs/RECON.md` |

---

## Wave 2 Integration (Planned)
- W2-COPY: Voice pass over content.yml
- W2-PERF: Asset weight & LCP budget audit (< 300 KB)
- W2-QA: Final Playwright + axe run on frozen dist
