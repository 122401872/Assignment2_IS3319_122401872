document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/jokes")
    .then(response => response.json())
    .then(data => {
        console.log("Received API Data:", data); // Debugging

        // Access 'data' object inside the response
        if (data && data.setup && data.punchline) {
            document.getElementById("setup").innerText = `"${data.setup}"`;   // Display the setup
            document.getElementById("punchline").innerText = `"${data.punchline}"`;  // Display the punchline
        } else {
            document.getElementById("setup").innerText = "Failed to load Joke";
            document.getElementById("punchline").innerText = "Failed to load Joke";
        }
    })
    .catch(error => {
        console.error("Error Fetching Quote", error);
        document.getElementById("setup").innerText = "Error Loading Joke";  // Show error in case of failure
        document.getElementById("punchline").innerText = "Error Loading Joke";
    });
});
