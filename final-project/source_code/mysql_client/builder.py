from faker import Faker

from mysql_client.models import TestUsers
fake = Faker()


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_test_user(self, username=None, password=None, email=None, access=None, active=None,start_active_time=None):
        if username is None:
            username = fake.first_name()
        if password is None:
            password = fake.password()
        if email is None:
            email = fake.email()
        if access is None:
            access = 1

        test_users = TestUsers(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time
        )
        self.client.session.add(test_users)
        self.client.session.commit()
        return test_users
