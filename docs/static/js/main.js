document.documentElement.classList.add("js");

const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector("#primary-links");

if (toggle && links) {
  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  links.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
}

const revealTargets = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealTargets.forEach((target) => observer.observe(target));
} else {
  revealTargets.forEach((target) => target.classList.add("is-visible"));
}

document.querySelectorAll(".abstract-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const abstractId = button.getAttribute("aria-controls");
    const abstract = abstractId ? document.getElementById(abstractId) : null;

    if (!abstract) {
      return;
    }

    const isExpanded = button.getAttribute("aria-expanded") === "true";
    abstract.classList.toggle("is-expanded", !isExpanded);
    button.setAttribute("aria-expanded", String(!isExpanded));
    button.textContent = isExpanded ? "Read more" : "Show less";
  });
});
