from ui.locators.page_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.registration_page import RegistrationPage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def do_login(self, username, password):
        self.send_data(locator=self.locators.LOGIN_INPUT, value=username)
        self.send_data(locator=self.locators.PASSWORD_INPUT, value=password)
        self.click(self.locators.SUBMIT_BUTTON)

    def invalid_login(self):
        self.find(self.locators.FLASH)

    def go_registration(self):
        self.click(self.locators.NEW_ACCOUNT)
        return RegistrationPage(driver=self.driver)
