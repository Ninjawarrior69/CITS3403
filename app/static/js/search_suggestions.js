document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const searchTypeSelect = document.getElementById("search-type");
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
      const searchType = searchTypeSelect ? searchTypeSelect.value : "books";

      if (!query) {
        suggestionsBox.innerHTML = "";
        return;
      }

      const response = await fetch(
        `/search-suggestions?q=${query}&type=${searchType}`,
      );

      const results = await response.json();

      suggestionsBox.innerHTML = "";

      if (results.length === 0) {
        const searchAll = document.createElement("a");

        searchAll.href = `/search?q=${query}&type=${searchType}`;

        searchAll.classList.add("suggestion-item", "suggestion-search-all");

        searchAll.textContent = `Search for "${query}"...`;

        suggestionsBox.appendChild(searchAll);

        return;
      }

      results.forEach((item) => {
        const suggestionItem = document.createElement("a");

        if (searchType === "users") {
          // Handle user suggestions
          suggestionItem.href = `/profile/${item.id}`;
          suggestionItem.classList.add("suggestion-item");

          const title = document.createElement("strong");
          title.textContent = item.username;

          const name = document.createElement("div");
          name.textContent = item.name || "";

          suggestionItem.appendChild(title);
          if (item.name) {
            suggestionItem.appendChild(name);
          }
        } else {
          // Handle book suggestions
          if (item.id) {
            suggestionItem.href = `/book/${item.id}`;
          } else {
            const params = new URLSearchParams({
              title: item.title || "",
              author: item.author || "",
              cover: item.cover_url || "",
            });

            if (item.openlibrary_id) {
              params.set("olid", item.openlibrary_id);
            }

            suggestionItem.href = `/import-book?${params.toString()}`;
          }

          suggestionItem.classList.add("suggestion-item");

          const title = document.createElement("strong");
          title.textContent = item.title;

          const author = document.createElement("div");
          author.textContent = item.author;

          suggestionItem.appendChild(title);
          suggestionItem.appendChild(author);
        }

        suggestionsBox.appendChild(suggestionItem);
      });
    }, 200);
  });

  document.addEventListener("click", (event) => {
    if (!searchWrapper.contains(event.target)) {
      suggestionsBox.innerHTML = "";
    }
  });
});
