
document.querySelectorAll(".toggle-password").forEach(function (button) {
    button.addEventListener("click", function () {
        const input = document.getElementById(this.dataset.target);

        if (!input) return;

        const showPassword = input.type === "password";

        input.type = showPassword ? "text" : "password";

        this.textContent = showPassword ? "Hide" : "Show";
    });
});
