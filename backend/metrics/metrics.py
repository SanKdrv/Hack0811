import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
from Hack0811.backend.facade import get_device_type, get_failure_point, get_serial_number  # Импортируем фасад
import csv

# Основная функция для обработки данных из CSV и вычисления F1 метрики
def process_csv_and_calculate_f1(csv_file: str):
    """
    Высчитывает и строит график метрики f1-score для типа оборудования, точки отказа и серийного номера по отдельности.
    :param csv_file: Путь до файла csv с шапкой "index,Тема,Описание,Тип оборудования,Точка отказа,Серийный номер",
     данные из которого будут использоваться для сравнения.
    :return:
    """
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
        # print(f'Тип оборудования: Ожидаемое: {true_types[-1]} | Полученное {pred_types[-1]}')
        # print(f'Точка отказа: Ожидаемое: {true_failure_points[-1]} | Полученное {pred_failure_points[-1]}')

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


def process_csv_and_calculate_f1_2(csv_file: str):
    """
    Высчитывает и строит график метрики f1-score для типа оборудования, точки отказа и серийного номера по отдельности.
    :param csv_file: Путь до файла csv с шапкой "index,Тема,Описание,Тип оборудования,Точка отказа,Серийный номер",
     данные из которого будут использоваться для сравнения.
    :return:
    """
    # Загружаем CSV файл
    df = pd.read_csv(csv_file)


    pred_types = []
    pred_failure_points = []
    pred_serial_numbers = []

    with open('E:\\contest\\Hackaton0811\\Hackaton\\Hack0811\\backend\\files\\submission.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        result = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        result.writerow(['index','Тип оборудования','Точка отказа','Серийный номер'])
    # Обрабатываем каждую строку в CSV
        for index, row in df.iterrows():
            # Предсказания от нейронной сети
            theme = str(row['Тема'])
            desc = str(row['Описание'])
            ind = str(row['index'])
            pred_type = get_device_type(theme + ' ' + desc)
            pred_failure_point = get_failure_point(theme + ' ' + desc)
            pred_serial_number = get_serial_number(theme + ' ' + desc)
            pred_types.append(pred_type)
            pred_failure_points.append(pred_failure_point)
            pred_serial_numbers.append(pred_serial_number)
            print([ind, pred_type, pred_failure_point,pred_serial_number])
            result.writerow([ind, pred_type, pred_failure_point,pred_serial_number])


    # Строим график
    categories = ['Тип оборудования  ', 'Точка отказа', 'Серийный номер']


if __name__ == '__main__':
    # Пример вызова функции с CSV файлом
    process_csv_and_calculate_f1_2('../../data/datasets/test_sila/test_data_sila/test_data.csv')