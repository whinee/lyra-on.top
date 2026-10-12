# Reconnaissance Report (Gate 0A)

Date: 2026-10-12
Branch: portfolio/oct17 (cut from main)

## 1. Git Status & History

- **Current branch:** `portfolio/oct17` (branched from `main` at `2b10c4d`)
- **Recent commits:**
  - `2b10c4d a :3` (Refactored config loader, added alltheutils, renamed constants)
  - `a065f63 a` (Initial commit)
- **Tracked modified/deleted files on main:**
  - `modified: .github/workflows/deploy.yml`
  - `deleted: docs/README.md`
  - `modified: main.py`
  - `modified: src/api/config/values/strings.yml`
  - `modified: src/api/templates/base.j2.html`
  - `deleted: src/pages/elements.html`
  - `deleted: src/pages/generic.html`
  - `modified: src/pages/index.html`
- **Untracked files (names only):**
  - `assets/` (contains Lyra doodle images)
  - `blog/` (draft content)
  - `docs/ai/` (master context documentation)
  - `src/api/static/stylesheets/index.css` (small utility CSS)
  - `.env` (local environment secrets - protected, unread)

## 2. Codebase Architecture & Tree

```
├── main.py                     # Entry point & FastAPI app definition
├── pyproject.toml              # Dependencies & project metadata
├── uv.lock                     # Lockfile (Python 3.10-3.13)
├── justfile                    # Task runner (dev, run, bootstrap, lint)
├── src/
│   ├── api/
│   │   ├── config/             # Environment & YAML loader
│   │   │   ├── constants.py
│   │   │   ├── env.py
│   │   │   ├── loader.py
│   │   │   └── values/strings.yml
│   │   ├── middlewares/        # Custom middlewares
│   │   │   └── auth.py
│   │   ├── models/             # Pydantic schemas
│   │   │   ├── settings.py
│   │   │   ├── strings.py
│   │   │   └── user.py
│   │   ├── routers/            # Endpoint routers (users currently commented out)
│   │   │   └── users.py
│   │   ├── static/             # Static assets mounted at /static/
│   │   │   ├── assets/
│   │   │   │   ├── fonts/      # FontAwesome files
│   │   │   │   └── images/     # Favicon, logo, and "landing page" stock images
│   │   │   ├── scripts/        # Existing client scripts
│   │   │   └── stylesheets/    # base.css, landing page.css, code.css, docs.css
│   │   ├── templates/          # Jinja2 templates (mounted at /templates/)
│   │   │   ├── base.j2.html
│   │   │   ├── code.j2.html    # HTTP error template
│   │   │   └── login/register  # Auth templates
│   │   └── utils.py            # CustomResponse & Jinja template helper
│   └── pages/                  # Static HTML files mounted at /
│       └── index.html          # Old Hielo static landing page
```

- **App Initialization:** `FastAPI` configured in `main.py` with `SessionMiddleware`.
- **Routing:**
  - `GET /docs` (Swagger UI with custom stylesheet)
  - `GET/POST /code/{code}` (renders status page via Jinja template `code.j2.html`)
  - `POST /webhook` (GitHub deployment webhook)
  - `app.mount("/static/", StaticFiles(...))`
  - `app.mount("/templates/", StaticFiles(...))`
  - `app.mount("/", StaticFiles(directory="src/pages", html=True))` (serves static files from `src/pages/`)
- **Python version:** System is Python 3.15.0rc2, `uv` managed Python 3.13.16 in `.venv`.

## 3. Current Functionality & Execution Status

- **Running status:** `uv sync` / `uv run` currently fails because `erdantic` in `[dependency-groups] dev` pulls `pygraphviz==1.14`, which fails C-compilation against Graphviz header files on GCC 15 / Python 3.13.
- `python-dotenv` was placed in dev dependencies rather than runtime dependencies despite being imported at runtime by `src/api/config/loader.py`.
- **Landing page appearance:** The existing `src/pages/index.html` is an old third-party template ("Hielo by TEMPLATED") with stock photography (`bg.jpg`, `pic01.jpg` - `pic04.jpg`, `slide01.jpg` - `slide05.jpg`) and outdated navigation ("Home", "Generic", "Elements"). It does not represent Lyra or WhiskerFrame.

## 4. `docs/ai/` Overview

- `docs/ai/master-context.md`: Single source of truth for portfolio facts, palette, stack rules, and section structure. Verified public-safe. No other files present.

## 5. `blog/` Overview

- Contains `00015 The World Has Gone Mad, And So HAve I.md`.
- No FastAPI route is registered for the blog in `main.py` or `src/api/routers/`.
- Per master context rules, `blog/` is completely out of scope for the Oct 17 release. It remains untouched and unregistered.

## 6. Area Decisions: Reuse / Refactor / Replace

| Area | Decision | Reason |
|---|---|---|
| `main.py` | **Refactor** | Route `/` to render Jinja2 `index.html` with content dictionary and slot helper; retain `/code/{code}` error handler; make session middleware secrets optional for local/freeze builds. |
| `src/api/config/` & `settings.py` | **Refactor** | Provide safe defaults for `JWT_SECRET` when running static freeze or local dev without `.env`; move `python-dotenv` to runtime dependencies. |
| `pyproject.toml` | **Refactor** | Drop `erdantic` (and its broken `pygraphviz` dependency); add `segno` for build-time QR generation. |
| `src/pages/index.html` | **Replace** | Obsolete third-party template; replace with FastAPI Jinja2 template rendering. |
| `src/api/templates/base.j2.html` | **Replace** | Replace with new semantic `templates/base.html` following Master Context design tokens and self-hosted fonts. |
| `src/api/static/stylesheets/base.css` | **Replace** | Replace old HSL/Roboto stylesheet with Master Context `tokens.css` and reset `base.css`. |
| `src/api/static/stylesheets/landing page.css` | **Retire** | 77KB legacy template CSS, unreferenced in new architecture. |
| `src/api/static/assets/images/landing page/` | **Retire** | 3MB of stock photography not relevant to the new site. |
| `src/api/static/assets/fonts/` | **Replace** | Replace legacy FontAwesome files with self-hosted woff2 Latin fonts (Fredoka, Nunito, JetBrains Mono). |
| `justfile` | **Refactor** | Ensure `dev`, `check`, `freeze`, and `test` recipes are fully wired and functional. |

## 7. Deviations from MASTER-CONTEXT.md

1. **Color Tokens:** Existing `base.css` uses HSL variables (`--bg-1`, `--fg-1`) completely mismatched with Master Context section 4 palette (`--bg: #191a28`, `--surface: #232540`, `--pink: #fd7da6`, etc.).
2. **External CDNs:** Existing templates load fonts from Google Fonts (`@import`) and CSS from Cloudflare CDN (`10up-sanitize.css`), violating the self-hosted zero-external-requests rule.
3. **Template Architecture:** Existing `main.py` serves `src/pages/` as raw static files rather than server-rendered Jinja2 templates loaded from a structured content file.
4. **Dependency Conflicts:** Dev dependency `erdantic` causes build failure on Python 3.13 with modern GCC; `python-dotenv` was misplaced in dev-only group.
5. **Hard Secret Requirements:** `load_settings()` in `src/api/models/settings.py` crashes on missing `JWT_SECRET`, blocking zero-config dev and static export pipelines.
