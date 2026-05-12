document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const searchTypeButton = document.getElementById("search-type-button");
  const searchTypeMenu = document.getElementById("search-type-menu");
  const searchTypeInput = document.getElementById("search-type-input");
  const searchTypeLabel = document.getElementById("search-type-label");
  const searchTypeOptions = document.querySelectorAll(".search-type-option");
  const suggestionsBox = document.getElementById("search-suggestions");
  const searchWrapper = document.querySelector(".search-wrapper");

  if (!searchInput || !suggestionsBox || !searchWrapper) {
    return;
  }

  let debounceTimeout;

  // Update placeholder based on search type
  const updatePlaceholder = () => {
    const type = searchTypeInput.value || "books";
    if (type === "users") {
      searchInput.placeholder = "Search Users";
      searchInput.setAttribute("aria-label", "Search users");
    } else {
      searchInput.placeholder = "Search books or authors...";
      searchInput.setAttribute("aria-label", "Search books or authors");
    }
  };

  // Toggle dropdown menu
  const toggleMenu = (open) => {
    if (open === undefined) {
      open = searchTypeMenu.hidden;
    }
    searchTypeMenu.hidden = !open;
    searchTypeButton.setAttribute("aria-expanded", open);
  };

  // Handle dropdown option selection
  searchTypeOptions.forEach((option) => {
    option.addEventListener("click", (e) => {
      e.preventDefault();
      const value = option.dataset.value;

      // Update hidden input
      searchTypeInput.value = value;

      // Update button label
      searchTypeLabel.textContent = option.textContent;

      // Update aria-selected
      searchTypeOptions.forEach((opt) => {
        opt.setAttribute("aria-selected", opt === option);
      });

      // Update placeholder
      updatePlaceholder();

      // Close menu
      toggleMenu(false);

      // Clear suggestions
      suggestionsBox.innerHTML = "";

      // Focus input
      searchInput.focus();
    });
  });

  // Toggle menu on button click
  searchTypeButton.addEventListener("click", () => {
    toggleMenu();
  });

  // Close menu when clicking outside
  document.addEventListener("click", (event) => {
    if (!searchWrapper.contains(event.target)) {
      toggleMenu(false);
      suggestionsBox.innerHTML = "";
    }
  });

  // Set initial placeholder
  updatePlaceholder();

  // Handle search input
  searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(async () => {
      const query = searchInput.value.trim();
      const searchType = searchTypeInput.value || "books";

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
          // Handle user suggestions - link to public profile by username
          suggestionItem.href = `/user/${item.username}`;
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
});
