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
    def normalize(ai_answer: str, norm_type: NormTypes):
        """
        Находит наиболее подходящий вариант из списка возможных ответов.

        :param user_answer: Строка с ответом пользователя.
        :return: Строка с наиболее подходящим каноническим ответом.
        """
        # Используем fuzzywuzzy для нахождения наилучшего совпадения
        best_match = None
        if norm_type == NormTypes.Equipment:
            best_match, score = process.extractOne(ai_answer, AnswerNormalizer._eq_types, scorer=fuzz.ratio)
        elif norm_type == NormTypes.Failure:
            best_match, score = process.extractOne(ai_answer, AnswerNormalizer._failure_points, scorer=fuzz.ratio)
        return best_match
