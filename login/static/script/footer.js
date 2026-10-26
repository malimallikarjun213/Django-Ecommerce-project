
document.addEventListener("DOMContentLoaded", function () {
    const yearElement = document.getElementById("footer-year");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
});

