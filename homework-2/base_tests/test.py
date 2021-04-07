import os

import allure
import pytest

from base_tests.base import BaseCase


class TestNegativeAuth(BaseCase):
    auto_login = False

    @allure.epic('Awesome PyTest framework')  # Негативный тест на авторизацию 1
    @allure.feature('UI tests')
    @allure.story('Log negative test')
    @pytest.mark.ui
    def test_auth_1(self):
        self.logger.info('Going to target.my.com, trying to login')
        self.login_page.PASSWORD = ''  # Не введен пароль

        with allure.step(f'First negative login cred\'s: {self.login_page.LOGIN, self.login_page.PASSWORD}'):
            with pytest.raises(AssertionError):
                self.login_page.login()
                url = self.login_page.get_url()
                assert url == 'https://target.my.com/dashboard'
                pytest.fail(msg='Bad cred\'s failed')

    @allure.epic('Awesome PyTest framework')  # Негативный тест на авторизацию 2
    @allure.feature('UI tests')
    @allure.story('Log negative test')
    @pytest.mark.ui
    def test_auth_2(self):
        self.logger.info('Going to target.my.com, trying to login')
        self.login_page.PASSWORD = self.login_page.PASSWORD.upper()  # Ввели пароль в верхнем регистре

        with allure.step(f'Second negative login cred\'s: {self.login_page.LOGIN, self.login_page.PASSWORD}'):
            with pytest.raises(AssertionError):
                self.login_page.login()
                url = self.login_page.get_url()
                assert url == 'https://target.my.com/dashboard'
                pytest.fail(msg='Bad cred\'s failed')

