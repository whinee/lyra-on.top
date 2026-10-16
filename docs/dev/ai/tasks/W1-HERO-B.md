# Task Spec: W1-HERO-B (Hero Variant B: Terminal-in-Cute Polish)

## Target & File Ownership
- Owned template partial: `src/api/templates/sections/hero_b.html`
- Owned stylesheet: `src/api/static/stylesheets/hero_b.css`
- DO NOT TOUCH: `hero_a.*`, `hero_c.*`, `base.html`, `tokens.css`, `base.css`, `main.py`, `content.yml`, `site.yaml`.

## Concept & Requirements
- Theme: **Terminal-in-Cute** (retro CRT / cyberdeck terminal aesthetic fused with cute pastels and sparkles).
- Benchmark: Match the visual density, intentionality, and responsiveness of Hero A without copying its sticker-sheet motif.
- Content Keys Read:
  - `content.hero.name`, `content.hero.tagline`, `content.hero.subtag`, `content.hero.pronouns`, `content.hero.kaomoji`
  - `content.hero.cta_slides.href`, `content.hero.cta_slides.label`
  - `content.hero.cta_hire.href`, `content.hero.cta_hire.label`
  - Asset slots: `get_slot('artist_doodle')` / `get_slot('hero_doodle')`
  - Mascot include: `{% include "partials/whisker.html" ignore missing %}`

## Specific Layout & Cascade Fixes
1. **Container & Grid:**
   - Define a responsive 2-column layout on desktop (min-width: 900px) and a clean single-column stacked layout on mobile (360px).
   - Eliminate giant empty dead zones inside and around the terminal window.
2. **Terminal Window Styling:**
   - Use tokens ONLY (`var(--bg)`, `var(--surface)`, `var(--raised)`, `var(--pink)`, `var(--lavender)`, `var(--baby-blue)`, `var(--baby-yellow)`, `var(--hot-pink)`, `var(--cursor-cyan)`). No hardcoded `#1a1a1a`.
   - Titlebar with colored dots (pink, yellow, cyan) and title text `lyra@whiskerframe:~/cyberdeck`.
   - Terminal screen with subtle scanline gradient, monospace font `var(--font-mono)`.
   - Structured terminal output:
     - Prompts (`uwu> whoami`, `uwu> cat /etc/tagline`, `uwu> status`)
     - Headline `<h1 id="hero-b-title" class="hero-title">` displaying `{{ content.hero.name }}` with blinking cursor `_`.
     - Tagline `{{ content.hero.tagline }}` and subtag `{{ content.hero.subtag }}`.
     - Status lines (`[OK] WhiskerFrame co-pilot online :3`, `[OK] Mode: FOSS or bust! ✧`).
3. **Heroine & Mascot Integration:**
   - In the art column (right side on desktop, stacked on mobile), frame the heroine doodle (`hero-doodle-img` from slot system) inside a cyberdeck monitor / CRT frame with tech telemetry borders.
   - Include the WhiskerFrame mascot (`partials/whisker.html`) with a terminal-styled co-pilot dialogue card ("cyberdeck co-pilot: ready to hack weird hardware! :3").
4. **Action Buttons (CTAs):**
   - Style `hero-actions` with terminal-styled buttons: prominent, glowing borders, high contrast, icons `✧` and `♡`.
5. **Responsiveness & A11y:**
   - At 360px, must fit cleanly with no horizontal scroll (`overflow-x: clip` or `break-word`).
   - Honor `prefers-reduced-motion` (disable cursor blinking / scanline animation when reduced motion is preferred).
   - Meet WCAG AA contrast (cyan/yellow/pink text against dark surface >= 4.5:1).
