// Submit form via AJAX
document.getElementById("bulkWordForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = document.getElementById("bulkInput").value.trim();
    const responseMsg = document.getElementById("responseMsg");

    const category = document.getElementById("categorySelect").value;
    const subcategory = document.getElementById("subcategorySelect").value;

    const newCategory = document.getElementById("newCategory").value.trim();
    const newSubcategory = document.getElementById("newSubcategory").value.trim();

    if (!text) {
        responseMsg.innerText = "Please enter some words!";
        responseMsg.style.color = "red";
        return;
    }

    // Prepare JSON payload
    const payload = {
        text: text,
        category: category || null,
        subcategory: subcategory || null,
        newCategory: newCategory,
        newSubcategory: newSubcategory
    };

    console.log("Sending payload:", payload); // debug

    try {
        const response = await fetch("/api/add_words/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            responseMsg.innerText = data.message;
            responseMsg.style.color = "green";

            // clear inputs
            document.getElementById("bulkInput").value = "";
            document.getElementById("newCategory").value = "";
            document.getElementById("newSubcategory").value = "";
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
