from flask import Flask, request, jsonify, render_template
import base64
import io
import csv
import json

from backend.classifiers.nemo_clf import NemoClf

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/send', methods=['POST'])
def send_to_server():
    """
    Получаем текст со странички
    :return: Сообщение о том, что мы получили сообщение
    """
    data = request.get_json()
    return receive_from_server(data['text'])


@app.route('/api/receive')
def receive_from_server(data):
    """
    Получает данные от клиента, анализирует их и возвращает результаты анализа.

    Метод принимает POST-запрос с JSON-данными, содержащими информацию о проблеме устройства.
    Возвращает JSON-ответ с результатами анализа.

    :param data: JSON-объект с данными о проблеме устройства
    :return: JSON-ответ с результатами анализа
    """
    analyzer = NemoClf()

    point_of_failure = analyzer.get_failure_point(report_content=data)
    type_of_device = analyzer.get_device_type(report_content=data)
    serial_number = analyzer.get_serial_number(report_content=data)

    return jsonify({"failure_point": point_of_failure, "device_type": type_of_device,
                    "serial_number": serial_number})


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
