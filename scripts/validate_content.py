#!/usr/bin/env python3
"""scripts/validate_content.py - CLI tool to validate content YAML and Markdown."""

import sys
from pathlib import Path

# Add project root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.api.config.content_loader import (  # noqa: E402
    load_all_content,
    validate_content,
)


def main() -> int:
    content_dir = Path("content").resolve()
    print(f"Validating content in {content_dir}...")
    errors = validate_content(content_dir)

    if errors:
        print(f"\n❌ Content validation FAILED with {len(errors)} error(s):\n")
        for idx, err in enumerate(errors, 1):
            print(f"[{idx}] {err}\n")
        return 1

    catalog = load_all_content(content_dir)
    print("\n✅ All content is valid! ✧")
    print(f"  - Projects: {len(catalog.public_projects)} public (total: {len(catalog.projects)})")
    print(f"  - Blog:     {len(catalog.public_blog)} public (drafts: {len(catalog.blog) - len(catalog.public_blog)})")
    print(f"  - Poems:    {len(catalog.public_poems)} public")
    print(f"  - Talks:    {len(catalog.public_talks)} public")
    print(f"  - Active Nav: {[item['label'] for item in catalog.active_nav]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
