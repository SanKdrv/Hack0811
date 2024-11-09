# IMIT_SPC "СИЛА"

## Суть кейса

Автоматизация деятельности сотрудников первой линии поддержки по диспетчеризации заявок.

Из письма клиента (тема, основная часть письма) необходимо автоматически выделить информацию о типе оборудования, на
котором произошла поломка, точке отказа (части оборудования, которая отказала) и серийном номере оборудования. 
При недостатке информации необходимо сообщить об этом клиенту.

## Подход к решению

1. Выделение трёх подзадач, которые могут решаться параллельно, а именно: определение типа оборудования, определение точки отказа, определение серийного номера.
2. Решение каждой подзадачи с применением нейронных сетей, языковых моделей, алгоритмов обработки текста
3. Разработка API и web-интерфейса
4. Ручная чистка, доработка датасета
5. Итеративное тестирование на датасете и доработка решения


## Структура кода

Представлена упрощенная структура кода, которая выделяет наиболее важные для работы системы файлы и директории.

```
Hack0811
├── frontend
├── data
|   └── datasets
|
└── backend
    ├── main.py
    ├── facade.py
    ├── classifiers
    |   ├── equipment_type
    |   ├── failure_point
    |   ├── serial_number
    |   └── nemo_clf.py
    |
    └── metrics
```

- **backend** — Содержит серверную часть, включая API для взаимодействия с классификаторами.
    - **main.py** — API, основной файл для обработки запросов и маршрутов API.
    - **facade.py** — фасад, включающий в себя основные функции для обращения к моделям.
    - **classifiers** — Подкаталог с различными классификаторами для типов оборудования, точек отказа и серийных
      номеров.
    - **metrics** — Скрипты для мониторинга и сбора статистики по работе модели.

- **frontend** — Фронтенд для визуализации данных и взаимодействия с пользователем.
    - **index.html** — Главная страница для отображения данных и вывода результатов.
    - **main.js** — Логика взаимодействия с сервером и обновления данных на странице.
    - **style.css** — Стилизация страницы.

- **data** — Хранилище для датасетов и других данных, используемых в проекте.
    - **datasets** — Датасеты для обучения и тестирования моделей.

## Технологии и библиотеки

- Python 3.12+
- Flask (для создания API)
- scikit-learn (для работы с данными)
- pandas (для работы с данными)
- matplotlib (для работы с данными)

## Зависимости

`requirements.txt`

### Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/SanKdrv/Hack0811.git
   cd Hack0811
   ```

2. Создайте и активируйте виртуальное окружение:

   ```
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:

    `pip install -r requirements.txt`

4. Запустите сервер:

   Для Flask:

   `python backend/main.py`

    Для FastAPI:
    
    `uvicorn backend.api:app --reload`


5. Откройте в браузере http://127.0.0.1:8000 для взаимодействия с API и фронтендом.

## Преимущества

* Использование обученных языковых моделей
* Исходный датасет используется как тестовый 
* Парсинг дополнительной информации об оборудовании по серийному номеру на сайте организации "СИЛА"
* Пользовательский интерфейс в виде чат-бота с обратной связью, который может быть внедрен на сайт организации "СИЛА" для удобства пользователя и ускорения бизнес-процессов
