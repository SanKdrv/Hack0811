import requests
import time
import logging
import json


class SerialNumberAPI:
    def __init__(self, base_url="https://sila.ru/sites/all/themes/sila/assets/scripts/serial_number.php",
                 log_level=None):
        """
        Конструктор класса SerialNumberAPI. Инициализирует URL API, заголовки, куки и другие параметры.

        :param base_url: URL для запроса. По умолчанию используется URL API.
        :param log_level: Уровень логирования. По умолчанию None, если не указан, логирование не настраивается.
        """
        self.base_url = base_url  # Базовый URL для запросов
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://sila.ru",
            "Referer": "https://sila.ru/ru/waranty-form",
        }
        self.cookies = {
            "SSESS97cc778a33e38e35fff56a73345e7d3c": "Toyo1jdykfCBjtm7HtpR1jndp1Z9TaDVAnKT4hkLSE8",
            # добавьте другие куки, если они изменяются
        }
        self.max_retries = 3  # Максимальное количество попыток для повторных запросов
        self.timeout = 10  # Время ожидания перед повтором запроса (в секундах)

        # Если задан log_level, настроим логирование
        if log_level:
            self._setup_logging(log_level)

    def _setup_logging(self, log_level):
        """
        Настроить логирование для записи сообщений в файл и вывод в консоль.

        :param log_level: Уровень логирования, например DEBUG, INFO, WARNING, ERROR.
        """
        log_format = '%(asctime)s - %(levelname)s - %(message)s'  # Формат для сообщений лога

        # Обработчик для записи логов в файл
        file_handler = logging.FileHandler('serial_number_api.log', mode='a', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format))

        # Обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))

        # Основная настройка логирования
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler],
            format=log_format
        )
        logging.info(f"Логирование настроено с уровнем: {logging.getLevelName(log_level)}")

    def get_model_by_serial(self, serial_number: str, retries=0) -> str | None:
        """
        Получить информацию о модели по серийному номеру с учетом повторных попыток в случае ошибок.

        :param serial_number: Серийный номер для поиска.
        :param retries: Текущий счетчик попыток (по умолчанию 0).
        :return: Возвращает информацию о модели в формате JSON или None в случае ошибки.
        """
        data = {
            "serial_number": serial_number,  # Серийный номер для запроса
        }

        logging.info(f"Отправка запроса для серийного номера: {serial_number}")

        try:
            # Отправка POST-запроса на сервер
            response = requests.post(self.base_url, headers=self.headers, cookies=self.cookies, data=data,
                                     timeout=self.timeout)

            if response.status_code == 200:
                logging.info(f"Запрос успешен. Ответ получен для серийного номера: {serial_number}")
                return str(json.loads(response.text))  # Возвращаем тело ответа в формате JSON
            else:
                logging.warning(f"Ошибка: получен статус {response.status_code} для серийного номера: {serial_number}")
                return "None"

        except requests.Timeout:
            # В случае тайм-аута выполняем повторную попытку
            logging.warning(f"Таймаут для серийного номера: {serial_number}. Повторная попытка...")

        except requests.RequestException as e:
            # В случае других ошибок запроса, логируем ошибку
            logging.error(f"Ошибка при запросе для серийного номера {serial_number}: {e}")

        # Повторный запрос в случае ошибки или тайм-аута
        if retries < self.max_retries:
            time.sleep(2)  # Задержка перед повтором
            logging.info(f"Повторная попытка для серийного номера: {serial_number} ({retries + 1}/{self.max_retries})")
            return self.get_model_by_serial(serial_number, retries + 1)
        else:
            logging.error(f"Превышено количество попыток для серийного номера: {serial_number}")
            return "None"


# Пример использования
if __name__ == "__main__":
    # Создание объекта API с уровнем логирования DEBUG
    api = SerialNumberAPI(log_level=logging.DEBUG)

    serial_number = "C223012430"  # Пример серийного номера
    model_info = api.get_model_by_serial(serial_number)  # Получаем информацию о модели

    if model_info and "success" in model_info and model_info["success"]:
        print(f"Информация о модели: {model_info}")
        print(f"Модель: {model_info['Model']}")
        # Пример структуры model_info:
        # {'success': 1, 'msg': 'Гарантия найдена', 'Number': 'C223012430', 'Model': 'НК2-1404',
        # 'ServiceDesk': 17, 'Warrantydue': '2027-02-09', 'WarrantyType': 'Базовая', 'FormattedWarantyDue': '09.02.2027'}
    else:
        print("Не удалось получить информацию о модели.")
