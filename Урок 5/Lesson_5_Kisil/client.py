"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse
import logging
import log.conf.client_config_log
from errors import ReqFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import MessageProcessing

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')

class Client:
    """
    Формирование запроса о присуствии и направлении его на сервер,
    разбор ответа сервера
    """
    @staticmethod
    def create_presence(account_name='Guest'):
        """
        Функция генерирует запрос о присутствии клиента
        :param account_name:
        :return:
        """
        # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out

    @staticmethod
    def process_ans(message):
        """
        Функция разбирает ответ сервера
        :param message:
        :return:
        """
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            #return f'400 : {message[ERROR]}'
        raise ReqFieldMissingError(RESPONSE)


    def main(self):
        """
        Загружаем параметы коммандной строки (ip и порт), если нет параметров, то задаём значения по умоланию.
        направляем запрос на сервер, разбираем ответ
        """

        try:
            server_address = sys.argv[1]
            server_port = int(sys.argv[2])
            if server_port < 1024 or server_port > 65535:
                CLIENT_LOGGER.critical(
                    f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                    f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
                raise ValueError
        except IndexError:
            server_address = DEFAULT_IP_ADDRESS
            server_port = DEFAULT_PORT
        except ValueError:
            SERVER_LOGGER.error(f'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)
        CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                           f'адрес сервера: {server_address}, порт: {server_port}')

        # Инициализация сокета и обмен
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((server_address, server_port))
            message_to_server = self.create_presence()
            MessageProcessing.send_message(transport, message_to_server)
            answer = self.process_ans(MessageProcessing.get_message(transport))
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
            print(answer)
        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        except ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                                f'{missing_error.missing_field}')
        except (ConnectionRefusedError):
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                                   f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    m = Client()
    m.main()
