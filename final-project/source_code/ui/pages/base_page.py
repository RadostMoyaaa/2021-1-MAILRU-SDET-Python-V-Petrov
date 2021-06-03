import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from ui.locators.page_locators import LoginPageLocators
from selenium.webdriver import ActionChains

logger = logging.getLogger('test')


class BasePage(object):
    url = 'http://app:8080'
    locators = LoginPageLocators()

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    @allure.step('Find element {locator}')
    def find(self, locator, timeout=20):
        # return self.wait(timeout).until(EC.presence_of_element_located(locator))
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def get_current_url(self):
        return self.driver.current_url

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    @allure.step('Clicking on {locator}')
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

    @allure.step('Send {value} to {locator}')
    def send_data(self, locator, value):
        form = self.find(locator)
        form.clear()
        form.send_keys(value)
