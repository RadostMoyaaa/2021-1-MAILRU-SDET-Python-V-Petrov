from selenium.webdriver.common.by import By


class BasePageLocators:
    # Кнопка "Войти" в header-е
    SIGN1_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class, "responseHead-module-button")]')

    # Кнопка "Войти" в auth форме
    SIGN2_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class,"authForm-module-button")] ')

    # Поле email в auth форме
    LOG_LOCATOR = (By.NAME, 'email')

    # Поле password в auth форме
    PASS_LOCATOR = (By.NAME, 'password')


class DashBoardPageLocators:
    # UserName
    USERNAME_LOCATOR = (By.XPATH, './/div[contains(@class, "right-module-userNameWrap")]')

    # Локаторы для Logout
    # Кнопка меню
    MENU_LOCATOR = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')

    # Кнопка выйти
    EXIT_LOCATOR = (By.XPATH, '//a[contains(@class, "rightMenu-module-rightMenuLink") and contains(text(), "Выйти")]')

    # Кнопка сегменты
    BTN_SEGMENTS_LOCATOR = (By.XPATH, './/a[contains(@class, "center-module-segments") and contains(text(), "Аудитории")]')

    # Кнопка профиль
    BTN_PROFILE_LOCATOR = (By.XPATH, './/a[contains(@class, "center-module-profile") and contains(text(), "Профиль")]')


class SegmentsPageLocators(DashBoardPageLocators):
    # Кнопка "Создайте аудиторный сегмент"
    BTN_CREATE_SEGMENT = (By.XPATH, './/a[@href="/segments/segments_list/new/"]')

    BTN_SELECT_SEGMENT = (By.XPATH, './/div[contains(text(), "Приложения и игры в соцсетях")]')

    BTN_CHECKBOX_PLAYERS = (By.XPATH, './/input[contains(@class, "adding-segments-source__checkbox ")]')

    TEXT_SEGMENT_ID = (By.XPATH, './/div[contains(@class, "segmentsTable-module-idCellWrap")]//span')

    BTN_ADD_SEGMENT = (By.XPATH, './/div[@class="button__text" and contains(text(), "{}")]')

    # Кнопка список сегментов
    BTN_LIST_SEGMENTS = (By.XPATH, './/span[text()="Список сегментов"]/following-sibling::span')

    # Чек-бокс выбрать все элементы по id
    BTN_CHECKBOX_ID_ALL = (By.XPATH, './/div[contains(@class, "segmentsTable-module-idHeaderCellWrap")]//input')

    # Кнопка действия
    BTN_ACTIONS = (By.XPATH, '//span[text() = "Действия"]')

    BTN_DELETE_ACTION = (By.XPATH, './/li[@title="Удалить"]')

    BTN_CHECKBOX_ID = (By.XPATH, './/div[contains(@data-test, "id-{}")]//input')

    README_SEGMENT = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/div/input')