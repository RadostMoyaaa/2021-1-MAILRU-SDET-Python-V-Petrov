from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BUTTON = (By.ID, 'submit')
    NEW_ACCOUNT = (By.XPATH, '//a[@href = "/reg"]')
    FLASH = (By.ID, 'flash')


class RegistrationPageLocators:
    USERNAME = (By.ID, 'username')
    EMAIL = (By.ID, 'email')
    PASS = (By.ID, 'password')
    CONFIRM = (By.ID, 'confirm')
    TERM_CHECK_BOX = (By.ID, 'term')
    SUBMIT_BUTTON = (By.ID, 'submit')
    ERROR_MESSAGE = (By.ID, 'flash')


class MainPageLocators:
    HOME_BUTTON = (By.XPATH, 'fsd')
    NAVBAR_BUTTON = (By.XPATH, "//li[@class='uk-parent']/a[contains(text(), '{}')]")
    NAVBAR_LINK = (By.XPATH, "//a[text()='{}']")
    OVERLAY_LINK = (By.XPATH, "//div[contains(text(), '{}')]/following-sibling::figure")
    VK_ID = (By.XPATH, "//div[@id='login-name']//li[(text()='VK ID: {}')]")
    LOGOUT_BUTTON = (By.XPATH, "//div[@id='logout']")
    RANDOM_TEXT = (By.XPATH, "//footer//p[2]")

