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

  // Prevent native drag-and-drop ghosting while keeping text selection and copy working
  document.addEventListener("dragstart", (e) => {
    e.preventDefault();
  });

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
        rootMargin: "0px 0px -40px 0px",
      },
    );

    document.querySelectorAll(".card, .foss-banner-card, .win-card").forEach((el) => {
      el.classList.add("scroll-pop");
      observer.observe(el);
    });
  }

  // 2. Global Delegated Click Feedback
  if (!prefersReducedMotion) {
    const REACTIONS = ["✧", "♡", ":3", "nya~", "✦", "★", "uwu", "purr~", "paws!"];
    const COLORS = [
      "var(--hot-pink)",
      "var(--baby-yellow)",
      "var(--cursor-cyan)",
      "var(--pink)",
      "var(--lavender)",
    ];

    document.addEventListener("click", (e) => {
      // Do not trigger if user is selecting text
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 0) {
        return;
      }

      // Do not trigger inside text inputs or editable fields
      if (e.target && e.target.closest("input, textarea, select, [contenteditable='true']")) {
        return;
      }

      const floater = document.createElement("span");
      floater.className = "fx-floater";
      floater.textContent = REACTIONS[Math.floor(Math.random() * REACTIONS.length)];
      floater.style.left = `${e.clientX}px`;
      floater.style.top = `${e.clientY}px`;
      floater.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      floater.style.fontSize = `${22 + Math.floor(Math.random() * 8)}px`;

      document.body.appendChild(floater);

      const cleanup = () => {
        if (floater.parentNode) {
          floater.remove();
        }
      };

      floater.addEventListener("animationend", cleanup, { once: true });
      setTimeout(cleanup, 1000); // Safety timeout
    });
  }
})();
