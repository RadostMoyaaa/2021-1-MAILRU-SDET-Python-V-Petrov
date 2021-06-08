import pytest
import requests
from selenium.common.exceptions import TimeoutException

from base import BaseCaseUi


def post_user_to_mock(name):
    """
    Функция для отправки данных в мок
    """
    data = {'name': name}
    response = requests.post('http://mock_container:5000/vk_id/add_user', json=data)
    assert response.status_code == 201
    return response.json()['id']


@pytest.mark.ui
@pytest.mark.positive
class TestLoginPage(BaseCaseUi):

    def test_login(self):
        assert self.driver.current_url in self.main_page.url, f'Main page is not opened'
        db_user = self.mysql_client.get_user(id=self.user.id)
        self.logger.info(f'Checking user status: {db_user}')
        assert db_user.active == 1 and db_user.start_active_time is not None, f'User logged, but he is not active'


@pytest.mark.ui
@pytest.mark.negative
class TestLoginPageNegative(BaseCaseUi):
    authorize = False

    def test_invalid_username_login(self):
        user = self.mysql_builder.create_test_user(username='')
        self.main_page = self.login_page.do_login(username=user.username, password=user.password)
        self.logger.info(f'Checking page url: {self.driver.current_url}')
        assert self.driver.current_url != self.main_page.url, f'Bad user log in: {self.driver.current_url}'

    def test_invalid_password_login(self):
        user = self.mysql_builder.create_test_user(password='')
        self.main_page = self.login_page.do_login(username=user.username, password=user.password)
        self.logger.info(f'Checking page url: {self.driver.current_url}')
        assert self.driver.current_url != self.main_page.url, f'Bad user log in: {self.driver.current_url}'


@pytest.mark.ui
@pytest.mark.positive
class TestRegistrationPage(BaseCaseUi):
    authorize = False

    def test_registration(self):
        self.registration_page = self.login_page.go_registration()
        ui_user = self.ui_user_builder.create_user()
        self.main_page = self.registration_page.registration(username=ui_user.username, email=ui_user.email,
                                                             password=ui_user.password, confirm=ui_user.password)
        self.logger.info(f'Checking page url: {self.driver.current_url}')
        assert self.driver.current_url == self.main_page.url, f'User doesnt log in: {self.driver.current_url}'
        db_user = self.mysql_client.get_user(username=ui_user.username)
        self.logger.info(f'Checking user status: {db_user}')
        assert db_user.active == 1 and db_user.start_active_time is not None, f'User {db_user} is not active after login ' \
                                                                              f'{db_user.start_active_time}'


@pytest.mark.ui
@pytest.mark.negative
class TestRegistrationPageNegative(BaseCaseUi):
    authorize = False

    def send_invalid_data_registration(self, expected_message, term=True, **kwargs):
        """
        Прокси функция, необходимая для параметризации тестов
        """
        self.registration_page = self.login_page.go_registration()
        user = self.ui_user_builder.create_user(**kwargs)
        self.main_page = self.registration_page.registration(username=user.username, email=user.email,
                                                             password=user.password, confirm=user.confirm, term=term)
        self.logger.info(f'Get page url: {self.driver.current_url}')
        assert self.driver.current_url != self.main_page.url, f'Invalid registration passed: {user}'
        if expected_message is not None:
            current_message = self.registration_page.get_error_message()
            self.logger.info(f'Get message status: {current_message}')
            assert current_message == expected_message, f'Got bad message:{current_message}, expected: {expected_message}'

    @pytest.mark.parametrize(("username", "expected_message"), [(0, None),
                                                                (1, "Incorrect username length"),
                                                                (17, "Incorrect username length")])
    def test_invalid_username_registration(self, username, expected_message):
        self.send_invalid_data_registration(expected_message=expected_message, username='a'*username)

    @pytest.mark.parametrize(("email", "expected_message"), [(1, "Incorrect email length"),
                                                             ("@gmail.com", "Invalid email address"),
                                                             (65, "Incorrect email length")])
    def test_invalid_email_registration(self, email, expected_message):  # +
        email = email if type(email) == str else 'a'*email
        self.send_invalid_data_registration(expected_message=expected_message, email=email)

    @pytest.mark.parametrize(("password", "expected_message"), [(0, None),
                                                                (1, "Incorrect password length"),
                                                                (256, "Incorrect password length")])
    def test_invalid_password_registration(self, password, expected_message):
        self.send_invalid_data_registration(expected_message=expected_message, password='a' * password)

    def test_invalid_confirm_registration(self):
        self.send_invalid_data_registration(expected_message='Passwords must match', password='1234', confirm='')

    def test_invalid_email_confirm_registration(self):  # 5. Bug with error message
        self.send_invalid_data_registration(expected_message='Incorrect email or passwords matching',
                                            email='123', confirm='')

    def test_invalid_term_registration(self):
        self.send_invalid_data_registration(expected_message=None, term=False)

    def test_invalid_exist_user_registration(self):
        exist_user = self.mysql_builder.create_test_user()
        self.send_invalid_data_registration(expected_message='User already exist', username=exist_user.username,
                                            email=exist_user.email, password=exist_user.password,
                                            confirm=exist_user.password)


@pytest.mark.ui
@pytest.mark.positive
class TestMainPage(BaseCaseUi):

    def go_navbar_link(self, navbar_btn_name, navbar_link, expected_url):
        self.main_page.go_to_navbar_link(navbar_btn_name, navbar_link)
        self.main_page.check_window(expected_url=expected_url)

    def go_overlay_link(self, btn_title, expected_url):
        self.main_page.go_to_overlay_link(btn_title)
        self.main_page.check_window(expected_url=expected_url)

    def test_python_history(self):  # 5. Bug - не открывается ссылка в новом окне
        self.go_navbar_link('Python', 'Python history', 'https://en.wikipedia.org/wiki/History_of_Python')

    def test_python_about_flask(self):
        self.go_navbar_link('Python', 'About Flask', 'https://flask.palletsprojects.com/en/1.1.x/#')

    def test_linux_centos(self):  # 6. Bug - открывается не та ссылка
        self.go_navbar_link('Linux', 'Download Centos7', 'https://www.centos.org/download/')

    def test_network_news(self):
        self.go_navbar_link('Network', 'News', 'https://www.wireshark.org/news/')

    def test_network_download(self):
        self.go_navbar_link('Network', 'Download', 'https://www.wireshark.org/#download')

    def test_network_examples(self):
        self.go_navbar_link('Network', 'Examples ', 'https://hackertarget.com/tcpdump-examples/')

    def test_menu_overlay_api(self):
        self.go_overlay_link(btn_title='What is an API?', expected_url='https://en.wikipedia.org/wiki/API')

    def test_menu_overlay_future(self):
        self.go_overlay_link(btn_title='Future of internet',
                             expected_url='https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/')

    def test_menu_overlay_smtp(self):
        self.go_overlay_link(btn_title='Lets talk about SMTP?',
                             expected_url='https://ru.wikipedia.org/wiki/SMTP')

    def test_menu_logout(self):
        self.main_page.click_logout()
        assert 'welcome' not in self.driver.current_url  # TODO исправить
        database_user = self.mysql_client.get_user(username=self.user.username)
        assert database_user.active == 0

    def test_vk_id(self):
        vk_id = post_user_to_mock(self.user.username)
        self.logger.info(f'POST user to mock, get id {vk_id}')
        self.main_page.driver.refresh()
        self.main_page.get_vk_id(expected_id=vk_id)


@pytest.mark.ui
@pytest.mark.negative
class TestMainPageNegative(BaseCaseUi):

    def test_non_exist_vk_id(self):
        with pytest.raises(TimeoutException):
            self.main_page.get_vk_id()

