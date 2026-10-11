#!/usr/bin/env python3
"""
scripts/check_contrast.py - Computes WCAG ratios for master context color matrix.

Exits non-zero if any pair marked allowed for body text is < 4.5 or large/UI < 3.0.
"""

import sys

SURFACES = {
    "--bg": "#191a28",
    "--surface": "#232540",
    "--raised": "#2f3257",
    "--blurple": "#3b3fa8",
    "--blurple-hi": "#5b5fe0",
}

FOREGROUNDS = {
    "pink": "#fd7da6",
    "lavender": "#ae89ff",
    "baby-blue": "#75beff",
    "baby-yellow": "#fff3a8",
    "hot-pink": "#ff6dd6",
    "periwinkle": "#8c9aff",
    "cursor-cyan": "#29dbff",
    "white": "#ffffff",
}

ALLOWED_BODY_PAIRS = [
    (fg, s)
    for fg in FOREGROUNDS
    for s in ["--bg", "--surface", "--raised"]
] + [
    ("baby-yellow", "--blurple"),
    ("cursor-cyan", "--blurple"),
    ("white", "--blurple"),
    ("white", "--blurple-hi"),
]

ALLOWED_LARGE_OR_UI_PAIRS = [
    ("baby-blue", "--blurple"),
    ("baby-yellow", "--blurple-hi"),
    ("cursor-cyan", "--blurple-hi"),
]


def srgb_to_lin(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def contrast_ratio(c1: str, c2: str) -> float:
    l1 = relative_luminance(c1)
    l2 = relative_luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def build_matrix() -> dict[tuple[str, str], float]:
    matrix = {}
    title_col = "foreground / surface"
    header = f"{title_col:<24}" + "".join(f"{s:<12}" for s in SURFACES)
    print(header)
    print("-" * 76)

    for fg_name, fg_hex in FOREGROUNDS.items():
        row_label = f"{fg_name} {fg_hex}"
        row_str = f"{row_label:<24}"
        for s_name, s_hex in SURFACES.items():
            cr = contrast_ratio(fg_hex, s_hex)
            matrix[(fg_name, s_name)] = cr
            row_str += f"{cr:<12.2f}"
        print(row_str)
    return matrix


def verify_pairings(matrix: dict[tuple[str, str], float]) -> list[str]:
    failures = []
    for fg, s in ALLOWED_BODY_PAIRS:
        cr = matrix[(fg, s)]
        if cr < 4.5:
            failures.append(f"FAIL Body: {fg} on {s} has ratio {cr:.2f} < 4.5")

    for fg, s in ALLOWED_LARGE_OR_UI_PAIRS:
        cr = matrix[(fg, s)]
        if cr < 3.0:
            failures.append(f"FAIL Large/UI: {fg} on {s} has ratio {cr:.2f} < 3.0")

    return failures


def main() -> int:
    print("=" * 76)
    print("WCAG 2.1 Contrast Matrix - Master Context Section 4 Spec")
    print("=" * 76)

    matrix = build_matrix()

    print("=" * 76)
    print("Verifying Allowed Pairings Compliance:")

    failures = verify_pairings(matrix)
    if failures:
        print("\nCONTRAST SPEC VIOLATIONS FOUND:")
        for fail in failures:
            print("  *", fail)
        return 1

    print("All allowed pairings pass WCAG criteria!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
