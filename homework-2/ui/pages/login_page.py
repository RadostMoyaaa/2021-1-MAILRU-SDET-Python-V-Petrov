from ui.pages.dashboard_page import DashBoardPage
from ui.locators.page_locators import BasePageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    url = 'https://target.my.com/'
    locators = BasePageLocators()

    def login(self):  # Метод логина
        self.go_link(self.url)

        sign1_btn = self.find(self.locators.SIGN1_BTN_LOCATOR)
        sign1_btn.click()

        self.send(self.locators.LOG_LOCATOR, self.LOGIN)
        self.send(self.locators.PASS_LOCATOR, self.PASSWORD)

        sign2_btn = self.find(self.locators.SIGN2_BTN_LOCATOR)
        sign2_btn.click()
        return DashBoardPage(self.driver)