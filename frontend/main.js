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

function isEmptyField(text) {
    return text.includes("Укажите") || text == "None";
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
                failure_point: smth,
                device_type: smth,
                serial_number: smth
            }
            данные не заполены: ответ начинается со слов Укажите, либо в поле None
        */
       console.log(data);

        if (isEmptyField(data.device_type) && isEmptyField(data.failure_point) && isEmptyField(data.serial_number)) {
            const msg = data.device_type + " " +  data.failure_point + " " + data.serial_number;
            addMessage("Все данные есть!", msg, "bot");
        } else {
            let msg = "";
            if (isEmptyField(data.device_type)) msg += "Тип оборудования, ";
            if (isEmptyField(data.failure_point)) msg += "Точка отказа, ";
            if (isEmptyField(data.serial_number)) msg += "Серийный номер";

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