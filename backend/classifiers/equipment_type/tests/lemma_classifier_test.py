import unittest
from ..lemma_classifier import EquipmentDetector

class TestEquipmentDetector(unittest.TestCase):
    def test_detect_server(self):
        """Тестирование обнаружения 'сервер' в тексте"""
        text = ("Добрый вечер! На сервере появились системные ошибки. Скрин и логи прилагаю."
                " Предварительно на 03.09.24 (совместно с работами по замене серверов) инженерам"
                " необходимо по возможности устранить проблему или согласовать новую платформу.")
        detector = EquipmentDetector()
        result = detector.get_device_type(text)
        self.assertEqual(result, "Сервер", "Детектор должен обнаружить 'сервер' в тексте")

    def test_detect_laptop(self):
        """Тестирование обнаружения 'ноутбук' в тексте"""
        text = ("Прошу произвести диагностику и сориентировать по условиям ремонта данного ноутбука.")
        detector = EquipmentDetector()
        result = detector.get_device_type(text)
        self.assertEqual(result, "Ноутбук", "Детектор должен обнаружить 'ноутбук' в тексте")

    def test_detect_storage(self):
        """Тестирование обнаружения 'схд' в тексте"""
        text = ("Описание: Прошу открыть заявку на замену диска в схд. dd503.region..ru - Disk 3.2"
                " @dd503-p1(active:1)# system show serial Serial number: CKM01212505744")
        detector = EquipmentDetector()
        result = detector.get_device_type(text)
        self.assertEqual(result, "СХД", "Детектор должен обнаружить 'схд' в тексте")

    def test_no_equipment_detected(self):
        """Тестирование случая, когда оборудование не должно быть обнаружено"""
        text = "Это обычное сообщение без упоминания оборудования."
        detector = EquipmentDetector()
        result = detector.get_device_type(text)
        self.assertIsNone(result, "Детектор не должен находить оборудование в тексте без ключевых слов")

    def test_detect_multiple_mentions(self):
        """Тестирование случая с несколькими упоминаниями разных типов оборудования"""
        text = ("Вышел из строя диск, пришедший на замену по гарантии. Был в резерве проработал 2 месяца."
                " Прошу открыть заявку на ремонт (замену диска) для ноутбука и сервера.")
        detector = EquipmentDetector()
        result = detector.get_device_type(text)
        self.assertIn(result, ["Ноутбук", "Сервер"], "Детектор должен обнаружить одно из упомянутых устройств")

if __name__ == '__main__':
    unittest.main()
