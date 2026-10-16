# Design & Architecture Contract (Gate 0B)

Single source of truth for file ownership, partial paths, CSS/JS modularity, and content bindings.

## 1. Orchestrator-Owned Files (DO NOT TOUCH)

Workers must NEVER edit these files directly. Any changes required must be requested via `docs/ai/NEEDS.md`:
- `src/api/static/stylesheets/tokens.css`
- `src/api/static/stylesheets/base.css`
- `src/api/templates/base.html`
- `src/api/templates/index.html`
- `src/api/models/content.py`
- `src/api/config/content_loader.py`
- `main.py`
- `pyproject.toml`
- `justfile`
- `scripts/freeze.py`
- `docs/ai/STATE.md`
- `docs/ai/master-context.md`
- `blog/` (completely read-only archive; do not touch)

---

## 2. Disjoint File Ownership Table

| Task ID | Description | Owned Templates / Code | Owned Stylesheet | Owned JS / Assets | Content Keys Read | Boundaries & Rules |
|---|---|---|---|---|---|---|
| **W1-HERO-A** | Hero A: maximalist sticker-sheet | `templates/sections/hero_a.html` | `stylesheets/hero_a.css` | None | `hero.*`, slots | All 10 layers; 360px clean; motion budget passes. |
| **W1-HERO-B** | Hero B: terminal-in-cute | `templates/sections/hero_b.html` | `stylesheets/hero_b.css` | None | `hero.*`, slots | Terminal boot sequence; reduced-motion safe. |
| **W1-HERO-C** | Hero C: shoujo manga panels | `templates/sections/hero_c.html` | `stylesheets/hero_c.css` | None | `hero.*`, slots | Manga panels; strict mobile wrap. |
| **W1-BRAND** | Wordmark, SVG logo, doodles | `templates/partials/brand/*` | None | `static/assets/images/brand/*` | None | Palette-only, scalable, a11y labels, each < 4 KB. |
| **W1-SIDEKICK** | WhiskerFrame mascot SVG | `templates/partials/whisker.html` | `stylesheets/whisker.css` | `static/scripts/whisker.js` | None | 3 states (blink, wiggle, bubble), < 8 KB, a11y label. |
| **W1-CURSOR** | Cat cursor + toggle | None | `stylesheets/cursor.css` | `static/scripts/cursor_toggle.js`, `static/assets/images/cursor/*` | None | Native CSS cursor, 32px/64px PNGs, accessible fallback. |
| **W1-MOTION** | Shared rAF loop, aurora, marquee | None | `stylesheets/fx.css` | `static/scripts/fx.js` | None | Passes `tests/test_perf.py` budget; JS-off clean. |
| **W1-ENGINE-QA** | Content engine tests & fixtures | `tests/test_content.py` | None | None | `content/**` | Tests auto-hide, drafts, bad dates, bad slugs. |
| **W1-PROJECTS** | Projects grid & detail pages | `templates/projects/*` | `stylesheets/projects.css` | None | `projects.yaml` | Featured-first; tag/status filter; no runtime API calls. |
| **W1-WRITING** | Writing hub, poems, song analysis | `templates/writing/*` | `stylesheets/writing.css` | None | `content/poems/*`, `content/song-analysis/*` | Preserved whitespace for poems; short lyric checks. |
| **W1-BLOG** | Blog index & detail, RSS | `templates/blog/*` | `stylesheets/blog.css` | `scripts/import_blog.py` | `content/blog/*` | Style signature intro/outro; never edit text. |
| **W1-RESUME** | Resume & CV (canonical /resume) | `templates/resume/*` | `stylesheets/resume.css` | None | `content/resume.yaml` | Public items only; deadname note verbatim; print CSS. |
| **W1-CONTACTS** | Obfuscated email & Discord | `templates/contacts/*` | `stylesheets/contacts.css` | None | `content/site.yaml` | Works with JS off; no raw email in HTML source. |
| **W1-TALKS** | Talks list & slides QR | `templates/talks/*` | `stylesheets/talks.css` | `scripts/make_qr.py` | `content/talks.yaml` | Scannable SVG QR; no runtime network calls. |
| **W1-STORY** | WhiskerFrame cyberdeck story | `templates/sections/story.html` | `stylesheets/story.css` | None | `whiskerframe.*` | Confirmed facts only; no invented specs. |
| **W1-FOSS** | Loudest FOSS slogan banner | `templates/sections/foss.html` | `stylesheets/foss.css` | None | `foss.*` | Verbatim slogan; contrast pass; readable at 360px. |
| **W1-WINS** | Hackathon wins (CodeKada) | `templates/sections/wins.html` | `stylesheets/wins.css` | None | `wins.*` | Only known fields; no fabricated placement. |
| **W1-NAV** | Nav bar, footer, 404, skip link | `templates/partials/nav.html`, `templates/sections/footer.html`, `templates/404.html` | `stylesheets/nav.css`, `stylesheets/footer.css` | None | `site.yaml` | Keyboard path; auto-hide aware. |
| **W1-META** | OG cards, manifest, robots | `templates/partials/meta.html` | None | `static/assets/images/meta/*`, `static/robots.txt` | `site.yaml` | 1200x630 OG image in palette; plain alt text. |
| **W1-A11Y** | Accessibility test suite | `tests/test_a11y.py` | None | None | None | Axe WCAG 2.1 AA, image-lock, keyboard tabs. |
| **W1-PERFLAB** | Performance & motion budget tests | `tests/test_perf.py` | None | None | None | 4x CPU throttle, long tasks, CLS, fps audit. |
| **W1-DEPLOY** | Cloudflare Pages deployment | `docs/ai/DEPLOY.md`, `wrangler.toml` | None | None | None | Static dist/ export configuration. |
| **W1-WORKER** | Cloudflare Python Worker | `worker/*`, `docs/ai/WORKER.md` | None | None | None | `GET /health` + `GET /api/hello` on `api.lyra-on.top`. |
| **W1-LEGACY** | Clean up unused legacy assets | Specific files named in RECON | None | None | None | Retire old palette CSS; no broken routes. |

---

## 3. General Worker Guidelines

1. **Colors:** Use CSS tokens from `tokens.css` only (`var(--bg)`, `var(--surface)`, `var(--pink)`, `var(--blurple)`, etc.). Never introduce hardcoded hex colors that violate WCAG 2.1 AA contrast matrix.
2. **Typography:** Use font variables `--font-display`, `--font-body`, `--font-mono`.
3. **Motion:** Follow `docs/ai/MOTION.md` strictly. All animations must honor `@media (prefers-reduced-motion: reduce)`.
4. **JS Independence:** All public routes and collections must be 100% readable with JavaScript disabled.
5. **Git Protocol:** Stage ONLY owned files (`git add <file>`). Never run `git add .` or touch untracked files.
