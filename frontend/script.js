document.getElementById("go").onclick = async () => {
    const topic = document.getElementById("topic").value;
    const out = document.getElementById("out");

    if (!topic.trim()) {
        out.innerText = "Please enter a topic.";
        return;
    }

    out.innerText = "Generating questions...\nThis may take a few seconds.";

    try {
        const response = await fetch("http://127.0.0.1:8000/quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic })
        });

        const data = await response.json();

        // If error returned
        if (data.error) {
            out.innerText = "Error: " + data.error;
            return;
        }

        // Render in clean formatted list
        out.innerHTML = "";
        data.questions.forEach(question => {
            const p = document.createElement("p");
            p.textContent = question;
            out.appendChild(p);
        });

    } catch (e) {
        out.innerText = "Error contacting backend. Make sure FastAPI is running.";
    }
};
