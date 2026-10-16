# Task Spec: W1-HERO-C (Hero Variant C: Shoujo-Manga Panel Polish)

## Target & File Ownership
- Owned template partial: `src/api/templates/sections/hero_c.html`
- Owned stylesheet: `src/api/static/stylesheets/hero_c.css`
- DO NOT TOUCH: `hero_a.*`, `hero_b.*`, `base.html`, `tokens.css`, `base.css`, `main.py`, `content.yml`, `site.yaml`.

## Concept & Requirements
- Theme: **Shoujo Manga Panel Layout** (dramatic manga comic panels, screentone dot patterns, speed lines, speech bubbles, sound effects, sparkles).
- Benchmark: Match the visual density, intentionality, and responsiveness of Hero A without copying its sticker-sheet motif.
- Content Keys Read:
  - `content.hero.name`, `content.hero.tagline`, `content.hero.subtag`, `content.hero.pronouns`, `content.hero.kaomoji`
  - `content.hero.cta_slides.href`, `content.hero.cta_slides.label`
  - `content.hero.cta_hire.href`, `content.hero.cta_hire.label`
  - Asset slots: `get_slot('artist_doodle')` / `get_slot('hero_doodle')`
  - Mascot include: `{% include "partials/whisker.html" ignore missing %}`
  - DO NOT use `content.site.*` (not present in Jinja `load_content()` render context and causes UndefinedError).

## Specific Layout & Cascade Fixes
1. **Fix Template Undefined Errors & Missing Elements:**
   - Replace all `content.site.*` references with `content.hero.*`.
   - Include `<link rel="stylesheet" href="/static/stylesheets/hero_c.css">` at top of template.
   - Include the heroine illustration (`get_slot('hero_doodle')`) inside the main manga heroine panel.
   - Include WhiskerFrame mascot (`partials/whisker.html`) in the sidekick panel.
   - Bind CTAs to `content.hero.cta_slides` and `content.hero.cta_hire`.
2. **CSS Token & Brand Compliance:**
   - PURGE all hardcoded `#000`, `#ddd`, `#fff`, `#eee`, `#ffb6c1` and font `'Comic Neue'`.
   - Use tokens ONLY: `var(--bg)`, `var(--surface)`, `var(--raised)`, `var(--blurple)`, `var(--pink)`, `var(--lavender)`, `var(--baby-blue)`, `var(--baby-yellow)`, `var(--hot-pink)`, `var(--cursor-cyan)`.
   - Fonts: `var(--font-display)` for titles & SFX, `var(--font-body)` for bubbles, `var(--font-mono)` for stats/tech lines.
   - Base section background: `var(--bg)` with subtle screentone dot pattern (`radial-gradient(var(--raised) 1.5px, transparent 1.5px)` with background `var(--bg)` or `var(--surface)`).
3. **Manga Panel Architecture:**
   - Panel cards: `background: var(--surface); border: 3px solid var(--pink); box-shadow: 4px 4px 0 var(--hot-pink); border-radius: var(--radius-sm); position: relative; overflow: hidden;`.
   - Speech bubbles: `background: var(--raised); border: 2px solid var(--baby-blue); color: var(--baby-yellow);` with distinct speech bubble pointer tail (`::after`).
   - Sound effect badges (SFX / onomatopoeia): e.g. `<span class="manga-sfx sfx-kira">✧ KIRA KIRA ✧</span>`, angled, dramatic manga styling.
   - Panel 1: Heroine Introduction with doodle, `<h1 id="hero-c-title" class="hero-title">` containing `{{ content.hero.name }}`, and speech bubble with tagline.
   - Panel 2: Sidekick WhiskerFrame cyberdeck with mascot speech bubble ("*purr* cyberdeck ready :3").
   - Panel 3: Character Dossier / Stats card with class, subtag, and FOSS slogan.
   - Panel 4: Dramatic Action CTA panel ("NEXT EPISODE ➡") with Slides and Hire buttons.
4. **Mobile Responsiveness (Strict Mobile Wrap):**
   - At desktop (>= 900px): dynamic asymmetric 2-column manga layout.
   - At mobile (< 900px down to 360px): strict single-column wrap. Panels stack naturally (100% width) with comfortable spacing and padding.
   - NO horizontal overflow at 360px.
   - Support `prefers-reduced-motion`.
