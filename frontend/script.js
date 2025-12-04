const chatWindow = document.getElementById("chat-window");
const input = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const subjectSelect = document.getElementById("subject-select");

/* Prevent accidental form submissions */
document.addEventListener("submit", (e) => e.preventDefault());
input.setAttribute("form", "noform");

let typingIndicator = null;

/* ---------------------------------------------------------
   CREATE TYPING DOTS INDICATOR
--------------------------------------------------------- */
function showTypingIndicator() {
    if (typingIndicator) return; // already visible

    typingIndicator = document.createElement("div");
    typingIndicator.classList.add("msg", "bot");
    typingIndicator.style.opacity = "0.7";
    typingIndicator.innerHTML = `
        <span class="typing-dots">
            <span>.</span><span>.</span><span>.</span>
        </span>
    `;

    chatWindow.appendChild(typingIndicator);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.remove();
        typingIndicator = null;
    }
}

/* ---------------------------------------------------------
   ADD MESSAGE TO CHAT (with working typing animation)
--------------------------------------------------------- */
function addMessage(text, sender = "user") {
    const msg = document.createElement("div");
    msg.classList.add("msg", sender);

    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // USER MESSAGE → no animation
    if (sender === "user") {
        msg.textContent = text;
        return;
    }

    // BOT MESSAGE → remove typing indicator first
    hideTypingIndicator();

    let index = 0;
    let buffer = "";

    function typeLoop() {
        if (index < text.length) {
            buffer += text[index];
            msg.textContent = buffer;
            index++;

            chatWindow.scrollTop = chatWindow.scrollHeight;

            setTimeout(typeLoop, 18); // typing speed
        } else {
            // After typing → render MathJax
            if (window.MathJax) {
                MathJax.typesetPromise([msg]);
            }
        }
    }

    typeLoop();
}

/* ---------------------------------------------------------
   SEND MESSAGE
--------------------------------------------------------- */
async function sendMessage() {
    const message = input.value.trim();
    const subject = subjectSelect.value;

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    // Show typing indicator immediately
    showTypingIndicator();

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, subject })
        });

        // SAFE JSON PARSE
        let raw = await res.text();
        console.log("RAW RESPONSE:", raw);

        let data;
        try {
            data = JSON.parse(raw);
        } catch {
            hideTypingIndicator();
            addMessage("⚠ Server returned invalid response.", "bot");
            return;
        }

        hideTypingIndicator();

        if (data.reply) {
            addMessage(data.reply, "bot");
        } else {
            addMessage("⚠ Error: " + (data.error || "Unknown issue."), "bot");
        }

    } catch (err) {
        hideTypingIndicator();
        addMessage("🛑 Server unreachable.", "bot");
        console.error(err);
    }
}

/* ---------------------------------------------------------
   EVENT LISTENERS
--------------------------------------------------------- */
sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        e.stopPropagation();
        sendMessage();
    }
});
