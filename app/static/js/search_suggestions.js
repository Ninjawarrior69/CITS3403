document.addEventListener("DOMContentLoaded", () => {
  // Support multiple search bars on the same page
  const searchWrappers = document.querySelectorAll(".search-wrapper");

  searchWrappers.forEach((searchWrapper) => {
    const searchInput = searchWrapper.querySelector(".search-input");
    const suggestionsBox = searchWrapper.querySelector(".search-suggestions");

    const searchTypeInput =
      searchWrapper.querySelector(".search-type-input") ||
      searchWrapper.querySelector("#search-type-input");

    const searchTypeButton = searchWrapper.querySelector("#search-type-button");
    const searchTypeMenu = searchWrapper.querySelector("#search-type-menu");
    const searchTypeLabel = searchWrapper.querySelector("#search-type-label");
    const searchTypeOptions = searchWrapper.querySelectorAll(".search-type-option");

    if (!searchInput || !suggestionsBox || !searchTypeInput) {
      return;
    }

    let debounceTimeout;

    const getSearchType = () => searchTypeInput.value || "books";

    const updatePlaceholder = () => {
      const type = getSearchType();

      if (type === "users") {
        searchInput.placeholder = "Search users...";
        searchInput.setAttribute("aria-label", "Search users");
      } else {
        searchInput.placeholder = "Search books or authors...";
        searchInput.setAttribute("aria-label", "Search books or authors");
      }
    };

    const clearSuggestions = () => {
      suggestionsBox.innerHTML = "";
    };

    const closeMenu = () => {
      if (searchTypeMenu && searchTypeButton) {
        searchTypeMenu.hidden = true;
        searchTypeButton.setAttribute("aria-expanded", "false");
      }
    };

    const toggleMenu = () => {
      if (!searchTypeMenu || !searchTypeButton) {
        return;
      }

      const shouldOpen = searchTypeMenu.hidden;
      searchTypeMenu.hidden = !shouldOpen;
      searchTypeButton.setAttribute("aria-expanded", shouldOpen.toString());
    };

    // Handle navbar search type dropdown
    searchTypeOptions.forEach((option) => {
      option.addEventListener("click", (event) => {
        event.preventDefault();

        const value = option.dataset.value;
        searchTypeInput.value = value;

        if (searchTypeLabel) {
          searchTypeLabel.textContent = option.textContent;
        }

        searchTypeOptions.forEach((opt) => {
          opt.setAttribute("aria-selected", opt === option);
        });

        updatePlaceholder();
        closeMenu();
        clearSuggestions();
        searchInput.focus();
      });
    });

    if (searchTypeButton) {
      searchTypeButton.addEventListener("click", (event) => {
        event.preventDefault();
        toggleMenu();
      });
    }

    // Handle normal select input on the search results page
    searchTypeInput.addEventListener("change", () => {
      updatePlaceholder();
      clearSuggestions();
      searchInput.focus();
    });

    // Fetch live suggestions while typing
    searchInput.addEventListener("input", () => {
      clearTimeout(debounceTimeout);

      debounceTimeout = setTimeout(async () => {
        const query = searchInput.value.trim();
        const searchType = getSearchType();

        if (!query) {
          clearSuggestions();
          return;
        }

        try {
          const response = await fetch(
            `/search-suggestions?q=${encodeURIComponent(query)}&type=${encodeURIComponent(searchType)}`
          );

          const results = await response.json();

          clearSuggestions();

          if (results.length === 0) {
            const searchAll = document.createElement("a");

            searchAll.href = `/search?q=${encodeURIComponent(query)}&type=${encodeURIComponent(searchType)}`;
            searchAll.classList.add("suggestion-item", "suggestion-search-all");
            searchAll.textContent = `Search for "${query}"...`;

            suggestionsBox.appendChild(searchAll);
            return;
          }

          // Render book or user suggestions
          results.forEach((item) => {
            const suggestionItem = document.createElement("a");
            suggestionItem.classList.add("suggestion-item");

            if (searchType === "users") {
              suggestionItem.href = `/user/${item.username}`;

              const title = document.createElement("strong");
              title.textContent = item.username;

              const name = document.createElement("div");
              name.textContent = item.name || "";

              suggestionItem.appendChild(title);

              if (item.name) {
                suggestionItem.appendChild(name);
              }
            } else {
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

              const title = document.createElement("strong");
              title.textContent = item.title;

              const author = document.createElement("div");
              author.textContent = item.author || "";

              suggestionItem.appendChild(title);
              suggestionItem.appendChild(author);
            }

            suggestionsBox.appendChild(suggestionItem);
          });
        } catch (error) {
          clearSuggestions();
        }
      }, 200);
    });

    // Hide suggestions when clicking outside the current search bar
    document.addEventListener("click", (event) => {
      if (!searchWrapper.contains(event.target)) {
        closeMenu();
        clearSuggestions();
      }
    });

    updatePlaceholder();
  });
});