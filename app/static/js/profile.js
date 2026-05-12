// Buttons
const followersBtn = document.getElementById("followers-btn");
const followingBtn = document.getElementById("following-btn");

// Modal elements
const modal = document.getElementById("modal");
const closeModal = document.getElementById("close-modal");
const modalTitle = document.getElementById("modal-title");
const modalList = document.getElementById("modal-list");

// Get username from page
const username = document
    .getElementById("profile-data")
    .dataset.username;


// Open modal
function openModal(title, users) {
    modalTitle.textContent = title;
    modalList.innerHTML = "";

    users.forEach(user => {
        const li = document.createElement("li");

        li.innerHTML = `
            <div class="user-row">
                ${user.avatar
                    ? `<img src="/static/${user.avatar}" class="avatar">`
                    : `<div class="avatar avatar-placeholder"></div>`
                }
                <span>${user.username}</span>
            </div>
        `;

        modalList.appendChild(li);
    });

    modal.style.display = "block";
}


// Fetch followers
async function loadFollowers() {
    const response = await fetch(`/profile/followers`); //`/users/${username}/followers`
    const data = await response.json();

    openModal("Followers", data);
}


// Fetch following
async function loadFollowing() {
    const response = await fetch(`/profile/following`);
    const data = await response.json();

    openModal("Following", data);
}


// Event listeners
followersBtn.addEventListener("click", loadFollowers);
followingBtn.addEventListener("click", loadFollowing);

closeModal.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});