from ui.locators.page_locators import RegistrationPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()

    def registration(self, username, email, password, confirm, term=True):
        self.logger.info(f'Registration - {username}, {email}, {password}, {confirm}, {term}')
        self.send_data(locator=self.locators.USERNAME, value=username)
        self.send_data(locator=self.locators.EMAIL, value=email)
        self.send_data(locator=self.locators.PASS, value=password)
        self.send_data(locator=self.locators.CONFIRM, value=confirm)
        if term:
            self.click(self.locators.TERM_CHECK_BOX)
        self.click(self.locators.SUBMIT_BUTTON)
        return MainPage(driver=self.driver)

    def get_error_message(self):
        message = self.find(self.locators.ERROR_MESSAGE)
        self.logger.info(f'Checking error message - {message.text}')
        return message.text
