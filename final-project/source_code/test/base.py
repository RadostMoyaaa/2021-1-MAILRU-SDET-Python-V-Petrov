import pytest

from builder.builder import UserBuilder
from mysql_client.builder import MySQLBuilder
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage


class BaseCaseApi:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client_api, mysql_client, logger):
        self.client_api = client_api
        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.api_user_builder = UserBuilder()
        self.logger = logger
        self.logger.info('Setup is done')
        if self.authorize:
            self.main_user = self.mysql_builder.create_test_user()
            self.do_authorize(username=self.main_user.username, password=self.main_user.password)
            self.logger.info('Authorize is done')
        yield
        # self.mysql_client.clear_all_users(self.mysql_builder.users, self.api_user_builder.users)

    def do_authorize(self, username, password, submit='Login', expected_status=302):
        return self.client_api.post_login(username, password, submit, expected_status)

    def add_user(self, username, password, email, expected_status=201):
        return self.client_api.post_add_user(username, password, email, expected_status)

    def delete_user(self, username, expected_status=204):
        return self.client_api.get_delete_user(username, expected_status)

    def block_user(self, username, expected_status=200):
        return self.client_api.get_block_user(username, expected_status)

    def unblock_user(self, username, expected_status=200):
        return self.client_api.get_unblock_user(username, expected_status)

    def register_user(self, username, password, email, confirm, term='y', expected_status=302):
        return self.client_api.post_registration(username=username, password=password,
                                                 email=email, confirm=confirm, term=term,
                                                 expected_status=expected_status)

    def logout_user(self, expected_status=302):
        return self.client_api.get_logout(expected_status=expected_status)


class BaseCaseUi:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest, driver, mysql_client, logger, ui_report):
        self.driver = driver
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.ui_user_builder = UserBuilder()
        self.logger = logger
        self.logger.info('Setup is done')
        if self.authorize:
            self.user = self.mysql_builder.create_test_user()
            self.main_page = self.login_page.do_login(username=self.user.username, password=self.user.password)
            self.logger.info('Authorize is done')
        yield
        # request.config.users = self.ui_user_builder.users
        # print('DB users in config:', request.config.users)
        # self.mysql_client.clear_all_users(self.mysql_builder.users, self.ui_user_builder.users)
