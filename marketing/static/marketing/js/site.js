const burgerBtn = document.getElementById("burgerBtn");
const mainNav = document.getElementById("mainNav");

if (burgerBtn && mainNav) {
    burgerBtn.addEventListener("click", () => {
        mainNav.classList.toggle("open");
    });
}
