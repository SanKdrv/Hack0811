from .classifiers.serial_number.regular_extractor import RegularExtractor
from .classifiers.Classifier import DeviceAnalysis


def get_serial_number(text: str) -> str:
    reg_extractor = RegularExtractor()
    # e = DeviceAnalysis()
    return reg_extractor.get_serial_number(text)


def get_failure_point(text: str) -> str:
    classifier = DeviceAnalysis()
    return classifier.get_point_of_failure(text)


def get_device_type(text: str) -> str:
    classifier = DeviceAnalysis()
    return classifier.get_type_of_device(text)

