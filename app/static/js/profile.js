// Buttons
const followersBtn = document.querySelectorAll(".btn-follow")[0];
const followingBtn = document.querySelectorAll(".btn-follow")[1];

// Modal elements
const modal = document.getElementById("modal");
const closeModal = document.getElementById("close-modal");
const modalTitle = document.getElementById("modal-title");
const modalList = document.getElementById("modal-list");

// Example data (replace with backend data later)
const followers = ["Alice", "Bob", "Charlie", "Diana"];
const following = ["Eve", "Frank", "Grace", "Hannah"];

// Function to open modal
function openModal(title, list) {
    modalTitle.textContent = title;
    modalList.innerHTML = "";
    list.forEach(user => {
        const li = document.createElement("li");
        li.textContent = user;
        modalList.appendChild(li);
    });
    modal.style.display = "block";
}

// Event listeners
followersBtn.addEventListener("click", () => openModal("Followers", followers));
followingBtn.addEventListener("click", () => openModal("Following", following));

closeModal.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
});