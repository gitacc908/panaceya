const burgerBtn = document.getElementById("burgerBtn");
const mainNav = document.getElementById("mainNav");

if (burgerBtn && mainNav) {
    burgerBtn.setAttribute("aria-expanded", "false");

    burgerBtn.addEventListener("click", () => {
        const opened = mainNav.classList.toggle("open");
        burgerBtn.setAttribute("aria-expanded", String(opened));
    });

    mainNav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            mainNav.classList.remove("open");
            burgerBtn.setAttribute("aria-expanded", "false");
        });
    });
}

const setupCarousel = (carousel) => {
    const track = carousel.querySelector("[data-carousel-track]");
    const slides = carousel.querySelectorAll(".carousel-slide");
    const prevBtn = carousel.querySelector("[data-carousel-prev]");
    const nextBtn = carousel.querySelector("[data-carousel-next]");
    const dots = carousel.querySelectorAll("[data-carousel-dot]");
    const autoplayMs = Number(carousel.getAttribute("data-carousel-autoplay")) || 0;
    const mode = carousel.getAttribute("data-carousel-mode") || "carousel";

    if (!track || slides.length === 0) {
        return;
    }

    let current = 0;
    const total = slides.length;
    let autoplayTimer = null;
    let pointerStartX = null;

    const setActiveDot = () => {
        dots.forEach((dot, index) => {
            dot.classList.toggle("is-active", index === current);
        });
    };

    const render = () => {
        if (mode === "slideshow") {
            slides.forEach((slide, index) => {
                const isActive = index === current;
                slide.classList.toggle("is-active", isActive);
                slide.setAttribute("aria-hidden", String(!isActive));
            });
        } else {
            track.style.transform = `translateX(-${current * 100}%)`;
        }

        if (prevBtn) {
            prevBtn.disabled = total <= 1;
        }
        if (nextBtn) {
            nextBtn.disabled = total <= 1;
        }

        setActiveDot();
    };

    const next = () => {
        current = (current + 1) % total;
        render();
    };

    const prev = () => {
        current = (current - 1 + total) % total;
        render();
    };

    const stopAutoplay = () => {
        if (autoplayTimer) {
            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    };

    const startAutoplay = () => {
        if (autoplayMs < 1000 || total <= 1) {
            return;
        }
        stopAutoplay();
        autoplayTimer = setInterval(next, autoplayMs);
    };

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            prev();
            startAutoplay();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            next();
            startAutoplay();
        });
    }

    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
            const index = Number(dot.getAttribute("data-carousel-dot"));
            if (!Number.isNaN(index)) {
                current = index;
                render();
                startAutoplay();
            }
        });
    });

    carousel.addEventListener("mouseenter", stopAutoplay);
    carousel.addEventListener("mouseleave", startAutoplay);

    carousel.addEventListener("pointerdown", (event) => {
        if (event.pointerType === "mouse" && event.button !== 0) {
            return;
        }
        pointerStartX = event.clientX;
        stopAutoplay();
    });

    carousel.addEventListener("pointerup", (event) => {
        if (pointerStartX === null) {
            startAutoplay();
            return;
        }

        const delta = event.clientX - pointerStartX;
        if (Math.abs(delta) > 40) {
            if (delta < 0) {
                next();
            } else {
                prev();
            }
        }

        pointerStartX = null;
        startAutoplay();
    });

    carousel.addEventListener("pointerleave", () => {
        pointerStartX = null;
        startAutoplay();
    });

    render();
    startAutoplay();
};

document.querySelectorAll("[data-carousel]").forEach(setupCarousel);

const revealElements = document.querySelectorAll("[data-reveal]");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

document.body.classList.add("has-motion");

if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealElements.forEach((item) => item.classList.add("is-visible"));
} else {
    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    obs.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.14,
            rootMargin: "0px 0px -8% 0px",
        }
    );

    revealElements.forEach((item) => observer.observe(item));
}
