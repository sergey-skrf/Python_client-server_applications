"""Программа-сервер"""

import socket
import sys
import argparse
import json
import logging
import log.conf.server_config_log
from errors import IncorrectDataRecivedError
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import MessageProcessing

#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')

class Server:
    """
    Обработка сообщений клиента
    """
    @staticmethod
    def process_client_message(message):
        """
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :return:
        """
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        if ACTION in message and\
                message[ACTION] == PRESENCE and\
                TIME in message and\
                USER in message and\
                message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        SERVER_LOGGER.error(f'Неверный запрос от клиета : {message}')
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


    def main(self):
        """
        Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
        Сначала обрабатываем порт:
        server.py -p 8079 -a 192.168.1.2
        :return:
        """

        try:
            if '-p' in sys.argv:
                listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            else:
                listen_port = DEFAULT_PORT
            if listen_port < 1024 or listen_port > 65535:
                SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                       f'{listen_port}. Допустимы адреса с 1024 до 65535.')
                raise ValueError
        except IndexError:
            SERVER_LOGGER.error(f'После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            SERVER_LOGGER.error(f'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)


        # Затем загружаем какой адрес слушать
        try:
            if '-a' in sys.argv:
                listen_address = sys.argv[sys.argv.index('-a') + 1]
            else:
                listen_address = ''
            SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                               f'адрес с которого принимаются подключения: {listen_address}. '
                               f'Если адрес не указан, принимаются соединения с любых адресов.')
        except IndexError:
            SERVER_LOGGER.error(f'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)


        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((listen_address, listen_port))

        # Слушаем порт
        transport.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = transport.accept()
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')

            try:
                message_from_client = MessageProcessing.get_message(client)
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')

                response = self.process_client_message(message_from_client)
                SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')

                MessageProcessing.send_message(client, response)
                SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')

                client.close()
            except IncorrectDataRecivedError:
                SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                    f'Соединение закрывается.')
                client.close()


if __name__ == '__main__':
    s = Server()
    s.main()
