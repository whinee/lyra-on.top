# MASTER CONTEXT: lyra-on.top

Public-safe. This is the ONLY personal context agents get for this project.
Do not read, request, or infer anything from private files (`~/.config/lyra/`,
`CONTEXT.md`, `INVENTORY.md`, `agy-context.json`, or any NDA/client material).
If a fact is not in this file or in the content files Lyra supplies, it is unknown.
Do not guess. Mark it `TODO(lyra)`.

## 1. Mission

Build **lyra-on.top**, Lyra's personal site and long-term home on the internet. The first
public milestone is **Sat 17 Oct 2026** (Hack & Yap Episode II, Zero-Ten Park, Makati; Lyra is a speaker).

Jobs, in priority order:

1. **Slides + QR**: people at the talk scan a QR / open a link, land here, reach her slides.
2. **Make Lyra known**: projects, writing, wins, the cyberdeck, the FOSS stance.
3. **Get her hired**: a recruiter finds who she is, what she builds, her resume, and contact info within 10 seconds.
4. **Be a living site**: she keeps adding projects, posts, poems with YAML/Markdown edits only, no code changes.

Audience reality: most first visits are **phones, on venue wifi, right after the talk**.
Mobile-first. Fast. Works with JS off.

## 2. Who Lyra is (approved public facts only)

- Name on the site: **Lyra Phasma** (also "Lyra"). Never use any legal name.
- Software developer. Python is her professional language. Do not list other languages as professional skills unless she states them.
- Student (BSCS, 4th year). Whether to show school/location: governed by `visibility` flags (section 6). Default: hidden.
- Neko (kittygirl) persona. Loves cute things, pastels, sparkles. This is her real personality; the site is allowed to be 100% this.
- Hackathon winner: **won CodeKada: The Online Hackathon by DevKada**. Other details: `TODO(lyra)`.
- Speaker at **Hack & Yap Episode II** (17 Oct 2026).
- Advocacy slogan (verbatim, keep exact casing):
  **"REBEL against corporate greed. REVEL in Free and Open Source Software!"**

### The cyberdeck: WhiskerFrame

- Her custom portable cyberdeck, named **WhiskerFrame**.
- Talk title idea (verbatim, may be used as a tagline):
  "Weird, Improvised Exciting Device (named WhiskerFrame), gets you noticed (a Cyberdeck story)".
- Its terminal theme is the pink/blurple palette this site wears.
- Build details (specs, parts, photos): `TODO(lyra)`. Do not invent specs.

### Candidate story beats (use ONLY after Lyra confirms at the Gate 0 review)

- Showed WhiskerFrame at the AWS Build Over Nights hackathon, which led to a booth role at the AWS User Group PH booth at AWS Builder Day 2026.
- Looks like a bomb at a glance (the "gets you noticed" joke).

### NOT on the site, ever

any startup or business venture and its co-founders, any client or NDA work, homelab hosts/IPs/domains besides lyra-on.top,
family/partner info, school/enrollment plans, legal name, home address, phone number,
anything not in Lyra's supplied content. Private repos never appear in the projects list.

## 3. Brand

Lyra says she doesn't know branding. This section **is** the brand. Follow it so every page feels like one person.

**Positioning (one sentence):** a kittygirl developer who builds weird hardware and real software, fights for FOSS, and is about to be on top. (`lyra-on.top`.)

**Archetype:** *the Heroine and her sidekick.* Lyra is the Heroine. WhiskerFrame (the cyberdeck) is the sidekick.

**Four pillars:**
1. **Cute, never childish.** Sparkly and bold, but the work underneath is serious.
2. **Weird hardware, real software.** The cyberdeck proves she ships physical and digital things.
3. **Rebel + Revel.** FOSS is a stance, stated loudly and joyfully.
4. **Honest.** Cute wrapper, literally true claims.

**Brand words:** bright, bold, sparkly, honest. (Not: sleek, enterprise, minimal, synergy.)

**Tagline (locked by Lyra): "neko dev. weird hardware. FOSS or bust."**
Three beats = three pillars (cute, hardware-to-software, FOSS). Use it verbatim in the hero, `<title>`/meta description, OG card, and `site.yaml`. Do not remix it. Alternates that may appear as small section captions only: "cute chaos, real engineering :3", "she builds weird things. her cyberdeck helps."

**Signature phrases (Lyra's own; reuse as brand catchphrases):**
- Greeting: **"Nyahallo!"** (hero speech bubble and first terminal line, 404 page, blog opener)
- Epithet: **"your local kittygirl hacker :3"** (about blurb, footer, sign-offs)
- Blog opener (her drafts): "Nyahallo! Your favorite kittygirl hacker here :3"
- Blog closer (her drafts): "Paws off the keyboard for now. I'm Lyra: your local kittygirl hacker :3"
Note: "hacker" is brand voice. Resume and recruiter-facing headlines stay "software developer".

**Signature motifs (use everywhere, consistently):**
- the **4-point sparkle** from the doodle (this is the brand's star; also the favicon)
- the **X hairclip** from the doodle (recurring glyph: bullets, dividers, 404, logo mark)
- **whisker lines**, **paw prints**, **hearts**
- the **block cursor** `▌` (terminal side of the brand)
- **die-cut stickers** with thick outlines and hard offset shadows

**Logo system (agents build as SVG):**
- Primary wordmark: `LYRA PHASMA` in the rounded display font with a sticker shadow, the dot or a letter replaced by a sparkle.
- URL wordmark: `lyra-on.top` with the sparkle as a divider.
- Monogram: a circular pink sticker with the X hairclip and a cat ear. Used as avatar and favicon alternate.
- Favicon: pink 4-point sparkle on blurple. Same emoji/glyph forever.

**Two voices (a deliberate contrast):**
- **Lyra:** excited, urgent, friendly, `!!` energy. Site copy.
- **WhiskerFrame:** deadpan terminal lowercase, `uwu>` prompts, `[ok]` status lines, dry one-liners ("[ok] lyra is on top"). Used in the sidekick's speech bubbles and terminal strips.

**Sticker badges (hero/section decoration; text must be true):** "CodeKada winner", "FOSS or bust", "neko dev", "speaker @ Hack & Yap", "cyberdeck builder".

## 4. Visual system (non-negotiable)

Theme: **blurple world, pastel foreground.** Cute level 10/10. Colorful, popping, lively, **dense, not sparse.**
Banned: corporate startup look, gray cards, stock gradients, hero-with-three-feature-icons, soulless sans-serif minimalism, template feel, big empty areas.

### Palette tokens (Lyra's current revision; ratios computed against each surface)

Foreground love order: **light pink > lavender > baby blue > baby yellow.**
Use them in that proportion (pink most, yellow least, as a sparkle accent).
These are Lyra's own values. Do not "tune" them. If a pair fails, change the pairing, not the color.

```css
:root {
  /* surfaces (blurple world) */
  --bg:        #191a28; /* base page */
  --surface:   #232540; /* cards */
  --raised:    #2f3257; /* hover / stickers */
  --blurple:   #3b3fa8; /* big color blocks */
  --blurple-hi:#5b5fe0; /* DECORATION + white text only */

  /* foreground */
  --pink:      #fd7da6; /* primary text and headlines */
  --lavender:  #ae89ff; /* secondary text */
  --baby-blue: #75beff; /* links, tags */
  --baby-yellow:#fff3a8;/* sparkles, highlights */

  /* accents from the palette */
  --hot-pink:  #ff6dd6;
  --periwinkle:#8c9aff;
  --cursor-cyan:#29dbff;/* blinking cursor, focus rings */
}
```

Contrast matrix (WCAG ratio, verified by script on 2026-10-12). Body text needs >= 4.5, large text/UI >= 3.

| foreground \ background | --bg | --surface | --raised | --blurple | --blurple-hi |
|---|---|---|---|---|---|
| pink #fd7da6 | 7.10 | 6.14 | 5.05 | **3.52** | **2.08** |
| lavender #ae89ff | 6.41 | 5.55 | **4.56 (barely)** | **3.18** | **1.88** |
| baby-blue #75beff | 8.66 | 7.49 | 6.16 | **4.29** | **2.54** |
| baby-yellow #fff3a8 | 15.28 | 13.22 | 10.87 | 7.57 | **4.48** |
| hot-pink #ff6dd6 | 6.90 | 5.96 | 4.90 | **3.42** | **2.02** |
| periwinkle #8c9aff | 6.71 | 5.80 | 4.77 | **3.32** | **1.97** |
| cursor-cyan #29dbff | 10.39 | 8.99 | 7.39 | 5.15 | **3.05** |
| white #ffffff | 17.22 | 14.89 | 12.25 | 8.53 | 5.05 |

Bold = fails body-text AA on that surface.

### Contrast rules (enforced by a build-time script, see orchestrator prompt)

- Text on `--bg`, `--surface`, `--raised`: any of pink, lavender, baby-blue, baby-yellow, hot-pink, periwinkle, cyan, white is fine. **Lavender on `--raised` is only 4.56:1, so no opacity, no thin weights, no text smaller than 16px there.**
- Text on `--blurple` (#3b3fa8): **only white, baby-yellow, or cursor-cyan.** Pink, lavender, baby-blue, hot-pink, periwinkle all FAIL there. Large text (>=24px or >=19px bold) in baby-blue (4.29) is allowed.
- Text on `--blurple-hi` (#5b5fe0): **white only.** Everything else fails. Pastels there are decoration, never text.
- Never put yellow or blue text on pink backgrounds. Never put pastel text on pastel backgrounds.
- Pop comes from **decoration** (stickers, gradients, borders, shadows, shapes, motion), not from low-contrast text.
- Color is never the only carrier of meaning. Focus ring: 3px `--cursor-cyan`, visible everywhere. Cyan on `--blurple-hi` is only 3.05, so give focus rings on that surface a white inner outline.

### Style language (steal from: sticker sheets, shoujo manga, Y2K web, Tamagotchi UIs, retro terminals)

- Sticker aesthetic: thick rounded borders, hard offset shadows in pink/blue (`box-shadow: 6px 6px 0 var(--hot-pink)`), rotations of -3 to 3 degrees.
- Gradients: pink -> lavender -> baby blue as ribbons, dividers, headline fills (keep a solid-color fallback for contrast).
- Sparkles, hearts, paw prints, dotted grids, checkerboards, scalloped edges, pixel stars, marquee tickers.
- Terminal-in-cute: WhiskerFrame sections use a mono "terminal window" card with a blinking cyan cursor and `uwu> ` prompts.
- Fonts: rounded display (e.g. Fredoka or M PLUS Rounded 1c) + friendly body (Nunito) + mono for terminal bits (JetBrains Mono or DotGothic16). **Self-host** woff2 (Latin subset) in `src/api/static/assets/fonts/`; no external font requests; always include fallbacks.
- Performance budget: first load **< 300 KB** transferred (excluding lazy-loaded below-fold images), LCP < 2.5 s on throttled 4G. No WebGL, no heavy libs, no JS frameworks. Images WebP/AVIF/SVG.

### Hero brief: the hero is where the brand lives. It must feel like a stage.

Dense and layered, back to front:
1. **Backdrop:** slowly drifting blurple aurora (large radial gradients on a pseudo-element animated with `transform` only), dotted grid or star field.
2. **Floaters:** 12 to 24 sparkles / hearts / paw prints drifting and twinkling.
3. **Wordmark:** huge `LYRA PHASMA` with sticker shadow; per-letter hover wiggle; the tagline underneath.
4. **Heroine:** the doodle, centered large, soft glow, gentle idle bob.
5. **Sidekick:** WhiskerFrame bottom corner, blinking, with cycling speech bubbles in its deadpan voice.
6. **Terminal strip:** typed-out `uwu> whoami` / `uwu> ls wins` lines (CSS `steps()` typing).
7. **Stickers:** 3 to 5 rotated badges from the badge list, slightly overlapping the doodle.
8. **Ticker:** a marquee strip carrying the FOSS slogan.
9. **CTAs:** "Slides", "Projects", "Hire me" as big chunky sticker buttons, plus a playful "pet the cyberdeck" button.
10. Scroll cue (bobbing paw or sparkle).

Every section below the hero keeps the same density: decoration, stickers, dividers, a little motion. Empty background is a defect.

### Motion budget (animate a lot, never lag)

- Animate **only `transform` and `opacity`.** Never animate `box-shadow`, `filter: blur`, `width/height/top/left`, or big gradients directly. Move gradient pseudo-elements with `transform` instead.
- At most **one** `requestAnimationFrame` loop on the whole page (shared by all JS effects). Everything else is CSS animation.
- Pause offscreen motion with `IntersectionObserver` + `animation-play-state: paused`. Use `content-visibility: auto` on below-fold sections.
- Cap concurrent animated elements (~24 in view). Use `will-change: transform` only on persistent movers, never globally.
- **Lite mode:** if `navigator.hardwareConcurrency <= 4`, `navigator.deviceMemory <= 4`, or `prefers-reduced-data`, halve floaters and drop the aurora drift. If `prefers-reduced-motion: reduce`: static, no loops, no typing animation (show final text).
- Verification (automated, Playwright): with 4x CPU throttling, hero shows no long tasks > 50 ms after load, CLS < 0.05, and measured frame rate stays >= 50 fps. Failing this fails the build.

### Interaction rules

**1. Images are not selectable.** Visitors should not highlight or drag images like text.
- Apply to `img, svg, picture, canvas, video, .sticker, .doodle`: `user-select: none; -webkit-user-select: none; -webkit-user-drag: none; -webkit-touch-callout: none;`, plus `draggable="false"` on `<img>`.
- If an image sits inside a link or button, make the **wrapper** the interactive element; use `pointer-events: none` on the image only when it does not need its own hover.
- **Never** `user-select: none` on `body` or text containers. Text stays selectable, copyable, and screen-reader readable. All images keep real `alt` text (decorative ones `alt=""`).
- This is cosmetic polish, not copy protection. Do not claim otherwise.

**2. Cat cursor, done natively.** No JS cursor follower, no `cursor: none`.
- Use CSS `cursor: url(...) x y, auto`, so the browser draws it: zero lag, works over everything, respects OS pointer behavior.
- Wrap in `@media (hover: hover) and (pointer: fine)`. Touch devices get nothing (they have no cursor).
- States: **default** = cat-ear arrow (pink, navy outline, white edge highlight); **pointer** (links/buttons) = paw; **text** inputs keep the **native I-beam**; disabled/not-allowed stay native.
- Assets: PNG 32x32 with `image-set()` 2x variant (64x64), hotspot on the arrow tip (the left ear tip). Always give a keyword fallback (`auto`, `pointer`).
- Must stay visible on `--bg`, `--blurple`, `--blurple-hi`, and pastel stickers (dark outline + light highlight edge). Test all.
- Footer toggle "boring cursor" (persists via guarded localStorage) turns it off. Reason: cursor visibility is an accessibility need for some people.

### Accessibility floor

Keyboard path through every page, 3px cyan focus ring, skip link, semantic landmarks, `lang`, alt text, `prefers-reduced-motion` honored, 4.5:1 contrast rules above, content readable and navigable with JS disabled.

## 5. Voice (all UI copy and page chrome)

Cutesy, uwu, super urgent, super friendly. Hype energy, like a friend pulling you by the sleeve to see something cool.

- First person as Lyra, direct address to the visitor.
- Kaomoji and `:3` are on-brand (small set: `:3`, `>w<`, `(=^･ω･^=)`, `✧`, `♡`). At most 1-2 per section.
- Short sentences, exclamation points, "wait wait wait look at this!!".
- Playful about herself, **precise about facts.** Never inflate what she built, won, or did.
- English only unless Lyra writes otherwise. Agents do not invent Tagalog.
- Alt text and ARIA labels are plain and descriptive (not uwu).
- UI copy has no profanity. **Lyra's own writing (blog, poems, song analyses) is hers verbatim, profanity included. Agents NEVER edit, polish, rewrite, voice-pass, or "improve" authored writing.** Only the chrome around it gets the cute voice.
- Microcopy: loading = "WhiskerFrame is booting >w<", 404 = "this page ran away :3", button = "pet the cyberdeck".

## 6. Site map and content system

### Principle: the engine is generic, the content is Lyra's

Everything visible is data in `content/`, validated by **Pydantic models** in `src/api/models/`. Lyra edits YAML/Markdown; templates never hard-code her facts. Invalid content **fails the build** with a human-readable error naming the file, field, and fix (`just validate`).

**Auto-hide rule:** a route ships and appears in the nav only if its content exists. Empty collection = no nav link, no page. A page with no content is worse than no page. The engine for every collection is built now; Lyra's content decides what is live.

### Routes

| Route | What | Source |
|---|---|---|
| `/` | Hero + highlights (slides, wins, cyberdeck, FOSS banner, latest writing, hire CTA) | `site.yaml` + others |
| `/projects` | All projects: filterable by tag/status, featured first | `content/projects.yaml` |
| `/projects/<slug>` | Optional detail/case-study page, only for entries that provide `body` | `content/projects/<slug>.md` |
| `/writing` | Hub: cards for each collection with latest items | derived |
| `/writing/poems` + `/writing/poems/<slug>` | Her poems, verbatim | `content/poems/*.md` |
| `/writing/song-analysis` + `/<slug>` | Her song analyses | `content/song-analysis/*.md` |
| `/blog` + `/blog/<slug>` + `/blog/rss.xml` | Blog | `content/blog/*.md` |
| `/resume` and `/cv` | **Same page.** Canonical = `/resume`. Public-safe achievements + "email me" note | `content/resume.yaml` |
| `/contacts` | GitHub, email, Discord (+ others she adds) | `site.yaml` |
| `/talks` | Speaking: Hack & Yap slides, QR | `content/talks.yaml` (auto-hide if empty) |
| `/404` | Cute 404 | static |

Optional later (engine-ready, content-gated): `/now`, `/uses` (dev setup only, never infra details), `/colophon` (how the site is built, privacy statement).

### Content model (Pydantic; sketch, orchestrator finalizes at Gate 0)

`site.yaml`: `title`, `tagline` ("neko dev. weird hardware. FOSS or bust."), `blog.signature_intro`, `blog.signature_outro`, `description`, `url`, `author_display_name` ("Lyra Phasma"), `nav` (auto-built; overridable order), `socials[]` (`kind`, `label`, `url` or `handle`, `visibility`), `email` (address + `obfuscate: true`), `availability` (optional line), `features` (toggles: `cat_cursor`, `lite_motion`...).

`projects.yaml` -> `projects[]`: `slug`, `title`, `summary` (<= 200 chars, Lyra's words), `repo_url`, `homepage_url?`, `tags[]`, `language?`, `status` (`active|maintained|archived|idea`), `featured` (bool), `year?`, `highlights[]?` (outcome bullets), `body?` (path to md for a detail page), `visibility` (`public` default only after Lyra marks it).
- Public GitHub repos only. Build-time check that `repo_url` is a well-formed GitHub URL; optional online link-check job that warns, never blocks. **No runtime GitHub API calls.** Stars/language may be fetched at freeze time into a cache file only if it needs no token; otherwise omit.
- `summary` and `highlights` are Lyra's. Agents may flag a weak or missing summary but never invent one.

`resume.yaml`: `headline`, `summary`, `achievements[]` (`title`, `year?`, `detail?`, `link?`, **`visibility: public|private`, default `private`**), `skills[]` (only what Lyra states), `speaking[]`, `education[]` (default private), `cta` text. Only `visibility: public` items render. This is a structural privacy guard.
- Email-me note (voice, keep her wording): "if u want my personal CV with my dead/government name in it, just email me here, and ask for it. we can talk more there as well :3"
- Print stylesheet so `/resume` prints cleanly. PDF download is a stretch (Lyra writes formal docs in LaTeX; a LaTeX-built PDF of the same public data is the ideal, but never at the cost of the deadline).

Markdown collections (`blog`, `poems`, `song-analysis`, `projects/*.md`): front matter `title`, `date`, `updated?`, `summary`, `tags[]`, `draft` (default false; drafts never freeze), `cover?` (+ alt text, required if present). Body is Markdown.
- Rendering: `markdown-it-py` (HTML passthrough OFF) + `pygments` highlighting restyled to the palette (contrast-checked). Poems render with preserved line breaks/whitespace. Reading time, prev/next, tag filtering, RSS for `/blog`.
- **Song analysis rule:** short excerpts only (a line or two at a time, always with analysis). Never full lyrics. Agents flag any file that contains a long lyric block and do not publish it.
- **Blog signature (style, never rewrite):** Lyra's posts already open and close with her greeting/sign-off (lines above). Those lines live **in the markdown, verbatim, and agents never touch them.** The engine only *styles* them: `site.yaml` holds `blog.signature_intro` and `blog.signature_outro` strings; if a post's first/last paragraph exactly matches, render it as a decorated block (greeting bubble with the sidekick; sign-off with paw + sparkle). No match = render normally. **Never inject or duplicate the text.** If a post lacks them, that is her choice.
- Existing `blog/` prototype: recon inventories it; originals stay read-only; usable entries are **copied** into `content/blog/`. Anything that does not parse becomes a `TODO(lyra)` entry, never silently dropped or "fixed".

Contacts rules: GitHub link; email via a dedicated public alias (e.g. `hi@lyra-on.top`, Cloudflare Email Routing forwarding to her real inbox, so her actual inbox and name are not exposed); Discord shown as a copyable handle (no invite links). Obfuscate the address against scrapers (assembled by tiny JS, `<noscript>` shows "name [at] domain"). Other socials only if Lyra adds them.

Slides/QR: `content/talks.yaml` holds the slides URL; the QR is generated at freeze time (`segno`) and shown on `/talks` and in the hero Slides sticker.

### Priority tiers (what must be live by Wed 14 Oct 18:00)

- **P0 (non-negotiable):** `/`, `/projects` (with Lyra's entries), `/resume` + `/cv`, `/contacts`, slides link/QR, cat cursor, image-lock, dense animated hero, passing checks.
- **P1 (live if content arrives by the content-drop deadline):** `/blog`, `/writing`, `/writing/poems`, `/writing/song-analysis`, `/talks`.
- **P2 (after production is live):** project case-study pages, `/now`, `/uses`, `/colophon`, tag pages, LaTeX PDF resume, Worker extras, and the delight set:
  - `/whiskerframe`: a tiny fake terminal in the page (vanilla JS, keyboard accessible, JS-off fallback = static transcript). Commands: `help`, `whoami`, `ls wins`, `cat slogan`, `projects`, `hire`. `hire` prints the contact info and `/resume` link. Recruiter-friendly and on-brand.
  - Per-post OG images generated at freeze time (Pillow, palette, title + sparkle) so every shared link looks cute.
  - A DevTools console greeting for curious devs ("nyahallo, fellow nerd. yes i wrote this. hire me -> /contacts"), an ASCII-cat comment in the HTML source, and `humans.txt`.
  - Konami-code cat parade (reduced-motion safe, one-shot, no loop).
  - Footer "stats for nerds": page weight, "no cookies, no trackers", build hash and frozen-at timestamp. Only claim "no trackers" while true.

## 7. Stack and deploy

**Existing repo:** `41 Software Projects/41.28 lyra-on.top` (branch `main`), FastAPI + server-rendered pages:

```
blog/  docs/ai/  src/api/{config/values, middlewares, models, routers,
static/{assets/{fonts,images/landing page}, scripts, stylesheets}, templates}  src/pages/
```

- Baseline to build on, not scripture. This file's design contract overrides older visual decisions. Recon first, reuse what fits, record every deviation.
- It has untracked work. Never delete, overwrite, stash, reset, or `git add .` over it. Stage specific files.
- `blog/`: read-only source for importing entries (section 6).
- `docs/ai/` is the **canonical home of every document made by or for AI agents** (this file, the orchestrator prompt, state, specs, reports; see "Artifact home" in section 8). Anything already in it that is not part of the kit is pre-existing: leave it in place and list it.

**Stack (Lyra's decision): FastAPI + Jinja2 + plain CSS + minimal vanilla JS.**
- **No Svelte, React, frontend framework, Tailwind, or Node build step.** Hand-written CSS from the tokens; ES-module vanilla JS only for interaction (sparkles, reveals, mascot, typing, copy-to-clipboard, cursor toggle).
- Python 3.13, `uv`, `just`, Pydantic, PyYAML (or `ruamel.yaml`), `markdown-it-py`, `pygments`, `segno`, Playwright for Python.
- Pages are Jinja templates with shared partials. Templates JS-optional.

**Deploy: two surfaces, separated on purpose.**
1. **Production face = static export on Cloudflare Pages** (`lyra-on.top`). `scripts/freeze.py` renders every public route (including every collection slug, `/cv`, RSS, sitemap, 404) via FastAPI's test client into `dist/`, copies `static/`. One source of truth, zero cold starts, works on venue wifi. `/cv` is served as the same page (Pages `_redirects` rewrite or a duplicate render with `rel=canonical` to `/resume`).
2. **FastAPI backend = Cloudflare Python Worker** at `api.lyra-on.top`. **Deploy it TODAY** as a `GET /health` + `GET /api/hello` skeleton so the pipeline is proven early. It is NOT on the critical path: the site must work identically with the Worker down, and no page may require it.
   - Worker extras (cute and optional, later): a "pet the cyberdeck" counter. Needs storage; **Workers KV or D1 is far simpler than Postgres + Alembic** for a counter. Postgres via Hyperdrive stays available if a real relational need appears (Alembic runs from local/CI, never inside the Worker). Verify current Cloudflare docs before choosing; Python Workers went GA in Sept 2026 and the details moved recently.
   - No user-submitted content (guestbook, forms) without rate limiting and moderation. Not before Oct 17.
3. Email: Cloudflare Email Routing for the public alias (manual dashboard step; document it in `docs/ai/DEPLOY.md`).

## 8. Working rules for every agent

**Artifact home: `docs/ai/`.** Every document made by or for AI agents lives there. Code, tests, scripts, content, and site assets stay in their normal places.

```
docs/ai/
  README.md              index (orchestrator maintains)
  master-context.md      THIS file; the only canonical copy
  orchestrator-prompt.md
  STATE.md  NEEDS.md  RECON.md  CONTRACT.md  MOTION.md  DEPLOY.md  WORKER.md
  tasks/<ID>.md          one self-contained spec per task
  issues/  reports/      QA findings, perf numbers, screenshots
  inputs/                source art + palette (doodle, piiiiink-a11y.json); site copies go to static/
  archive/               superseded files (e.g. the previous master-context)
```

Rules: one canonical copy of each doc (move, never duplicate). Agents read context only from `docs/ai/`. A new agent-facing artifact goes here, not in the repo root.


1. Facts: only from this file and Lyra's content files. Unknown means `TODO(lyra)`. Never fabricate achievements, specs, dates, names, links, projects, or posts.
2. Never edit Lyra's authored writing (section 5).
3. Never commit secrets. `.env.example` only.
4. Stay inside your task's owned files. Orchestrator-owned: `stylesheets/tokens.css`, `stylesheets/base.css`, `templates/base.html`, the Pydantic models, `content/` schema files, the app factory/`main.py`, `pyproject.toml`, `justfile`, `scripts/freeze.py`.
5. Commit messages and code comments: plain and professional. UI copy: cute voice.
6. Every task ends with: `just check` green (lint, validate, tests, contrast, freeze), no console errors, a note in `docs/ai/STATE.md`.
7. Stage specific files, never `git add .`. Do not touch untracked files or anything outside your task. Destructive actions need Lyra's approval.
8. If blocked twice on the same problem, stop and write the blocker to `docs/ai/NEEDS.md` instead of looping.

## 9. `TODO(lyra)` register (Lyra supplies; agents never invent)

- **Content drop (deadline Tue 13 Oct 22:00):** blog entries (or confirm the ones in `blog/`), poems, song analyses, projects list (title, repo, one-line summary, tags), resume achievements marked public/private
- Tagline pick (section 3)
- Slides URL; whether the QR points to slides or to this site
- Public email alias; GitHub handle; Discord handle; availability line (and any other social she wants)
- CodeKada details (year, project, team/solo, placement wording)
- Artist credit name and link (second doodle coming)
- WhiskerFrame specs, photos, confirmed story beats from section 2
- Confirm: static export on Pages is the Oct 17 production path; Worker is parallel, not critical
- Confirm: profanity allowed only inside her own authored writing