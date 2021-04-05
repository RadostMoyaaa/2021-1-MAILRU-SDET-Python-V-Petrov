import time

import pytest

from ui.tests.base import BaseCase


@pytest.mark.skip
class TestNegativeAuth(BaseCase):
    auto_login = False

    def test_auth_1(self):   # Негативный тест на авторизацию 1
        try:
            self.login_page.LOGIN = 'moxxxywork@gmail.com'
            self.login_page.PASSWORD = ''  # Не введен пароль
            self.login_page.login()
            url = self.login_page.get_url()
            assert url == 'https://target.my.com/dashboard'
        except AssertionError:
            return
        raise Exception(f'Bad Auth is passed LOGIN: {self.login_page.LOGIN}, PASSWORD: {self.login_page.PASSWORD}')

    def test_auth_2(self):  # Негативный тест на авторизацию 2
        try:
            self.login_page.LOGIN = 'moxxxywork@gmail.com'
            self.login_page.PASSWORD = self.login_page.PASSWORD.upper()  # Ввели пароль в верхнем регистре
            self.login_page.login()
            url = self.login_page.get_url()
            assert url == 'https://target.my.com/dashboard'
        except AssertionError:
            return
        raise Exception(f'Bad Auth is passed LOGIN: {self.login_page.LOGIN}, PASSWORD: {self.login_page.PASSWORD}')


class TestSegments(BaseCase):

    def test_add_segment(self):  # Тест на добавления сегмента
        segments_page = self.dashboard_page.go_to_segments()
        segment_id = segments_page.create_segment()
        segments_page.driver.refresh()
        assert segment_id in segments_page.get_segments_id_list()

    def test_delete_segment(self):  # Тест на удаление сегмента
        segments_page = self.dashboard_page.go_to_segments()
        segment_id = segments_page.create_segment()
        segments_page.driver.refresh()
        segments_page.delete_segment(segment_id)
        assert segment_id not in segments_page.get_segments_id_list()

