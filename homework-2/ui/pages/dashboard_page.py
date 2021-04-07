from ui.pages.base_page import BasePage
from ui.locators.page_locators import DashBoardPageLocators


class DashBoardPage(BasePage):  # Класс страницы Dashboard
    url = 'https://target.my.com/dashboard'
    locators = DashBoardPageLocators()
