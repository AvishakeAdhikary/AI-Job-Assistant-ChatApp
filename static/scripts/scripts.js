document.addEventListener("DOMContentLoaded", () => {
    const chat = document.getElementById("chat");
    const input = document.getElementById("chat-input");
    const inputButton = document.getElementById("chat-input-button");
    const attachFileButton = document.getElementById("fileupload");
    let hasBotStarted = false;

    function formatMessage(text) {
        // Replace text enclosed in double asterisks with bold formatting
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
        // Replace text enclosed in triple backticks with code formatting
        text = text.replace(/```(.*?)```/g, '<code>$1</code>');
    
        // Format links to be clickable
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    
        // Preserve new lines
        text = text.replace(/\n/g, '<br>');
    
        return text;
    }    

    function addMsg(msg, type) {
        const message = document.createElement("p");
        if (type === "user") {
            message.setAttribute("class", "text-bg-primary p-3 text-end d-flex flex-column justify-content-end");
            message.setAttribute("id", "userMsg");
            message.setAttribute("style", "margin-top: 5px; max-width: max-content; border-radius: 16px 0 16px 16px; align-self: flex-end");
        } else if (type === "bot") {
            message.setAttribute("class", "text-bg-warning p-3 text-start d-flex flex-column justify-content-start");
            message.setAttribute("id", "botMsg");
            message.setAttribute("style", "margin-top: 5px; max-width: max-content; border-radius: 0 16px 16px 16px;");
        }
        msg = formatMessage(msg);
        message.innerHTML = msg;
        chat.appendChild(message);
        input.value = "";
        chat.scrollTop = chat.scrollHeight;
    }

    function addLoading()
    {
        const message = document.createElement("p");
        message.setAttribute("class", "text-bg-light p-3 text-start d-flex justify-content-start");
        message.setAttribute("id", "loading-image-p");
        message.setAttribute("style", "margin-top: 5px; max-width: max-content; border-radius: 0 16px 16px 16px;");
        const loadingImage = document.createElement("img");
        loadingImage.setAttribute("src", "static/images/loading.gif");
        loadingImage.setAttribute("style", "height : 40px; width : max-content;");
        message.appendChild(loadingImage);
        chat.appendChild(message);
        chat.scrollTop = chat.scrollHeight;
    }

    function removeLoading()
    {
        const loadingImage = document.getElementById("loading-image-p");
        chat.removeChild(loadingImage);
        chat.scrollTop = chat.scrollHeight;
    }

    input.addEventListener("keyup", (keyboardEvent) => {
        if (keyboardEvent.key === 'Enter' && input.value.trim() != "") {
            console.log("inputvalue: ",input.value)
            if(attachFileButton.value != "")
            {
                const userMessage = input.value;
                addMsg(userMessage, "user");
                addLoading();
                console.log(attachFileButton.value,"File is being uploaded");
                const formData = new FormData();
                formData.append('file', attachFileButton.files[0]);
                formData.append('message', userMessage);
                fetch('/submitfile', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    removeLoading();
                    attachFileButton.value = '';
                    addMsg(data.message, "bot");
                })
                .catch((error) => {
                    console.error('Error:', error);
                    removeLoading();
                    attachFileButton.value = '';
                    addMsg(data.message, "bot");
                });
            }
            else{
                const userMessage = input.value;
                addMsg(userMessage, "user");
                addLoading();
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
                    removeLoading();
                    addMsg(data.message, "bot");
                })
                .catch((error) => {
                    removeLoading();
                    console.error('Error:', error);
                });
            }
        }
    });

    function init() {
        hasBotStarted = true;
        addMsg("Hello, I am AI Job Chat Assistant.", "bot");
        addMsg("How can I help you today?", "bot");
        addLoading();
        fetch('/getChatHistory')
        .then(response => response.json())
        .then(data => {
            removeLoading();
            data.messages.reverse().forEach((msg) => {
                if (msg.role === "assistant") {
                    addMsg(msg.content, "bot");
                } else if (msg.role === "user") {
                    addMsg(msg.content, "user");
                }
            });
        })
        .catch(error => {
            console.error('Error:', error)
            removeLoading();
        });
    }

    init();
});
