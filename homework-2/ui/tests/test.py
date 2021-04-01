import time

import pytest

from ui.tests.base import BaseCase


class TestOne(BaseCase):

    def test_negative_auth1(self):  # Негативный тест на авторизацию 1
        try:
            self.base_page.LOGIN = 'moxxxywork@gmail.com'
            self.base_page.PASSWORD = ''
            self.base_page.login()
            url = self.base_page.get_url()
            assert url == 'https://target.my.com/dashboard'
        except AssertionError:
            return
        raise Exception(f'Bad Auth is passed LOGIN: {self.base_page.LOGIN}, PASSWORD: {self.base_page.PASSWORD}')

    def test_negative_auth2(self):
        pass

