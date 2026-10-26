
const helpSearch = document.getElementById("helpSearch");
const faqItems = document.querySelectorAll(".faq-item");
const helpCards = document.querySelectorAll(".help-card");

helpSearch.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();

    faqItems.forEach(function (item) {
        item.style.display = item.textContent
            .toLowerCase()
            .includes(query) ? "" : "none";
    });

    helpCards.forEach(function (card) {
        card.style.display = card.textContent
            .toLowerCase()
            .includes(query) ? "" : "none";
    });
});
