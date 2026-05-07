document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("search-input");
    const suggestionsBox = document.getElementById("search-suggestions");

    if (!searchInput || !suggestionsBox) {
        return;
    }

    searchInput.addEventListener("input", async () => {

        const query = searchInput.value.trim();

        if (!query) {
            suggestionsBox.innerHTML = "";
            return;
        }

        const response = await fetch(`/search-suggestions?q=${query}`);

        const books = await response.json();

        suggestionsBox.innerHTML = "";

        books.forEach(book => {

            const item = document.createElement("a");

            item.href = `/book/${book.id}`;

            item.classList.add("suggestion-item");

            const title = document.createElement("strong");
            title.textContent = book.title;

            const author = document.createElement("div");
            author.textContent = book.author;

            item.appendChild(title);
            item.appendChild(author);

            suggestionsBox.appendChild(item);

        });

    });

});