console.log("EDIT PROFILE JS LOADED");

document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("favorite-search");
    const suggestionsBox = document.getElementById("favorite-suggestions");
    const hiddenInput = document.getElementById("favorite-books-input");
    const grid = document.getElementById("favorite-books-grid");
    const searchPanel = document.getElementById(
        "favorite-search-panel"
    );

    if (
        !searchInput ||
        !suggestionsBox ||
        !hiddenInput ||
        !grid ||
        !searchPanel
    ) {
        return;
    }

    let debounceTimeout;

    // Store selected favorite books
    let favoriteBooks = window.initialFavoriteBooks || [];

    // Search input
    searchInput.addEventListener("input", () => {

        clearTimeout(debounceTimeout);

        debounceTimeout = setTimeout(async () => {

            const query = searchInput.value.trim();

            if (!query) {
                suggestionsBox.innerHTML = "";
                return;
            }

            const response = await fetch(
                `/search-suggestions?q=${query}`
            );

            const books = await response.json();

            renderSuggestions(books);

        }, 200);

    });

    // Render AJAX suggestions
    function renderSuggestions(books) {

        suggestionsBox.innerHTML = "";

        if (books.length === 0) {
            return;
        }

        books.forEach(book => {

            const item = document.createElement("div");

            item.classList.add("suggestion-item");

            item.innerHTML = `
                <strong>${book.title}</strong>
                <div>${book.author}</div>
            `;

            item.addEventListener("click", () => {
                addFavoriteBook(book);
            });

            suggestionsBox.appendChild(item);

        });

    }


    // Add book to favorites
    function addFavoriteBook(book) {


        // Limit to 4 books
        if (favoriteBooks.length >= 4) {
            return;
        }

        // Prevent duplicates
        const exists = favoriteBooks.some(
            favorite => favorite.id === book.id
        );

        if (exists) {
            return;
        }

        favoriteBooks.push(book);

        updateGrid();

        updateHiddenInput();

        suggestionsBox.innerHTML = "";
        searchInput.value = "";

        // Hide search panel
        searchPanel.classList.add("hidden");

    }

    // Update favorite books grid
    function updateGrid() {

        const slots = grid.querySelectorAll(".favorite-slot");

        slots.forEach((slot, index) => {

            slot.innerHTML = "";

            const book = favoriteBooks[index];

            // Empty slot
            if (!book) {

                slot.innerHTML = `
                    <div class="empty-slot">
                        +
                    </div>
                `;

                const emptySlot = slot.querySelector(
                    ".empty-slot"
                );

                emptySlot.addEventListener("click", () => {

                    console.log("PLUS CLICKED");

                    searchPanel.classList.remove("hidden");

                    searchInput.focus();

                });

                return;
            }

            // Book slot
            slot.innerHTML = `
                <img
                    src="${book.cover_url}"
                    class="favorite-book-cover"
                    alt="${book.title}"
                >

                <button
                    type="button"
                    class="remove-book-btn"
                    data-index="${index}"
                >
                    ✕
                </button>
            `;
        });

        bindRemoveButtons();

    }

    // Remove favorite book
    function bindRemoveButtons() {

        document
            .querySelectorAll(".remove-book-btn")
            .forEach(button => {

                button.addEventListener("click", () => {

                    const index = button.dataset.index;

                    favoriteBooks.splice(index, 1);

                    updateGrid();

                    updateHiddenInput();

                });

            });

    }

    // Update hidden input
    function updateHiddenInput() {

        hiddenInput.value = favoriteBooks
            .map(book => book.id)
            .join(",");

    }

    // Close suggestions when clicking outside
    document.addEventListener("click", (event) => {

        if (
            !searchInput.contains(event.target)
            &&
            !suggestionsBox.contains(event.target)
        ) {
            suggestionsBox.innerHTML = "";
        }

    });

    // Initial render
    updateGrid();
    updateHiddenInput();

    const avatarUpload = document.getElementById("avatar-upload");

    const avatarTrigger = document.getElementById("avatar-trigger");

    const avatarPreview = document.getElementById("profile-avatar-preview");

    if (avatarUpload && avatarPreview) {

        avatarUpload.addEventListener("change", function(event) {

            const file = event.target.files[0];

            if (file) {

                const reader = new FileReader();

                reader.onload = function(e) {

                    avatarPreview.src = e.target.result;

                };

                reader.readAsDataURL(file);
            }
        });

        avatarTrigger.addEventListener("click", () => {
           avatarUpload.click();
        });
    }

});