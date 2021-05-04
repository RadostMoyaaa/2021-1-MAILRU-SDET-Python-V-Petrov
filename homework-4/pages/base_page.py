import random
import string
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def is_present(self, locator):
        try:
            self.find_visible(locator, timeout=20)
            result = True
        except TimeoutException:
            result = False
        return result

    def find_visible(self, locator, timeout=30):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def finds(self, locator, timeout=30):
        self.wait(timeout).until(EC.presence_of_all_elements_located(locator))
        return self.wait(timeout).until(EC.visibility_of_all_elements_located(locator))

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def click(self, locator, timeout=30):
        for i in range(20):
            try:
                element = self.find_visible(locator, timeout)
                element = self.wait(timeout).until(
                    EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == 9:
                    raise

    def send_data(self, locator, value):
        form = self.find_visible(locator)
        form.clear()
        form.send_keys(value)

    def random_text(self, count):
        result = ''
        for x in range(count):
            result += random.choice(string.ascii_letters)
        return result

    def change_locator(self, locator, text):
        return locator[0], locator[1].format(text)

    def swipe_element_lo_left(self, locator, count):
        web_element = self.find_visible(locator)
        left_x = web_element.location['x']
        right_x = left_x + web_element.rect['width']
        upper_y = web_element.location['y']
        lower_y = upper_y + web_element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        action = TouchAction(self.driver)
        for _ in range(count):
            action. \
                press(x=right_x, y=middle_y). \
                wait(ms=300). \
                move_to(x=left_x, y=middle_y). \
                release(). \
                perform()

    def swipe_up(self, swipetime=200):
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element(self, locator, max_swipes=10):
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def tap_back_btn(self, taps=1):
        for _ in range(taps):
            self.driver.back()
