import pytest
from selenium import webdriver
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


