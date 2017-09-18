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
        with self.app_test as client:
            response = client.get('/get_wiki/lviv')
            self.assertTrue(status.is_success(response.status_code))

    def test_get_wiki_fail(self):
        with self.app_test as client:
            response = client.get('/get_wiki/lvivasdzxc')
            self.assertTrue(status.is_client_error(response.status_code))


    def test_get_words_success(self):
        with self.app_test as client:
            response = client.get('/get_words/lviv')
            self.assertTrue(status.is_success(response.status_code))

    def test_get_words_fail(self):
        with self.app_test as client:
            response = client.get('/get_words/lvivasdzxc')
            self.assertTrue(status.is_client_error(response.status_code))

    def test_get_words_fail_with_n(self):
        with self.app_test as client:
            response = client.get('/get_words/lvivasdzxc/8')
            self.assertTrue(status.is_client_error(response.status_code))

    def test_get_words_alot(self):
        with self.app_test as client:
                response = client.get('/get_words/lviv/10000')
                self.assertTrue(status.is_success(response.status_code))

    def test_get_words_zero(self):
        with self.app_test as client:
            response = client.get('/get_words/lviv/0')
            self.assertTrue(status.is_success(response.status_code))

    def test_get_words_negative(self):
        with self.app_test as client:
            response = client.get('/get_words/lviv/-1')
            self.assertTrue(status.is_client_error(response.status_code))

    def test_joke_sucess(self):
        with self.app_test as client:
            response = client.get('/get_joke')
            self.assertTrue(status.is_success(response.status_code))

    def test_joke_first_name_sucess(self):
        with self.app_test as client:
            response = client.get('/get_joke?firstName=Bruce')
            self.assertTrue(status.is_success(response.status_code))

    def test_joke_last_name_sucess(self):
        with self.app_test as client:
            response = client.get('/get_joke?lastName=Lee')
            self.assertTrue(status.is_success(response.status_code))

    def test_joke_full_name_sucess(self):
        with self.app_test as client:
            response = client.get('/get_joke?firstName=Bruce&lastName=Lee')
            self.assertTrue(status.is_success(response.status_code))



if __name__ == '__main__':
    unittest.main()