import logging
import allure

from ui.locators.page_locators import MainPageLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class MainPage(BasePage):
    locators = MainPageLocators()

    def go_to_navbar_link(self, navbar_button, navbar_link):
        button = self.find((self.locators.NAVBAR_BUTTON[0], self.locators.NAVBAR_BUTTON[1].format(navbar_button)))
        self.action_chains.move_to_element(button).perform()
        self.click((self.locators.NAVBAR_LINK[0], self.locators.NAVBAR_LINK[1].format(navbar_link)))

    def go_to_overlay_link(self, title):
        self.click((self.locators.OVERLAY_LINK[0], self.locators.OVERLAY_LINK[1].format(title)))

    def click_logout(self):
        self.click(self.locators.LOGOUT_BUTTON)

    def get_random_text_in_footer(self):
        return self.find(self.locators.RANDOM_TEXT).text
