import pytest
import variables
import locators


class BaseCase:  # Базовый кейс
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):  # Setup фикстура
        self.driver = driver  # Сохраняем драйвер

    @pytest.fixture(scope='function')
    def login(self):  # Фикстура логина
        self.go_link(variables.LINK)

        sign1_btn = self.find(locators.SIGN1_BTN_LOCATOR)  # Ищем кнопку войти, кликаем
        sign1_btn.click()

        self.send(locators.LOG_LOCATOR, variables.LOGIN)  # Отправляем данные в поле логин
        self.send(locators.PASS_LOCATOR, variables.PASSWORD)  # Отправляем данные в поле пароль

        sign2_btn = self.find(locators.SIGN2_BTN_LOCATOR)  # Ищем кнопку войти в форме, кликаем
        sign2_btn.click()

    def go_link(self, link):  # Метод перехода на страницу по ссылке
        self.driver.get(link)

    def find(self, locator):  # Метод поиска элемента по локатору
        return self.driver.find_element(*locator)

    def send(self, locator, value):  # Метод отправки данных в форму
        form = self.find(locator)
        form.clear()
        form.send_keys(value)
