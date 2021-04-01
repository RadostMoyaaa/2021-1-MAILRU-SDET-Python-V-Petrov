import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest):
        print('Фикстура setup')
        self.base_page: BasePage = request.getfixturevalue('base_page')
