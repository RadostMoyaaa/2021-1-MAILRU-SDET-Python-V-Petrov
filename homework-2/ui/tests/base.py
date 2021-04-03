import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.dashboard_page import DashBoardPage
from ui.pages.login_page import LoginPage
from ui.pages.base_page import BasePage


class BaseCase:

    auto_login = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest):
        print('Фикстура setup')
        # self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.auto_login:
            self.dashboard_page: DashBoardPage = request.getfixturevalue('dashboard_page')
