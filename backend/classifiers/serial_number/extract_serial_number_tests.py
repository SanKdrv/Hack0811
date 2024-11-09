import unittest
from regular_extractor import RegularExtractor  # Импортируем класс

class TestSerialNumberExtractor(unittest.TestCase):
    def setUp(self):
        """
        Настройка, выполняемая перед каждым тестом.
        Создаем экземпляр обработчика.
        """
        self.extractor = RegularExtractor()

    def test_simple_serial_number(self):
        """
        Тест для простого серийного номера.
        """
        text = "Прошу взять в ремонт ноутбук с серийным номером C223100360."
        expected = "C223100360"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_multiple_serial_numbers(self):
        """
        Тест для нескольких серийных номеров в одном тексте.
        """
        text = "Также прошу проверить серийные номера C223094534, D251110041 и C223014328."
        expected = "C223094534"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_russian_letters_and_mixed_case(self):
        """
        Тест для серийных номеров с русскими буквами и смешанным регистром.
        """
        text = "Серийные номера с ошибками: с223091001, C223012430 и С111120102."
        expected = "C223091001"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_concatenated_serial_numbers(self):
        """
        Тест для серийных номеров, которые идут подряд.
        """
        text = "Номера подряд: c223013523С223092735."
        expected = "C223013523"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_mixed_case_and_spacing(self):
        """
        Тест для смешанных регистра и пробелов между серийниками.
        """
        text = "Серийный номер: c223012961 с223100312. Следующий: C223090725."
        expected = "C223012961"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_multiple_concatenated_serial_numbers(self):
        """
        Тест для нескольких серийников, которые идут подряд без пробелов.
        """
        text = "Несколько номеров подряд: C223012430d252030021D251110041."
        expected = "C223012430"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_russian_and_latin_letters_mixed(self):
        """
        Тест для серийных номеров с русскими и латинскими буквами.
        """
        text = "Проверьте серийник: С111120102 и C223013523."
        expected = "C111120102"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_mixed_serial_numbers_with_repetitions(self):
        """
        Тест для серийных номеров, которые повторяются.
        """
        text = "Серийный номер встречается дважды: CKМ01212505744 и CKM01212505744."
        expected = "CKM01212505744"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_mixed_russian_english_letters(self):
        """
        Тест для смешанных наборов букв + слипшиеся.
        """
        text = "Серийный номер встречается дважды: CKМ01212505744cKm01212505744."
        expected = "CKM01212505744"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_mixed_with_russian_letters_in_sequence(self):
        """
        Тест для серийных номеров с русскими буквами.
        """
        text = "Ошибки с русскими буквами: С112040045, C222090950, C223090096."
        expected = "C112040045"
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

    def test_no_serial_numbers(self):
        """
        Тест для текста без серийных номеров.
        """
        text = "Текст без серийных номеров."
        expected = None
        self.assertEqual(self.extractor.extract_serial_number_from_text(text), expected)

if __name__ == '__main__':
    unittest.main()
