function toggleSection(id, button) {
  const section = document.getElementById(id);

  if (section.classList.contains("review-collapsed")) {
    section.classList.remove("review-collapsed");
    button.innerText = "Show Less";
  } else {
    section.classList.add("review-collapsed");
    button.innerText = "Show More";
  }
}

function toggleReviewEdit(formId, displayId) {
  const form = document.getElementById(formId);
  const display = document.getElementById(displayId);

  if (!form || !display) return;

  form.classList.toggle("d-none");
  display.classList.toggle("d-none");
}

document.querySelectorAll(".my-review-edit-form").forEach((form) => {
  const stars = form.querySelectorAll(".my-review-star");
  const input = form.querySelector(".my-review-stars-input");

  function updateStars(value) {
    input.value = value;

    stars.forEach((star) => {
      const starValue = Number(star.dataset.value);
      star.textContent = starValue <= value ? "★" : "☆";
    });
  }

  stars.forEach((star) => {
    star.addEventListener("click", () => {
      updateStars(Number(star.dataset.value));
    });
  });
});