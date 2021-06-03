import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage


class UnsupportedBrowserType(Exception):
    pass


def get_driver(config):  # Функция установления настроек подключения браузера к селеноиду
    browser_name = config['browser']
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.set_capability("browserVersion", "89.0")
        caps = {'browserName': browser_name,
                'version': '89.0',
                'sessionTimeout': '2m'}
        browser = webdriver.Remote(command_executor=f"http://selenoid:4444/wd/hub",
                                   options=options, desired_capabilities=caps)
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')
    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):  # Фикстура драйвера
    url = config['url']
    browser = get_driver(config)
    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.close()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)