import enum

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class NormTypes(enum.Enum):
    Equipment = 0
    Failure = 1


class AnswerNormalizer:
    _eq_types = ['Ноутбук', "СХД", "Сервер"]
    _failure_points = [
        "jack", "SFP модуль", "Wifi-антенна", "Wi-fi модуль", "Аккумулятор",
        "Блок питания", "Вентилятор", "Динамики", "Диск", "Камера",
        "Клавиатура", "Материнская плата", "Матрица", "Оперативная память",
        "Программное обеспечение", "Сервер"
    ]

    @staticmethod
    def normalize(ai_answer: str, norm_type: NormTypes, threshold: int = 70):
        """
        Находит наиболее подходящий вариант из списка возможных ответов.
        Если степень схожести ниже порога, возвращает None.

        :param ai_answer: Строка с ответом пользователя.
        :param norm_type: Тип нормализации (Equipment или Failure).
        :param threshold: Порог схожести для принятия совпадений.
        :return: Строка с наиболее подходящим каноническим ответом или None.
        """
        best_match = None
        score = 0
        if norm_type == NormTypes.Equipment:
            best_match, score = process.extractOne(ai_answer, AnswerNormalizer._eq_types, scorer=fuzz.ratio)
        elif norm_type == NormTypes.Failure:
            best_match, score = process.extractOne(ai_answer, AnswerNormalizer._failure_points, scorer=fuzz.ratio)

        # Проверка, что совпадение достаточно хорошее
        if score < threshold:
            return None  # Возвращаем None, если совпадение слишком слабое

        return best_match
