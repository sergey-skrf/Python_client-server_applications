"""Утилиты"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decos import Log

class MessageProcessing:
    """
    Приём и декодирование сообщений,
    кодирование и их отправка
    """
    @classmethod
    @Log()
    def get_message(cls, client):
        """
        Утилита приёма и декодирования сообщения
        принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
        :param client:
        :return:
        """

        encoded_response = client.recv(MAX_PACKAGE_LENGTH)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode(ENCODING)
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError

    @classmethod
    @Log()
    def send_message(cls, sock, message):
        """
        Утилита кодирования и отправки сообщения
        принимает словарь и отправляет его
        :param sock:
        :param message:
        :return:
        """

        js_message = json.dumps(message)
        encoded_message = js_message.encode(ENCODING)
        sock.send(encoded_message)
