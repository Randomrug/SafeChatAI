const chatBox = document.getElementById("chat-box");
const inputBox = document.getElementById("user-input");

// In-memory conversation history that gets sent to the LLM on every request.
// Toxic user turns are NEVER stored here — only safe user messages and the
// assistant's replies. This keeps the LLM context clean and aligned.
const conversationHistory = [];

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function createUserMessage(text) {

    const wrapper = document.createElement("div");
    wrapper.className = "message user";

    wrapper.innerHTML = `
        <div class="bubble">
            ${escapeHtml(text)}
        </div>
    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();
}

function createAIMessage(text) {

    const wrapper = document.createElement("div");
    wrapper.className = "message ai";

    wrapper.innerHTML = `
        <div class="bubble">
            ${escapeHtml(text)}
        </div>
    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();
}

function createBlockedMessage(reasons) {

    let reasonHtml = "";

    reasons.forEach(reason => {

        reasonHtml += `
            <div class="reason-item">
                • ${reason.label} (${reason.score}%)
            </div>
        `;

    });

    const wrapper = document.createElement("div");
    wrapper.className = "message ai";

    wrapper.innerHTML = `
        <div class="blocked-card">

            <div class="blocked-title">
                🚨 Message Blocked
            </div>

            <div>
                SafeChat detected potentially harmful content.
            </div>

            <div class="reason-list">
                ${reasonHtml}
            </div>

            <div class="blur-text">
                ███████████████████████████████████
            </div>

        </div>
    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();
}

function createTypingIndicator() {

    const wrapper = document.createElement("div");

    wrapper.className = "message ai";
    wrapper.id = "typing-indicator";

    wrapper.innerHTML = `
        <div class="bubble typing">
            SafeChat AI is typing...
        </div>
    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();
}

function removeTypingIndicator() {

    const typing = document.getElementById(
        "typing-indicator"
    );

    if (typing) {
        typing.remove();
    }
}

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}

async function sendMessage() {

    const message = inputBox.value.trim();

    if (!message) return;

    // Do NOT render the original message yet — wait for moderation result.
    // The original text is never stored or shown if it is toxic.

    inputBox.value = "";

    createTypingIndicator();

    try {

        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message,
                    history: conversationHistory
                })
            }
        );

        const data = await response.json();

        removeTypingIndicator();

        if (data.blocked) {

            // Show the blocked card (with moderation scores only — no original text)
            createBlockedMessage(
                data.reasons
            );

            // Then automatically have the AI respond with a gentle reminder
            createAIMessage(
                data.reply
            );

            // Record the gentle reminder as an assistant turn so the LLM
            // has continuity if the user continues. The toxic user turn
            // is intentionally NOT added to history.
            conversationHistory.push({
                role: "assistant",
                content: data.reply
            });

            return;
        }

        // Safe path: show the user's original message, then the AI reply
        createUserMessage(message);

        createAIMessage(
            data.reply
        );

        // Add both turns to history so the LLM has multi-turn context
        // on subsequent requests.
        conversationHistory.push({
            role: "user",
            content: message
        });

        conversationHistory.push({
            role: "assistant",
            content: data.reply
        });

    }

    catch(error) {

        removeTypingIndicator();

        createAIMessage(
            "⚠️ Error connecting to server."
        );

        console.error(error);
    }
}

inputBox.addEventListener(
    "keypress",
    function(e) {

        if (e.key === "Enter") {

            sendMessage();
        }
    }
);

scrollToBottom();

