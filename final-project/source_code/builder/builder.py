from dataclasses import dataclass

import faker

fake = faker.Faker()


@dataclass
class User:
    username: str = None
    password: str = None
    email: str = None


class UserBuilder:
    users = []

    def create_user(self, username=None, password=None, email=None):
        if username is None:
            username = fake.lexify(text='??????')

        if password is None:
            password = fake.password()

        if email is None:
            email = fake.email()
        user = User(username=username, password=password, email=email)
        self.users.append(user)
        return user
