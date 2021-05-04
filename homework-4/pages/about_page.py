from pages.base_page import BasePage
from locators.page_locators import AboutPageLocators


class AboutPage(BasePage):
    locators = AboutPageLocators()

    def get_version(self):
        about_text = self.find_visible(self.locators.ABOUT_LOCATOR).text
        about_text = about_text.split()[-1]
        return about_text

    def get_copyright(self):
        copyright_text = self.find_visible(self.locators.COPYRIGHT_LOCATOR).text
        copyright_text = copyright_text.split('.')[-2]
        return copyright_text

