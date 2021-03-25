import pytest
import variables
import locators
import time
import random
import string

class BaseCase:  # Базовый кейс
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):  # Setup фикстура
        self.driver = driver  # Сохраняем драйвер

    @pytest.fixture(scope='function')
    def login(self):  # Фикстура логина
        self.go_link(variables.LINK)

        sign1_btn = self.find(locators.SIGN1_BTN_LOCATOR)
        sign1_btn.click()

        self.send(locators.LOG_LOCATOR, variables.LOGIN)
        self.send(locators.PASS_LOCATOR, variables.PASSWORD)

        sign2_btn = self.find(locators.SIGN2_BTN_LOCATOR)
        sign2_btn.click()

    def go_link(self, link):  # Метод перехода на страницу по ссылке
        self.driver.get(link)

    def find(self, locator):  # Метод поиска элемента по локатору
        return self.driver.find_element(*locator)

    def send(self, locator, value):  # Метод отправки данных в форму
        form = self.find(locator)
        form.clear()
        form.send_keys(value)

    def get_url(self):  # Метод для получения текущего url
        return self.driver.current_url

    def logout(self):  # Метод логаута
        time.sleep(3)
        menu_btn = self.find(locators.MENU_LOCATOR)
        menu_btn.click()

        time.sleep(3)
        exit_btn = self.find(locators.EXIT_LOCATOR)
        exit_btn.click()
        time.sleep(3)

    def random_text(self, count, type_text=''):  # Метод генерации текста
        result = ''
        if type_text == 'phone':
            result += '+'
            if count > 11:
                count = 11
            for x in range(count):
                result += str(random.randint(0, 9))
        elif type_text == 'email':
            for x in range(count):
                result += random.choice(string.ascii_letters)
            result += '@gmail.com'
        else:
            for x in range(count):
                result += random.choice(string.ascii_letters)
        return result

    def change_contacts(self):  # Метод изменения данных в профиле
        btn_profile = self.find(locators.BTN_PROFILE_LOCATOR)
        btn_profile.click()

        fio = self.random_text(10)
        self.send(locators.FIO_LOCATOR, fio)

        phone = self.random_text(11, 'phone')
        self.send(locators.PHONE_LOCATOR, phone)

        mail = self.random_text(7, 'email')
        self.send(locators.MAIL_LOCATOR, mail)

        btn_save = self.find(locators.BTN_SAVE_LOCATOR)
        btn_save.click()

        time.sleep(2)

        self.driver.refresh()
        return fio, mail, phone
