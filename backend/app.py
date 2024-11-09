from flask import Flask, request, jsonify
import base64
import io
import csv

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/get_message')
def get_message():
    # Здесь надо реализовать считывание сообщения
    message = "Привет, мир!"  # Примерное значение
    return {"message": message}




@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if not data:
        return jsonify({"error": "Пожалуйста, отправьте данные в формате JSON"}), 400

    message = data.get('message')
    if not message:
        return jsonify({"error": "Необходимо передать поле 'message'"}), 400

    # Здесь вы можете реализовать логику сохранения сообщения
    # Например, записать его в файл или базу данных
    print(f"Получено сообщение: {message}")

    return jsonify({"status": "OK", "message": f"Сообщение '{message}' успешно получено"}), 200


@app.route('/read_csv_base64')
def read_csv_base64():
    csv_data = request.args.get('csv_data')
    if not csv_data:
        return jsonify({"error": "Пожалуйста, передайте параметр csv_data в формате base64"}), 400

    try:
        decoded_bytes = base64.b64decode(csv_data)
        csv_string = decoded_bytes.decode('utf-8')

        # Читаем CSV из строки
        csv_reader = csv.reader(io.StringIO(csv_string))
        data = list(csv_reader)

        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/return_csv_base64', methods=['POST'])
def return_csv_base64():
    data = request.json
    if not data:
        return jsonify({"error": "Пожалуйста, отправьте данные в формате JSON"}), 400

    csv_content = data.get('csv_content')
    if not csv_content:
        return jsonify({"error": "Необходимо передать поле 'csv_content'"}), 400

    try:
        # Создаем объект StringIO для хранения CSV-данных
        csv_io = io.StringIO(csv_content)

        # Читаем CSV из StringIO
        csv_reader = csv.reader(csv_io)
        data = list(csv_reader)

        # Конвертируем список в строку
        csv_string = '\n'.join([','.join(row) for row in data])

        # Кодируем в base64
        encoded_csv = base64.b64encode(csv_string.encode('utf-8')).decode('utf-8')

        return jsonify({"csv_base64": encoded_csv})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
