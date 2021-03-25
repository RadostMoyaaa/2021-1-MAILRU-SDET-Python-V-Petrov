import variables
import locators
from base import BaseCase


class TestSite(BaseCase):  # Класс тест-сьют

    def test_login(self, login):  # Тест функции логина
        assert self.driver.current_url == variables.LINK_DASHBOARD
