
document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".recent-slider");
    const track = document.querySelector(".recent-track");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");

    if (!slider || !track || !prevBtn || !nextBtn) {
        return;
    }

    function getScrollAmount() {
        const card = track.querySelector(".recent-card");

        if (!card) return slider.clientWidth;

        const trackStyle = window.getComputedStyle(track);
        const gap = parseFloat(trackStyle.gap) || 0;

        return card.getBoundingClientRect().width + gap;
    }

    function updateButtons() {
        const maxScroll = slider.scrollWidth - slider.clientWidth;

        prevBtn.disabled = slider.scrollLeft <= 2;
        nextBtn.disabled = slider.scrollLeft >= maxScroll - 2;
    }

    nextBtn.addEventListener("click", function () {
        slider.scrollBy({
            left: getScrollAmount(),
            behavior: "smooth"
        });
    });

    prevBtn.addEventListener("click", function () {
        slider.scrollBy({
            left: -getScrollAmount(),
            behavior: "smooth"
        });
    });

    slider.addEventListener("scroll", updateButtons);
    window.addEventListener("resize", updateButtons);

    updateButtons();
});
