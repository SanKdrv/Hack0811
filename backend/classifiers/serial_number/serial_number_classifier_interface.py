from abc import ABC, abstractmethod


class SerialNumberClassifierInterface(ABC):
    """
    Абстрактный интерфейс для классификаторов серийных номеров.
    """

    @abstractmethod
    def extract_serial_number_from_text(self, text: str) -> str:
        """
        Метод для извлечения серийного номера из текста.

        :param text: Входной текст для анализа.
        :return: Список серийных номеров, найденных в тексте.
        """
        pass

