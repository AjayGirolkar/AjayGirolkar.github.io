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
