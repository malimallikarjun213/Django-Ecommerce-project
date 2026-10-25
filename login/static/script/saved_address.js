document.addEventListener("DOMContentLoaded", function () {

    const addButton = document.getElementById("addAddressBtn");
    const addressList = document.getElementById("addressList");
    const addressFormBox = document.getElementById("addressFormBox");
    const addressForm = document.getElementById("addressForm");
    const cancelButton = document.getElementById("cancelBtn");
    const formTitle = document.getElementById("formTitle");

    const addressId = document.getElementById("addressId");
    const fullName = document.getElementById("fullName");
    const phone = document.getElementById("phone");
    const fullAddress = document.getElementById("fullAddress");
    const city = document.getElementById("city");
    const state = document.getElementById("state");
    const pincode = document.getElementById("pincode");
    const addressType = document.getElementById("addressType");

    let addresses = [];

    // Load addresses from browser storage
    try {
        addresses = JSON.parse(
            localStorage.getItem("proshopAddresses") || "[]"
        );

        if (!Array.isArray(addresses)) {
            addresses = [];
        }
    } catch (error) {
        addresses = [];
    }

    // Save addresses in browser storage
    function saveAddresses() {
        try {
            localStorage.setItem(
                "proshopAddresses",
                JSON.stringify(addresses)
            );
            return true;
        } catch (error) {
            alert("Could not save addresses in this browser.");
            return false;
        }
    }

    // Show the form
    function showForm(address = null) {
        addressForm.reset();

        if (address) {
            formTitle.textContent = "Edit Address";

            addressId.value = address.id;
            fullName.value = address.name;
            phone.value = address.phone;
            fullAddress.value = address.address;
            city.value = address.city;
            state.value = address.state;
            pincode.value = address.pincode;
            addressType.value = address.type;
        } else {
            formTitle.textContent = "Add New Address";
            addressId.value = "";
        }

        addressFormBox.hidden = false;
        addressFormBox.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    // Hide the form
    function hideForm() {
        addressFormBox.hidden = true;
        addressForm.reset();
        addressId.value = "";
    }

    // Display all addresses
    function displayAddresses() {
        addressList.replaceChildren();

        if (addresses.length === 0) {
            const message = document.createElement("p");
            message.className = "empty-message";
            message.textContent = "No saved addresses yet.";
            addressList.appendChild(message);
            return;
        }

        addresses.forEach(function (address) {
            const card = document.createElement("div");
            card.className = "address-card";

            const type = document.createElement("span");
            type.className = "address-type";
            type.textContent = address.type;

            const heading = document.createElement("h3");
            heading.textContent = address.name;

            const phoneText = document.createElement("p");
            phoneText.textContent = "Phone: " + address.phone;

            const addressText = document.createElement("p");
            addressText.textContent = address.address;

            const locationText = document.createElement("p");
            locationText.textContent =
                address.city + ", " + address.state +
                " - " + address.pincode;

            const actions = document.createElement("div");
            actions.className = "address-actions";

            const editButton = document.createElement("button");
            editButton.type = "button";
            editButton.className = "edit-btn";
            editButton.textContent = "Edit";

            editButton.addEventListener("click", function () {
                showForm(address);
            });

            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.className = "delete-btn";
            deleteButton.textContent = "Delete";

            deleteButton.addEventListener("click", function () {
                if (confirm("Do you want to delete this address?")) {
                    addresses = addresses.filter(function (item) {
                        return item.id !== address.id;
                    });

                    if (saveAddresses()) {
                        displayAddresses();
                    }
                }
            });

            actions.appendChild(editButton);
            actions.appendChild(deleteButton);

            card.appendChild(type);
            card.appendChild(heading);
            card.appendChild(phoneText);
            card.appendChild(addressText);
            card.appendChild(locationText);
            card.appendChild(actions);

            addressList.appendChild(card);
        });
    }

    // Add new address button
    addButton.addEventListener("click", function () {
        showForm();
    });

    // Cancel button
    cancelButton.addEventListener("click", hideForm);

    // Save new address or update existing address
    addressForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!addressForm.reportValidity()) {
            return;
        }

        const existingId = addressId.value;

        const newAddress = {
            id: existingId || String(Date.now()),
            name: fullName.value.trim(),
            phone: phone.value.trim(),
            address: fullAddress.value.trim(),
            city: city.value.trim(),
            state: state.value.trim(),
            pincode: pincode.value.trim(),
            type: addressType.value
        };

        if (existingId) {
            addresses = addresses.map(function (item) {
                return item.id === existingId ? newAddress : item;
            });
        } else {
            addresses.push(newAddress);
        }

        if (saveAddresses()) {
            displayAddresses();
            hideForm();
        }
    });

    // Show saved addresses when page opens
    displayAddresses();

});