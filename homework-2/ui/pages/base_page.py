import random
import string

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
        self.driver = driver

    def go_link(self, link):  # Метод перехода на страницу по ссылке
        self.driver.get(link)

    def find(self, locator, timeout=20):
        self.wait(timeout).until(EC.presence_of_element_located(locator))
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def finds(self, locator, timeout=20):
        self.wait(timeout).until(EC.presence_of_all_elements_located(locator))
        return self.wait(timeout).until(EC.visibility_of_all_elements_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def click(self, locator, timeout=20):
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

    def get_url(self):  # Метод для получения текущего url
        return self.driver.current_url

    def random_text(self, count):  # Метод генерации текста
        result = ''
        for x in range(count):
            result += random.choice(string.ascii_letters)
        return result
