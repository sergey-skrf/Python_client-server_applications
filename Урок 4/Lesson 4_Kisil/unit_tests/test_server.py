"""Unit-тесты сервера"""

import sys
import os
import unittest
#sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import Server

class TestServer(unittest.TestCase):
    '''
    Класс с тестом для сервера
    '''

    err_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        """Ошибка если нет действия"""
        test_server = Server().process_client_message({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test_server, self.err_dict)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        test_server = Server().process_client_message({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}})
        print(test_server)
        self.assertEqual(test_server, self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        test_server = Server().process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test_server, self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        test_server = Server().process_client_message({ACTION: PRESENCE, TIME: '1.1'})
        self.assertEqual(test_server, self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        test_server = Server().process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}})
        self.assertEqual(test_server, self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        test_server = Server().process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test_server, self.ok_dict)



if __name__ == '__main__':
    unittest.main()
