import logging
import os
import shutil
import sys
import pytest
import time
import settings
import requests
from requests.exceptions import ConnectionError
from all_code.mock import flask_mock
from all_code.http_api_client.client import HttpMockClient


def wait(host=None, port=None, name=None):
    if host is None or port is None or name is None:
        raise TypeError(f'Something is NoneType: host - {host}, port - {port}, name - {name}')
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{name} did not started in 5s!')


def start_mock():
    flask_mock.run_mock()
    wait(host=settings.MOCK_HOST, port=settings.MOCK_PORT, name=start_mock.__name__)


def stop_mock():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_configure(config):
    base_test_dir = base_dir()
    if not hasattr(config, 'workerinput'):
        start_mock()
        make_dir(base_test_dir, config)


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_mock()


@pytest.fixture(scope='function')
def mock_client():
    return HttpMockClient(settings.MOCK_HOST, int(settings.MOCK_PORT))


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'client.log')

    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('client')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


def base_dir():
    if sys.platform.startswith('win'):
        base_test_dir = 'C:\\tests'
    else:
        base_test_dir = '/tmp/tests'
    return base_test_dir


def make_dir(base_test_dir, config):
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)
    config.base_test_dir = base_test_dir
