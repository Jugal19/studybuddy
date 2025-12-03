const chatWindow = document.getElementById("chat-window");
const input = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const subjectSelect = document.getElementById("subject-select");

function addMessage(text, sender = "user") {
    const msg = document.createElement("div");
    msg.classList.add("msg", sender);

    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    if (sender === "bot") {
        let i = 0;

        function typeChar() {
            if (i < text.length) {
                msg.textContent += text.charAt(i);
                i++;
                chatWindow.scrollTop = chatWindow.scrollHeight;
                requestAnimationFrame(typeChar);
            }
        }

        requestAnimationFrame(typeChar);
    } else {
        msg.textContent = text;
    }
}

async function sendMessage() {
    const message = input.value.trim();
    const subject = subjectSelect.value;

    if (!message) return;

    addMessage(message, "user");

    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                subject: subject
            })
        });

        const data = await res.json();

        if (data.reply) {
            addMessage(data.reply, "bot");
        } else {
            addMessage("⚠ Error: " + (data.error || "Unknown issue."), "bot");
        }

    } catch (err) {
        addMessage("Server unreachable 🛑\nCheck backend.", "bot");
        console.error(err);
    }
}

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});
