from selenium.webdriver.common.by import By


class LoginPageLocators:
    SIGN1_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class, "responseHead-module-button")]')
    SIGN2_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class,"authForm-module-button")] ')
    LOG_LOCATOR = (By.NAME, 'email')
    PASS_LOCATOR = (By.NAME, 'password')


class DashBoardPageLocators:
    USERNAME_LOCATOR = (By.XPATH, './/div[contains(@class, "right-module-userNameWrap")]')
    MENU_LOCATOR = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')
    EXIT_LOCATOR = (By.XPATH, '//a[contains(@class, "rightMenu-module-rightMenuLink") and contains(text(), "Выйти")]')
    BTN_SEGMENTS_LOCATOR = (By.XPATH, './/a[contains(@class, "center-module-segments") and contains(text(), "Аудитории")]')
    BTN_PROFILE_LOCATOR = (By.XPATH, './/a[contains(@class, "center-module-profile") and contains(text(), "Профиль")]')
    BTN_COMPANY_LOCATOR = (By.XPATH, './/a[text() = "Кампании"]')


class SegmentsPageLocators(DashBoardPageLocators):
    BTN_CREATE_SEGMENT = (By.XPATH, './/a[@href="/segments/segments_list/new/"]')
    BTN_SELECT_SEGMENT = (By.XPATH, './/div[contains(text(), "Приложения и игры в соцсетях")]')
    BTN_CHECKBOX_PLAYERS = (By.XPATH, './/input[contains(@class, "adding-segments-source__checkbox ")]')
    TEXT_SEGMENT_ID = (By.XPATH, './/div[contains(@class, "segmentsTable-module-idCellWrap")]//span')
    BTN_ADD_SEGMENT = (By.XPATH, './/div[@class="button__text" and contains(text(), "{}")]')
    BTN_LIST_SEGMENTS = (By.XPATH, './/span[text()="Список сегментов"]/following-sibling::span')
    BTN_CHECKBOX_ID_ALL = (By.XPATH, './/div[contains(@class, "segmentsTable-module-idHeaderCellWrap")]//input')
    BTN_ACTIONS = (By.XPATH, '//span[text() = "Действия"]')
    BTN_DELETE_ACTION = (By.XPATH, './/li[@title="Удалить"]')
    BTN_CHECKBOX_ID = (By.XPATH, './/div[contains(@data-test, "id-{}")]//input')
    INPUT_SEGMENT_NAME = (By.XPATH, './/div[@class="js-segment-name"]//input')
    BTN_NAME_SEGMENT = (By.XPATH, ".//a[text() ='{}']")


class CompanyPageLocators(DashBoardPageLocators):
    TITLE_INSTR_COMPANY = (By.XPATH, '//div[contains(text(), "С чего начать?")]')
    BTN_CREATE1_COMPANY = (By.XPATH, './/a[text() = "Создайте рекламную кампанию"]')
    BTN_CREATE2_COMPANY = (By.XPATH, './/div[@data-test="button"]/div[text()="Создать кампанию"]')
    BTN_TARGET_COMPANY = (By.XPATH, './/div[text() = "{}"]')
    INPUT_URL_COMPANY = (By.XPATH, './/input[@data-gtm-id = "ad_url_text"]')
    INPUT_NAME_COMPANY = (By.XPATH, './/div[contains(@class, "input_campaign-name")]//input')
    BTN_ADV_TYPE_COMPANY = (By.ID, 'patterns_4')
    INP_UPD_IMG_COMPANY = (By.XPATH, './/input[@type="file" and @data-test="image_240x400"]')
    BTN_SAVE_COMPANY = (By.XPATH, './/button[@data-class-name="Submit"]/div[text() = "Создать кампанию"]')
    LINKS_COMPANY = (By.XPATH, './/div[@data-entity-type="campaign"]//a')
