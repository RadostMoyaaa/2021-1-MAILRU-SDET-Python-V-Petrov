import time

import pytest

from ui.tests.base import BaseCase


class TestNegativeAuth1(BaseCase):
    auto_login = False

    def test(self):  # Негативный тест на авторизацию 1
        try:
            self.login_page.LOGIN = 'moxxxywork@gmail.com'
            self.login_page.PASSWORD = ''
            self.login_page.login()
            url = self.login_page.get_url()
            assert url == 'https://target.my.com/dashboard'
        except AssertionError:
            return
        raise Exception(f'Bad Auth is passed LOGIN: {self.login_page.LOGIN}, PASSWORD: {self.login_page.PASSWORD}')


class TestNegativeAuth2(BaseCase):

    def test(self):  # Негативный тест на авторизацию 2
        print(self.dashboard_page.get_url())


