const _bar = () => document.getElementById("page-loading-bar");
document.addEventListener("htmx:beforeRequest", () => {
  const b = _bar(); if (b) { b.style.width = "30%"; b.style.opacity = "1"; }
});
document.addEventListener("htmx:afterRequest", () => {
  const b = _bar(); if (b) { b.style.width = "100%"; setTimeout(() => { b.style.opacity = "0"; b.style.width = "0"; }, 300); }
});

function toggleMenu() {
  document.getElementById("mobileMenu").classList.toggle("open");
}

function initSidebarObserver() {
  const anchors = document.querySelectorAll(".sidebar-link[href^='#']");
  if (!anchors.length) return;

  const targets = [...anchors].map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        anchors.forEach(a => a.classList.remove("active"));
        const link = document.querySelector(`.sidebar-link[href="#${entry.target.id}"]`);
        if (link) link.classList.add("active");
      }
    });
  }, { rootMargin: "-20% 0px -70% 0px" });

  targets.forEach(t => observer.observe(t));
}

initSidebarObserver();

function updateActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll(".nav-links a, .mobile-menu a").forEach((a) => {
    const href = new URL(a.href, location.origin).pathname;
    a.classList.toggle("active", href === path);
  });
}

document.addEventListener("htmx:afterSettle", () => {
  updateActiveNav();
  window.scrollTo({ top: 0, behavior: "instant" });
  initSidebarObserver();
  if (document.getElementById("ep-root")) loadHtmxTarget("ep-root", "/_/endpoints-body");
  if (document.getElementById("cl-root")) loadHtmxTarget("cl-root", "/_/changelog-body");
  document.querySelectorAll("pre code:not(.hljs)").forEach((el) => hljs.highlightElement(el));
});

function loadHtmxTarget(id, url) {
  const el = document.getElementById(id);
  if (!el || !el.querySelector(".ep-spinner")) return;
  htmx.ajax("GET", url, { target: "#" + id, swap: "innerHTML" });
}

function switchInstall(btn, name) {
  document
    .querySelectorAll(".install-tab")
    .forEach((b) => b.classList.remove("active"));
  document
    .querySelectorAll(".install-body")
    .forEach((p) => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById("inst-" + name).classList.add("active");
}

function switchExample(btn, name) {
  document
    .querySelectorAll(".example-btn")
    .forEach((b) => b.classList.remove("active"));
  document
    .querySelectorAll(".example-panel")
    .forEach((p) => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById(name).classList.add("active");
}

function switchExTab(btn, name) {
  const bar = btn.closest(".examples-tab-bar");
  bar.querySelectorAll(".ex-tab").forEach((b) => b.classList.remove("active"));
  bar.closest(".examples-tabs").querySelectorAll(".ex-tab-panel").forEach((p) => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById(name).classList.add("active");
}

function switchTab(btn, name) {
  // ct-group: inline header tabs (.ct-btn / .ct-panel)
  const ctGroup = btn.closest(".ct-group");
  if (ctGroup) {
    const wrap = ctGroup.closest(".code-tabs-wrap");
    wrap.querySelectorAll(".ct-btn").forEach((b) => b.classList.remove("active"));
    wrap.querySelectorAll(".ct-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(name).classList.add("active");
    return;
  }
  // tab-group: pill tabs (.tab-btn / .tab-panel)
  const group = btn.closest(".tab-group");
  const card = group ? group.parentElement : document;
  card.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
  card.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById(name).classList.add("active");
}

function copyBlock(btn) {
  const block = btn.closest(".code-block");
  const active = block.querySelector(".ct-panel.active code") || block.querySelector("code");
  navigator.clipboard.writeText(active.textContent).then(() => {
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = "Copy";
      btn.classList.remove("copied");
    }, 2000);
  });
}

function copyCmd(id, btn) {
  navigator.clipboard
    .writeText(document.getElementById(id).textContent)
    .then(() => {
      btn.textContent = "Copied!";
      btn.classList.add("copied");
      setTimeout(() => {
        btn.textContent = "Copy";
        btn.classList.remove("copied");
      }, 2000);
    });
}

