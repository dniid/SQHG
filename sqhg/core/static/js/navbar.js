document.addEventListener('DOMContentLoaded', function () {
// Desktop Constants
    // Open Sub-Items
    const openUserSubItems = document.getElementById("openUserSubItems");
    const openQuestionnairesSubItems = document.getElementById("openQuestionnairesSubItems");

    // Sub-Items
    const userSubItems = document.getElementById("userSubItems");
    const questionnairesSubItems = document.getElementById("questionnairesSubItems");

    // Sub-Items Icons
    const userChevronDown = document.getElementById("userChevronDown");
    const userChevronUp = document.getElementById("userChevronUp");
    const questionnairesChevronDown = document.getElementById("questionnairesChevronDown");
    const questionnairesChevronUp = document.getElementById("questionnairesChevronUp");

// Mobile Constants
    // Open Menu
    const mobileOpenMenu = document.getElementById("mobileOpenMenu");

    // Menu
    const mobileMenu = document.getElementById("mobileMenu");

    // Open Sub-Items
    const mobileOpenUserSubItems = document.getElementById("mobileOpenUserSubItems");
    const mobileOpenQuestionnairesSubItems = document.getElementById("mobileOpenQuestionnairesSubItems");

    // Sub-Items
    const mobileUserSubItems = document.getElementById("mobileUserSubItems");
    const mobileQuestionnairesSubItems = document.getElementById("mobileQuestionnairesSubItems");

    // Sub-Items Icons
    const mobileUserChevronDown = document.getElementById("mobileUserChevronDown");
    const mobileUserChevronUp = document.getElementById("mobileUserChevronUp");
    const mobileQuestionnairesChevronDown = document.getElementById("mobileQuestionnairesChevronDown");
    const mobileQuestionnairesChevronUp = document.getElementById("mobileQuestionnairesChevronUp");

// Base Constants
    // Body Content
    const bodyContent = document.getElementById("bodyContent");


// Desktop Functions
    // Open Sub-Items
    openUserSubItems.addEventListener("click", (event) => {
        if (userSubItems.classList.contains("hidden")) {
            userSubItems.classList.remove("hidden");
            userChevronUp.classList.remove("hidden");
            userChevronDown.classList.add("hidden");
        } else {
            userSubItems.classList.add("hidden");
            userChevronUp.classList.add("hidden");
            userChevronDown.classList.remove("hidden");
        }
    });

    openQuestionnairesSubItems.addEventListener("click", (event) => {
        if (questionnairesSubItems.classList.contains("hidden")) {
            questionnairesSubItems.classList.remove("hidden");
            questionnairesChevronUp.classList.remove("hidden");
            questionnairesChevronDown.classList.add("hidden");
        } else {
            questionnairesSubItems.classList.add("hidden");
            questionnairesChevronUp.classList.add("hidden");
            questionnairesChevronDown.classList.remove("hidden");
        }
    });

// Mobile Functions
    // Open Menu
    mobileOpenMenu.addEventListener("click", (event) => {
        if (mobileMenu.classList.contains("hidden")) {
            mobileMenu.classList.remove("hidden");
            bodyContent.classList.add("hidden");
        } else {
            mobileMenu.classList.add("hidden");
            bodyContent.classList.remove("hidden");
        }
    });

    // Open Sub-Items
    mobileOpenUserSubItems.addEventListener("click", (event) => {
        if (mobileUserSubItems.classList.contains("hidden")) {
            mobileUserSubItems.classList.remove("hidden");
            mobileUserChevronUp.classList.remove("hidden");
            mobileUserChevronDown.classList.add("hidden");
        } else {
            mobileUserSubItems.classList.add("hidden");
            mobileUserChevronUp.classList.add("hidden");
            mobileUserChevronDown.classList.remove("hidden");
        }
    });

    mobileOpenQuestionnairesSubItems.addEventListener("click", (event) => {
        if (mobileQuestionnairesSubItems.classList.contains("hidden")) {
            mobileQuestionnairesSubItems.classList.remove("hidden");
            mobileQuestionnairesChevronUp.classList.remove("hidden");
            mobileQuestionnairesChevronDown.classList.add("hidden");
        } else {
            mobileQuestionnairesSubItems.classList.add("hidden");
            mobileQuestionnairesChevronUp.classList.add("hidden");
            mobileQuestionnairesChevronDown.classList.remove("hidden");
        }
    });
});
