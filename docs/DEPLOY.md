# Deployment Runbook: Cloudflare Workers Static Assets (`lyra-on.top`)

Static deployment runbook for the lyra-on.top portfolio targeting **Cloudflare Workers Static Assets**.

---

## 1. Architecture Overview

- **Source:** FastAPI + Jinja2 templates + plain CSS tokens.
- **Export Pipeline:** `scripts/freeze.py` captures all public routes into `dist/` with zero runtime Python overhead.
- **Hosting:** Cloudflare Workers Static Assets (edge network).
- **Domain:** `https://lyra-on.top` (primary static site Worker).
- **API Worker:** Separate Python API Worker at `api.lyra-on.top` (`worker/main.py`).

**Why Workers Static Assets:**
Provides lightning-fast global edge delivery, 0ms cold starts, and seamless static asset routing without Pages dependencies.

---

## 2. Local Build & Validation Steps

To build and validate the static distribution locally:

```bash
# 1. Install dependencies & uv sync
uv sync

# 2. Run comprehensive checks & static freeze
just check
```

`just check` executes:
1. Validate content and nav (`scripts/validate_content.py`)
2. WCAG 2.1 AA contrast matrix (`scripts/check_contrast.py`)
3. `TODO(lyra)` audit (`scripts/check_todos.py`)
4. Ruff linting (`ruff check .`)
5. Pytest test suite (`pytest tests`)
6. Freeze routes into `dist/` (`scripts/freeze.py`)

To test the frozen output locally:
```bash
just preview
```
Opens http://localhost:8080 serving `dist/`.

To test via Wrangler CLI locally:
```bash
npx wrangler dev
```

---

## 3. GitHub Actions CI/CD Pipeline

Automated deployment is defined in `.github/workflows/deploy-worker.yml`.
- **Trigger:** Pushes to `main` and `workflow_dispatch`.
- **Security:** Least privilege (`permissions: contents: read`), concurrency protection against overlapping deployments, 10-minute timeout.
- **Steps:** Checkout → Setup Python 3.13 → Install `uv` & dependencies → Run `just check` → Deploy via `cloudflare/wrangler-action@v3`.

---

## 4. Operator Setup & Secrets Checklist

Lyra must configure the following external prerequisites before automated GitHub Actions deployment can succeed.

### Step 1: Cloudflare Account ID & API Token
1. **Cloudflare Account ID:**
   - Location: Cloudflare Dashboard sidebar / URL overview.
   - Value name: `CLOUDFLARE_ACCOUNT_ID`.
2. **Cloudflare API Token:**
   - Location: Cloudflare Dashboard → My Profile → API Tokens → Create Token.
   - Template: Use **Edit Cloudflare Workers** template.
   - Permissions scope: Account-level Workers Scripts (Edit) and Workers KV / Static Assets as required.
   - Value name: `CLOUDFLARE_API_TOKEN`.

### Step 2: GitHub Repository Secrets
1. Navigate to GitHub repository: `whinee/lyra-on.top`
2. Go to **Settings → Secrets and variables → Actions → New repository secret**.
3. Add the two secrets:
   - Name: `CLOUDFLARE_ACCOUNT_ID` | Value: [Your Account ID]
   - Name: `CLOUDFLARE_API_TOKEN` | Value: [Your API Token]

### Step 3: Production Domain Cutover (`lyra-on.top`)
- **Warning:** Do not cut over production DNS / routing without explicit operator approval.
- Initial validation will deploy to `workers.dev` preview or preview deployments. Once verified, custom route mapping for `lyra-on.top` can be enabled in Cloudflare Workers settings.

---

## 5. Verification Checklist Post-Deploy
- [ ] GitHub Actions workflow `Deploy Worker Static Assets` passes successfully.
- [ ] Desktop layout renders at 1280px without horizontal scroll.
- [ ] Mobile layout renders clean at 360px viewport.
- [ ] Talk slides QR code scans cleanly.
- [ ] Zero external network calls.
