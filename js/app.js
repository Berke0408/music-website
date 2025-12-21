document.querySelectorAll(".acc-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    btn.classList.toggle("open");
  });
});
