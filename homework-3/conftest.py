import os

import pytest

import config
from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client():
    return ApiClient(config.URL)


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))