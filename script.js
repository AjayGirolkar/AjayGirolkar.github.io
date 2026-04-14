const header = document.querySelector(".site-header");
const revealItems = document.querySelectorAll(".reveal");
const year = document.getElementById("year");
const themeToggle = document.querySelector(".theme-toggle");
const root = document.body;
const savedTheme = localStorage.getItem("theme-preference");

if (year) {
  year.textContent = new Date().getFullYear();
}

if (savedTheme === "dark") {
  root.dataset.theme = "dark";
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";

    if (nextTheme === "dark") {
      root.dataset.theme = "dark";
    } else {
      delete root.dataset.theme;
    }

    localStorage.setItem("theme-preference", nextTheme);
  });
}

window.addEventListener("scroll", () => {
  if (!header) return;
  header.classList.toggle("scrolled", window.scrollY > 18);
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    });
  },
  { threshold: 0.14 }
);

revealItems.forEach((item, index) => {
  item.style.transitionDelay = `${index * 70}ms`;
  observer.observe(item);
});

/* ── Typewriter ───────────────────────────────────── */
function initTypewriter() {
  const el = document.getElementById('hero-typewriter');
  if (!el) return;
  const phrases = ['scale.', 'ship fast.', 'look amazing.', 'perform.', 'last.'];
  let pi = 0, ci = 0, del = false;
  function tick() {
    const p = phrases[pi];
    el.textContent = p.slice(0, ci);
    if (!del && ci === p.length) { setTimeout(() => { del = true; tick(); }, 2000); return; }
    if (del && ci === 0) { del = false; pi = (pi + 1) % phrases.length; }
    ci += del ? -1 : 1;
    setTimeout(tick, del ? 48 : 88);
  }
  tick();
}

/* ── Counter animation ────────────────────────────── */
function initCounters() {
  const els = document.querySelectorAll('[data-counter]');
  if (!els.length) return;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target, target = +el.dataset.counter, suf = el.dataset.suffix || '';
      const dur = 1500, t0 = performance.now();
      const run = now => {
        const p = Math.min((now - t0) / dur, 1), ease = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(ease * target) + suf;
        if (p < 1) requestAnimationFrame(run);
      };
      requestAnimationFrame(run);
      obs.unobserve(el);
    });
  }, { threshold: 0.6 });
  els.forEach(el => obs.observe(el));
}

/* ── App demo tabs ────────────────────────────────── */
function initAppTabs() {
  const tabs = document.querySelectorAll('.app-tab');
  const demos = document.querySelectorAll('.app-demo');
  if (!tabs.length) return;
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const t = tab.dataset.app;
      tabs.forEach(x => x.classList.remove('active'));
      demos.forEach(x => x.classList.remove('active'));
      tab.classList.add('active');
      document.querySelector(`.app-demo[data-app="${t}"]`)?.classList.add('active');
    });
  });
}

/* ── Parallax (hero phones) ───────────────────────── */
function initParallax() {
  const ph = document.querySelector('.hero-phone-float');
  if (!ph || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  window.addEventListener('scroll', () => {
    ph.style.transform = `translateY(${scrollY * 0.05}px) rotate(-1.5deg)`;
  }, { passive: true });
}

/* ── Calendar interactivity ───────────────────────── */
function initCalendar() {
  document.querySelectorAll('.cal-available').forEach(d => {
    d.addEventListener('click', () => {
      document.querySelectorAll('.cal-available').forEach(x => x.classList.remove('cal-selected'));
      d.classList.add('cal-selected');
    });
  });
  document.querySelectorAll('.time-slot').forEach(s => {
    s.addEventListener('click', () => {
      document.querySelectorAll('.time-slot').forEach(x => x.classList.remove('slot-selected'));
      s.classList.add('slot-selected');
    });
  });
}

/* ── Collapsible sections ─────────────────────────── */
function initCollapsibleSections() {
  const headers = document.querySelectorAll('.collapse-header');
  headers.forEach(header => {
    const section = header.closest('.collapsible-section');
    const bodyId = header.getAttribute('aria-controls');
    const body = bodyId ? document.getElementById(bodyId) : header.nextElementSibling;

    const toggle = () => {
      const isCollapsed = section.classList.contains('collapsed');
      section.classList.toggle('collapsed', !isCollapsed);
      header.setAttribute('aria-expanded', String(isCollapsed));

      if (isCollapsed) {
        // Trigger reveal animations inside the newly opened section
        const revealEls = body ? body.querySelectorAll('.reveal:not(.visible)') : [];
        revealEls.forEach((el, i) => {
          setTimeout(() => el.classList.add('visible'), i * 60 + 50);
        });
      }
    };

    header.addEventListener('click', toggle);
    header.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initTypewriter();
  initCounters();
  initAppTabs();
  initParallax();
  initCalendar();
  initCollapsibleSections();
});
