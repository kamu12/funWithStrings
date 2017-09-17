import os
from fun_with_strings import FunWithStringsAPI
from flask_api import status
from flask import current_app
import unittest
import tempfile

class StringsTestCase(unittest.TestCase):

    def setUp(self):
        fs = FunWithStringsAPI(__name__)
        self.app = fs.app
        fs.app.testing = True
        self.app_test = fs.app.test_client()

    def test_get_word_success(self):
        with self.app_test as client:
            response = client.get('/get_word')
            self.assertTrue(status.is_success(response.status_code))

    def test_get_wiki_success(self):
        with self.app.test_request_context():
            fs = FunWithStringsAPI(__name__)
            fs.word = 'lviv'
            response = fs.get_wiki()
            self.assertTrue(status.is_success(response.status_code))

    def test_get_wiki_fail(self):
        with self.app.test_request_context():
            fs = FunWithStringsAPI(__name__)
            fs.word = 'lvivlvivlviv'
            response = fs.get_wiki()
            self.assertTrue(status.is_client_error(response.status_code))

    def test_get_words_success(self):
        with self.app.test_request_context():
            fs = FunWithStringsAPI(__name__)
            fs.word = 'lviv'
            response = fs.get_words()
            self.assertTrue(status.is_success(response.status_code))

    def test_get_words_fail(self):
        with self.app.test_request_context():
            fs = FunWithStringsAPI(__name__)
            fs.word = 'lviveiunewd'
            response = fs.get_words()
            self.assertTrue(status.is_client_error(response.status_code))

if __name__ == '__main__':
    unittest.main()