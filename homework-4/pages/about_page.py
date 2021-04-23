from pages.base_page import BasePage
from locators.page_locators import AboutPageLocators


class AboutPage(BasePage):
    locators = AboutPageLocators()

    def check_version(self, version):
        version = version.split('v')[-1].split('.apk')[0]
        about_text = self.find_visible(self.locators.ABOUT_LOCATOR).text
        about_text = about_text.split()[-1]
        assert version == about_text, f'ERROR version:{version}, about_text:{about_text}'

    def check_copyright(self, phrase):
        copyright_text = self.find_visible(self.locators.COPYRIGHT_LOCATOR).text
        copyright_text = copyright_text.split('.')[-2]
        assert phrase in copyright_text, f'ERROR phrase:{phrase}, about_text:{copyright_text}'
