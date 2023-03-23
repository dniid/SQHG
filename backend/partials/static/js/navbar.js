const navClick1 = document.getElementById("nav-click-1");
const navClick2 = document.getElementById("nav-click-2");
const navSubItens1 = document.getElementById("nav-sub-items-1");
const navSubItens2 = document.getElementById("nav-sub-items-2");
const navChevD1 = document.getElementById("nav-chevron-down-1");
const navChevD2 = document.getElementById("nav-chevron-down-2");
const navChevU1 = document.getElementById("nav-chevron-up-1");
const navChevU2 = document.getElementById("nav-chevron-up-2");

const mobileNavClick = document.getElementById("mobile-nav-click");
const mobileMenu = document.getElementById("mobile-menu");
const content = document.getElementById("content");


navClick1.addEventListener("click", (event) => {
    if (navSubItens1.classList.contains("hidden")) {
        navSubItens1.classList.remove("hidden");
        navChevU1.classList.remove("hidden");
        navChevD1.classList.add("hidden");
    } else {
        navSubItens1.classList.add("hidden");
        navChevU1.classList.add("hidden");
        navChevD1.classList.remove("hidden");
    }
});

navClick2.addEventListener("click", (event) => {
    if (navSubItens2.classList.contains("hidden")) {
        navSubItens2.classList.remove("hidden");
        navChevU2.classList.remove("hidden");
        navChevD2.classList.add("hidden");
    } else {
        navSubItens2.classList.add("hidden");
        navChevU2.classList.add("hidden");
        navChevD2.classList.remove("hidden");
    }
});

mobileNavClick.addEventListener("click", (event) => {
    if (mobileMenu.classList.contains("hidden")) {
        mobileMenu.classList.add("hidden");
        content.classList.remove("hidden");
    } else {
        mobileMenu.classList.remove("hidden");
        content.classList.add("hidden");
    }
});
