import shutil
import sys



from mysql_client.client import MySqlClient
import os
from api_client.client import ApiClient
import attributes
import logging
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default=f'http://app:8080')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--device', default='web')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    device = request.config.getoption('--device')
    return {'url': url, 'browser': browser, 'device': device}


@pytest.fixture(scope='session')
def mysql_client():
    my_sql_client = MySqlClient(user='test_qa', password='qa_test', db_name='TEST')
    my_sql_client.connect()
    yield my_sql_client
    my_sql_client.connection.close()


def prepare_database():
    my_sql_client = MySqlClient(user='test_qa', password='qa_test', db_name='TEST')
    my_sql_client.recreate_db()
    my_sql_client.connect()
    my_sql_client.create_table_test_users()
    my_sql_client.connection.close()


def base_dir(base_test_dir):
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')[:100]
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


def pytest_configure(config):
    base_test_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        prepare_database()
        base_dir(base_test_dir)
    config.base_test_dir = base_test_dir


# def pytest_unconfigure(config):  # TODO исправить
#     if not hasattr(config, 'workerinput'):
#         print('Unconfigure')
#         # my_sql_client = MySqlClient(user='test_qa', password='qa_test', db_name='TEST')
#         # my_sql_client.connect()
#         # # my_sql_client.clear_all_users()
#         # my_sql_client.connection.close()


@pytest.fixture(scope='function')
def client_api():
    return ApiClient(f"http://app:8080")


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
