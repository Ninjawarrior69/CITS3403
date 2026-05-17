document.addEventListener("DOMContentLoaded", function () {
    const progressModal = document.getElementById("progressModal");
    const progressForm = document.getElementById("progressForm");

    if (!progressModal || !progressForm) {
        return;
    }

    progressModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        if (!button) {
            return;
        }

        const itemId = button.getAttribute("data-item-id");

        if (!itemId) {
            return;
        }

        progressForm.action = `/shelf/${itemId}/progress`;
    });
});