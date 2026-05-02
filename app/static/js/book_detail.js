console.log("JS LOADED");

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

// fake data
function toggleRead(btn) {
    if (!btn.dataset.count) {
        const randomCount = Math.floor(Math.random() * 200) + 50;
        btn.dataset.count = randomCount;
    }

    let count = parseInt(btn.dataset.count);

    if (btn.classList.contains("active")) {
        btn.classList.remove("active");
        btn.innerText = "Want to Read";
    } else {
        btn.classList.add("active");
        btn.innerText = `✓ Added · ${count + 1} readers`;
    }
}

function postReview() {
    const text = document.getElementById("review-input").value.trim();

    if (text === "") {
        alert("Please write something!");
        return;
    }

    if (selectedRating === 0) {
        alert("Please rate the book first!");
        return;
    }

    const div = document.createElement("div");
    div.classList.add("review-item");

    div.innerHTML = `
        <p><strong>You</strong> - ${"★".repeat(selectedRating)}</p>
        <p>${text}</p>
        <hr>
    `;

    document.getElementById("review-list").prepend(div);

    document.getElementById("review-input").value = "";

    selectedRating = 0;
    showStars(0);
}

document.addEventListener("DOMContentLoaded", () => {

    let selectedRating = 0;
    const stars = document.querySelectorAll("#rating span");

    stars.forEach((star, index) => {

        star.addEventListener("mouseenter", () => {
            showStars(index + 1);
        });

        document.getElementById("rating").addEventListener("mouseleave", () => {
            showStars(selectedRating);
        });


        star.addEventListener("click", () => {

            if (selectedRating === index + 1) {
                selectedRating = 0;
            } else {
                selectedRating = index + 1;
            }

            showStars(selectedRating);
        });
    });

    function showStars(rating) {
        stars.forEach((s, i) => {
            s.innerText = i < rating ? "★" : "☆";
        });
    }

});