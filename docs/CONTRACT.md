# Design & Architecture Contract (Gate 0B)

Single source of truth for file ownership, partial paths, CSS/JS modularity, and content bindings.

## 1. Orchestrator-Owned Files (DO NOT TOUCH)

Workers must NEVER edit these files directly. Any changes required must be requested via `NEEDS.md`:
- `src/api/static/stylesheets/tokens.css` (or `stylesheets/tokens.css`)
- `src/api/static/stylesheets/base.css` (or `stylesheets/base.css`)
- `src/api/templates/base.html` (or `templates/base.html`)
- `src/api/templates/index.html` (or `templates/index.html`)
- `src/api/config/values/content.yml`
- `src/api/config/content.py`
- `main.py`
- `pyproject.toml`
- `justfile`
- `STATE.md`
- `blog/` (completely out of scope; do not touch)

---

## 2. Section Contract Table

| Section / Task | Owned Template Partial | Owned Stylesheet | Owned JS Module | Content Keys Read | Boundaries / Prohibitions |
|---|---|---|---|---|---|
| **W1-HERO-A** | `templates/sections/hero_a.html` | `stylesheets/hero_a.css` | None | `hero.*`, `slots.hero_doodle`, `slots.artist_doodle` | Must render clean at 360px & 1280px; must not touch `base.html` or `tokens.css`. |
| **W1-HERO-B** | `templates/sections/hero_b.html` | `stylesheets/hero_b.css` | None | Same as Hero A | Terminal-in-cute aesthetic with boot sequence. Reduced-motion safe. |
| **W1-HERO-C** | `templates/sections/hero_c.html` | `stylesheets/hero_c.css` | None | Same as Hero A | Shoujo manga panel layout. Strict mobile wrap. |
| **W1-SIDEKICK** | `templates/partials/whisker.html` | `stylesheets/whisker.css` | `src/api/static/scripts/whisker.js` | None (mascot component) | Self-contained inline SVG (< 8 KB), palette-only colors, 3 interactive states (idle blink, wiggle, bubble), a11y label. |
| **W1-STORY** | `templates/sections/story.html` | `stylesheets/story.css` | None | `whiskerframe.*` | Read only confirmed facts. No invented hardware specs. |
| **W1-FOSS** | `templates/sections/foss.html` | `stylesheets/foss.css` | None | `foss.*` | Slogan verbatim. Contrast >= 4.5 body, >= 3.0 large. Readable at 360px. |
| **W1-WINS** | `templates/sections/wins.html` | `stylesheets/wins.css` | None | `wins.*` | Render only known fields (`content.wins['items']`). Unknowns remain hidden or graceful. |
| **W1-HIRE** | `templates/sections/hire.html` | `stylesheets/hire.css` | None | `hire.*` | Keyboard accessible; mailto + GitHub link; prominent CTA. |
| **W1-SLIDES** | `templates/sections/slides.html` | `stylesheets/slides.css` | None (`scripts/make_qr.py` build-time) | `slides.*` | Build-time SVG QR generated with `segno`. Scannable on mobile screens. No runtime network calls. |
| **W1-FX** | None | `stylesheets/fx.css` | `src/api/static/scripts/fx.js` | None | Sparkles, floater animations, scroll reveals. Must degrade gracefully with JS off; zero animation when `prefers-reduced-motion` is active. |
| **W1-META** | Head meta partial (submitted via `NEEDS.md`) | None | None | `meta.*` | Creates `src/api/static/assets/images/meta/og-card.png`, favicon, sitemap.xml, robots.txt. |
| **W1-A11Y** | None | None | None | None | Owns `tests/*`. Playwright suite for axe WCAG AA, keyboard tabs, 360/768/1280px layouts, JS-disabled tests. |
| **W1-DEPLOY** | None | None | None | None | Owns `docs/DEPLOY.md`, `wrangler.toml`. Cloudflare Pages configuration. |
| **W1-LEGACY** | Legacy files named in `docs/RECON.md` | None | None | None | Retire old template assets and unused stylesheets. No dead links. |

---

## 3. General Worker Guidelines

1. **Colors:** Use CSS variables from `tokens.css` only (`var(--bg)`, `var(--surface)`, `var(--pink)`, etc.). Never introduce custom hex colors or external CSS frameworks.
2. **Typography:** Use font variables `--font-display`, `--font-body`, `--font-mono`. No external font requests.
3. **Motion:** Every animation must be wrapped inside or respect `@media (prefers-reduced-motion: reduce)`.
4. **JS Independence:** All critical content and links MUST be accessible with JavaScript disabled.
5. **Commits:** Stage only owned files (`git add <file>`). Never run `git add .` or stage files belonging to other tasks.
