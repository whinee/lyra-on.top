# OLD vs NEW Master Context Comparison: docs/ai/archive/OLD-VS-NEW.md

Recorded during Step -1 Relocation (2026-10-12).

## 1. Tagline & Branding
- **Old:** Tagline was `"Software developer, cyberdeck builder, and FOSS advocate! ✧"`.
- **New:** Tagline is **LOCKED by Lyra** to: `"neko dev. weird hardware. FOSS or bust."` (3 beats = cute, hardware-to-software, FOSS). Use verbatim in hero, title, meta, OG card, and `site.yaml`.
- **New additions:**
  - Signature greeting: `"Nyahallo!"`
  - Signature epithet: `"your local kittygirl hacker :3"`
  - Blog opener: `"Nyahallo! Your favorite kittygirl hacker here :3"`
  - Blog closer: `"Paws off the keyboard for now. I'm Lyra: your local kittygirl hacker :3"`
  - Signature motifs: 4-point sparkle, X hairclip, whisker lines, paw prints, hearts, block cursor `▌`, die-cut stickers.

## 2. Content Engine & Scope
- **Old:** Single static landing page (`/`) with section partials (`hero`, `slides`, `story`, `foss`, `wins`, `hire`, `footer`) driven by a single `content.yml`.
- **New:** Full multi-route content engine validated by Pydantic models in `src/api/models/` (`Site`, `Project`, `Resume`, `Talk`, `Post`):
  - Routes: `/`, `/projects`, `/projects/<slug>`, `/writing`, `/writing/poems`, `/writing/song-analysis`, `/blog`, `/resume`, `/cv` (canonical `/resume`), `/contacts`, `/talks`, `/404`.
  - **Auto-hide rule:** Empty collections produce no route and no nav link. Nav is dynamically assembled from populated content.
  - Markdown collections (`content/blog/*.md`, `content/poems/*.md`, `content/song-analysis/*.md`) with Pygments styling and poem whitespace preservation.
  - Song analysis rule: short excerpts only (no full lyrics).
  - Authored text rule: Never edit Lyra's writing; style blog opener/closer only if exact match.

## 3. Infrastructure & Deployment
- **Old:** Static export on Cloudflare Pages (`lyra-on.top`).
- **New:** Two surfaces separated:
  - Surface 1: Static export on Cloudflare Pages (`lyra-on.top`) with `/cv` canonical to `/resume`.
  - Surface 2: Cloudflare Python Worker deployed to `api.lyra-on.top` (`GET /health`, `GET /api/hello`, strict CORS `lyra-on.top`). Not on critical path.

## 4. Interaction & Accessibility
- **New additions:**
  - Cat cursor: 32x32 & 64x64 PNG arrow + paw pointer with "boring cursor" toggle in footer.
  - Image lock: images non-draggable and non-selectable (`user-select: none`, `-webkit-user-drag: none`), while body text remains 100% selectable.

## 5. Privacy & Secrets
- Both versions strictly forbid private files (`~/.config/lyra/*`, NDA, client work).
- Resume `achievements[]`, `education[]` default to `visibility: private`. Only `public` renders.
