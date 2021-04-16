import pytest

import config
from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client():
    return ApiClient(config.URL)
