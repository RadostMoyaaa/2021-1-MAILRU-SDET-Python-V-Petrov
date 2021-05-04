import os

import pytest
from appium import webdriver as awd
from pages.main_page import MainPage


@pytest.fixture(scope='function')
def capability_select(root, config):
    capability = {"platformName": "Android",
                  "platformVersion": "8.1",
                  "automationName": "Appium",
                  "appPackage": "ru.mail.search.electroscope",
                  "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
                  "app": os.path.join(root, 'stuff', config['apk']),
                  "orientation": "PORTRAIT",
                  "autoGrantPermissions": True,
                  "disableWindowAnimation": True,
                  }
    return capability


@pytest.fixture(scope='session')
def root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_addoption(parser):
    parser.addoption('--appium', default='http://127.0.0.1:4723/wd/hub')
    parser.addoption('--apk', default='Marussia_v1.39.1.apk')


@pytest.fixture(scope='session')
def config(request):
    appium = request.config.getoption('--appium')
    apk = request.config.getoption('--apk')
    return {'appium': appium, 'apk': apk}


@pytest.fixture(scope='function')
def driver(config, capability_select):
    appium_url = config['appium']
    desired_capability = capability_select
    driver = awd.Remote(appium_url, desired_capabilities=desired_capability)
    yield driver
    driver.quit()


@pytest.fixture()
def main_page(driver):
    return MainPage(driver=driver)
