const form = document.getElementById("fitForm");
const resultBox = document.getElementById("result");
const scoreEl = document.getElementById("score");
const messageEl = document.getElementById("message");
const imageEl = document.getElementById("uploadedImage");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    scoreEl.textContent = "Analyzing...";
    messageEl.textContent = "Please wait while we analyze your fitness structure.";
    resultBox.classList.remove("hidden");

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            scoreEl.textContent = "Error";
            messageEl.textContent = data.error;
            return;
        }

        scoreEl.textContent = `${data.bodyfitscore} / 100`;
        messageEl.textContent = data.message;
        const imageEl = document.getElementById("uploadedImage");
        imageEl.style.display = "block";

    } catch (err) {
        scoreEl.textContent = "Error";
        messageEl.textContent = "Something went wrong. Please try again.";
    }
});
