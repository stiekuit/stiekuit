// login.js

function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show a success or error message
        if (data.message === "Login successful") {
            // Redirect to chatbot page or handle accordingly
            window.location.href = "/chat.html";
        }
    });
}
