import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.dashboard_page import DashBoardPage
from ui.pages.login_page import LoginPage


class BaseCase:

    auto_login = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest, logger):

        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.logger = logger

        if self.auto_login:
            self.dashboard_page: DashBoardPage = request.getfixturevalue('dashboard_page')
