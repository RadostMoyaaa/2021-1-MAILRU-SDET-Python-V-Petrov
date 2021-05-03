from locators.page_locators import NewsPageLocators
from pages.base_page import BasePage


class NewsPage(BasePage):
    locators = NewsPageLocators()

    def select_source(self, source):
        self.click(self.change_locator(self.locators.BTN_SELECT_SOURCE, source))
        return self.is_present(self.change_locator(self.locators.SELECTED_LOCATOR, source))

    def return_to_main_page(self, taps):
        self.tap_back_btn(taps)
