from abc import ABC, abstractmethod


class SerialNumberClassifierInterface(ABC):
    """
    Абстрактный интерфейс для классификаторов серийных номеров.
    """

    @abstractmethod
    def extract_serial_number_from_text(self, text: str) -> str | None:
        """
        Метод для извлечения первого серийного номера из текста.

        :param text: Входной текст для анализа.
        :return: Первый серийный номер найденный в тексте или None, если номер не найден.
        """
        pass

