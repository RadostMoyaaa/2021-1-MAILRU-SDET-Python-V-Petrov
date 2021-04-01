from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from ui.locators.page_locators import BasePageLocators


class BasePage(object):
    locators = BasePageLocators()

    LOGIN = 'moxxxywork@gmail.com'
    PASSWORD = 'gFwXDGpiM8wus2M'
    url = 'https://target.my.com/'

    def __init__(self, driver):
        print('Создается объект BasePage')
        self.driver = driver

    def go_link(self, link):  # Метод перехода на страницу по ссылке
        self.driver.get(link)

    def find(self, locator, timeout=10):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def click(self, locator, timeout=10):
        for i in range(10):
            try:
                element = self.find(locator, timeout)
                element = self.wait(timeout).until(
                    EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == 9:
                    raise

    def send(self, locator, value):  # Метод отправки данных в форму
        form = self.find(locator)
        form.clear()
        form.send_keys(value)

    def login(self):  # Фикстура логина
        self.go_link(self.url)

        sign1_btn = self.find(self.locators.SIGN1_BTN_LOCATOR)
        sign1_btn.click()

        self.send(self.locators.LOG_LOCATOR, self.LOGIN)
        self.send(self.locators.PASS_LOCATOR, self.PASSWORD)

        sign2_btn = self.find(self.locators.SIGN2_BTN_LOCATOR)
        sign2_btn.click()

    def get_url(self):  # Метод для получения текущего url
        return self.driver.current_url
