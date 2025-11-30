// Submit form via AJAX
document.getElementById("bulkWordForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent normal form submission

    const input = document.getElementById("bulkInput").value.trim();
    const responseMsg = document.getElementById("responseMsg");

    if (!input) {
        responseMsg.innerText = "Please enter some words!";
        responseMsg.style.color = "red";
        return;
    }

    try {
        const response = await fetch("/api/add_words/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (response.ok) {
            responseMsg.innerText = data.message;
            responseMsg.style.color = "green";
            document.getElementById("bulkInput").value = ""; // clear textarea
        } else {
            responseMsg.innerText = data.message || "Something went wrong.";
            responseMsg.style.color = "red";
        }
    } catch (err) {
        responseMsg.innerText = "Error connecting to server.";
        responseMsg.style.color = "red";
    }
});

// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
