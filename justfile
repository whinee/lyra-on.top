# regex to match recipe names and their comments:
# ^    (?P<recipe>\S+)(?P<args>(?:\s[^#\s]+)*)(?:\s+# (?P<docs>.+))*

# Choose recipes
default:
    @ just -lu

[private]
nio_dev:
    @ python -m no_implicit_optional dev; exit 0

[private]
nio_src:
    @ python -m no_implicit_optional src; exit 0

[private]
ruff:
    @ python -m ruff check src --fix; exit 0

# Set up development environment
[unix]
bootstrap:
    #!/usr/bin/env bash
    rm -rf .venv
    rm -f uv.lock
    uv venv
    source .venv/bin/activate
    uv sync

# Set up development environment
[windows]
bootstrap:
    Remove-Item -Recurse -Force .venv
    Remove-Item -Force uv.lock
    uv venv
    . .\.venv\Scripts\Activate.ps1
    uv sync

# Lint codebase
lint:
    just nio_dev
    just nio_src
    python -m mdformat docs
    python -m black -q .
    just ruff

# Run web app
run:
    ENV=development hypercorn main:app --reload --bind 0.0.0.0:8000 --workers 16

# Run web app in a lightweight way
run_local:
    ENV=development hypercorn main:app --reload --bind 0.0.0.0:8000 --workers 1
