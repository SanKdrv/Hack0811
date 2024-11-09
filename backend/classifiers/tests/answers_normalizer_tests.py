import unittest
from ..answers_noramalizer import AnswerNormalizer, NormTypes

class TestAnswerNormalizer(unittest.TestCase):

    def test_normalize_equipment(self):
        # Проверяем нормализацию для оборудования
        result = AnswerNormalizer.normalize("ноутбук", NormTypes.Equipment)
        self.assertEqual(result, "Ноутбук")

        result = AnswerNormalizer.normalize("сервер", NormTypes.Equipment)
        self.assertEqual(result, "Сервер")

        result = AnswerNormalizer.normalize("схд", NormTypes.Equipment)
        self.assertEqual(result, "СХД")

    def test_normalize_failure(self):
        # Проверяем нормализацию для неисправностей
        result = AnswerNormalizer.normalize("аккумулятор", NormTypes.Failure)
        self.assertEqual(result, "Аккумулятор")

        result = AnswerNormalizer.normalize("блок питания", NormTypes.Failure)
        self.assertEqual(result, "Блок питания")

        result = AnswerNormalizer.normalize("динамики", NormTypes.Failure)
        self.assertEqual(result, "Динамики")

        result = AnswerNormalizer.normalize("wi-fi модуль", NormTypes.Failure)
        self.assertEqual(result, "Wi-fi модуль")

    def test_no_match_with_threshold_equipment(self):
        # Проверяем случай, когда нет подходящего совпадения и схожесть ниже порога
        result = AnswerNormalizer.normalize("монитор", NormTypes.Equipment, threshold=80)
        # Ожидаем, что результат будет None, так как схожесть ниже порога
        self.assertIsNone(result)

    def test_no_match_with_threshold_failure_as_None(self):
        # Проверяем случай, когда нет подходящего совпадения и схожесть ниже порога
        result = AnswerNormalizer.normalize("None", NormTypes.Failure, threshold=80)
        # Ожидаем, что результат будет None, так как схожесть ниже порога
        self.assertIsNone(result)
    def test_no_match_with_threshold_failure_as_Nan(self):
        # Проверяем случай, когда нет подходящего совпадения и схожесть ниже порога
        result = AnswerNormalizer.normalize("Nan", NormTypes.Failure, threshold=80)
        # Ожидаем, что результат будет None, так как схожесть ниже порога
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
