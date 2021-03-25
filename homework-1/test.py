import variables
import locators
from base import BaseCase
import pytest


class TestSite(BaseCase):  # Класс тест-сьют

    def test_login(self, login):  # Тест функции логина
        assert self.driver.current_url == variables.LINK_DASHBOARD

    def test_logout(self, login):  # Тест функции логаута
        self.logout()
        sign = self.find(locators.SIGN1_BTN_LOCATOR)
        assert sign.text == variables.SIGN_BTN_TEXT

    def test_change_contact(self, login):  # Тест функции изменения данных в профайле
        fio, mail, phone = self.change_contacts()
        assert fio == self.find(locators.FIO_LOCATOR).get_attribute('value') and \
               phone == self.find(locators.PHONE_LOCATOR).get_attribute('value') and \
               mail == self.find(locators.MAIL_LOCATOR).get_attribute('value')

    @pytest.mark.parametrize(('xpath_btn', 'target_elem'), [(locators.BTN_PROFILE_LOCATOR, locators.PHONE_LOCATOR),
                                                            (locators.BTN_SEGMENTS_LOCATOR,
                                                             locators.TEXT_SEGMENTS_LOCATOR)])
    def test_links(self, login, xpath_btn, target_elem):  # Тест проверки перехода по секциям
        btn = self.find(xpath_btn)
        btn.click()

        elem = self.finds(target_elem)
        assert len(elem) != 0
