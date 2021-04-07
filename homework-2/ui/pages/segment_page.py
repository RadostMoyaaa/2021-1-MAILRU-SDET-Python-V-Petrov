from ui.locators.page_locators import SegmentsPageLocators
from ui.pages.base_page import BasePage


class SegmentsPage(BasePage):  # Страница аудитории
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentsPageLocators()

    def delete_segments(self):  # Метод всех удаления сегментов
        count = int(self.find(self.locators.BTN_LIST_SEGMENTS).text)
        if count != 0:
            self.click(self.locators.BTN_CHECKBOX_ID_ALL)
            self.click(self.locators.BTN_ACTIONS)
            self.click(self.locators.BTN_DELETE_ACTION)
        else:
            return

    def delete_segment(self, segment_id):
        self.click((self.locators.BTN_CHECKBOX_ID[0], self.locators.BTN_CHECKBOX_ID[1].format(segment_id)))
        self.click(self.locators.BTN_ACTIONS)
        self.click(self.locators.BTN_DELETE_ACTION)
        self.driver.refresh()
        return self.find(self.locators.BTN_LIST_SEGMENTS).text

    def create_segment(self):  # Метод добавления сегмента - новый
        count = self.find(self.locators.BTN_LIST_SEGMENTS).text  # Получаем количество сегментов
        if int(count) != 0:  # Если количество сегментов больше нуля
            self.click((self.locators.BTN_ADD_SEGMENT[0],
                        self.locators.BTN_ADD_SEGMENT[1].format('Создать сегмент')))  # Клик создать
        else:
            self.click(self.locators.BTN_CREATE_SEGMENT)  # Клик создать сегмент

        self.click(self.locators.BTN_SELECT_SEGMENT)  # Выбрать категорию сегмента

        self.click(self.locators.BTN_CHECKBOX_PLAYERS)  # Клик чекбокс

        self.click((self.locators.BTN_ADD_SEGMENT[0],
                    self.locators.BTN_ADD_SEGMENT[1].format('Добавить сегмент')))  # Клик добавить

        name = self.random_text(5)  # Рандом текста

        self.send(self.locators.INPUT_SEGMENT_NAME, name)  # Отправляем имя

        self.click((self.locators.BTN_ADD_SEGMENT[0],
                    self.locators.BTN_ADD_SEGMENT[1].format('Создать сегмент')))  # Клик создать

        segment_name_link = self.find((self.locators.BTN_NAME_SEGMENT[0], self.locators.BTN_NAME_SEGMENT[1].format(name)))

        href = segment_name_link.get_attribute('href')  # Получаем атрибут href у ссылки нашего сегмента

        segment_id = ''.join(i for i in href if i.isdigit())  # Сохраняем id

        return segment_id  # Возвращаем id

    def get_segments_id_list(self):  # Метод получения всех id сегментов
        segment_list = self.finds(self.locators.TEXT_SEGMENT_ID)
        segment_list = [x.text for x in segment_list]
        return segment_list

