
/* =====================================
   PROSHOP PROFILE PAGE
   ===================================== */

// Profile elements
const editBtn = document.getElementById("editBtn");
const editModal = document.getElementById("editModal");
const closeBtn = document.getElementById("closeBtn");
const cancelBtn = document.getElementById("cancelBtn");
const profileForm = document.getElementById("profileForm");
const photoInput = document.getElementById("photoInput");
const profilePhoto = document.getElementById("profilePhoto");
const passwordBtn = document.getElementById("passwordBtn");

// Profile fields
const fields = [
    "name",
    "username",
    "email",
    "phone",
    "dob",
    "gender",
    "address",
    "city",
    "state",
    "pin",
    "country"
];

// Default profile data
const defaults = {
    name: "",
    username: "",
    email: "",
    phone: "",
    dob: "",
    gender: "",
    address: "",
    city: "",
    state: "",
    pin: "",
    country: "India"
};

let profile = { ...defaults };

/* =====================================
   LOAD PROFILE
   ===================================== */

function loadProfile() {
    try {
        const saved = localStorage.getItem("proshopProfile");

        if (saved) {
            const parsed = JSON.parse(saved);

            fields.forEach(key => {
                if (typeof parsed[key] === "string") {
                    profile[key] = parsed[key];
                }
            });
        }

        const savedPhoto = localStorage.getItem("proshopPhoto");

        if (savedPhoto && profilePhoto) {
            profilePhoto.src = savedPhoto;
        }
    } catch (error) {
        console.warn("Could not load saved profile.", error);
    }

    renderProfile();
}

/* =====================================
   DISPLAY PROFILE DATA
   ===================================== */

function renderProfile() {
    const displayValues = {
        displayName: profile.name || "Your Name",
        displayEmail: profile.email || "Email not added",
        nameValue: profile.name || "Not added yet",
        usernameValue: profile.username || "Not added yet",
        accountUsername: profile.username || "Not added yet",
        emailValue: profile.email || "Not added yet",
        phoneValue: profile.phone || "Not added yet",
        dobValue: profile.dob || "Not added yet",
        genderValue: profile.gender || "Not specified",
        addressValue: profile.address || "Not added yet",
        cityValue: profile.city || "Not added yet",
        stateValue: profile.state || "Not added yet",
        pinValue: profile.pin || "Not added yet",
        countryValue: profile.country || "Not added yet"
    };

    Object.entries(displayValues).forEach(([id, value]) => {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    });
}

/* =====================================
   OPEN AND CLOSE EDIT PROFILE MODAL
   ===================================== */

function openModal() {
    if (!editModal || !profileForm) return;

    fields.forEach(key => {
        const input = document.getElementById(key + "Input");

        if (input) {
            input.value = profile[key] || "";
        }
    });

    editModal.classList.add("show");
    document.body.style.overflow = "hidden";
}

function closeModal() {
    if (!editModal) return;

    editModal.classList.remove("show");
    document.body.style.overflow = "";
}

if (editBtn) {
    editBtn.addEventListener("click", openModal);
}

if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
}

if (cancelBtn) {
    cancelBtn.addEventListener("click", closeModal);
}

// Close when clicking outside the modal
if (editModal) {
    editModal.addEventListener("click", function(event) {
        if (event.target === editModal) {
            closeModal();
        }
    });
}

// Close when pressing Escape
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeModal();
    }
});

/* =====================================
   SAVE PROFILE CHANGES
   ===================================== */

if (profileForm) {
    profileForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const updatedProfile = {};

        fields.forEach(key => {
            const input = document.getElementById(key + "Input");

            updatedProfile[key] = input
                ? input.value.trim()
                : "";
        });

        if (
            !updatedProfile.name ||
            !updatedProfile.username ||
            !updatedProfile.email
        ) {
            alert("Please fill in your name, username and email.");
            return;
        }

        profile = updatedProfile;

        renderProfile();

        try {
            localStorage.setItem(
                "proshopProfile",
                JSON.stringify(profile)
            );

            closeModal();
            alert("Profile updated successfully!");
        } catch (error) {
            closeModal();

            alert(
                "Profile updated on this page, but could not be saved in browser storage."
            );
        }
    });
}

/* =====================================
   UPLOAD PROFILE PHOTO
   ===================================== */

if (photoInput && profilePhoto) {
    photoInput.addEventListener("change", function() {
        const file = photoInput.files[0];

        if (!file) return;

        if (!file.type.startsWith("image/")) {
            alert("Please select an image file.");
            photoInput.value = "";
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            alert("Please select an image smaller than 2 MB.");
            photoInput.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function() {
            profilePhoto.src = reader.result;

            try {
                localStorage.setItem("proshopPhoto", reader.result);
                alert("Profile photo updated!");
            } catch (error) {
                alert(
                    "Photo updated for this session, but could not be saved in browser storage."
                );
            }
        };

        reader.onerror = function() {
            alert("Could not read this image. Please try another one.");
        };

        reader.readAsDataURL(file);
        photoInput.value = "";
    });
}

/* =====================================
   CHANGE PASSWORD DEMO
   ===================================== */

if (passwordBtn) {
    passwordBtn.addEventListener("click", function() {
        alert(
            "Password changing will be connected when authentication is added."
        );
    });
}

/* =====================================
   SIDEBAR MOVING INDICATOR
   ===================================== */

const nav = document.querySelector(".sidebar nav");
const indicator = document.getElementById("navIndicator");
const links = document.querySelectorAll(".sidebar .nav-link");

let activeLink = document.querySelector(
    ".sidebar .nav-link.active"
);

// Move the blue background behind a sidebar link
function moveIndicator(link, animate = true) {
    if (!nav || !indicator || !link) return;

    const navRect = nav.getBoundingClientRect();
    const linkRect = link.getBoundingClientRect();

    indicator.style.transition = animate
        ? "top 0.3s ease, left 0.3s ease, width 0.3s ease, height 0.3s ease"
        : "none";

    indicator.style.top =
        (linkRect.top - navRect.top + nav.scrollTop) + "px";

    indicator.style.left =
        (linkRect.left - navRect.left + nav.scrollLeft) + "px";

    indicator.style.width = linkRect.width + "px";
    indicator.style.height = linkRect.height + "px";
    indicator.style.opacity = "1";
}

// Initialize the indicator on the active link
function initializeIndicator() {
    if (!links.length || !indicator || !nav) return;

    if (!activeLink) {
        activeLink = links[0];
        activeLink.classList.add("active");
    }

    moveIndicator(activeLink, false);
}

// Move the indicator when a sidebar link is clicked
links.forEach(link => {
    link.addEventListener("click", function(event) {
        // Current links use href="#", so prevent page jumping
        if (this.getAttribute("href") === "#") {
            event.preventDefault();
        }

        links.forEach(item => {
            item.classList.remove("active");
        });

        this.classList.add("active");
        activeLink = this;

        moveIndicator(this, true);
    });
});

// Set the initial indicator position
if (document.readyState === "complete") {
    initializeIndicator();
} else {
    window.addEventListener("load", initializeIndicator);
}

// Keep the indicator correctly positioned after resizing
window.addEventListener("resize", function() {
    moveIndicator(activeLink, false);
});

/* =====================================
   START THE PROFILE PAGE
   ===================================== */

loadProfile();
