import pytest
from api_client.client import ResponseStatusCodeException
from base import BaseCaseApi, BaseCaseUi
import allure


class PageOpenException(Exception):
    pass


# API TESTS
class TestMyAppCaseApi(BaseCaseApi):

    @pytest.mark.api
    @pytest.mark.positive
    def test_add_user(self):  # Bug - 1. Test add user, BUG 210 status
        self.new_user = self.api_user_builder.create_user()
        self.add_user(self.new_user.username, self.new_user.password, self.new_user.email)
        user = self.mysql_client.get_user(username=self.new_user.username, password=self.new_user.password,
                                          email=self.new_user.email)
        assert user.username == self.new_user.username and user.password == self.new_user.password \
               and user.email == self.new_user.email

    @pytest.mark.api
    @pytest.mark.positive
    def test_delete_user(self):  # Test delete user
        new_database_user = self.mysql_builder.create_test_user()
        self.client_api.get_delete_user(username=new_database_user.username)
        assert self.mysql_client.check_exist_user(id=new_database_user.id) is False

    @pytest.mark.api
    @pytest.mark.positive
    def test_block_user(self):  # Test block user
        new_database_user = self.mysql_builder.create_test_user()
        self.client_api.get_block_user(username=new_database_user.username)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 0

    @pytest.mark.api
    @pytest.mark.positive
    def test_unblock_user(self):  # Test unblock user
        new_database_user = self.mysql_builder.create_test_user(access=0)
        self.client_api.get_unblock_user(username=new_database_user.username)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 1

    @pytest.mark.api
    @pytest.mark.positive
    def test_status(self):  # Test status
        self.client_api.get_status()

    @pytest.mark.api
    @pytest.mark.positive
    def test_registration(self):  # Test reg
        new_user = self.api_user_builder.create_user()
        response = self.client_api.post_registration(username=new_user.username, password=new_user.password,
                                                     email=new_user.email, confirm=new_user.password)
        assert 'welcome' in response.headers['Location']

    @pytest.mark.api
    @pytest.mark.positive
    def test_logout(self):  # Test logout
        response = self.client_api.get_logout()
        assert 'login' in response.headers['Location']
        user = self.mysql_client.get_user(username=self.main_user.username)
        assert user.active == 0


class TestMyAppCaseApiNegative(BaseCaseApi):
    authorize = False

    @pytest.mark.api
    @pytest.mark.negative
    def test_negative_username_registration(self):
        user = self.api_user_builder.create_user(username='1234')
        with pytest.raises(ResponseStatusCodeException):
            self.client_api.post_registration(username=user.username, password=user.password,
                                              email=user.email, confirm=user.password)

    @pytest.mark.api
    @pytest.mark.negative
    def test_negative_password_registration(self):
        user = self.api_user_builder.create_user(password='')
        with pytest.raises(ResponseStatusCodeException):
            self.client_api.post_registration(username=user.username, password=user.password,
                                              email=user.email, confirm=user.password)

    @pytest.mark.api
    @pytest.mark.negative
    def test_negative_confirm_registration(self):
        user = self.api_user_builder.create_user()
        with pytest.raises(ResponseStatusCodeException):
            self.client_api.post_registration(username=user.username, password=user.password,
                                              email=user.email, confirm='')

    @pytest.mark.api
    @pytest.mark.negative
    def test_negative_term_registration(self):  # 2 Bug with term
        user = self.api_user_builder.create_user()
        with pytest.raises(ResponseStatusCodeException):
            self.client_api.post_registration(username=user.username, password=user.password,
                                              email=user.email, confirm=user.password, term='n')

    @pytest.mark.api
    @pytest.mark.negative
    def test_negative_login(self):
        user = self.api_user_builder.create_user()
        with pytest.raises(ResponseStatusCodeException):
            self.client_api.post_login(username=user.username, password=user.password)


# UI TESTS
class TestLoginPage(BaseCaseUi):

    @pytest.mark.ui
    @pytest.mark.positive
    def test_login(self):
        user = self.mysql_builder.create_test_user()
        self.login_page.do_login(username=user.username, password=user.password)
        assert 'welcome' in self.login_page.get_current_url()
        db_user = self.mysql_client.get_user(id=user.id)
        assert db_user.active == 1 and db_user.start_active_time is not None

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_username_login(self):
        bd_user = self.mysql_builder.create_test_user(username='')
        self.login_page.do_login(username=bd_user.username, password=bd_user.password)
        assert 'welcome' not in self.login_page.get_current_url()

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_username_password(self):
        user = self.ui_user_builder.create_user(password='')
        self.login_page.do_login(username=user.username, password=user.password)
        assert 'welcome' not in self.login_page.get_current_url()


class TestRegistrationPage(BaseCaseUi):
    @pytest.mark.ui
    @pytest.mark.positive
    def test_registration(self):  # 3. Bug with registration, user is not active after registration
        self.registration_page = self.login_page.go_registration()
        ui_user = self.ui_user_builder.create_user()
        self.registration_page.registration(username=ui_user.username, email=ui_user.email,
                                            password=ui_user.password, confirm=ui_user.password)
        assert 'welcome' in self.registration_page.get_current_url()
        db_user = self.mysql_client.get_user(username=ui_user.username)
        assert db_user.active == 1 and db_user.start_active_time is not None

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_username_registration(self):
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user(username='')
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm=user.password)
        assert 'welcome' not in self.registration_page.get_current_url()

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_email_length_registration(self):
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user(email='')
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm=user.password)
        assert self.registration_page.get_error_message() == 'Incorrect email length'

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_email_confirm_registration(self):  # 4. Bug with error message
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user(email='123')
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm='')
        assert self.registration_page.get_error_message() == 'Incorrect email and passwords matching'

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_password_registration(self):
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user(password='')
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm=user.password)
        assert 'welcome' not in self.registration_page.get_current_url()

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_confirm_registration(self):
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user()
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm='')
        assert self.registration_page.get_error_message() == 'Passwords must match'

    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_term_registration(self):
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user()
        self.registration_page.registration(username=user.username, email=user.email,
                                            password=user.password, confirm=user.password, term=False)
        assert 'welcome' not in self.registration_page.get_current_url()

    @pytest.mark.ui
    @pytest.mark.new
    def test_invalid_exist_user_registration(self):
        exist_user = self.mysql_builder.create_test_user()
        self.registration_page = self.login_page.go_registration()
        self.registration_page.registration(username=exist_user.username, email=exist_user.email,
                                            password=exist_user.password, confirm=exist_user.password)
        assert self.registration_page.get_error_message() == 'User already exist'


class TestMainPage(BaseCaseUi):

    def go_navbar_link(self, navbar_btn_name, navbar_link, expected_url):
        self.registration_page = self.login_page.go_registration()
        self.user = self.ui_user_builder.create_user()
        self.main_page = self.registration_page.registration(self.user.username, self.user.email, self.user.password,
                                                             self.user.password)
        self.main_page.go_to_navbar_link(navbar_btn_name, navbar_link)
        try:
            window = self.driver.window_handles
            self.driver.switch_to_window(window[1])
        except:
            raise PageOpenException('the page did not open in a separate window')
        assert self.driver.current_url == expected_url, f'the expected link {expected_url} is not equal ' \
                                                        f'to the current one{self.driver.current_url} '

    def go_overlay_link(self, btn_title, expected_url):
        self.registration_page = self.login_page.go_registration()
        self.user = self.ui_user_builder.create_user()
        self.main_page = self.registration_page.registration(self.user.username, self.user.email, self.user.password,
                                                             self.user.password)
        self.main_page.go_to_overlay_link(btn_title)
        try:
            window = self.driver.window_handles
            self.driver.switch_to_window(window[1])
        except:
            raise PageOpenException('the page did not open in a separate window')
        assert self.driver.current_url == expected_url, f'the expected link {expected_url} is not equal ' \
                                                        f'to the current one{self.driver.current_url}'

    @pytest.mark.ui
    @pytest.mark.positive
    def test_python_history(self):  # 5. Bug - не открывается ссылка в новом окне
        self.go_navbar_link('Python', 'Python history', 'https://en.wikipedia.org/wiki/History_of_Python')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_python_about_flask(self):
        self.go_navbar_link('Python', 'About Flask', 'https://flask.palletsprojects.com/en/1.1.x/#')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_linux_centos(self):  # 6. Bug - открывается не та ссылка
        self.go_navbar_link('Linux', 'Download Centos7', 'https://www.centos.org/download/')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_network_news(self):
        self.go_navbar_link('Network', 'News', 'https://www.wireshark.org/news/')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_network_download(self):
        self.go_navbar_link('Network', 'Download', 'https://www.wireshark.org/#download')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_network_examples(self):
        self.go_navbar_link('Network', 'Examples ', 'https://hackertarget.com/tcpdump-examples/')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_menu_overlay_api(self):
        self.go_overlay_link(btn_title='What is an API?', expected_url='https://en.wikipedia.org/wiki/API')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_menu_overlay_future(self):
        self.go_overlay_link(btn_title='Future of internet',
                             expected_url='https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_menu_overlay_smtp(self):
        self.go_overlay_link(btn_title='Lets talk about SMTP?',
                             expected_url='https://ru.wikipedia.org/wiki/SMTP')

    @pytest.mark.ui
    @pytest.mark.positive
    def test_menu_logout(self):
        self.registration_page = self.login_page.go_registration()
        self.user = self.ui_user_builder.create_user()
        self.main_page = self.registration_page.registration(self.user.username, self.user.email,
                                                             self.user.password,self.user.password)
        self.main_page.click_logout()
        assert 'welcome' not in self.driver.current_url
        database_user = self.mysql_client.get_user(username=self.user.username)
        assert database_user.active == 0

    @pytest.mark.ui
    @pytest.mark.positive
    def test_menu_random_text(self):
        self.registration_page = self.login_page.go_registration()
        self.user = self.ui_user_builder.create_user()
        self.main_page = self.registration_page.registration(self.user.username, self.user.email,
                                                             self.user.password, self.user.password)
        random_text_first = self.main_page.get_random_text_in_footer()
        self.main_page.driver.refresh()
        random_text_second = self.main_page.get_random_text_in_footer()
        assert random_text_first != random_text_second
