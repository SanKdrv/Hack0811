import spacy

# Загружаем предобученную модель spaCy для обработки текстов на русском языке
# Модель содержит информацию о морфологии, синтаксисе и лемматизации слов
nlp = spacy.load("ru_core_news_lg")


class EquipmentDetector:
    """
    Класс EquipmentDetector используется для определения упоминания
    определённых типов оборудования в тексте. Анализируется текст на наличие
    заранее заданных ключевых слов, представляющих различные виды оборудования.
    """

    def __init__(self):
        """
        Инициализирует объект EquipmentDetector.

        Атрибуты:
        - equipment_keywords (list): Список ключевых слов, соответствующих типам оборудования.
        """
        self._equipment_keywords = ["сервер", "ноутбук", "схд"]  # Ключевые леммы для идентификации оборудования

    def detect_equipment(self, text: str) -> str | None:
        """
        Метод для обнаружения упоминания оборудования в тексте.

        Обрабатывает текст с использованием spaCy, проверяя каждое слово
        на соответствие списку ключевых лемм, представляющих оборудование.

        Args:
            text: исходный текст, из которого будет извлекаться тип оборудования

        Returns:
            - str: Лемма найденного оборудования, если оно присутствует в тексте.
            - None: Если ни одно из ключевых слов не было найдено.

        Пример:
        >>> detector = EquipmentDetector("сервер перегрелся")
        >>> detector.detect_equipment()
        'сервер'
        """

        # Обрабатываем текст с помощью spaCy, получая объект с токенами и их атрибутами
        doc = nlp(text)

        # Проходим по каждому слову (токену) в обработанном тексте
        for token in doc:
            # Сравниваем лемму токена (приведенную к нижнему регистру) с ключевыми словами
            if token.lemma_.lower() in self._equipment_keywords:
                if token.lemma_.lower() == "схд":
                    return "СХД"
                return token.lemma_.capitalize()  # Возвращаем найденное оборудование, если совпадение найдено

        # Возвращаем None, если в тексте не обнаружено упоминаний оборудования
        return None


# Пример использования класса EquipmentDetector
if __name__ == "__main__":
    # Пример текста для анализа
    text = """У серверов СИЛА НК2-1404 S/N C222091115 возникла проблема:
    На прошлой неделе сотрудник работал как обычно, вечером ушёл домой, утром 
    пришёл и на ноутбуке показало, что нет системы
    В ходе проверки было обнаружено полное обнуление SSD Диска включая SMART"""

    # Создаем объект класса EquipmentDetector, передавая текст для анализа
    detector = EquipmentDetector()

    # Вызываем метод detect_equipment для определения упоминания оборудования
    equipment_found = detector.detect_equipment(text)

    # Выводим результат
    if equipment_found:
        print("Оборудование, упомянутое в тексте:", equipment_found)
    else:
        print("Оборудование не найдено.")
