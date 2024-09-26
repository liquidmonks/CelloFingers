document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
        // Disable the button to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        // You can add client-side validations here if necessary
    });
});
