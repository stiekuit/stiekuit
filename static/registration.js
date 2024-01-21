document.addEventListener("DOMContentLoaded", function () {
    // Add an event listener to the registration form
    var registrationForm = document.getElementById("registration-form");
    if (registrationForm) {
        registrationForm.addEventListener("submit", function (event) {
            event.preventDefault();

            // Get the username and password from the form
            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;

            // Make a POST request to the registration endpoint
            fetch("/registration", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "username": username, "password": password })
            })
            .then(response => response.json())
            .then(data => {
                // Display the registration message
                var messageElement = document.getElementById("registration-message");
                messageElement.textContent = data.message;
            });
        });
    }
});
