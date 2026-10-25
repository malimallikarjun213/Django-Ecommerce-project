

document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const navContent = document.getElementById("navContent");

    const profileToggle = document.getElementById("profileToggle");
    const profileDropdown = document.getElementById("profileDropdown");
    const profileMenu = document.querySelector(".profile-menu");

    // Open and close the mobile navigation
    if (menuToggle && navContent) {
        menuToggle.addEventListener("click", function () {
            const isOpen = navContent.classList.toggle("open");

            menuToggle.textContent = isOpen ? "✕" : "☰";
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        // Close mobile menu when a navigation link is selected
        document.querySelectorAll(".nav-links a").forEach(function (link) {
            link.addEventListener("click", function () {
                navContent.classList.remove("open");
                menuToggle.textContent = "☰";
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });

        // Reset menu on larger screens
        window.addEventListener("resize", function () {
            if (window.innerWidth > 650) {
                navContent.classList.remove("open");
                menuToggle.textContent = "☰";
                menuToggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    // Open and close the profile dropdown
    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener("click", function (event) {
            event.stopPropagation();

            const isOpen = profileDropdown.classList.toggle("show");
            profileToggle.setAttribute("aria-expanded", String(isOpen));
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function (event) {
            if (
                profileMenu &&
                !profileMenu.contains(event.target)
            ) {
                closeProfileDropdown();
            }
        });

        function closeProfileDropdown() {
            profileDropdown.classList.remove("show");
            profileToggle.setAttribute("aria-expanded", "false");
        }
    }
});




const indicator = document.getElementById("navIndicator");
const links = document.querySelectorAll(".nav-link");

let activeLink = document.querySelector(".nav-link.active");


function moveIndicator(link, animate = true) {
    if (!link) return;

    indicator.style.transition = animate
        ? "left 0.3s ease, width 0.3s ease"
        : "none";

    indicator.style.left = link.offsetLeft + "px";
    indicator.style.width = link.offsetWidth + "px";
    indicator.style.opacity = "1";
}

// Show the white shadow button on Home immediately
window.addEventListener("load", () => {
    moveIndicator(activeLink, false);
});

links.forEach(link => {
    link.addEventListener("click", function(event) {
        if (this.getAttribute("href") === "#") {
            event.preventDefault();
        }

        links.forEach(item => item.classList.remove("active"));

        this.classList.add("active");
        activeLink = this;

        moveIndicator(this, true);
    });
});

