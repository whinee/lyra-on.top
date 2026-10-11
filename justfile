# Choose recipes
default:
    @ just -lu

# Set up development environment
bootstrap:
    uv sync

# Run web app in lightweight dev mode
dev:
    ENV=development uv run hypercorn main:app --reload --bind 127.0.0.1:8000 --workers 1

# Run web app with multiple workers
run:
    ENV=development uv run hypercorn main:app --reload --bind 0.0.0.0:8000 --workers 4

# Check contrast ratios
contrast:
    uv run python scripts/check_contrast.py

# Check TODO(lyra) markers
todos:
    uv run python scripts/check_todos.py

# Strict check TODO(lyra) markers (fails if any found)
todos-strict:
    uv run python scripts/check_todos.py --strict

# Generate slides QR code
qr:
    uv run python scripts/make_qr.py

# Freeze static site to dist/
freeze:
    uv run python scripts/freeze.py

# Serve frozen dist/ directory locally
preview port="8080": freeze
    python3 -m http.server {{port}} --directory dist

# Capture 360px and 1280px screenshots of hero variants
screenshots:
    uv run python scripts/screenshot_heroes.py

# Deploy static dist/ to Cloudflare Pages
deploy: freeze
    npx wrangler pages deploy dist --project-name=lyra-on-top

# Lint codebase
lint:
    uv run ruff check .

# Run test suite
test:
    uv run pytest tests

# Run comprehensive validation (contrast, todos, lint, test, freeze)
check:
    just contrast
    just todos
    just lint
    just test
    just freeze
