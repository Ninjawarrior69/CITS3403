
function toggleSection(id, button) {
    const section = document.getElementById(id);

    if (section.classList.contains("review-collapsed")) {
        section.classList.remove("review-collapsed");
        button.innerText = "Show Less";
    } else {
        section.classList.add("review-collapsed");
        button.innerText = "Show More";
    }
}