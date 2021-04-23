import os

import pytest
from appium import webdriver as awd  # Импорт webdriver аппиума
from pages.main_page import MainPage


def capability_select():
    capability = {"platformName": "Android",
                  "platformVersion": "8.1",
                  "automationName": "Appium",
                  "appPackage": "ru.mail.search.electroscope",
                  "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
                  "app": 'C:\\Users\\Nero\Desktop\MailRuHomework\\2021-1-MAILRU-SDET-Python-V-Petrov\homework-4\stuff\Marussia_v1.39.1.apk',
                  "orientation": "PORTRAIT",
                  "autoGrantPermissions": True
                  }
    return capability


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_addoption(parser):  # Функция добавления опций
    parser.addoption('--appium', default='http://127.0.0.1:4723/wd/hub')


@pytest.fixture(scope='session')
def config(request):  # Парсер опций
    appium = request.config.getoption('--appium')
    return {'appium': appium}


@pytest.fixture(scope='function')
def driver(config):
    appium_url = config['appium']   # Запрос адрес сервера appium с config
    desired_capability = capability_select()
    driver = awd.Remote(appium_url, desired_capabilities=desired_capability)
    yield driver


@pytest.fixture()
def main_page(driver):
    return MainPage(driver=driver)
