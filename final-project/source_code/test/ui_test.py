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
        """
        Тестирование авторизации в LoginPage - проверка изменения статуса пользователя в бд
        1. Создать в БД валидного пользователя
        2. Авторизоваться и перейти на страницу MainPage
        3. Сделать запрос по созданному пользователю в БД
        4. Проверить поля активность и начало времени активности
        Ожидаемый результат: статус активности пользователя 1.
        """
        assert self.driver.current_url in self.main_page.url, f'Main page is not opened'
        db_user = self.mysql_client.get_user(id=self.user.id)
        self.logger.info(f'Checking user status: {db_user}')
        assert db_user.active == 1 and db_user.start_active_time is not None, f'User logged, but he is not active'


@pytest.mark.ui
@pytest.mark.negative
class TestLoginPageNegative(BaseCaseUi):
    authorize = False

    def test_invalid_username_login(self):
        """
        Негативное тестирование авторизации в LoginPage - авторизация с невалидным именем пользователя
        1. Создать пользователя с пустым именем
        2. Авторизоваться на странице LoginPage
        3. Проверить текущую страницу браузера
        Ожидаемый результат: авторизация не прошла, браузер открыт на странице LoginPage.
        """
        user = self.mysql_builder.create_test_user(username='')
        self.main_page = self.login_page.do_login(username=user.username, password=user.password)
        self.logger.info(f'Checking page url: {self.driver.current_url}')
        assert self.driver.current_url != self.main_page.url, f'Bad user log in: {self.driver.current_url}'

    def test_invalid_password_login(self):
        """
        Негативное тестирование авторизации в LoginPage - авторизация с невалидным паролем пользователя
        1. Создать пользователя с пустым паролем
        2. Авторизоваться на странице LoginPage
        3. Проверить текущую страницу браузера
        Ожидаемый результат: авторизация не прошла, браузер открыт на странице LoginPage.
        """
        user = self.mysql_builder.create_test_user(password='')
        self.main_page = self.login_page.do_login(username=user.username, password=user.password)
        self.logger.info(f'Checking page url: {self.driver.current_url}')
        assert self.driver.current_url != self.main_page.url, f'Bad user log in: {self.driver.current_url}'


@pytest.mark.ui
@pytest.mark.positive
class TestRegistrationPage(BaseCaseUi):
    authorize = False

    def test_registration(self):
        """
        Тестирование регистрации в RegistrationPage - регистрация пользователя
        1. Перейти на страницу регистрации
        2. Создать валидного пользователя и передать данные пользователя на страницу RegistrationPage
        3. Нажать кнопку регистрации
        4. Проверить зарегистрированного пользователя в базе данных
        Ожидаемый результат: пользователь зарегистрирован и активен.
        """
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
        """
        Негативное тестирование регистрации на RegistrationPage - невалидный username
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя с невалидным username
        3. Ввести данные поль.-я во все поля формы RegistrationPage, поставить галочку согласия, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
        self.send_invalid_data_registration(expected_message=expected_message, username='a'*username)

    @pytest.mark.parametrize(("email", "expected_message"), [(1, "Incorrect email length"),
                                                             ("@gmail.com", "Invalid email address"),
                                                             (65, "Incorrect email length")])
    def test_invalid_email_registration(self, email, expected_message):  # +
        """
        Негативное тестирование регистрации на RegistrationPage - невалидный email
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя с невалидным email
        3. Ввести данные поль.-я во все поля формы RegistrationPage, поставить галочку согласия, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
        email = email if type(email) == str else 'a'*email
        self.send_invalid_data_registration(expected_message=expected_message, email=email)

    @pytest.mark.parametrize(("password", "expected_message"), [(0, None),
                                                                (1, "Incorrect password length"),
                                                                (256, "Incorrect password length")])
    def test_invalid_password_registration(self, password, expected_message):
        """
        Негативное тестирование регистрации на RegistrationPage - невалидный password
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя с невалидным password
        3. Ввести данные поль.-я во все поля формы RegistrationPage, поставить галочку согласия, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
        self.send_invalid_data_registration(expected_message=expected_message, password='a' * password)

    def test_invalid_confirm_registration(self):
        """
        Негативное тестирование регистрации на RegistrationPage - невалидный confirm
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя с невалидным confirm
        3. Ввести данные поль.-я во все поля формы RegistrationPage, поставить галочку согласия, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
        self.send_invalid_data_registration(expected_message='Passwords must match', password='1234', confirm='')

    def test_invalid_email_confirm_registration(self):
        """
        Негативное тестирование регистрации на RegistrationPage - невалидный email, confirm
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя с невалидным email, confirm
        3. Ввести данные поль.-я во все поля формы RegistrationPage, поставить галочку согласия, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
        self.send_invalid_data_registration(expected_message='Incorrect email or passwords matching',
                                            email='123', confirm='')

    def test_invalid_term_registration(self):
        """
        Негативное тестирование регистрации на RegistrationPage - отсутствие согласия
        0. Открыть страницу LoginPage
        1. Перейти на RegistrationPage
        2. Создать объект пользователя
        3. Ввести данные поль.-я во все поля формы RegistrationPage, нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        Ожидаемый результат: Сообщение отсутствует, пользователь не зарегистрирован
        """
        self.send_invalid_data_registration(expected_message=None, term=False)

    def test_invalid_exist_user_registration(self):
        """
        Негативное тестирование регистрации на RegistrationPage - регистрация существующего пользователя
        0. Добавить в БД валидного пользователя
        1. Открыть страницу LoginPage
        2. Перейти на RegistrationPage
        3. Ввести данные добавленного поль.-я во все поля формы RegistrationPage, поставить галочку согласия,
        нажать кнопку Register
        4. Проверить url текущей на страницы на несоответствие url MainPage
        5. Проверяем ожидаемое сообщение с отображаемым
        Ожидаемый результат: Сообщение корректное, пользователь не зарегистрирован
        """
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

    def test_python_history(self):
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Python
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Python
        3. Кликнуть на кнопку в сабменю Python history
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://en.wikipedia.org/wiki/History_of_Python
        """
        self.go_navbar_link('Python', 'Python history', 'https://en.wikipedia.org/wiki/History_of_Python')

    def test_python_about_flask(self):
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Python
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Python
        3. Кликнуть на кнопку в сабменю About Flask
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://flask.palletsprojects.com/en/1.1.x/#
        """
        self.go_navbar_link('Python', 'About Flask', 'https://flask.palletsprojects.com/en/1.1.x/#')

    def test_linux_centos(self):  # 6. Bug - открывается не та ссылка
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Linux
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Linux
        3. Кликнуть на кнопку в сабменю Download Centos7
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://www.centos.org/download/
        """
        self.go_navbar_link('Linux', 'Download Centos7', 'https://www.centos.org/download/')

    def test_network_news(self):
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Network
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Network
        3. Кликнуть на кнопку в сабменю News
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://www.wireshark.org/news/
        """
        self.go_navbar_link('Network', 'News', 'https://www.wireshark.org/news/')

    def test_network_download(self):
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Network
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Network
        3. Кликнуть на кнопку в сабменю Download
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://www.wireshark.org/#download
        """
        self.go_navbar_link('Network', 'Download', 'https://www.wireshark.org/#download')

    def test_network_examples(self):
        """
        Тестирование navbar в MainPage - переход по сабменю в кнопке Network
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Передвинуть курсор к кнопке Network
        3. Кликнуть на кнопку в сабменю Examples
        4. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://hackertarget.com/tcpdump-examples/
        """
        self.go_navbar_link('Network', 'Examples ', 'https://hackertarget.com/tcpdump-examples/')

    def test_menu_overlay_api(self):
        """
        Тестирование overlay кнопок в MainPage - клик на overlay кнопку What is an API?
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Кликнуть на overlay кнопку What is an API?
        3. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://en.wikipedia.org/wiki/API
        """
        self.go_overlay_link(btn_title='What is an API?', expected_url='https://en.wikipedia.org/wiki/API')

    def test_menu_overlay_future(self):
        """
        Тестирование overlay кнопок в MainPage - клик на overlay кнопку Future of internet?
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Кликнуть на overlay кнопку Future of internet?
        3. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://www.popularmechanics.com/technology/infrastructure/
        a29666802/future-of-the-internet/
        """
        self.go_overlay_link(btn_title='Future of internet',
                             expected_url='https://www.popularmechanics.com/technology/infrastructure/'
                                          'a29666802/future-of-the-internet/')

    def test_menu_overlay_smtp(self):
        """
        Тестирование overlay кнопок в MainPage - клик на overlay кнопку Lets talk about SMTP?
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Кликнуть на overlay кнопку What is an API?
        3. Проверить, что открылось новое окно
        Ожидаемый результат: URL в новом окне соответствует https://ru.wikipedia.org/wiki/SMTP
        """
        self.go_overlay_link(btn_title='Lets talk about SMTP?',
                             expected_url='https://ru.wikipedia.org/wiki/SMTP')

    def test_menu_logout(self):
        """
        Тестирование кнопки logout в MainPage - клик на logout кнопку
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Кликнуть на кнопку logout
        3. Проверить, что произошёл выход с главной страницы
        4. Сделать запрос в БД по созданному пользователю, проверить свойство active
        Ожидаемый результат: Свойство active равно 0
        """
        self.main_page.click_logout()
        assert 'http://app:8080/welcome' != self.driver.current_url
        database_user = self.mysql_client.get_user(username=self.user.username)
        assert database_user.active == 0

    def test_vk_id(self):
        """
        Тестирование присутствия VK_ID в MainPage
        0. Создать в БД пользователя
        1. Авторизоваться
        2. Отправить в мок данные по пользователю, получить vk_id от мока
        3. Обновить страницу
        4. Найти элемент с полученным vk_id
        Ожидаемый результат: Элемент в vk_id найден
        """
        vk_id = post_user_to_mock(self.user.username)
        self.logger.info(f'POST user to mock, get id {vk_id}')
        self.main_page.driver.refresh()
        self.main_page.get_vk_id(expected_id=vk_id)


@pytest.mark.ui
@pytest.mark.negative
class TestMainPageNegative(BaseCaseUi):

    def test_non_exist_vk_id(self):
        """
        Тестирование отсутствия VK_ID в MainPage
        0. Создать в БД пользователя
        1. Авторизоваться
        3. Проверить отсутствие элемента VK_ID
        Ожидаемый результат: Элемент в vk_id не найден
        """
        with pytest.raises(TimeoutException):
            self.main_page.get_vk_id()


