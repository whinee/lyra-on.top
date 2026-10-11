# Deployment Guide: Cloudflare Pages (lyra-on.top)

Static deployment runbook for the lyra-on.top portfolio. Target deadline: Wed 14 Oct 2026 18:00 (Asia/Manila).

---

## 1. Architecture Overview

- **Source:** FastAPI + Jinja2 templates + plain CSS tokens.
- **Export Pipeline:** `scripts/freeze.py` captures all public routes into `dist/` with zero runtime Python overhead.
- **Hosting:** Cloudflare Pages (global CDN edge network).
- **Domain:** `https://lyra-on.top`

**Why static export first:**
Visitors will scan the talk QR on phone cellular or venue WiFi right after the Hack & Yap talk. Static files have 0ms Python cold starts, zero backend database dependencies, and survive traffic spikes effortlessly.

---

## 2. Build & Export Steps

To build the static distribution locally:

```bash
# 1. Install dependencies
uv sync

# 2. Run quality checks & build
just check
```

`just check` will:
1. Validate WCAG 2.1 AA contrast matrix (`scripts/check_contrast.py`)
2. Audit `TODO(lyra)` markers (`scripts/check_todos.py`)
3. Lint codebase with ruff (`ruff check .`)
4. Build SVG QR code (`scripts/make_qr.py`)
5. Freeze routes into `dist/` (`scripts/freeze.py`)

Output lands in `dist/`:
- `dist/index.html`
- `dist/404.html`
- `dist/robots.txt`
- `dist/sitemap.xml`
- `dist/static/` (stylesheets, scripts, images, self-hosted fonts)

---

## 3. Deployment Options

### Option A: Cloudflare Wrangler CLI (Direct)

```bash
# Deploy to preview / production
npx wrangler pages deploy dist --project-name=lyra-on-top
```

### Option B: Cloudflare Pages Git Integration

1. In Cloudflare Dashboard -> **Workers & Pages** -> **Create application** -> **Pages**.
2. Connect GitHub repository `whinee/lyra-on.top`.
3. Configure build settings:
   - **Framework preset:** None
   - **Build command:** `pip install uv && uv sync && uv run python scripts/freeze.py`
   - **Build output directory:** `dist`
4. Root directory: `/`

---

## 4. Custom Domain Checklist: `lyra-on.top`

- [ ] Add custom domain in Cloudflare Pages dashboard: `lyra-on.top` and `www.lyra-on.top`.
- [ ] Verify DNS records in DNS registrar:
  - CNAME `lyra-on.top` -> `lyra-on-top.pages.dev` (or Cloudflare proxied apex).
  - CNAME `www` -> `lyra-on-top.pages.dev`.
- [ ] SSL/TLS setting: **Full (strict)**.
- [ ] Verify HTTPS redirect is enforced: HTTP 301 -> HTTPS.
- [ ] Verify custom 404 page serves `dist/404.html` on missing paths.

---

## 5. Verification Checklist Post-Deploy

- [ ] Desktop layout renders at 1280px without horizontal scroll.
- [ ] Mobile layout renders clean at 360px viewport.
- [ ] Talk slides QR code scans cleanly from screen using a phone camera.
- [ ] Mascot (WhiskerFrame) interactive states work with JS on; fallback displays clean with JS off.
- [ ] Page weight under 300 KB transferred on throttled 4G network.
- [ ] Zero external network calls (all fonts and scripts self-hosted).
