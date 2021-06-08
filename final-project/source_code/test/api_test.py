import pytest


from base import BaseCaseApi


@pytest.mark.api
@pytest.mark.positive
class TestLoginUserApi(BaseCaseApi):
    authorize = False

    def test_login_exist_user(self):
        """
        Тестирование функции /login
        1. Создать в БД валидного пользователя
        2. Авторизоваться, отправляя POST запрос с данными пользователя и ожидать 302 статус
        3. Сделать запрос по созданному пользователю в БД
        4. Проверить поля активность и начало времени активности
        Ожидаемый результат: пользователь активен, время присутствует
        """
        user = self.mysql_builder.create_test_user()
        self.do_authorize(username=user.username, password=user.password)
        db_user = self.mysql_client.get_user(username=user.username)
        assert db_user.active == 1 and db_user.start_active_time is not None, f'User is logged, but status: ' \
                                                                              f'active - {db_user.active},' \
                                                                              f'time - {db_user.start_active_time}'


@pytest.mark.api
@pytest.mark.negative
class TestLoginUserNegativeApi(BaseCaseApi):
    authorize = False

    def test_negative_none_exist_user(self):
        """
        Негативное тестирование функции /login
        1. Авторизоваться, отправляя POST запрос с данными несуществующего пользователя и ожидать 401 статус
        Ожидаемый результат: запрос вернул 401
        """
        self.do_authorize(username='123456', password='1234567', expected_status=401)

    def test_login_invalid_username(self):
        """
        Негативное тестирование функции /login - - логирования пользователя без логина
        1. Создать в БД валидного пользователя
        2. Авторизоваться, отправляя POST запрос с пустым именем пользователя и ожидать 200 статус
        Ожидаемый результат: запрос вернул 200
        """
        user = self.mysql_builder.create_test_user()
        self.do_authorize(username='', password=user.password, expected_status=200)

    def test_login_invalid_password(self):
        """
        Негативное тестирование функции /login - логирования пользователя без пароля
        1. Создать в БД валидного пользователя
        2. Авторизоваться, отправляя POST запрос с пустым паролем пользователя и ожидать 200 статус
        Ожидаемый результат: запрос вернул 200
        """
        user = self.mysql_builder.create_test_user()
        self.do_authorize(username=user.username, password='', expected_status=200)


@pytest.mark.api
@pytest.mark.positive
class TestAddUserApi(BaseCaseApi):

    def test_add_user(self):
        """
        Тестирование функции /api/add_user - добавление валидного пользователя
        1. Авторизоваться
        2. Создать валидный объект пользователя, сохранить в список созданных пользователей
        3. Авторизоваться, отправляя POST запрос с пустым паролем пользователя и ожидать 201 статус
        4. Сделать запрос в БД, проверить, что пользователь создан
        Ожидаемый результат: запрос вернул 201, пользователь создан
        """
        new_user = self.api_user_builder.create_user()
        self.add_user(new_user.username, new_user.password, new_user.email)
        db_user = self.mysql_client.get_user(username=new_user.username, password=new_user.password,
                                             email=new_user.email)
        assert db_user.username == new_user.username


@pytest.mark.api
@pytest.mark.negative
class TestAddUserNegativeApi(BaseCaseApi):

    def test_add_exist_user(self):
        """
        Негативное тестирование функции /api/add_user - добавление существующего пользователя
        1. Авторизоваться
        2. Создать в БД валидного пользователя, сохранить в список созданных пользователей
        3. Авторизоваться, отправляя POST запрос с пустым паролем пользователя и ожидать 201 статус
        4. Сделать запрос в БД, проверить, что пользователь создан
        Ожидаемый результат: запрос вернул 201, пользователь создан
        """
        new_user = self.mysql_builder.create_test_user()
        self.add_user(username=new_user.username, password=new_user.password,
                      email=new_user.email, expected_status=304)
        users = self.mysql_client.get_users(username=new_user.username)
        assert len(users) == 1, f'Exist user is duplicated: {users}'


@pytest.mark.api
@pytest.mark.positive
class TestDeleteUserApi(BaseCaseApi):

    def test_delete_user(self):
        new_database_user = self.mysql_builder.create_test_user()
        self.delete_user(username=new_database_user.username)
        users = self.mysql_client.get_users(username=new_database_user.username)
        assert len(users) == 0, f'User was not deleted: {users}'


@pytest.mark.api
@pytest.mark.negative
class TestDeleteUserNegativeApi(BaseCaseApi):

    def test_delete_non_exist_user(self):
        non_exist_user = self.api_user_builder.create_user()
        self.delete_user(username=non_exist_user.username, expected_status=404)


@pytest.mark.api
@pytest.mark.positive
class TestBlockUserApi(BaseCaseApi):

    def test_block_user(self):
        new_database_user = self.mysql_builder.create_test_user()
        self.block_user(username=new_database_user.username)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 0, f'User {new_database_user} was not blocked {changed_user.access}'


@pytest.mark.api
@pytest.mark.negative
class TestBlockUserNegativeApi(BaseCaseApi):

    def test_block_blocked_user(self):
        new_database_user = self.mysql_builder.create_test_user(access=0)
        self.block_user(username=new_database_user.username, expected_status=304)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 0, f'Blocked user {new_database_user} was changed - access is {changed_user.access}'


@pytest.mark.api
@pytest.mark.positive
class TestUnblockUserApi(BaseCaseApi):

    def test_unblock_user(self):
        new_database_user = self.mysql_builder.create_test_user(access=0)
        self.unblock_user(username=new_database_user.username, expected_status=200)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 1, f'Blocked user {new_database_user} was not unblocked - ' \
                                         f'access is {changed_user.access}'


@pytest.mark.api
@pytest.mark.negative
class TestUnblockUserNegativeApi(BaseCaseApi):

    def test_unblock_non_blocked_user(self):
        new_database_user = self.mysql_builder.create_test_user()
        self.unblock_user(username=new_database_user.username, expected_status=304)
        changed_user = self.mysql_client.get_user(id=new_database_user.id)
        assert changed_user.access == 1, f'Blocked user {new_database_user} was changed - ' \
                                         f'access is {changed_user.access}'


@pytest.mark.api
@pytest.mark.positive
class TestRegistrationUserApi(BaseCaseApi):
    authorize = False

    def test_valid_registration(self):
        user = self.api_user_builder.create_user()
        self.register_user(username=user.username, password=user.password,
                           email=user.email, confirm=user.password)
        users = self.mysql_client.get_users(username=user.username)
        assert len(users) == 1, f'User {user} was not created: {users}'


@pytest.mark.api
@pytest.mark.negative
class TestRegistrationNegativeUserApi(BaseCaseApi):
    authorize = False

    @pytest.mark.parametrize("name", [0, 1, 17])
    def test_invalid_username_registration(self, name):
        user = self.api_user_builder.create_user(username='a'*name)
        self.register_user(username=user.username, password=user.password, email=user.email, confirm=user.password,
                           expected_status=400)
        users = self.mysql_client.get_users(username=user.username)
        assert len(users) == 0, f'Invalid user was registered {users}'

    @pytest.mark.parametrize("password", [0, 1, 256])
    def test_invalid_password_registration(self, password):
        user = self.api_user_builder.create_user(password='a'*password)
        self.register_user(username=user.username, password=user.password, email=user.email,
                           confirm=user.password, expected_status=400)
        users = self.mysql_client.get_users(username=user.username)
        assert len(users) == 0, f'Invalid user was registered {users}'

    @pytest.mark.parametrize(("password", "confirm"), [(6, 0)])
    def test_negative_confirm_registration(self, password, confirm):
        user = self.api_user_builder.create_user(password='a' * password)
        self.register_user(username=user.username, password=user.password, email=user.email,
                           confirm='a'*confirm, expected_status=400)
        users = self.mysql_client.get_users(username=user.username)
        assert len(users) == 0, f'Invalid user was registered {users}'

    def test_negative_term_registration(self):
        user = self.api_user_builder.create_user()
        self.register_user(username=user.username, password=user.password, email=user.email,
                           confirm=user.password, term='n', expected_status=400)

    @pytest.mark.parametrize("email", [0, "@gmail.com", 65])
    def test_negative_email_registration(self, email):
        email = email if type(email) == str else 'a'*email
        user = self.api_user_builder.create_user(email=email)
        self.register_user(username=user.username, password=user.password, email=user.email,
                           confirm=user.confirm, expected_status=400)
        users = self.mysql_client.get_users(username=user.username)
        assert len(users) == 0, f'Invalid user was registered {users}'


@pytest.mark.api
@pytest.mark.positive
class TestLogoutUserApi(BaseCaseApi):
    def test_logout(self):
        response = self.logout_user()
        assert 'login' in response.headers['Location']  # TODO Исправить assert
        user = self.mysql_client.get_user(username=self.main_user.username)
        assert user.active == 0, f'User {user} is still active after logout'


@pytest.mark.api
@pytest.mark.negative
class TestLogoutUserNegativeApi(BaseCaseApi):
    authorize = False

    def test_negative_logout(self):
        response = self.logout_user()
        assert 'http://app:8080/login?next=/logout' == response.headers['Location']  # TODO Исправить assert
