const progressModal = document.getElementById("progressModal");

progressModal.addEventListener("show.bs.modal", function (event) {

    const button = event.relatedTarget;

    const itemId = button.getAttribute("data-item-id");

    const form = document.getElementById("progressForm");

    form.action = `/shelf/${itemId}/progress`;
});