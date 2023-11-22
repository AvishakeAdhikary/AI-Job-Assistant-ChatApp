document.addEventListener("DOMContentLoaded", () => {
    const chat = document.getElementById("chat");
    const input = document.getElementById("chat-input");
    let hasBotStarted = false;

    function addMsg(msg, type) {
        const message = document.createElement("p");
        if (type === "user") {
            message.setAttribute("class", "text-primary-emphasis text-end d-flex justify-content-end");
            message.setAttribute("id", "userMsg");
        } else if (type === "bot") {
            message.setAttribute("class", "text-warning text-start d-flex justify-content-start");
            message.setAttribute("id", "botMsg");
        }
        message.textContent = msg;
        chat.appendChild(message);
        input.value = "";
    }

    input.addEventListener("keyup", (keyboardEvent) => {
        if (keyboardEvent.key === 'Enter' && input.value.trim() != "") {
            const userMessage = input.value;
            addMsg(userMessage, "user");
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                }),
            })
            .then(response => response.json())
            .then(data => {
                addMsg(data.message, "bot");
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    });

    function init() {
        hasBotStarted = true;
        addMsg("Hello, I am Chat Assistant.", "bot");
        addMsg("How can I help you today?", "bot");
    }

    init();
});
