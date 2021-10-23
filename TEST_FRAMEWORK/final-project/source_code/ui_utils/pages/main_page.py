import allure

from ui_utils.locators.page_locators import MainPageLocators
from ui_utils.pages.base_page import BasePage


class MainPage(BasePage):
    locators = MainPageLocators()
    url = f'http://app:8080/welcome/'

    def check_navbar_link(self, navbar_btn_name, navbar_link, expected_url):
        self.go_to_navbar_link(navbar_btn_name, navbar_link)
        self.check_window(expected_url=expected_url)

    def check_overlay_link(self, btn_title, expected_url):
        self.go_to_overlay_link(btn_title)
        self.check_window(expected_url=expected_url)

    def go_to_navbar_link(self, navbar_button, navbar_link):
        self.logger.info(f'Going navbar {navbar_button}, click {navbar_link}')
        button = self.find((self.locators.NAVBAR_BUTTON[0], self.locators.NAVBAR_BUTTON[1].format(navbar_button)))
        self.action_chains.move_to_element(button).perform()
        self.click((self.locators.NAVBAR_LINK[0], self.locators.NAVBAR_LINK[1].format(navbar_link)))

    def go_to_overlay_link(self, title):
        self.logger.info(f'Click overlay {title}')
        self.click((self.locators.OVERLAY_LINK[0], self.locators.OVERLAY_LINK[1].format(title)))

    def click_logout(self):
        self.logger.info(f'Click logout')
        self.click(self.locators.LOGOUT_BUTTON)

    def get_vk_id(self, expected_id=''):
        vk_id_locator = (self.locators.VK_ID[0], self.locators.VK_ID[1].format(expected_id))
        self.find(vk_id_locator)
        self.logger.info(f'Checking VK_ID: expected - {expected_id}')

    def get_username(self):
        name = self.find(self.locators.USERNAME_TEXT).text
        return name


