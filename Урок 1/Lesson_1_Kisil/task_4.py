"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

list_of_words = ['разработка', 'администрирование', 'protocol', 'standard']
for el in list_of_words:
    EL_STR_BYTES = str.encode(el, encoding='utf-8')
    print(EL_STR_BYTES)
    BYTES_DEC = bytes.decode(EL_STR_BYTES, encoding='utf-8')
    print(BYTES_DEC)
    print('*' * 20)
