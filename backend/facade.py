from backend.classifiers.serial_number.regular_extractor import RegularExtractor
from .classifiers.nemo_clf import NemoClf
from .classifiers.serial_number.serial_number_api import SerialNumberAPI

from .classifiers.equipment_type.lemma_classifier import EquipmentDetector

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
    # classifier = EquipmentDetector()
    classifier = NemoClf()
    return classifier.get_device_type(text)


def get_model_info_by_serial_number(serial_number: str) -> dict | None:
    """
    Получение информации о модели по серийному номеру.
    Структура возвращаемого значения:
    {'success': 1, 'msg': 'Гарантия найдена', 'Number': 'C223012430', 'Model': 'НК2-1404',
    'ServiceDesk': 17, 'Warrantydue': '2027-02-09', 'WarrantyType': 'Базовая', 'FormattedWarantyDue': '09.02.2027'}
    :param serial_number: Серийный номер оборудования.
    :return: Информация о серийном номере в словаре (dict) или None, если серийный номер не найден на сайте.
    """
    api = SerialNumberAPI()
    model_info = api.get_model_by_serial(serial_number)

    if model_info and "success" in model_info and model_info["success"]:
        return model_info
    else:
        return None
