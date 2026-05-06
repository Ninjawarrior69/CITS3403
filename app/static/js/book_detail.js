console.log("JS LOADED");

let selectedRating = 0;

function toggleSection(id, button) {
    const section = document.getElementById(id);

    if (section.classList.contains("collapsed")) {
        section.classList.remove("collapsed");
        button.innerText = "Show Less";
    } else {
        section.classList.add("collapsed");
        button.innerText = "Show More";
    }
}

function toggleFollow(btn) {
    if (btn.innerText === "Follow") {
        btn.innerText = "Following";
    } else {
        btn.innerText = "Follow";
    }
}


document.addEventListener("DOMContentLoaded", () => {
    const ratingBox = document.getElementById("rating");
    const ratingStars = document.querySelectorAll("#rating span");

    const ratingInput = document.getElementById("rating-stars");
    const reviewRatingInput = document.getElementById("review-stars");

    const ratingForm = document.getElementById("rating-form");
    const reviewForm = document.getElementById("review-form");
    const reviewInput = document.getElementById("review-input");

    if (!ratingBox || ratingStars.length === 0) {
        return;
    }

    selectedRating = Number(ratingBox.dataset.currentRating || 0);
    
    if (ratingInput) {
        ratingInput.value = selectedRating;
    }

    if (reviewRatingInput) {
        reviewRatingInput.value = selectedRating;
    }

    updateStars(selectedRating, ratingStars);

    ratingStars.forEach((star) => {
        star.addEventListener("mouseenter", () => {
            updateStars(Number(star.dataset.value), ratingStars);
        });

        star.addEventListener("click", () => {
            const clickedRating = Number(star.dataset.value);

            if (selectedRating === clickedRating) {
                selectedRating = 0;
            } else {
                selectedRating = clickedRating;
            }

            if (ratingInput) {
                ratingInput.value = selectedRating;
            }

            if (reviewRatingInput) {
                reviewRatingInput.value = selectedRating;
            }

            updateStars(selectedRating, ratingStars);
        });
    });

    ratingBox.addEventListener("mouseleave", () => {
        updateStars(selectedRating, ratingStars);
    });

    if (ratingForm) {
        ratingForm.addEventListener("submit", (event) => {
            if (selectedRating === 0) {
                event.preventDefault();
                alert("Please choose a rating first.");
            }
        });
    }

    if (reviewForm) {
        reviewForm.addEventListener("submit", (event) => {
            const reviewText = reviewInput.value.trim();

            if (selectedRating === 0) {
                event.preventDefault();
                alert("Please rate the book before posting a review.");
                return;
            }

            if (reviewText === "") {
                event.preventDefault();
                alert("Please write something before posting your review.");
            }
        });
    }
});

function updateStars(value, stars) {
    stars.forEach((star) => {
        if (Number(star.dataset.value) <= value) {
            star.innerText = "★";
        } else {
            star.innerText = "☆";
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const openBtn = document.getElementById("openShelfModal");
  const modal = document.getElementById("shelfModal");
  const closeBtn = document.getElementById("closeShelfModal");

  if (!openBtn || !modal || !closeBtn) {
    return;
  }

  openBtn.addEventListener("click", function () {
    modal.classList.add("show");
  });

  closeBtn.addEventListener("click", function () {
    modal.classList.remove("show");
  });

  modal.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.classList.remove("show");
    }
  });
});