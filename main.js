(() => {
  "use strict";

  const STORAGE_KEY = "farzana_clinic_map_consent_v1";
  const root = document.documentElement;
  const body = document.body;
  const menuToggle = document.querySelector(".js-menu-toggle");
  const menu = document.querySelector("#primary-navigation");
  const dialog = document.querySelector("#demo-dialog");
  const dialogMessage = dialog?.querySelector("[data-dialog-message]");
  const dialogClose = dialog?.querySelector(".js-dialog-close");
  const privacyBar = document.querySelector("#privacy-bar");
  const consentLoadMap = document.querySelector("#consent-load-map");
  const consentDeclineMap = document.querySelector("#consent-decline-map");
  const loadMapBtn = document.querySelector("#load-map-btn");
  const mapFrame = document.querySelector("#map-frame");
  const mapPlaceholder = document.querySelector("#map-placeholder");
  const resetPrivacy = document.querySelector("#reset-privacy");
  const resetStatus = document.querySelector("#reset-privacy-status");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let lastDemoTrigger = null;

  function readPreference() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  }

  function writePreference(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch {
      // Keep the site usable when storage is blocked.
    }
  }

  function removePreference() {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // A blocked storage area does not prevent visitors from using the page.
    }
  }

  function loadInteractiveMap() {
    if (!mapFrame) return;
    const iframe = mapFrame.querySelector("iframe[data-src]");
    if (iframe && !iframe.getAttribute("src")) {
      iframe.setAttribute("src", iframe.getAttribute("data-src"));
    }
    mapFrame.hidden = false;
    if (mapPlaceholder) {
      mapPlaceholder.hidden = true;
    }
  }

  function closeMenu({ restoreFocus = false } = {}) {
    if (!menu || !menuToggle) return;
    menu.hidden = true;
    menuToggle.setAttribute("aria-expanded", "false");
    body.classList.remove("menu-open");
    if (restoreFocus) menuToggle.focus();
  }

  function openMenu() {
    if (!menu || !menuToggle) return;
    menu.hidden = false;
    menuToggle.setAttribute("aria-expanded", "true");
    body.classList.add("menu-open");
  }

  function dialogIsOpen() {
    return Boolean(dialog && (dialog.open || dialog.hasAttribute("open")));
  }

  function openDemoDialog(actionLabel) {
    if (!dialog) return;
    lastDemoTrigger = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    if (dialogMessage) {
      dialogMessage.textContent = `${actionLabel} is a demonstration interaction. A live clinic website could connect this control to a verified clinic contact or booking provider.`;
    }
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
      dialog.classList.add("dialog--fallback-open");
    }
    dialogClose?.focus();
  }

  function closeDemoDialog() {
    if (!dialogIsOpen()) return;
    if (typeof dialog.close === "function" && dialog.open) {
      dialog.close();
    } else {
      dialog.removeAttribute("open");
      dialog.classList.remove("dialog--fallback-open");
      restoreDemoFocus();
    }
  }

  function restoreDemoFocus() {
    if (lastDemoTrigger?.isConnected) lastDemoTrigger.focus();
    lastDemoTrigger = null;
  }

  function measurePersistentUi() {
    if (privacyBar && !privacyBar.hidden) {
      root.style.setProperty("--privacy-bar-height", `${privacyBar.offsetHeight}px`);
    }
    const quickActions = document.querySelector(".mobile-quick-actions");
    const quickActionsVisible = quickActions && getComputedStyle(quickActions).display !== "none";
    body.classList.toggle("has-quick-actions", Boolean(quickActionsVisible));
    if (quickActionsVisible) {
      root.style.setProperty("--quick-actions-height", `${quickActions.offsetHeight}px`);
    } else {
      root.style.setProperty("--quick-actions-height", "0px");
    }
  }

  function showPrivacyBar() {
    if (!privacyBar) return;
    privacyBar.hidden = false;
    body.classList.add("has-privacy-bar");
    measurePersistentUi();
  }

  function hidePrivacyBar() {
    if (!privacyBar) return;
    privacyBar.hidden = true;
    body.classList.remove("has-privacy-bar");
    root.style.setProperty("--privacy-bar-height", "0px");
  }

  function setupAccordions() {
    document.querySelectorAll(".js-accordion-trigger").forEach((trigger) => {
      const details = trigger.closest("details");
      if (!details) return;
      trigger.setAttribute("aria-expanded", String(details.open));
      details.addEventListener("toggle", () => {
        trigger.setAttribute("aria-expanded", String(details.open));
      });
    });
  }

  function setupReveals() {
    const sections = [...document.querySelectorAll("main > section")];
    if (!sections.length || reducedMotion.matches || !("IntersectionObserver" in window)) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("reveal--visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.08 });
    sections.forEach((section) => {
      section.classList.add("reveal");
      observer.observe(section);
    });
    reducedMotion.addEventListener?.("change", (event) => {
      if (!event.matches) return;
      observer.disconnect();
      sections.forEach((section) => section.classList.remove("reveal", "reveal--visible"));
    });
  }

  menuToggle?.addEventListener("click", () => {
    if (menuToggle.getAttribute("aria-expanded") === "true") {
      closeMenu({ restoreFocus: true });
    } else {
      openMenu();
    }
  });
  menu?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu({ restoreFocus: true });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && dialogIsOpen()) {
      event.preventDefault();
      closeDemoDialog();
      return;
    }
    if (event.key === "Escape" && menuToggle?.getAttribute("aria-expanded") === "true") {
      closeMenu({ restoreFocus: true });
    }
  });
  window.matchMedia("(min-width: 75rem)").addEventListener?.("change", (event) => {
    if (event.matches && menu && menuToggle) {
      menu.hidden = false;
      menuToggle.setAttribute("aria-expanded", "false");
      body.classList.remove("menu-open");
    } else {
      closeMenu();
    }
  });

  document.querySelectorAll(".js-demo-action").forEach((action) => {
    action.addEventListener("click", () => openDemoDialog(action.dataset.demoAction || "This control"));
  });
  dialogClose?.addEventListener("click", closeDemoDialog);
  dialog?.addEventListener("close", restoreDemoFocus);

  consentLoadMap?.addEventListener("click", () => {
    writePreference("granted");
    loadInteractiveMap();
    hidePrivacyBar();
  });

  consentDeclineMap?.addEventListener("click", () => {
    writePreference("declined");
    hidePrivacyBar();
  });

  loadMapBtn?.addEventListener("click", () => {
    writePreference("granted");
    loadInteractiveMap();
    hidePrivacyBar();
  });

  resetPrivacy?.addEventListener("click", () => {
    removePreference();
    if (resetStatus) {
      resetStatus.hidden = false;
      resetStatus.textContent = "Your map preference has been reset. The preference notice will appear when you return to the homepage, and the interactive map will remain blocked until permission is granted.";
    }
  });

  document.querySelectorAll("#current-year").forEach((year) => {
    year.textContent = String(new Date().getFullYear());
  });

  if (menu && menuToggle && window.matchMedia("(max-width: 74.99rem)").matches) closeMenu();

  const currentPreference = readPreference();
  if (currentPreference === "granted") {
    loadInteractiveMap();
  } else if (!currentPreference) {
    if (privacyBar) showPrivacyBar();
  }

  setupAccordions();
  setupReveals();
  window.addEventListener("resize", measurePersistentUi, { passive: true });
  if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(measurePersistentUi);
    if (privacyBar) observer.observe(privacyBar);
    const quickActions = document.querySelector(".mobile-quick-actions");
    if (quickActions) observer.observe(quickActions);
  }
  root.classList.add("js-ready");
  measurePersistentUi();
})();
