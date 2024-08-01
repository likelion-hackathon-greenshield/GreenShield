document.addEventListener("DOMContentLoaded", function () {
  const bars = document.querySelectorAll(".bar1 .bar");
  bars.forEach((bar) => {
    const score = bar.getAttribute("data-score");
    if (score) {
      const height = (score - 1) * 64; // 1점에 64px
      bar.style.height = `${height}px`;
    }
  });
});
