from pages.base_page import BasePage
from locators.page_locators import MainPageLocators
from pages.settings_page import SettingsPage


class MainPage(BasePage):  # Базовая страница
    locators = MainPageLocators()

    def send_question(self, question):
        self.click(self.locators.BTN_KEYBOARD)
        self.send_data(self.locators.INP_TEXT, question)
        self.click(self.locators.BTN_SEND_TEXT)
        self.driver.hide_keyboard()

    def swipe_from_to_target_and_click(self, from_btn, target_btn, count_swipes=2):
        new_from_btn_locator = self.change_locator(self.locators.ITEM_WITH_TEXT, from_btn)
        self.swipe_element_lo_left(new_from_btn_locator, count_swipes)
        new_target_btn_locator = self.change_locator(self.locators.ITEM_WITH_TEXT, target_btn)
        self.click(new_target_btn_locator)

    def check_article(self, check):
        new_article_locator = self.change_locator(self.locators.ITEM_WITH_TEXT, check)
        target_text = self.find_visible(new_article_locator).text
        assert check == target_text, f'Error: check: {check}, target text: {target_text} '

    def check_dialog_answer(self, check):
        answer = self.finds(self.locators.DIALOG_ANSWER)[1].text
        assert answer == check, f'Error: check: {check}, answer: {answer} '

    def go_to_settings(self):
        self.click(self.locators.BTN_SETTINGS)
        return SettingsPage(driver=self.driver)

    def check_news_track_name(self, check):
        track = self.find_visible(self.locators.TRACK_NEWS).text
        assert track == check, f'Error: check {check}, track {track}'
