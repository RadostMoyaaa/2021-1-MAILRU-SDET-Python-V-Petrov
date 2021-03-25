import pytest
from selenium import webdriver


# Фикстура driver
@pytest.fixture(scope='function')
def driver():
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.maximize_window()
    yield browser
    browser.close()
