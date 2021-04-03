import pytest
from selenium import webdriver

from ui.pages.login_page import LoginPage
from ui.pages.base_page import BasePage


@pytest.fixture(scope='function')
def driver():  # Фикстура драйвера
    browser = webdriver.Chrome()
    print('Фикстура driver')
    yield browser
    browser.close()


@pytest.fixture
def base_page(driver):  # Фикстура для создания объекта BasePage
    print('Фикстура base_page')
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):  # Фикстура для создания объекта BasePage
    print('Фикстура login_page')
    return LoginPage(driver=driver)


@pytest.fixture
def dashboard_page(driver, login_page):  # Фикстура для создания объекта BasePage
    print('Фикстура dashboard_page')
    return login_page.login()
