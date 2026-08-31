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

const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ── Scroll effects ───────────────────────────────── */
// One passive, rAF-throttled listener drives every scroll effect. Separate
// non-passive listeners each doing their own DOM writes made scrolling stutter.
const scrollEffects = [];
let scrollQueued = false;

function runScrollEffects() {
  scrollQueued = false;
  const y = window.scrollY;
  for (const effect of scrollEffects) effect(y);
}

window.addEventListener(
  "scroll",
  () => {
    if (scrollQueued) return;
    scrollQueued = true;
    requestAnimationFrame(runScrollEffects);
  },
  { passive: true }
);

if (header) {
  let scrolled = null;
  scrollEffects.push((y) => {
    const next = y > 18;
    if (next === scrolled) return; // Skip the DOM write when nothing changed.
    scrolled = next;
    header.classList.toggle("scrolled", next);
  });
}

if (reduceMotion) {
  // Nothing to stagger when the fade is off — show it all up front.
  revealItems.forEach((item) => item.classList.add("visible"));
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      });
    },
    // rootMargin pre-triggers reveal ~600px before the element enters the
    // viewport, so it has finished fading in by the time the user reaches it.
    { threshold: 0, rootMargin: "0px 0px 600px 0px" }
  );

  // Stagger restarts in each section and caps at STAGGER_MAX steps. A running
  // page-wide index gave the last elements a ~2s transition-delay, which read
  // as the page loading late while scrolling.
  const STAGGER_STEP = 60;
  const STAGGER_MAX = 4;
  const groupCounts = new Map();

  revealItems.forEach((item) => {
    const group = item.closest("section") || document.body;
    const i = groupCounts.get(group) || 0;
    groupCounts.set(group, i + 1);
    item.style.transitionDelay = `${Math.min(i, STAGGER_MAX) * STAGGER_STEP}ms`;
    observer.observe(item);
  });
}

/* ── Typewriter ───────────────────────────────────── */
function initTypewriter() {
  const el = document.getElementById('hero-typewriter');
  if (!el) return;
  const phrases = ['scale.', 'ship fast.', 'look amazing.', 'perform.', 'last.'];
  let pi = 0, ci = 0, del = false;
  let timer = null, onScreen = true;

  if (reduceMotion) { el.textContent = phrases[0]; return; }

  function tick() {
    timer = null;
    // Nothing to animate while the hero is scrolled away; a text write every
    // ~88ms for the whole page kept forcing layout during scroll.
    if (!onScreen) return;
    const p = phrases[pi];
    el.textContent = p.slice(0, ci);
    if (!del && ci === p.length) { del = true; timer = setTimeout(tick, 2000); return; }
    if (del && ci === 0) { del = false; pi = (pi + 1) % phrases.length; }
    ci += del ? -1 : 1;
    timer = setTimeout(tick, del ? 48 : 88);
  }

  new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    if (onScreen && timer === null) tick();
  }).observe(el);

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

/* ── Work grid → app detail (portfolio root page) ─── */
// The grid cards and the #apps tabs address the same demos by
// data-app, so a card just drives the existing tab and scrolls.
function initWorkGrid() {
  const cards = document.querySelectorAll('.work-card[data-app]');
  const target = document.getElementById('apps');
  if (!cards.length || !target) return;
  const reduce = reduceMotion;
  cards.forEach(card => {
    card.addEventListener('click', () => {
      document.querySelector(`.app-tab[data-app="${card.dataset.app}"]`)?.click();
      // Offset for the sticky header so the tab row isn't hidden under it.
      const top = target.getBoundingClientRect().top + window.scrollY - 84;
      window.scrollTo({ top, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
}

/* ── Parallax (hero phones) ───────────────────────── */
function initParallax() {
  const phone = document.querySelector('.hero-phone-float');
  if (!phone || reduceMotion) return;
  // Drive the wrapper, not the phone: the phone runs the phoneFloat keyframes,
  // and a CSS animation beats an inline transform, so writing to the phone on
  // every scroll frame did nothing but burn main-thread time.
  const wrap = phone.closest('.hero-phone-wrap') || phone.parentElement;
  const hero = document.getElementById('hero');
  if (!wrap) return;
  let last = null;
  scrollEffects.push(y => {
    // Once the hero is off screen there is nothing left to shift.
    const offset = hero && y > hero.offsetHeight ? null : Math.round(y * 0.05);
    if (offset === last) return;
    last = offset;
    wrap.style.transform = offset === null ? '' : `translate3d(0, ${offset}px, 0)`;
  });
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
        // Cap the stagger — an uncapped one made the last rows of a long
        // panel appear a second or more after the click.
        const revealEls = body ? body.querySelectorAll('.reveal:not(.visible)') : [];
        revealEls.forEach((el, i) => {
          setTimeout(() => el.classList.add('visible'), Math.min(i, 4) * 60 + 40);
        });
      }
    };

    header.addEventListener('click', toggle);
    header.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });
}

/* ── Screenshot carousels ─────────────────────────── */
function initScreenshotCarousels() {
  document.querySelectorAll('.screenshot-carousel').forEach(carousel => {
    const slides = carousel.querySelectorAll('.sc-slide');
    if (slides.length < 2) return;

    const phone = carousel.closest('.app-demo-phone');
    const dotsWrap = phone ? phone.querySelector('.carousel-dots') : null;
    if (!dotsWrap) return;

    let current = 0;
    let timer = null;

    // Build dots
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Screen ${i + 1}`);
      dot.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(dot);
    });

    function goTo(idx) {
      slides[current].classList.remove('active');
      dotsWrap.children[current].classList.remove('active');
      current = (idx + slides.length) % slides.length;
      slides[current].classList.add('active');
      dotsWrap.children[current].classList.add('active');
    }

    function startAuto() {
      if (reduceMotion) return;
      timer = setInterval(() => goTo(current + 1), 2800);
    }
    function stopAuto() { clearInterval(timer); timer = null; }

    // Pause on hover / tap
    const zone = phone || carousel;
    zone.addEventListener('mouseenter', stopAuto);
    zone.addEventListener('mouseleave', startAuto);
    zone.addEventListener('focusin', stopAuto);
    zone.addEventListener('focusout', startAuto);

    // Restart carousel when its tab becomes active
    const appDemo = carousel.closest('.app-demo');
    if (appDemo) {
      const observer = new MutationObserver(() => {
        if (appDemo.classList.contains('active')) {
          goTo(0);
          stopAuto();
          startAuto();
        } else {
          stopAuto();
        }
      });
      observer.observe(appDemo, { attributes: true, attributeFilter: ['class'] });
    }

    startAuto();
  });
}

/* ── Warm lazy images after first paint ───────────── */
// Initial load only fetches what is on screen. Once the page has painted, the
// rest of the screenshots are pulled into the HTTP cache during idle time, so
// opening a panel or switching an app tab shows them with no pop-in.
function preloadLazyImages() {
  const warm = () => {
    const urls = [];
    const seen = new Set();
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      const url = img.getAttribute('src');
      if (!url || img.complete || seen.has(url)) return;
      seen.add(url);
      urls.push(url);
    });
    if (!urls.length) return;

    // Two at a time, in document order. Flipping every image to eager at once
    // queued ~2MB behind one connection; a detached Image also warms the cache
    // for images the panel keeps unrendered via content-visibility, which a
    // loading="eager" flip on its own would not.
    const CONCURRENCY = 2;
    let next = 0;
    const pump = () => {
      if (next >= urls.length) return;
      const loader = new Image();
      loader.decoding = 'async';
      loader.addEventListener('load', pump, { once: true });
      loader.addEventListener('error', pump, { once: true });
      loader.src = urls[next++];
    };
    for (let i = 0; i < CONCURRENCY; i++) pump();
  };

  if ('requestIdleCallback' in window) {
    requestIdleCallback(warm, { timeout: 2000 });
  } else {
    setTimeout(warm, 1200);
  }
}

/* ── Per-app detail toggle (portfolio page) ───────── */
// The portfolio page shows every screen at once, so the
// problem/result copy, feature list and stack live behind a
// per-app toggle instead of always being on screen.
function initAppDetailToggles() {
  document.querySelectorAll('.app-detail-toggle').forEach(btn => {
    const panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    const label = btn.querySelector('.adt-text');
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      btn.classList.toggle('open', !open);
      panel.classList.toggle('open', !open);
      if (label) label.textContent = open ? 'More details' : 'Hide details';
    });
  });
}

/* ── Screen lightbox (portfolio page) ─────────────── */
function initScreenLightbox() {
  const lb = document.getElementById('screen-lightbox');
  const shots = document.querySelectorAll('.screen-shot-btn');
  if (!lb || !shots.length) return;

  const img = lb.querySelector('.lb-img');
  const cap = lb.querySelector('.lb-cap');
  let group = [];
  let index = 0;
  let lastFocus = null;

  function show(i) {
    if (!group.length) return;
    index = (i + group.length) % group.length;
    const btn = group[index];
    const thumb = btn.querySelector('img');
    img.src = btn.dataset.full;
    img.alt = thumb ? thumb.alt : '';
    cap.textContent = `${btn.dataset.caption} — ${index + 1} of ${group.length}`;
  }

  function open(btn) {
    const strip = btn.closest('.screen-strip');
    group = strip ? Array.from(strip.querySelectorAll('.screen-shot-btn')) : [btn];
    lastFocus = btn;
    show(group.indexOf(btn));
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-close').focus();
  }

  function close() {
    lb.classList.remove('open');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  shots.forEach(btn => btn.addEventListener('click', () => open(btn)));
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', () => show(index - 1));
  lb.querySelector('.lb-next').addEventListener('click', () => show(index + 1));
  // Backdrop click closes; clicks on the image or controls don't.
  lb.addEventListener('click', e => { if (e.target === lb) close(); });

  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initTypewriter();
  initCounters();
  initAppTabs();
  initWorkGrid();
  initScreenshotCarousels();
  initParallax();
  initCalendar();
  initCollapsibleSections();
  initAppDetailToggles();
  initScreenLightbox();
});

window.addEventListener('load', preloadLazyImages);
