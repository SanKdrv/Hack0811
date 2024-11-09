from .classifiers.serial_number.regular_extractor import RegularExtractor
from .classifiers.nemo_clf import NemoClf


def get_serial_number(text: str) -> str | None:
    """
    Принимает исходный текст. Извлекает первый серийный номер и возвращает его,
    если серийный номер не найден, то возвращает None.
    :param text: Исходный текст для извлечения из него серйиного номера.
    :return: Первый серийный номер в тексте или None, если серийный номер не найден.
    """
    reg_extractor = RegularExtractor()
    # e = NemoClf()
    return reg_extractor.get_serial_number(text)


def get_failure_point(text: str) -> str:
    """
    Принимает исходный текст. Извлекает точку отказа и возвращает ее,
    если точка отказа не выявлена, то возвращает None.
    :param text: Исходный текст для извлечения из него точки отказа.
    :return: Точка отказа или None, если точка отказа не выявлена.
    """
    classifier = NemoClf()
    return classifier.get_failure_point(text)


def get_device_type(text: str) -> str:
    """
    Принимает исходный текст. Извлекает тип оборудования и возвращает его,
    если тип оборудования не выявлен, то возвращает None.
    :param text: Исходный текст для извлечения из него типа оборудования.
    :return: Тип оборудования или None, если тип оборудования не выявлен.
    """
    classifier = NemoClf()
    return classifier.get_device_type(text)
