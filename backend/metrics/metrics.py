import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
from Hack0811.backend.facade import get_device_type, get_failure_point, get_serial_number  # Импортируем фасад


# Основная функция для обработки данных из CSV и вычисления F1 метрики
def process_csv_and_calculate_f1(csv_file: str):
    # Загружаем CSV файл
    df = pd.read_csv(csv_file)

    # Инициализация списков для хранения реальных и предсказанных значений
    true_types = []
    true_failure_points = []
    true_serial_numbers = []

    pred_types = []
    pred_failure_points = []
    pred_serial_numbers = []

    # Обрабатываем каждую строку в CSV
    for index, row in df.iterrows():
        # Истинные значения
        true_types.append(row['Тип оборудования'])
        true_failure_points.append(row['Точка отказа'])
        true_serial_numbers.append(row['Серийный номер'])

        # Предсказания от нейронной сети
        pred_types.append(get_device_type(row['Тема'] + ' ' + row['Описание']))
        pred_failure_points.append(get_failure_point(row['Тема'] + ' ' + row['Описание']))
        pred_serial_numbers.append(get_serial_number(row['Тема'] + ' ' + row['Описание']))

    # Вычисляем F1 метрику для каждого из столбцов
    f1_types = precision_recall_fscore_support(true_types, pred_types, average='macro')[2]
    f1_failure_points = precision_recall_fscore_support(true_failure_points, pred_failure_points, average='macro')[2]
    f1_serial_numbers = precision_recall_fscore_support(true_serial_numbers, pred_serial_numbers, average='macro')[2]

    print(f"F1 for Type: {f1_types}")
    print(f"F1 for Failure Point: {f1_failure_points}")
    print(f"F1 for Serial Number: {f1_serial_numbers}")

    # Строим график
    categories = ['Type', 'Failure Point', 'Serial Number']
    f1_scores = [f1_types, f1_failure_points, f1_serial_numbers]

    plt.bar(categories, f1_scores, color=['blue', 'green', 'red'])
    plt.xlabel('Categories')
    plt.ylabel('F1 Score')
    plt.title('F1 Score for Different Categories')
    plt.ylim([0, 1])
    plt.show()


if __name__ == '__main__':
    # Пример вызова функции с CSV файлом
    process_csv_and_calculate_f1('../../data/datasets/test_data/train_data_corrected.csv')
