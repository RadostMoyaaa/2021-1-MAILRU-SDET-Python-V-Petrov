import logging
import random
import string

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

logger = logging.getLogger('test')


class BasePage(object):  # Базовая страница
    url = 'https://target.my.com/'

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    @allure.step('Going {link}')
    def go_link(self, link):  # Метод перехода на страницу по ссылке
        self.driver.get(link)

    @allure.step('Find element {locator}')
    def find(self, locator, timeout=20):  # Метод поиска эелемента с ожиданием видимости
        self.wait(timeout).until(EC.presence_of_element_located(locator))
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    @allure.step('Find elements {locator}')
    def finds(self, locator, timeout=20):  # Метод поиска эелементов с ожиданием видимости
        self.wait(timeout).until(EC.presence_of_all_elements_located(locator))
        return self.wait(timeout).until(EC.visibility_of_all_elements_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    @allure.step('Clicking on {locator}')
    def click(self, locator, timeout=20):  # Метод клика
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

    @allure.step('Send {value} to {locator}')
    def send(self, locator, value):  # Метод отправки данных в форму
        form = self.find(locator)
        form.clear()
        form.send_keys(value)

    def get_url(self):  # Метод для получения текущего url
        return self.driver.current_url

    @allure.step('Generate text')
    def random_text(self, count):  # Метод генерации текста
        result = ''
        for x in range(count):
            result += random.choice(string.ascii_letters)
        return result

    @allure.step('Find invisible element {locator}')
    def find_invisible(self, locator, timeout=20):  # Метод поиска элемента без ожидания видимости
        return self.wait(timeout).until(EC.presence_of_element_located(locator))