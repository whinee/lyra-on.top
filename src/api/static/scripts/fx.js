/**
 * fx.js - Lightweight client effects & interactions.
 * JS-optional: Site remains 100% accessible and readable with JS disabled.
 * Respects prefers-reduced-motion: reduce.
 */

(() => {
  // Check reduced-motion preference
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Progressive enhancement: mark HTML as js-enhanced
  document.documentElement.classList.add("js-enhanced");

  // 1. Scroll-Pop Reveal Observer
  if (!prefersReducedMotion && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-revealed");
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -40px 0px"
      }
    );

    document.querySelectorAll(".card, .foss-banner-card, .win-card").forEach((el) => {
      el.classList.add("scroll-pop");
      observer.observe(el);
    });
  }

  // 2. Click Floater Accents (Sparkles & Hearts)
  if (!prefersReducedMotion) {
    const ICONS = ["✧", "♡", "★", "✦", ":3"];

    document.addEventListener("click", (e) => {
      // Only trigger on interactive clicks (buttons, stickers, links)
      const target = e.target.closest(".btn, .sticker, .win-card, a");
      if (!target) return;

      const floater = document.createElement("span");
      floater.className = "fx-floater";
      floater.textContent = ICONS[Math.floor(Math.random() * ICONS.length)];
      floater.style.left = `${e.clientX - 10}px`;
      floater.style.top = `${e.clientY - 10}px`;
      floater.style.color = Math.random() > 0.5 ? "var(--hot-pink)" : "var(--baby-yellow)";
      floater.style.fontSize = `${14 + Math.floor(Math.random() * 10)}px`;

      document.body.appendChild(floater);

      floater.addEventListener("animationend", () => {
        floater.remove();
      });
    });
  }
})();
