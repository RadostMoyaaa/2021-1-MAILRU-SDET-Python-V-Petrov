import config
from ui.pages.dashboard_page import DashBoardPage
from ui.locators.page_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):  # Страница Логина
    url = 'https://target.my.com/'
    locators = LoginPageLocators()
    LOGIN = config.LOGIN
    PASSWORD = config.PASSWORD

    def login(self):  # Метод логина
        self.go_link(self.url)

        sign1_btn = self.find_visible(self.locators.SIGN1_BTN_LOCATOR)
        sign1_btn.click()

        self.send_data(self.locators.LOG_LOCATOR, self.LOGIN)
        self.send_data(self.locators.PASS_LOCATOR, self.PASSWORD)

        sign2_btn = self.find_visible(self.locators.SIGN2_BTN_LOCATOR)
        sign2_btn.click()
        url = self.get_current_url()

        return DashBoardPage(self.driver)

    def change_creds(self, log, passw):
        self.LOGIN = log
        self.PASSWORD = passw