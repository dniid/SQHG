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

const mobileNavClick1 = document.getElementById("mobile-nav-click-1");
const mobileNavClick2 = document.getElementById("mobile-nav-click-2");
const mobileNavSubItens1 = document.getElementById("mobile-nav-sub-items-1");
const mobileNavSubItens2 = document.getElementById("mobile-nav-sub-items-2");
const mobileNavChevD1 = document.getElementById("mobile-nav-chevron-down-1");
const mobileNavChevD2 = document.getElementById("mobile-nav-chevron-down-2");
const mobileNavChevU1 = document.getElementById("mobile-nav-chevron-up-1");
const mobileNavChevU2 = document.getElementById("mobile-nav-chevron-up-2");


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
        mobileMenu.classList.remove("hidden");
        content.classList.add("hidden");
    } else {
        mobileMenu.classList.add("hidden");
        content.classList.remove("hidden");
    }
});

mobileNavClick1.addEventListener("click", (event) => {
    if (mobileNavSubItens1.classList.contains("hidden")) {
        mobileNavSubItens1.classList.remove("hidden");
        mobileNavChevU1.classList.remove("hidden");
        mobileNavChevD1.classList.add("hidden");
    } else {
        mobileNavSubItens1.classList.add("hidden");
        mobileNavChevU1.classList.add("hidden");
        mobileNavChevD1.classList.remove("hidden");
    }
});

mobileNavClick2.addEventListener("click", (event) => {
    if (mobileNavSubItens2.classList.contains("hidden")) {
        mobileNavSubItens2.classList.remove("hidden");
        mobileNavChevU2.classList.remove("hidden");
        mobileNavChevD2.classList.add("hidden");
    } else {
        mobileNavSubItens2.classList.add("hidden");
        mobileNavChevU2.classList.add("hidden");
        mobileNavChevD2.classList.remove("hidden");
    }
});