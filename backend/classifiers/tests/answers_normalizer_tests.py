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

    def test_no_match_equipment(self):
        # Проверяем случай, когда нет точного совпадения
        result = AnswerNormalizer.normalize("монитор", NormTypes.Equipment)
        # Ожидаем, что результат будет наиболее похож на один из существующих вариантов
        self.assertIn(result, AnswerNormalizer._eq_types)

    def test_no_match_failure(self):
        # Проверяем случай, когда нет точного совпадения для неисправности
        result = AnswerNormalizer.normalize("экран", NormTypes.Failure)
        # Ожидаем, что результат будет наиболее похож на один из существующих вариантов
        self.assertIn(result, AnswerNormalizer._failure_points)


if __name__ == '__main__':
    unittest.main()
