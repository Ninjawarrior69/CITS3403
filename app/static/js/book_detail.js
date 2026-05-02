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
    const text = document.getElementById("review-text").value;

    if (!text) return;

    const div = document.createElement("div");
    div.classList.add("review-item");
    div.innerText = text;

    document.getElementById("review-list").prepend(div);
}