import requests
import json

from .serial_number.regular_extractor import RegularExtractor
from .serial_number.clf_interface import SerialNumberClassifierInterface
from config import CLF_ADDRESS


def serial_numbers_matching(report_content: str, llm_extracted_serial_number: str) -> bool:
    reg_extractor = RegularExtractor()

    if reg_extractor.get_serial_number(report_content) == llm_extracted_serial_number:
        return True
    return False


class NemoClf(SerialNumberClassifierInterface):
    """
    Класс для анализа устройств и определения их проблем.

    Attributes:
        url (str): URL API для отправки запросов (берётся из config.py).
    """

    def __init__(self, url: str = CLF_ADDRESS):
        """
        Инициализация класса NemoClf.

        Args:
            url (str): URL API для отправки запросов (берётся из config.py).
        """
        self.url = url

    def get_failure_point(self, report_content: str) -> str:
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
                                              'проанализировать информацию и определить так называемую "точку '
                                              'отказа". Точка отказа - это компонент устройства, в котором возникла '
                                              'проблема. Вот ВСЕ СУЩЕСТВУЮЩИЕ ТОЧКИ ОТКАЗА: [jack, SFP-модуль, '
                                              'wifi-антенна, wi-fi модуль, Аккумулятор, Блок питания, Вентилятор, '
                                              'Динамики, Диск, Камера, Клавиатура, Материнская плата, Матрица, '
                                              'Оперативная память, Программное обеспечение, Сервер].  Запомните: '
                                              'ответ необходимо вывести одним словом или определением. Если точка '
                                              'отказа не определена, то нужно вывести "Укажите точку отказа явно" НЕ '
                                              'ПИШИ ДОПОЛНИТЕЛЬНЫЕ ТЕКСТЫ. ТОЛЬКО "Укажите точку отказа явно", '
                                              'ПОЖАЛУЙСТА.'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)

        return json.loads(response.text)['choices'][0]['message']['content']

    def get_device_type(self, report_content: str) -> str:
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
                                              'СУЩЕСТВУЮЩИЕ ТИПЫ ОБОРУДОВАНИЯ: [Ноутбук, Сервер, СХД].  Запомните: '
                                              'ответ необходимо вывести одним словом или определением.'
                                              'Если тип оборудования не определен, нужно вывести "Укажите тип '
                                              'оборудования явно".НЕ ПИШИ ДОПОЛНИТЕЛЬНЫЕ ТЕКСТЫ. ТОЛЬКО "Укажите тип '
                                              'оборудования явно", ПОЖАЛУЙСТА.'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)

        return json.loads(response.text)['choices'][0]['message']['content']

    def get_serial_number(self, report_content: str) -> str | None:
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
                            'информацию и определить ПЕРВЫЙ ПОПАВШИЙСЯ СЕРИЙНЫЙ НОМЕР, из всех указанных в письме. '
                            'Вот как могут выглядеть серийные номера: [С222090774, D252030011, CKM00194300973].  '
                            'Запомните: НАЙДЕННЫЙ СЕРИЙНЫЙ НОМЕР НУЖНО ПЕРЕВЕСТИ В ВЕРХНИЙ РЕГИСТР И НА ЛАТИНИЦУ. '
                            'Пример вашей работы: вы получаете "сн123421242", вы выводите "SN123421242". Если '
                            'серийный номер не найден, нужно вывести "Укажите серийный номер явно" И НИЧЕГО БОЛЬШЕ.'},
                {"role": "user", "content": report_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=True)
        res = json.loads(response.text)['choices'][0]['message']['content']

        if serial_numbers_matching(report_content, res):
            return res
        return None
