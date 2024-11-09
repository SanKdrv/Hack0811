import requests
import json


class DeviceAnalysis:
    """
    Класс для анализа устройств и определения их проблем.

    Attributes:
        url (str): URL API для отправки запросов (по умолчанию "http://127.0.0.1:1234/v1/chat/completions").
    """

    def __init__(self, url: str = "http://127.0.0.1:1234/v1/chat/completions"):
        """
        Инициализация класса DeviceAnalysis.

        Args:
            url (str): URL API для отправки запросов (по умолчанию "http://127.0.0.1:1234/v1/chat/completions").
        """
        self.url = url

    def get_point_of_failure(self, report_content: str) -> str:
        """
        Функция анализирует предоставленный текст и определяет точку отказа оборудования.

        Args:
        report_content (str): Текст для анализа (Тема + Содержимое).

        Returns:
        str: Определенная точка отказа оборудования.
        """

        headers = {"Content-Type": "application/json"}
        data = {
            "model": "vikhr-nemo-12b-instruct-r-21-09-24",
            "messages": [
                {"role": "system", "content": 'Вам на вход подаётся текст и тема сообщения в тех. поддержку. Вам нужно '
                                              'проанализировать информацию и определить так называемую "точку отказа". Точка '
                                              'отказа - это компонент устройства, в котором возникла проблема. Вот ВСЕ '
                                              'СУЩЕСТВУЮЩИЕ ТОЧКИ ОТКАЗА: [jack, SFP-модуль, wifi-антенна, wi-fi модуль, '
                                              'Аккумулятор, Блок питания, Вентилятор, Динамики, Диск, Камера, Клавиатура, '
                                              'Материнская плата, Матрица, Оперативная память, Программное обеспечение, '
                                              'Сервер].  Запомните: ответ необходимо вывести одним словом или определением.'
                                              'Если точка отказа не определена, то нужно вывести "NaN". НИЧЕГО КРОМЕ '
                                              '"NaN". НЕ ПИШИ ДОПОЛНИТЕЛЬНЫЕ ТЕКСТЫ. ТОЛЬКО "NaN", ПОЖАЛУЙСТА.'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)

        return json.loads(response.text)['choices'][0]['message']['content']

    def get_type_of_device(self, report_content: str) -> str:
        """
        Функция анализирует предоставленный текст и определяет тип оборудования.

        Args:
        report_content (str): Текст для анализа (Тема + Содержимое).

        Returns:
        str: Определенный тип оборудования.
        """

        headers = {"Content-Type": "application/json"}
        data = {
            "model": "vikhr-nemo-12b-instruct-r-21-09-24",
            "messages": [
                {"role": "system", "content": 'Вам на вход подаётся текст и тема сообщения в тех. поддержку. Вам нужно '
                                              'проанализировать информацию и определить тип оборудования. Вот ВСЕ '
                                              'СУЩЕСТВУЮЩИЕ ТИПЫ ОБОРУДОВАНИЯ: [Ноутбук, Сервер, СХД].  Запомните: ответ '
                                              'необходимо вывести одним словом или определением.'
                                              'Если тип оборудования не определен, нужно вывести "NaN". НИЧЕГО КРОМЕ '
                                              '"NaN". НЕ ПИШИ ДОПОЛНИТЕЛЬНЫЕ ТЕКСТЫ. ТОЛЬКО "NaN", ПОЖАЛУЙСТА.'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)

        return json.loads(response.text)['choices'][0]['message']['content']

    def get_serial_number(self, report_content: str) -> str:
        """
            Функция анализирует предоставленный текст и определяет серийный номер.

            Args:
            report_content (str): Текст для анализа (Тема + Содержимое).

            Returns:
            str: Определенный серийный номер.
            """

        headers = {"Content-Type": "application/json"}
        data = {
            "model": "vikhr-nemo-12b-instruct-r-21-09-24",
            "messages": [
                {"role": "system",
                 "content": 'Вам на вход подаётся текст и тема сообщения в тех. поддержку. Вам нужно проанализировать '
                            'информацию и определить ВСЕ СЕРИЙНЫЕ НОМЕРА, которые указаны в письме. Вот как могут '
                            'выглядеть серийные номера: [С222090774, D252030011, CKM00194300973].  Запомните: ответ '
                            'необходимо вывести одним словом или определением. Если серийный номер не найден, '
                            'нужно вывести "NaN". НИЧЕГО КРОМЕ "NaN". НЕ ПИШИ ДОПОЛНИТЕЛЬНЫЕ ТЕКСТЫ. ТОЛЬКО "NaN", '
                            'ПОЖАЛУЙСТА. ЕСЛИ ЕСТЬ СЕРИЙНЫЙ НОМЕР, ТО НЕ ПИШИ "NaN".'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)

        return json.loads(response.text)['choices'][0]['message']['content']
