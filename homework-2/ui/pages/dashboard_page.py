from ui.pages.segment_page import SegmentsPage
from ui.pages.base_page import BasePage
from ui.locators.page_locators import DashBoardPageLocators


class DashBoardPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = DashBoardPageLocators()

    def go_to_segments(self):
        self.click(self.locators.BTN_SEGMENTS_LOCATOR)
        return SegmentsPage(self.driver)