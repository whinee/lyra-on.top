#!/usr/bin/env python3
"""
scripts/check_todos.py - Scan repository for TODO(lyra) markers.

Lists all occurrences with file and line. Exits non-zero ONLY when --strict is passed.
"""

import argparse
import os
import sys
from pathlib import Path

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

IGNORE_FILES = {
    "check_todos.py",
}


def scan_file(file_path: Path) -> list[tuple[int, str]]:
    matches = []
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                if "TODO(lyra)" in line:
                    matches.append((line_no, line.strip()))
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    return matches


def collect_todos(root: Path) -> list[tuple[Path, int, str]]:
    all_todos = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for filename in filenames:
            if filename in IGNORE_FILES:
                continue
            file_path = Path(dirpath) / filename
            rel_path = file_path.relative_to(root)
            for line_no, content in scan_file(file_path):
                all_todos.append((rel_path, line_no, content))
    return all_todos


def main() -> int:
    parser = argparse.ArgumentParser(description="Check for TODO(lyra) markers in the project.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any TODO(lyra) is found")
    parser.add_argument("--path", default=".", help="Root path to scan (default: current dir)")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    all_todos = collect_todos(root)

    print(f"Found {len(all_todos)} TODO(lyra) item(s):")
    print("-" * 60)
    for path, line_no, content in all_todos:
        print(f"{path}:{line_no}  ->  {content}")
    print("-" * 60)

    if args.strict and all_todos:
        print(f"Strict check failed: {len(all_todos)} unresolved TODO(lyra) found.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
