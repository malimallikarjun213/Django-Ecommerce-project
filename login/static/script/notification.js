
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("notificationForm");
    const masterToggle = document.getElementById("masterToggle");
    const toggles = [
        ...document.querySelectorAll(".notification-toggle")
    ];
    const resetButton = document.getElementById("resetButton");
    const status = document.getElementById("notificationStatus");

    // Defaults match the Django model.
    const defaults = {
        order_updates: true,
        offers_deals: true,
        wishlist_alerts: true,
        personalized_recommendations: true,
        security_alerts: true,
        email_notifications: true,
        sms_notifications: false,
        push_notifications: false
    };

    function updateMaster() {
        masterToggle.checked = toggles.every(
            toggle => toggle.checked
        );

        masterToggle.indeterminate =
            !masterToggle.checked &&
            toggles.some(toggle => toggle.checked);
    }

    function updateStatus() {
        const enabled = toggles.filter(
            toggle => toggle.checked
        ).length;

        status.textContent = enabled === toggles.length
            ? "All notifications enabled"
            : enabled === 0
                ? "All optional notifications off"
                : `${enabled} notification preferences enabled`;
    }

    masterToggle.addEventListener("change", function () {
        toggles.forEach(toggle => {
            toggle.checked = masterToggle.checked;
        });

        updateMaster();
        updateStatus();
    });

    toggles.forEach(toggle => {
        toggle.addEventListener("change", function () {
            updateMaster();
            updateStatus();
        });
    });

    resetButton.addEventListener("click", function () {
        toggles.forEach(toggle => {
            toggle.checked = defaults[toggle.name];
        });

        updateMaster();
        updateStatus();

        // Submit defaults to Django and save them in the database.
        form.requestSubmit();
    });

    updateMaster();
    updateStatus();
});


document.querySelectorAll(".success-alert").forEach(function (alert) {
    setTimeout(function () {
        if (alert.isConnected) {
            alert.style.transition = "opacity 0.3s ease";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 300);
        }
    }, 3500);
});
