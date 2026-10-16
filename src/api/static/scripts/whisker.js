/**
 * whisker.js - Interactive client script for WhiskerFrame mascot.
 * Fully optional enhancement (JS-optional site).
 * Supports bounded testable animation states & client-side boss fight easter egg.
 */

(() => {
  const mascot = document.getElementById("whisker-mascot");
  const speech = document.getElementById("whisker-speech");
  const speechText = document.getElementById("whisker-speech-text");
  const arena = document.getElementById("whisker-boss-arena");
  const exitBtn = document.getElementById("boss-exit-btn");
  const powerFill = document.getElementById("boss-power-fill");
  const powerTrack = document.getElementById("boss-power-track");
  const statusText = document.getElementById("boss-status-text");
  const termLeft = document.getElementById("boss-term-left-body");
  const termRight = document.getElementById("boss-term-right-body");
  const victoryBanner = document.getElementById("boss-victory-banner");
  const mascotDock = document.getElementById("boss-mascot-dock");

  if (!mascot || !speech || !speechText) return;

  const PHRASES = [
    "WhiskerFrame booted! :3",
    "Pet the cyberdeck! (=^･ω･^=)",
    "REVEL in FOSS! ✧",
    "Running in pure blurple >w<",
    "Lyra + WhiskerFrame on top! ♡",
    "Beep boop, hackathon ready! ★",
  ];

  const RANDOM_STATES = ["wiggle", "bounce", "curious-tilt", "heart-pulse"];

  let phraseIndex = 0;
  let timeoutId = null;
  let clickCount = 0;
  let inBossFight = false;
  let power = 0;
  let decayInterval = null;
  let originalParent = mascot.parentNode;
  let originalNextSibling = mascot.nextSibling;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function selectRandomState() {
    const nextState = RANDOM_STATES[Math.floor(Math.random() * RANDOM_STATES.length)];
    // Bounded phase offset between -0.05s and -0.4s so animation starts smoothly without jitter to frame zero
    const offset = (-(Math.random() * 0.35 + 0.05)).toFixed(3);
    mascot.style.setProperty("--anim-offset", `${offset}s`);
    mascot.setAttribute("data-state", nextState);
    return nextState;
  }

  function triggerReaction() {
    if (inBossFight) {
      handleBossClick();
      return;
    }

    clickCount += 1;
    phraseIndex = (phraseIndex + 1) % PHRASES.length;
    speechText.textContent = PHRASES[phraseIndex];
    speech.classList.add("active");

    selectRandomState();

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    // Check if 10 clicks have unlocked the boss fight
    if (clickCount >= 10 && arena) {
      timeoutId = setTimeout(() => {
        startBossFight();
      }, 400);
      return;
    }

    timeoutId = setTimeout(() => {
      speech.classList.remove("active");
      mascot.setAttribute("data-state", "idle");
    }, 2800);
  }

  // --- Boss Fight Mechanics (100% Client-Side Synthetic Simulation) ---
  function startBossFight() {
    if (inBossFight) return;
    inBossFight = true;
    power = 20;

    if (arena && mascotDock) {
      arena.classList.add("active");
      arena.setAttribute("aria-hidden", "false");
      mascotDock.appendChild(mascot);
    }

    document.body.classList.add("boss-active");
    updateBossUI();

    if (decayInterval) clearInterval(decayInterval);
    decayInterval = setInterval(() => {
      if (!inBossFight) return;
      if (power > 0 && power < 100) {
        power = Math.max(0, power - 1.2);
        updateBossUI();
      }
    }, 120);
  }

  function handleBossClick() {
    power = Math.min(100, power + 12);
    selectRandomState();
    updateBossUI();
  }

  function updateBossUI() {
    if (!inBossFight) return;

    const roundedPower = Math.round(power);
    if (powerFill) powerFill.style.width = `${roundedPower}%`;
    if (powerTrack) powerTrack.setAttribute("aria-valuenow", `${roundedPower}`);

    if (roundedPower < 35) {
      if (statusText) statusText.textContent = "OVERCLOCK STARTING! CLICK FASTER! :3";
      if (termLeft) {
        termLeft.textContent =
          "[SIMULATED RUNTIME - PURE TEXT ONLY]\n" +
          "$ fake-env install python3-minimal git\n" +
          "Reading synthetic state... 100%\n" +
          "Packages staged in memory cache.";
      }
      if (termRight) {
        termRight.textContent =
          "[SIMULATED TELEMETRY - NON-ROUTABLE DEMO]\n" +
          "Interface lo: 127.0.0.1 link active\n" +
          "Listening for synthetic burst packets...";
      }
      document.body.classList.remove("boss-active-shake");
      if (victoryBanner) victoryBanner.style.display = "none";
    } else if (roundedPower < 75) {
      if (statusText) statusText.textContent = "FREQUENCY RISING! 4.8 GHz OVERCLOCK! ✧";
      if (termLeft) {
        termLeft.textContent =
          "[SIMULATED RUNTIME - PURE TEXT ONLY]\n" +
          "$ git clone https://example.com/demo/whisker-os.git\n" +
          "Cloning into 'whisker-os'...\n" +
          "remote: Enumerating objects: 42, done.\n" +
          "remote: Total 42 (delta 18), reused 42\n" +
          "Receiving objects: 100% (42/42), done.";
      }
      if (termRight) {
        termRight.textContent =
          "[SIMULATED TELEMETRY - NON-ROUTABLE DEMO]\n" +
          "$ mock-audit --target 192.0.2.1\n" +
          "Target: 192.0.2.1 (RFC 5737 TEST-NET-1)\n" +
          "Port 80/tcp: SYN_SENT -> SYN_ACK\n" +
          "Wireshark dummy capture: 64 packets simulated.";
      }
      if (!prefersReducedMotion) {
        document.body.classList.add("boss-active-shake");
      }
      if (victoryBanner) victoryBanner.style.display = "none";
    } else if (roundedPower < 100) {
      if (statusText) statusText.textContent = "CRITICAL OVERLOAD! ALMOST AT MAX POWER! ★";
      if (termLeft) {
        termLeft.textContent =
          "[SIMULATED RUNTIME - PURE TEXT ONLY]\n" +
          "$ pytest ./tests/simulated_kernel/\n" +
          "================ 128 passed in 0.04s ================\n" +
          "Kernel patch applied cleanly.\n" +
          "CPU core frequency: PEAK OVERCLOCK.";
      }
      if (termRight) {
        termRight.textContent =
          "[SIMULATED TELEMETRY - NON-ROUTABLE DEMO]\n" +
          "Wireshark trace analysis complete:\n" +
          "All frames captured on loopback interface.\n" +
          "0 dropped frames. Zero buffer overrun.\n" +
          "Cyberdeck link: UNSTOPPABLE.";
      }
      if (victoryBanner) victoryBanner.style.display = "none";
    } else {
      // 100% Maximum Power Victory!
      if (statusText) statusText.textContent = "★ MAXIMUM POWER REACHED! MONOLITH DEFEATED! ★";
      if (victoryBanner) victoryBanner.style.display = "block";
      document.body.classList.remove("boss-active-shake");
    }
  }

  function exitBossFight() {
    inBossFight = false;
    power = 0;
    clickCount = 0;

    if (decayInterval) {
      clearInterval(decayInterval);
      decayInterval = null;
    }

    if (arena) {
      arena.classList.remove("active");
      arena.setAttribute("aria-hidden", "true");
    }

    document.body.classList.remove("boss-active", "boss-active-shake");

    // Restore mascot to its original layout position
    if (originalParent) {
      if (originalNextSibling) {
        originalParent.insertBefore(mascot, originalNextSibling);
      } else {
        originalParent.appendChild(mascot);
      }
    }

    mascot.setAttribute("data-state", "idle");
    if (speech) speech.classList.remove("active");
  }

  // Event Listeners
  mascot.addEventListener("click", triggerReaction);

  mascot.setAttribute("tabindex", "0");
  mascot.setAttribute("role", "button");
  mascot.setAttribute("aria-label", "Pet WhiskerFrame cyberdeck sidekick");

  mascot.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      triggerReaction();
    }
  });

  if (exitBtn) {
    exitBtn.addEventListener("click", exitBossFight);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && inBossFight) {
      exitBossFight();
    }
  });

  // Expose testable programmatic API on window for regression suites
  window.__whiskerFrame = {
    getState: () => mascot.getAttribute("data-state"),
    getClickCount: () => clickCount,
    getPower: () => power,
    isInBossFight: () => inBossFight,
    triggerReaction: () => triggerReaction(),
    startBossFight: () => startBossFight(),
    exitBossFight: () => exitBossFight(),
  };
})();
