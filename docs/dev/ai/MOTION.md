# MOTION.md - Motion Budget & Performance Invariants

Single source of truth for motion design, performance constraints, and automated verification rules for `lyra-on.top`.

## Core Philosophy
Animate heavily, but never lag. Visual density and lively charm must not compromise low-end devices, battery life, or accessibility.

---

## 1. Allowed & Forbidden CSS Properties

| Rule | Details | Reason |
|---|---|---|
| **ALLOWED** | `transform`, `opacity` | Compositor-only properties. Run on GPU without triggering layout or paint. |
| **FORBIDDEN** | `box-shadow`, `filter: blur()`, `width`, `height`, `top`, `left`, `margin`, `padding` in animation keyframes | Trigger layout recalculation and paint on every frame. Immediate drop to < 30 fps on mobile. |
| **Workaround** | To animate glows or shadows, animate opacity of a pseudo-element (`::after`) with pre-rendered shadow or filter. |

---

## 2. Animation Concurrency & Runtime Budget

1. **At most ONE `requestAnimationFrame` loop on the page:**
   - All interactive canvas / cursor / particle effects must hook into a single shared dispatcher (`static/scripts/fx.js`).
   - Standalone `setInterval` or uncoordinated `rAF` loops are strictly forbidden.
2. **Offscreen Animation Pausing:**
   - Any animated section below the viewport must pause its CSS animations using `IntersectionObserver` + `animation-play-state: paused;`.
   - Utilize CSS `content-visibility: auto;` on below-fold containers to skip layout offscreen.
3. **Element Concurrency Cap:**
   - Maximum **24 concurrent animated elements** visible in the viewport at any time.
4. **`will-change` Hygiene:**
   - Apply `will-change: transform;` only to persistent active movers (e.g. hero floating doodles).
   - Never apply `will-change` globally or to static stickers.

---

## 3. Lite Mode & Accessibility Adaptations

### A. Lite Mode (Resource-Constrained Devices)
Triggered when:
- `navigator.hardwareConcurrency <= 4`, OR
- `navigator.deviceMemory <= 4`, OR
- `navigator.connection?.saveData === true`

**Adaptation:**
- Halve the number of background floaters/sparkles (from 12 to 6).
- Disable complex aurora gradient drift.
- Marquee speed reduced to linear low-frequency scroll.

### B. Reduced Motion Mode (`prefers-reduced-motion: reduce`)
Triggered automatically via OS/browser accessibility setting:
- **Zero continuous loops:** all rotations, bobs, and floaters stop at `transform: none;`.
- **Zero typing animations:** terminal text renders immediately at full length.
- **Instant scroll:** no smooth-scroll hijacking.
- **Static decorations:** sparkles and stickers display without oscillating transforms.

---

## 4. Quantitative Performance Thresholds

Tested on Chrome / Playwright with **4x CPU throttling**:

| Metric | Target | Hard Fail Threshold |
|---|---|---|
| **LCP (Largest Contentful Paint)** | < 1.2s | > 2.0s |
| **CLS (Cumulative Layout Shift)** | < 0.02 | >= 0.05 |
| **Long Tasks post-load** | 0 tasks > 50ms | Any task > 50ms |
| **Hero Animated Framerate** | 60 fps | < 50 fps |
| **Initial Transfer Weight (HTML+CSS+JS)** | < 350 KB | > 500 KB |

---

## 5. Verification Test Suite

- `tests/test_perf.py` runs Playwright automated tests enforcing these thresholds.
- Regressions cause `just test` and CI pipeline to exit non-zero.
