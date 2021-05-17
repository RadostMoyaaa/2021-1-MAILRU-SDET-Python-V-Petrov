from mock.flask_mock import SURNAME_DATA
from base_test import BaseTest


class Test(BaseTest):
    def test_get(self):
        surname = self.get_surname(self.user.name, 404)
        assert 'not found' in surname

    def test_add(self):
        SURNAME_DATA[self.user.name] = self.user.surname
        surname = self.get_surname(self.user.name, 200)
        assert self.user.surname == surname

    def test_put(self):
        SURNAME_DATA[self.user.name] = self.user.surname
        self.user.surname = 'Romanov'
        self.put_update_user_surname(self.user.name, self.user.surname, 201)
        assert self.get_surname(self.user.name, 200) == self.user.surname

    def test_delete(self):
        SURNAME_DATA[self.user.name] = self.user.surname
        self.delete_user_surname(self.user.name, 204)
        surname = self.get_surname(self.user.name, 404)
        assert 'not found' in surname
