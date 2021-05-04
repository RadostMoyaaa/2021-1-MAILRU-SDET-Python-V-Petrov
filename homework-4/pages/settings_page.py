from pages.about_page import AboutPage
from pages.base_page import BasePage
from locators.page_locators import SettingsPageLocators
from pages.news_page import NewsPage


class SettingsPage(BasePage):
    locators = SettingsPageLocators()

    def click_to_news_sources(self):
        self.swipe_to_element(self.locators.BTN_NEWS_SOURCES, max_swipes=3)
        self.click(self.locators.BTN_NEWS_SOURCES)
        return NewsPage(driver=self.driver)

    def click_to_about_app(self):
        self.swipe_to_element(self.locators.BTN_ABOUT, max_swipes=3)
        self.click(self.locators.BTN_ABOUT)
        return AboutPage(driver=self.driver)