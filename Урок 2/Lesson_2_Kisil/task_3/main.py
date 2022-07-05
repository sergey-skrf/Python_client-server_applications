"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

def write_to_yaml(file_name):
    """
    :param file_name: наименование файла для сохранения.
    :return: None
    """
    data_list = {
        'items': ['computer', 'printer', 'keyboard', 'mouse'],
        'items_quantity': 4,
        'items_price': {
            'computer': '200€-1000€',
            'keyboard': '5€-50€',
            'mouse': '4€-7€',
            'printer': '100€-300€'
        },
    }

    for el in data_list['items_price']:
        data_list['items_price'][el] = data_list['items_price'][el].encode("unicode_escape").decode("utf-8")

    with open(file_name, 'w', encoding='UTF-8') as file:
        yaml.dump(data_list, file, default_flow_style=False, allow_unicode=True)

    with open(file_name, encoding='UTF-8') as file:
        data_from_the_file = yaml.load(file, yaml.Loader)

    print('Результат проверки: ', data_list == data_from_the_file)


if __name__ == '__main__':
    write_to_yaml('new_file_yaml.yaml')
