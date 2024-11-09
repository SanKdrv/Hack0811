import re
from .clf_interface import SerialNumberClassifierInterface


class RegularExtractor(SerialNumberClassifierInterface):
    def __init__(self):
        # Задание карты замены для русских букв на латинские
        self._replacement_map = {
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y',
            'Х': 'X'
        }

    def _normalize_text(self, text):
        """
        Приводит текст к верхнему регистру и заменяет русские буквы на латинские аналоги.

        :param text: Входной текст
        :return: Нормализованный текст
        """
        # Приводим текст к верхнему регистру
        text = text.upper()

        # Заменяем русские буквы на латинские
        for rus, eng in self._replacement_map.items():
            text = text.replace(rus, eng).replace(rus.lower(), eng.lower())

        return text

    def get_serial_number(self, text: str) -> str:
        """
        Извлекает первый серийный номер из текста.

        Серийный номер следующего шаблона: [A-Za-z]{1,6}[0-9]{9,12}

        :param text: Входной текст
        :return: Первый найденный серийный номер или None, если не найден
        """
        # Приводим текст к нормализованному виду
        normalized_text = self._normalize_text(text)

        # Шаблон для поиска серийных номеров
        pattern = r'[A-Za-z]{1,6}[0-9]{9,12}'
        # Находим все совпадения
        matches = re.findall(pattern, normalized_text)
        if matches:
            return matches[0]
        return "Уточнить"
