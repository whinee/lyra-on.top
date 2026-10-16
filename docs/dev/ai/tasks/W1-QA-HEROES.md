# Task Spec: W1-QA-HEROES (Independent Visual QA Review)

## Target & File Ownership
- Audit scope: Rendered output of Hero A, Hero B, Hero C at 360px and 1280px.
- Reports output: `reports/qa-heroes-review.md`
- Screenshot runner: `just screenshots`
- Test runner: `just check`

## Acceptance Criteria
1. Capture fresh screenshots of all variants at 360px and 1280px (`just screenshots`).
2. Verify visual composition, density, spacing, and hierarchy:
   - Compare Hero B and Hero C against Hero A as benchmark.
   - Confirm no giant dead zones or empty cards.
   - Confirm no text clipping, overlapping, or horizontal scrolling at 360px.
   - Confirm color token usage and WCAG AA contrast (minimum 4.5:1 for body text, 3:1 for large text).
   - Confirm keyboard focus visibility and reduced motion compliance.
3. Validate frozen static output:
   - Ensure `just check` passes with all tests green.
   - Confirm static freeze renders properly.
4. Record all findings, screenshot paths, and remaining items in `reports/qa-heroes-review.md`.
