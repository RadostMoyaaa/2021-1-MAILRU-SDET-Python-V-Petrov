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


class TestSegments(BaseCase):

    @allure.epic('Awesome PyTest framework')  # Тест на добавления сегмента
    @allure.feature('UI tests')
    @allure.story('Segments add test')
    @pytest.mark.ui
    def test_add_segment(self):
        self.logger.info(f'Going to segments, trying to create segment')

        with allure.step(f'Creating segment...'):
            segments_page = self.dashboard_page.go_to_segments()
            segment_id = segments_page.create_segment()
            segments_page.driver.refresh()
            segments_id_list = segments_page.get_segments_id_list()

        with allure.step(f'Checking "{segment_id}" in {segments_id_list}'):
            assert segment_id in segments_id_list

    @allure.epic('Awesome PyTest framework')  # Тест на удаление сегмента
    @allure.feature('UI tests')
    @allure.story('Segments delete test')
    @pytest.mark.ui
    def test_delete_segment(self):
        self.logger.info(f'Going to segments, trying to create and delete segment')

        with allure.step(f'Creating and deleting segment...'):
            segments_page = self.dashboard_page.go_to_segments()
            segment_id = segments_page.create_segment()
            segments_page.driver.refresh()
            segments_page.delete_segment(segment_id)
            segments_id_list = segments_page.get_segments_id_list()

        with allure.step(f'Checking created and deleted "{segment_id}" in {segments_id_list}'):
            assert segment_id not in segments_id_list
