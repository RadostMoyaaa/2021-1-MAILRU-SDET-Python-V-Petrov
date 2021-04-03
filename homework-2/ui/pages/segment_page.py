import time

from ui.locators.page_locators import SegmentsPageLocators
from ui.pages.base_page import BasePage

from selenium.common.exceptions import TimeoutException

class SegmentsPage(BasePage):  # Страница аудитории
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentsPageLocators()

    def create_segment(self):  # Метод добавления сегмента
        self.delete_segments()
        self.click(self.locators.BTN_CREATE_SEGMENT)   # Клик создать сегмент

        self.click(self.locators.BTN_SELECT_SEGMENT)  # Выбрать категорию сегмента

        self.click(self.locators.BTN_CHECKBOX_PLAYERS)  # Клик чекбокс

        self.click((self.locators.BTN_ADD_SEGMENT[0],
                    self.locators.BTN_ADD_SEGMENT[1].format('Добавить сегмент')))  # Клик добавить

        self.click((self.locators.BTN_ADD_SEGMENT[0],
                    self.locators.BTN_ADD_SEGMENT[1].format('Создать сегмент')))  # Клик создать

        id = self.find(self.locators.TEXT_SEGMENT_ID).text  # Сохраняем id

        return id  # Возвращаем id

    def delete_segments(self):  # Метод всех удаления сегментов
        try:
            self.find(self.locators.TEXT_SEGMENT_ID, timeout=3)
            self.click(self.locators.BTN_CHECKBOX_ID_ALL)
            self.click(self.locators.BTN_ACTIONS)
            self.click(self.locators.BTN_DELETE_ACTION)
        except TimeoutException:
            return

    def delete_segment(self):
        pass