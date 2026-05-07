document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("search-input");
    const suggestionsBox = document.getElementById("search-suggestions");
    const searchWrapper = document.querySelector(".search-wrapper");

    if (!searchInput || !suggestionsBox || !searchWrapper) {
        return;
    }

    let debounceTimeout;

    searchInput.addEventListener("input", () => {

        clearTimeout(debounceTimeout);

        debounceTimeout = setTimeout(async () => {

            const query = searchInput.value.trim();

            if (!query) {
                suggestionsBox.innerHTML = "";
                return;
            }

            const response = await fetch(`/search-suggestions?q=${query}`);

            const books = await response.json();

            suggestionsBox.innerHTML = "";

            if (books.length === 0) {

                const searchAll = document.createElement("a");

                searchAll.href = `/search?q=${query}`;

                searchAll.classList.add(
                    "suggestion-item",
                    "suggestion-search-all"
                );

                searchAll.textContent = `Search for "${query}"...`;

                suggestionsBox.appendChild(searchAll);

                return;
            }

            books.forEach(book => {

                const item = document.createElement("a");

                item.href = `/import-book?olid=${encodeURIComponent(book.openlibrary_id)}`;

                item.classList.add("suggestion-item");

                const title = document.createElement("strong");
                title.textContent = book.title;

                const author = document.createElement("div");
                author.textContent = book.author;

                item.appendChild(title);
                item.appendChild(author);

                suggestionsBox.appendChild(item);

            });

        }, 200);

    });

    document.addEventListener("click", (event) => {

        if (!searchWrapper.contains(event.target)) {
            suggestionsBox.innerHTML = "";
        }

    });

});