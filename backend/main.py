from flask import Flask, request, jsonify, render_template, make_response, send_file
import io
import csv

import pandas as pd

from backend.classifiers.nemo_clf import NemoClf
from backend.facade import get_failure_point, get_device_type, get_serial_number
from config import TEMPLATES_DIR
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=TEMPLATES_DIR, static_url_path="")


@app.route('/')
def index():
    print(TEMPLATES_DIR)
    return render_template('index.html')


@app.route('/api/send', methods=['POST'])
def send_to_server():
    """
    Получаем текст со странички
    :return: Результат отработки данных с сервера
    """
    data = request.get_json()
    return receive_from_server(data['text'])


@app.route('/api/receive', methods=['POST'])
def receive_from_server(data):
    """
    Получает данные от клиента, анализирует их и возвращает результаты анализа.

    Метод принимает POST-запрос с JSON-данными, содержащими информацию о проблеме устройства.
    Возвращает JSON-ответ с результатами анализа.

    :param data: JSON-объект с данными о проблеме устройства
    :return: JSON-ответ с результатами анализа
    """
    failure_point = get_failure_point(data)
    device_type = get_device_type(data)
    serial_number = get_serial_number(data)
    # point_of_failure = analyzer.get_failure_point(report_content=data)
    # type_of_device = analyzer.get_device_type(report_content=data)
    # serial_number = analyzer.get_serial_number(report_content=data)

    return jsonify({"failure_point": failure_point, "device_type": device_type,
                    "serial_number": serial_number})


# TODO: fix
@app.route('/process_csv', methods=['POST'])
def process_csv():
    """
    Получает csv файл из запроса и обрабатывается моделью.

    Метод принимает POST-запрос с JSON-данными, в которых находится csv-файл,
     содержащий информацию о проблемах устройств.
    Возвращает JSON-ответ в котором csv-файл с результатами анализа.

    :param data: JSON-объект с csv файлом, в котором находятся данныме о проблемах устройств
    :return: JSON-ответ с csv файлом, в котором находятся результатамы анализа
    """
    # Получаем CSV-файл из запроса
    csv_file = request.files['csv_file']

    # Читаем CSV-файл в DataFrame pandas
    df = pd.read_csv(csv_file)

    # Пробегаем по каждой строке и выводим ячейки
    processed_data = []
    for _, row in df.iterrows():
        processed_row = []
        for cell in row:
            processed_row.append(str(cell))
        processed_data.append(processed_row)

    # Создаем новый DataFrame с обработанными данными
    new_df = pd.DataFrame(processed_data, columns=df.columns)

    # Сохраняем результат обратно в CSV
    output_buffer = io.StringIO()
    new_df.to_csv(output_buffer, index=False)
    output_buffer.seek(0)

    # Отправляем ответ клиенту
    response = make_response(send_file(output_buffer, mimetype='text/csv'))
    response.headers["Content-Disposition"] = f"attachment; filename=processed_{request.files['csv_file'].filename}"
    return response


if __name__ == '__main__':
    app.run()
