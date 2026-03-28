// Animación de entrada en cards
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".product-card");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
          }, i * 60);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  cards.forEach((card) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(24px)";
    card.style.transition = "opacity .4s ease, transform .4s ease, border-color .25s, box-shadow .25s";
    observer.observe(card);
  });
});
