/**
 * whisker.js - Interactive client script for WhiskerFrame mascot.
 * Fully optional enhancement (JS-optional site).
 */

(() => {
  const mascot = document.getElementById("whisker-mascot");
  const speech = document.getElementById("whisker-speech");
  const speechText = document.getElementById("whisker-speech-text");

  if (!mascot || !speech || !speechText) return;

  const PHRASES = [
    "WhiskerFrame booted! :3",
    "Pet the cyberdeck! (=^･ω･^=)",
    "REVEL in FOSS! ✧",
    "Running in pure blurple >w<",
    "Lyra + WhiskerFrame on top! ♡",
    "Beep boop, hackathon ready! ★"
  ];

  let phraseIndex = 0;
  let timeoutId = null;

  function triggerReaction() {
    phraseIndex = (phraseIndex + 1) % PHRASES.length;
    speechText.textContent = PHRASES[phraseIndex];

    speech.classList.add("active");
    mascot.setAttribute("data-state", "wiggle");

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      speech.classList.remove("active");
      mascot.setAttribute("data-state", "idle");
    }, 2800);
  }

  // Click & Touch events
  mascot.addEventListener("click", triggerReaction);

  // Keyboard accessibility
  mascot.setAttribute("tabindex", "0");
  mascot.setAttribute("role", "button");
  mascot.setAttribute("aria-label", "Pet WhiskerFrame cyberdeck sidekick");

  mascot.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      triggerReaction();
    }
  });
})();
