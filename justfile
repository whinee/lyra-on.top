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

# Freeze static site to dist/
freeze:
    uv run python scripts/freeze.py

# Lint codebase
lint:
    uv run ruff check .

# Run test suite
test:
    uv run pytest tests

# Run comprehensive validation (contrast, todos, lint, freeze)
check:
    just contrast
    just todos
    just lint
    just freeze
