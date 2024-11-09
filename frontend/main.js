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
    return text.includes("Уточнить") || text == "None";
}

async function sendMessage() {
    const inputTheme = document.getElementById("messageInputTheme");
    const inputText = document.getElementById("messageInputText");
    const theme = inputTheme.value.trim();
    const text = inputText.value.trim();
    let serial_number = "";

    if (text === "" || theme === "") return;

    addMessage(theme, text, "user");
    inputTheme.value = "";
    inputText.value = "";
    inputText.ariaPlaceholder = "Введите текст сообщения...";

    const message = theme + " " + text;

    await fetch('/api/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ msg: message })
    })
    .then(response => {
        if (!response.ok) {
            console.log(response);
            throw new Error("Сервер вернул ошибку");
        }
        return response.json();
    })
    .then(data => { 
        if (!isEmptyField(data.device_type) && !isEmptyField(data.failure_point) && !isEmptyField(data.serial_number)) {
            const msg = `
            Здравствуйте! <br>

            Ваше устройство: ${data.device_type}<br>
            Точка неисправности: ${data.failure_point}<br>
            Серийный номер: ${data.serial_number}<br>

            Ваша заявка принята в работу!<br>

            С уважением,
            Служба поддержки компании «Сила»
            `;

            addMessage("Все данные есть!", msg, "bot");
            serial_number = data.serial_number; 
        } else {
            let msg = "Здравствуйте! Пожалуйста, уточните следующие данные для продолжения обработки заявки:<br>";
            if (isEmptyField(data.device_type)) msg += "&nbsp;&nbsp;&nbsp;&nbsp; - Тип оборудования, <br>";
            if (isEmptyField(data.failure_point)) msg += "&nbsp;&nbsp;&nbsp;&nbsp; - Точка отказа, <br>";
            if (isEmptyField(data.serial_number)) msg += "&nbsp;&nbsp;&nbsp;&nbsp; - Серийный номер<br>";

            addMessage("Не хватает данных.", msg, "bot");
        }
    })
    .catch(error => {1
        console.error('Ошибка:', error);
        addMessage("Произошла ошибка при получении ответа от сервера при запросе на данные метрик. Проверьте подключение или обратитесь к разработчику.", "", "bot");
    });

    if (!isEmptyField(serial_number)) {
        await fetch('/get_model_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: serial_number })
        }).then(response => {
            if (!response.ok) {
                console.log(response);
                throw new Error("Сервер вернул ошибку");
            }
            return response.json();
        })
        .then(data => {
            if (!isEmptyField(data.model_info)) {
                const msg = 
                `
                    Вот, какую информацию я смог найти по вашему товару. Надеюсь, она будет полезна!
                    ${data.model_info}
                `;
                addMessage("Данные найдены!", msg, "bot");
            } else {
                const msg = "К сожалению, я не смог найти информацию о вашем товаре в нашем каталоге.";
                addMessage("Данные не найдены!", msg, "bot");
            }
        }).catch(error => {1
            console.error('Ошибка:', error);
            addMessage("Произошла ошибка при получении ответа от сервера при запросе по серийному номеру. Проверьте подключение или обратитесь к разработчику.", "", "bot");
        });
    }
    
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