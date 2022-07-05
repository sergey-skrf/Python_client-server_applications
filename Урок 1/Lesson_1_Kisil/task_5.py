"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import chardet

def ping_of_web_resources(resource):
    '''
    Утилита пига ресурсов
    :param resource:
    :return:
    '''
    args_resource = ['ping', resource]
    resource_ping = subprocess.Popen(args_resource, stdout=subprocess.PIPE)
    for line in resource_ping.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))

list_resources = ['yandex.ru', 'youtube.com']
for el in list_resources:
    ping_of_web_resources(el)
