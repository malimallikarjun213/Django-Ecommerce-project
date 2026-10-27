
document.addEventListener("DOMContentLoaded", function () {
    const cartProducts = document.getElementById("cartProducts");

    function updateCartTotals() {
        const items = document.querySelectorAll(".cart-item");

        let totalItems = 0;
        let totalAmount = 0;

        items.forEach(function (item) {
            const price = Number(item.dataset.price) || 0;
            const quantityElement = item.querySelector(".quantity-value");
            const quantity = Number(quantityElement.textContent) || 0;
            const subtotal = price * quantity;

            item.querySelector(".subtotal-value").textContent =
                subtotal.toLocaleString("en-IN", {
                    maximumFractionDigits: 2
                });

            totalItems += quantity;
            totalAmount += subtotal;
        });

        const formattedTotal = "₹" + totalAmount.toLocaleString("en-IN", {
            maximumFractionDigits: 2
        });

        document.getElementById("totalItems").textContent = totalItems;
        document.getElementById("summaryItems").textContent = totalItems;
        document.getElementById("headerTotal").textContent = formattedTotal;
        document.getElementById("summarySubtotal").textContent = formattedTotal;
        document.getElementById("summaryTotal").textContent = formattedTotal;
    }

    cartProducts.addEventListener("click", function (event) {
        const button = event.target.closest("button");

        if (!button) return;

        const item = button.closest(".cart-item");

        if (!item) return;

        const quantityElement = item.querySelector(".quantity-value");

        if (button.classList.contains("increase")) {
            quantityElement.textContent =
                Number(quantityElement.textContent) + 1;

            updateCartTotals();
        }

        if (button.classList.contains("decrease")) {
            const quantity = Number(quantityElement.textContent);

            if (quantity > 1) {
                quantityElement.textContent = quantity - 1;
                updateCartTotals();
            }
        }

        if (button.classList.contains("remove-btn")) {
            const confirmed = confirm(
                "Are you sure you want to remove this product from your cart?"
            );

            if (confirmed) {
                /*
                 * This removes the row from the current page only.
                 * Connect this action to your Django remove-cart view
                 * to delete the item from the actual cart.
                 */
                item.remove();

                updateCartTotals();

                if (!document.querySelector(".cart-item")) {
                    location.reload();
                }
            }
        }
    });

    const placeOrderBtn = document.getElementById("placeOrderBtn");

    if (placeOrderBtn) {
        placeOrderBtn.addEventListener("click", function () {
            alert(
                "Connect this button to your Django checkout or place-order URL."
            );
        });
    }

    updateCartTotals();
});
