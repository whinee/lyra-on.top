from pathlib import Path
from typing import Any

import yaml

CONTENT_FILE = Path(__file__).resolve().parent / "values" / "content.yml"

def load_content() -> dict[str, Any]:
    """Load the content dictionary from content.yml."""
    if not CONTENT_FILE.exists():
        raise RuntimeError(f"Content file missing: {CONTENT_FILE}")
    with open(CONTENT_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected mapping in {CONTENT_FILE}")
    return data

def get_slot(content: dict[str, Any], slot_name: str) -> dict[str, str]:
    """Resolve an asset slot with its fallback."""
    slots = content.get("slots", {})
    slot = slots.get(slot_name, {})
    src = slot.get("src")
    if not src:
        src = slot.get("fallback", "")
    return {
        "src": src,
        "alt": slot.get("alt", ""),
    }
