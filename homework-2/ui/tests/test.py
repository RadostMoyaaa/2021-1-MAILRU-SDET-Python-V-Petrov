import time

import pytest

from ui.tests.base import BaseCase


@pytest.mark.skip
class TestNegativeAuth1(BaseCase):  # Негативный тест на авторизацию 1
    auto_login = False

    def test(self):
        try:
            self.login_page.LOGIN = 'moxxxywork@gmail.com'
            self.login_page.PASSWORD = ''  # Не введен пароль
            self.login_page.login()
            url = self.login_page.get_url()
            assert url == 'https://target.my.com/dashboard'
        except AssertionError:
            return
        raise Exception(f'Bad Auth is passed LOGIN: {self.login_page.LOGIN}, PASSWORD: {self.login_page.PASSWORD}')


@pytest.mark.skip
class TestNegativeAuth2(BaseCase):  # Негативный тест на авторизацию 2
    auto_login = False

    def test(self):
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
    @pytest.mark.skip
    def test_add_segment(self):  # Тест на добавления сегмента
        segments_page = self.dashboard_page.go_to_segments()
        segments_page.delete_segments()
        segment_id = segments_page.create_segment()
        segments_page.driver.refresh()
        assert segment_id == segments_page.find(segments_page.locators.TEXT_SEGMENT_ID).text

    @pytest.mark.parametrize('c', list(range(3)))
    def test_delete_segment(self, c):  # Тест на добавления сегмента
        segments_page = self.dashboard_page.go_to_segments()
        segments_page.delete_segments()
        segment_id = segments_page.create_segment()
        count = segments_page.delete_segment(segment_id)
        assert count == '0'



