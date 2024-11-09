document.getElementById("sendButton").addEventListener("click", sendMessage);
document.getElementById("messageInputTheme").addEventListener("keydown", function (event) { if (event.key === "Enter") sendMessage(); });
document.getElementById("messageInputText").addEventListener("keydown", function (event) { if (event.key === "Enter") sendMessage(); });


function checkEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}


function showStatus(text) {
    const statusMessage = document.getElementById("statusMessage");
    statusMessage.textContent = message;
    statusMessage.style.color = type === "success" ? "green" : "red";
}

function sendMessage() {
    const inputTheme = document.getElementById("messageInputTheme");
    const inputText = document.getElementById("messageInputText");
    const theme = inputTheme.value.trim();
    const text = inputText.value.trim();

    if (text === "" || theme === "") return;

    addMessage(theme, text, "user");
    inputTheme.value = "";
    inputText.value = "Введите текст сообщения...";

    const message = theme + " " + text;

    fetch('/api/gptresponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({ msg: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Сервер вернул ошибку");
        }
        return response.json();
    })
    .then(data => {
        /*
            я буду ожидать от вас json такой структуры:
            {
                type: smth,
                failure_point: smth,
                serial_number: smth
            }
            отправляете те данные, которые есть. Если чего-то нет, то я обрабатываю это
        */
       console.log(data);
        if (data.type_of_device && data.failure_point && data.serial_number) {
            const msg = data.type_of_device + " " +  data.failure_point + " " + data.serial_number;
            addMessage("Все данные есть!", msg, "bot");
        } else {
            let msg = "";
            if (!data.type_of_device) msg += "Тип оборудования, ";
            if (!data.failure_point) msg += "Точка отказа, ";
            if (!data.serial_number) msg += "Серийный номер";

            addMessage("Есть отсутствующие данные", msg, "bot");
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        addMessage("Произошла ошибка при получении ответа от сервера. Проверьте подключение или обратитесь к разработчику.", "", "bot");
    });
}

function addMessage(theme, text, sender) {
    const class_name = sender == "user" ? "msg_u" : "msg_b";
    const h2 = sender == "user" ? "Тема: " : "Статус: ";
    const chatMessages = document.getElementById("chatMessages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", sender);
    messageElement.innerHTML = "<p>" + theme + "</p>" + "<p>" + text + "</p>";
    messageElement.innerHTML = `<div class="${class_name}"><h2>${h2}</h2>${theme}</div><div class="${class_name}"><h2>Текст:</h2>${text}</div>`
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendToServer() {
            const inputText = document.getElementById('inputField').value;
            fetch('/api/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: inputText }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('outputField').value = JSON.stringify(data.value)
            });
        }