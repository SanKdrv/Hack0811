from .classifiers.serial_number.regular_extractor import RegularExtractor
from .classifiers.nemo_clf import NemoClf


def get_serial_number(text: str) -> str | None:
    reg_extractor = RegularExtractor()
    # e = NemoClf()
    return reg_extractor.get_serial_number(text)


def get_failure_point(text: str) -> str:
    classifier = NemoClf()
    return classifier.get_failure_point(text)


def get_device_type(text: str) -> str:
    classifier = NemoClf()
    return classifier.get_device_type(text)

