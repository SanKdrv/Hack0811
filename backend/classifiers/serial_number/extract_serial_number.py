import re

class SerialNumberExtractor:
    def __init__(self):
        # Задание карты замены для русских букв на латинские
        self.replacement_map = {
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y',
            'Х': 'X'
        }

    def normalize_text(self, text):
        """
        Приводит текст к верхнему регистру и заменяет русские буквы на латинские аналоги.

        :param text: Входной текст
        :return: Нормализованный текст
        """
        # Приводим текст к верхнему регистру
        text = text.upper()

        # Заменяем русские буквы на латинские
        for rus, eng in self.replacement_map.items():
            text = text.replace(rus, eng).replace(rus.lower(), eng.lower())

        return text

    def extract_serial_number(self, text):
        """
        Извлекает серийный номер из текста.

        Серийный номер должен содержать от 1 до 6 букв, за которыми следуют от 9 до 12 цифр.

        :param text: Входной текст
        :return: Список найденных серийных номеров
        """
        # Приводим текст к нормализованному виду
        normalized_text = self.normalize_text(text)

        # Шаблон для поиска серийных номеров
        pattern = r'[A-Za-z]{1,6}[0-9]{9,12}'
        # Находим все совпадения
        matches = re.findall(pattern, normalized_text)

        return matches
