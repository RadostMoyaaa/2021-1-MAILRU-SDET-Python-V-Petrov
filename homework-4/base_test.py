import pytest
from _pytest.fixtures import FixtureRequest

from pages.main_page import MainPage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, request: FixtureRequest):
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.config = config