from appium.webdriver.common.mobileby import By


class MainPageLocators:
    BTN_KEYBOARD = (By.ID, 'ru.mail.search.electroscope:id/keyboard')
    INP_TEXT = (By.ID, 'ru.mail.search.electroscope:id/input_text')
    BTN_SEND_TEXT = (By.ID, 'ru.mail.search.electroscope:id/text_input_action')
    ARTICLE_NAME = (By.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    ITEM_WITH_TEXT = (By.XPATH, "//*[contains(@text, '{}')]")
    DIALOG_ANSWER = (By.ID, 'ru.mail.search.electroscope:id/dialog_item')
    BTN_SETTINGS = (By.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    TRACK_NEWS = (By.ID, 'ru.mail.search.electroscope:id/player_track_name')
    BTN_STOP_NEWS = (By.ID, 'ru.mail.search.electroscope:id/play_button')
    BTN_BAR = (By.ID, 'ru.mail.search.electroscope:id/player_seek_bar')


class SettingsPageLocators:
    BTN_NEWS_SOURCES = (By.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    BTN_ABOUT = (By.ID, 'ru.mail.search.electroscope:id/user_settings_about')


class NewsPageLocators:
    BTN_SELECT_SOURCE = (By.XPATH, '//*[@resource-id="ru.mail.search.electroscope:id/news_sources_item_title" '
                                   'and @text="{}"]')
    SELECTED_LOCATOR = (By.XPATH, '//*[contains(@text, "{}")]/following-sibling::android.widget.ImageView[1]')


class AboutPageLocators:
    ABOUT_LOCATOR = (By.ID, 'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT_LOCATOR = (By.ID, 'ru.mail.search.electroscope:id/about_copyright')
