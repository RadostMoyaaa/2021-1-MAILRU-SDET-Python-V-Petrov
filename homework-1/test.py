import variables
import locators
from base import BaseCase


class TestSite(BaseCase):  # Класс тест-сьют

    def test_login(self, login):  # Тест функции логина
        assert self.driver.current_url == variables.LINK_DASHBOARD

    def test_logout(self, login):  # Тест функции логаута
        self.logout()
        sign = self.find(locators.SIGN1_BTN_LOCATOR)
        assert sign.text == variables.SIGN_BTN_TEXT

