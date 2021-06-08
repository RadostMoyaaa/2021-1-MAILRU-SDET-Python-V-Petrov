import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from ui.locators.page_locators import LoginPageLocators
from selenium.webdriver import ActionChains

logger = logging.getLogger('test')


class PageOpenException(Exception):
    pass


class BasePage(object):
    url = 'http://app:8080'
    locators = LoginPageLocators()

    def __init__(self, driver):
        self.driver = driver
        self.logger = logger

    def find(self, locator, timeout=5):
        self.logger.info(f'Find element {locator}')
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def get_current_url(self):
        return self.driver.current_url

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def click(self, locator, timeout=3):
        self.logger.info(f'Clicking on {locator}')
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

    def send_data(self, locator, value):
        form = self.find(locator)
        form.clear()
        form.send_keys(value)
        self.logger.info(f'Send {value} to {locator}')

    def check_window(self, expected_url):
        self.logger.info(f'Checking window {expected_url}')
        try:
            window = self.driver.window_handles
            self.driver.switch_to_window(window[1])
        except:
            raise PageOpenException('the page did not open in a separate window')
        assert self.driver.current_url == expected_url, f'the expected link {expected_url} is not equal ' \
                                                        f'to the current one{self.driver.current_url} '
