from dataclasses import dataclass

import faker

fake = faker.Faker()


@dataclass
class User:
    name: str = None
    surname: str = None


class Builder:

    @staticmethod
    def create_user(name=None, surname=None):
        fake_user = fake.name().split()
        if name is None:
            name = fake_user[0]

        if surname is None:
            surname = fake_user[1]

        return User(name=name, surname=surname)
