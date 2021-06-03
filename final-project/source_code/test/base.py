import pytest
import logging

from builder.builder import UserBuilder
from mysql_client.builder import MySQLBuilder
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage

logger = logging.getLogger('test')


class BaseCaseApi:  # Base Case Object API
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client_api, mysql_client):
        self.client_api = client_api
        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.api_user_builder = UserBuilder()
        if self.authorize:
            self.main_user = self.mysql_builder.create_test_user()
            logger.info('Creating main user, then authorize')
            self.do_authorize(username=self.main_user.username, password=self.main_user.password)
        yield
        # self.mysql_client.clear_all_users(self.mysql_builder.users, self.api_user_builder.users)

    def do_authorize(self, username, password):
        return self.client_api.post_login(username, password)

    def add_user(self, username, password, email):
        return self.client_api.post_add_user(username, password, email)


class BaseCaseUi:

    authorize = True
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest, driver, mysql_client, logger):
        self.driver = driver
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.ui_user_builder = UserBuilder()
        self.logger = logger
        yield
        # self.mysql_client.clear_all_users(self.mysql_builder.users)
