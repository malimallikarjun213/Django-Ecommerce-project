
document.addEventListener("DOMContentLoaded", function () {
    const viewport = document.getElementById("techViewport");
    const track = document.getElementById("techTrack");
    const prevButton = document.getElementById("techPrev");
    const nextButton = document.getElementById("techNext");

    if (!viewport || !track || !prevButton || !nextButton) {
        return;
    }

    function getScrollAmount() {
        const card = track.querySelector(".tech-card");

        if (!card) return viewport.clientWidth;

        const trackStyle = getComputedStyle(track);
        const gap = parseFloat(trackStyle.columnGap) || 0;

        return card.getBoundingClientRect().width + gap;
    }

    function updateArrows() {
        const maxScroll = viewport.scrollWidth - viewport.clientWidth;

        prevButton.style.display =
            viewport.scrollLeft <= 2 ? "none" : "flex";

        nextButton.style.display =
            viewport.scrollLeft >= maxScroll - 2 ? "none" : "flex";
    }

    nextButton.addEventListener("click", function () {
        viewport.scrollBy({
            left: getScrollAmount(),
            behavior: "smooth"
        });
    });

    prevButton.addEventListener("click", function () {
        viewport.scrollBy({
            left: -getScrollAmount(),
            behavior: "smooth"
        });
    });

    viewport.addEventListener("scroll", updateArrows, {
        passive: true
    });

    window.addEventListener("resize", updateArrows);

    if ("ResizeObserver" in window) {
        new ResizeObserver(updateArrows).observe(track);
    }

    updateArrows();
});
