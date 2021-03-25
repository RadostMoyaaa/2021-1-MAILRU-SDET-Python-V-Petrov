from selenium.webdriver.common.by import By

# Локаторы для Login
# Кнопка "Войти" в header-е
SIGN1_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class, "responseHead-module-button")]')

# Кнопка "Войти" в auth форме
SIGN2_BTN_LOCATOR = (By.XPATH, './/div[contains(text(), "Войти") and contains(@class,"authForm-module-button")] ')

# Поле email в auth форме
LOG_LOCATOR = (By.NAME, 'email')

# Поле password в auth форме
PASS_LOCATOR = (By.NAME, 'password')

# UserName
USERNAME_LOCATOR = (By.XPATH, './/div[contains(@class, "right-module-userNameWrap")]')

# Локаторы для Logout
# Кнопка меню
MENU_LOCATOR = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')

# Кнопка выйти
EXIT_LOCATOR = (By.XPATH, '//a[contains(@class, "rightMenu-module-rightMenuLink") and contains(text(), "Выйти")]')

# Локаторы для изменения данных в профиле
# Кнопка профиль
BTN_PROFILE_LOCATOR = (By.XPATH, './/a[contains(@class, "center-module-profile") and contains(text(), "Профиль")]')

# Поле ФИО
FIO_LOCATOR = (By.XPATH, './/div[@data-name ="fio"]//input')

# Поле ТЕЛЕФОН
PHONE_LOCATOR = (By.XPATH, './/div[@data-name ="phone"]//input')

# Поле EMAIL
MAIL_LOCATOR = (By.XPATH, './/div[@data-class-name ="AdditionalEmailRow"]//input')

# Кнопка СОХРАНИТЬ
BTN_SAVE_LOCATOR = (By.XPATH, './/button[@class="button button_submit"]//div[contains(text(), "Сохранить")]')